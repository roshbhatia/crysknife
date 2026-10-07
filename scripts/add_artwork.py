import hashlib
import json
import math
from pathlib import Path
import re

from PIL import Image, ImageFilter


root = Path(__file__).resolve().parents[1]
source = root / "assets/frida.png"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "a7c80525068856ffaabe642369a3466a534b14bf7bf8c164e03b5128d39b1cdf"
pitch = 0.6
minimum_feature = 0.2
width = 40
image = Image.open(source).convert("RGBA").getchannel("A").filter(ImageFilter.GaussianBlur(2))
image.thumbnail((round(width / pitch), round(width / pitch)), Image.Resampling.BOX)


def parse(text):
    tokens = iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text))
    stack = []
    for token in tokens:
        if token == "(":
            stack.append([])
        elif token == ")":
            node = stack.pop()
            if not stack:
                return node
            stack[-1].append(node)
        else:
            stack[-1].append(token.strip('"'))
    raise ValueError("Incomplete KiCad expression")


def children(node, kind):
    return [item for item in node if isinstance(item, list) and item[0] == kind]


def child(node, kind):
    return next(iter(children(node, kind)), None)


for side, center in [("left", 159), ("right", 176)]:
    board_path = root / f"build/pcb/fridakeeb_{side}.kicad_pcb"
    text = board_path.read_text()
    assert '"frida-silkscreen"' not in text, "Regenerate the PCB before applying artwork."
    board = parse(text)
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
    top = 82 - image.height * pitch / 2
    for row in range(image.height):
        for col in range(image.width):
            alpha = image.getpixel((col, row))
            x, y = left + (col + 0.5) * pitch, top + (row + 0.5) * pitch
            size = pitch * math.sqrt(alpha / 255)
            clear = all(math.hypot(x - px, y - py) > radius + size / math.sqrt(2)
                        for px, py, radius in keepouts)
            if size >= minimum_feature and clear:
                pixels.append((x - size / 2, y - size / 2, x + size / 2, y + size / 2))
    rectangles = "\n".join(
        f'(fp_rect (start {x0-center:.4f} {y0-82:.4f}) (end {x1-center:.4f} {y1-82:.4f}) '
        '(stroke (width 0) (type default)) (fill solid) (layer "F.SilkS"))'
        for x0, y0, x1, y1 in pixels
    )
    footprint = f'\n(footprint "frida-silkscreen" (layer "F.Cu") (at {center} 82) (attr board_only exclude_from_pos_files exclude_from_bom)\n{rectangles}\n)\n'
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
