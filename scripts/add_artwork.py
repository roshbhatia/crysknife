import hashlib
import json
import math
from pathlib import Path
from kicad_sexp import parse, children, child

from PIL import Image, ImageFilter, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[1]
source = root / "assets/frida.png"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "a7c80525068856ffaabe642369a3466a534b14bf7bf8c164e03b5128d39b1cdf"
pitch = 0.6
minimum_feature = 0.2
width = 40
image = Image.open(source).convert("RGBA").getchannel("A").filter(ImageFilter.GaussianBlur(2))
image.thumbnail((round(width / pitch), round(width / pitch)), Image.Resampling.BOX)


for side, center in [("left", 159), ("right", 176)]:
    board_path = root / f"build/pcb/fridakeeb_{side}.kicad_pcb"
    text = board_path.read_text()
    assert "frida-silkscreen" not in text, "Regenerate the PCB before applying artwork."
    board = parse(text)
    middle_home = next(fp for fp in children(board, "footprint")
                       if any(p[1:3] == ["Reference", "S11"] for p in children(fp, "property")))
    center = float(child(middle_home, "at")[1]) + (2 if side == "left" else -2)
    image_center_y = float(child(middle_home, "at")[2]) + 8.125
    keepouts = []
    for footprint in children(board, "footprint"):
        at = child(footprint, "at")
        fx, fy = map(float, at[1:3])
        angle = math.radians(float(at[3]) if len(at) > 3 else 0)
        for pad in children(footprint, "pad"):
            layers = child(pad, "layers")[1:]
            if not set(layers) & {"F.Mask", "*.Mask"}:
                continue
            local = child(pad, "at")
            x, y = map(float, local[1:3])
            px = fx + x * math.cos(angle) + y * math.sin(angle)
            py = fy - x * math.sin(angle) + y * math.cos(angle)
            size = list(map(float, child(pad, "size")[1:3]))
            keepouts.append((px, py, math.hypot(*size) / 2 + 0.3))
    pixels = []
    left = center - image.width * pitch / 2
    top = image_center_y - image.height * pitch / 2
    for row in range(image.height):
        for col in range(image.width):
            alpha = image.getpixel((col, row))
            x, y = left + (col + 0.5) * pitch, top + (row + 0.5) * pitch
            size = pitch * math.sqrt(alpha / 255)
            clear = all(math.hypot(x - px, y - py) > radius + size / math.sqrt(2)
                        for px, py, radius in keepouts)
            if size >= minimum_feature and clear:
                pixels.append((x - size / 2, y - size / 2, x + size / 2, y + size / 2))
    font = ImageFont.truetype(str(root / "assets/kingjola.ttf"), 512)
    title_center = 110 if side == "left" else 225
    for label, cy, max_width, max_height in [
        ("Fridacorne", 72, 34, 4),
        ("v1.0.0", 88, 30, 3.2),
        ("by @fraud", 91, 24, 2.6),
    ]:
        label_font = font if label == "Fridacorne" else ImageFont.load_default(size=512)
        box = label_font.getbbox(label)
        mask = Image.new("L", (box[2]-box[0], box[3]-box[1]))
        ImageDraw.Draw(mask).text((-box[0], -box[1]), label, font=label_font, fill=255)
        grid = 0.2
        mask.thumbnail((round(max_width/grid), round(max_height/grid)), Image.Resampling.LANCZOS)
        x_start = title_center-mask.width*grid/2
        y_start = cy-mask.height*grid/2
        for row in range(mask.height):
            for col in range(mask.width):
                if mask.getpixel((col, row)) < 100:
                    continue
                x, y = x_start+(col+0.5)*grid, y_start+(row+0.5)*grid
                clear = all(math.hypot(x-px, y-py) > radius+grid/math.sqrt(2)
                            for px, py, radius in keepouts)
                assert clear, (side, label, x, y, "Lettering overlaps a pad or switch hole")
                pixels.append((x-grid/2, y-grid/2, x+grid/2, y+grid/2))
    stackup = """(stackup
      (layer "F.SilkS" (type "Top Silk Screen") (color "Black"))
      (layer "F.Mask" (type "Top Solder Mask") (color "White"))
      (layer "F.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 1" (type "core") (thickness 1.53) (material "FR4")
        (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.035))
      (layer "B.Mask" (type "Bottom Solder Mask") (color "White"))
      (layer "B.SilkS" (type "Bottom Silk Screen") (color "Black")))"""
    text = text.replace('(setup', '(setup\n'+stackup, 1)
    rectangles = "\n".join(
        f'(fp_rect (start {x0-center:.4f} {y0-image_center_y:.4f}) (end {x1-center:.4f} {y1-image_center_y:.4f}) '
        '(stroke (width 0) (type default)) (fill solid) (layer "F.SilkS"))'
        for x0, y0, x1, y1 in pixels
    )
    reference = '(property "Reference" "ART1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 1 1) (thickness 0.15))))'
    footprint = f'\n(footprint "fridakeeb:frida-silkscreen" (layer "F.Cu") (at {center} {image_center_y}) (attr board_only exclude_from_pos_files exclude_from_bom)\n{reference}\n{rectangles}\n)\n'
    closing = text.rfind(")")
    board_path.write_text(text[:closing] + footprint + text[closing:])
    svg_rectangles = "".join(
        f'<rect x="{x0:.4f}" y="{y0:.4f}" width="{x1-x0:.4f}" height="{y1-y0:.4f}"/>'
        for x0, y0, x1, y1 in pixels
    )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="40mm" height="40mm" viewBox="{left} {top} 40 40"><rect x="{left}" y="{top}" width="40" height="40" fill="white"/><g fill="black">{svg_rectangles}</g></svg>'
    (root / f"build/pcb/frida-{side}.svg").write_text(svg)
    print(json.dumps({"side": side, "rectangles": len(pixels), "minimum_feature_mm": minimum_feature,
                      "layer": "F.SilkS", "pad_clearance_mm": 0.3}))
