import hashlib
import json
import math
import re
from pathlib import Path
from kicad_sexp import parse, children, child
from generate_tscircuit import edge_points

from PIL import Image, ImageFilter, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[1]
source = root / "assets/frida.png"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "a7c80525068856ffaabe642369a3466a534b14bf7bf8c164e03b5128d39b1cdf"
minimum_feature = 0.2
portrait_alpha = Image.open(source).convert("RGBA").getchannel("A").filter(ImageFilter.GaussianBlur(2))


for side in ("left", "right"):
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
            if not set(layers) & {"F.Mask", "B.Mask", "*.Mask"}:
                continue
            local = child(pad, "at")
            x, y = map(float, local[1:3])
            px = fx + x * math.cos(angle) + y * math.sin(angle)
            py = fy - x * math.sin(angle) + y * math.cos(angle)
            size = list(map(float, child(pad, "size")[1:3]))
            keepouts.append((px, py, math.hypot(*size) / 2 + 0.3))
    silk_segments = []
    silk_boxes = []
    for footprint in children(board, "footprint"):
        at = child(footprint, "at")
        fx, fy = map(float, at[1:3])
        angle = math.radians(float(at[3]) if len(at) > 3 else 0)

        def world(point):
            x, y = map(float, point[1:3])
            return (fx+x*math.cos(angle)+y*math.sin(angle), fy-x*math.sin(angle)+y*math.cos(angle))

        for graphic in footprint:
            if not isinstance(graphic, list):
                continue
            layer = child(graphic, "layer")
            if not layer or layer[1] not in ("F.SilkS", "B.SilkS"):
                continue
            stroke = child(graphic, "stroke")
            clearance = 0.25+(float(child(stroke, "width")[1])/2 if stroke else 0)
            if graphic[0] == "fp_line":
                a, b = [world(child(graphic, key)) for key in ("start", "end")]
                silk_segments.append((a, b, clearance))
            elif graphic[0] == "fp_poly":
                points = [world(p) for p in children(child(graphic, "pts"), "xy")]
                silk_boxes.append((min(p[0] for p in points)-clearance, min(p[1] for p in points)-clearance,
                                   max(p[0] for p in points)+clearance, max(p[1] for p in points)+clearance))
            elif graphic[0].startswith("fp_") and graphic[0] not in ("fp_text",):
                raise ValueError((side, "Unsupported native silkscreen graphic", graphic[0]))

    def clear_silk(x, y, radius):
        if any(x0-radius <= x <= x1+radius and y0-radius <= y <= y1+radius
               for x0, y0, x1, y1 in silk_boxes):
            return False
        for (ax, ay), (bx, by), clearance in silk_segments:
            margin = clearance+radius
            if not min(ax, bx)-margin <= x <= max(ax, bx)+margin or not min(ay, by)-margin <= y <= max(ay, by)+margin:
                continue
            dx, dy = bx-ax, by-ay
            t = max(0, min(1, ((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)))
            if math.hypot(x-ax-t*dx, y-ay-t*dy) <= margin:
                return False
        return True

    edges = [edge_points(n) for n in board if isinstance(n, list)
             and n[0] in ("gr_line", "gr_arc") and child(n, "layer")[1] == "Edge.Cuts"]
    outline = edges.pop(0)
    while edges:
        for index, edge in enumerate(edges):
            if math.dist(outline[-1], edge[0]) < 1e-4:
                break
            if math.dist(outline[-1], edge[-1]) < 1e-4:
                edge = list(reversed(edge))
                break
        else:
            raise ValueError("Disconnected artwork boundary")
        outline.extend(edge[1:])
        edges.pop(index)
    assert math.dist(outline[0], outline[-1]) < 1e-4, "Open artwork boundary"
    segments = list(zip(outline, outline[1:]))

    def inside(x, y):
        crossings = 0
        for (ax, ay), (bx, by) in segments:
            if (ay > y) != (by > y) and x < ax+(y-ay)*(bx-ax)/(by-ay):
                crossings += 1
        return crossings % 2 == 1

    def edge_clearance(x, y):
        distances = []
        for (ax, ay), (bx, by) in segments:
            dx, dy = bx-ax, by-ay
            t = max(0, min(1, ((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)))
            distances.append(math.hypot(x-ax-t*dx, y-ay-t*dy))
        return min(distances)

    min_x, min_y = [min(p[i] for p in outline) for i in (0, 1)]
    max_x, max_y = [max(p[i] for p in outline) for i in (0, 1)]
    title_center = 110 if side == "left" else 225
    lettering_boxes = [(title_center, 69.5, 36, 6), (title_center, 88, 32, 5.2),
                       (title_center, 91, 26, 4.6)]
    original_labels = []
    for footprint in children(board, "footprint"):
        placement = child(footprint, "at")
        fx, fy = map(float, placement[1:3])
        angle = math.radians(float(placement[3]) if len(placement) > 3 else 0)
        for label in children(footprint, "fp_text") + children(footprint, "property"):
            layer = child(label, "layer")
            if "hide" in label or not layer or layer[1] != "F.SilkS":
                continue
            at = child(label, "at")
            if not at:
                continue
            size = child(child(child(label, "effects"), "font"), "size")
            if not size:
                continue
            lx, ly = float(at[1]), float(at[2])
            px = fx+lx*math.cos(angle)+ly*math.sin(angle)
            py = fy-lx*math.sin(angle)+ly*math.cos(angle)
            if label[2] in ("ON", "OFF"):
                px += -3 if side == "left" else 3
            radius = math.hypot(len(label[2])*float(size[1])*0.8, float(size[2]))/2+0.4
            original_labels.append((label[2], px, py, len(label[2])*float(size[1])*0.8, float(size[2]), angle))
            lettering_boxes.append((px, py, radius*2, radius*2))
    components = {next(p[2] for p in children(fp, "property") if p[1] == "Reference"): list(map(float, child(fp, "at")[1:3]))
                  for fp in children(board, "footprint")}
    arrows = []
    for name, ref, offset, target_offset in [
        ("reset", "RST1", (0, 7), (0, 2.8)),
        ("brain", "MCU1", (0, 1), (0, -5)),
        ("battery", "JST1", (-6, 6), (-3, 0)),
        ("power", "PWR1", (-7, 9), (-6, 0)),
    ]:
        x, y = components[ref]
        if side == "right":
            offset = (-offset[0], offset[1])
            target_offset = (-target_offset[0], target_offset[1])
        arrows.append((name, x+offset[0], y+offset[1], x+target_offset[0], y+target_offset[1]))
        lettering_boxes.append((x+offset[0], y+offset[1], 12, 4))
        lettering_boxes.append((x+(offset[0]+target_offset[0])/2, y+(offset[1]+target_offset[1])/2,
                                abs(offset[0]-target_offset[0])+1.5, abs(offset[1]-target_offset[1])+1.5))
    pixels = []
    portraits = 0

    def portrait(cx, cy, portrait_width, dot_pitch, hero=False):
        portrait_image = portrait_alpha.copy()
        portrait_image.thumbnail((round(portrait_width/dot_pitch), round(portrait_width/dot_pitch)), Image.Resampling.BOX)
        before = len(pixels)
        left = cx-portrait_image.width*dot_pitch/2
        top = cy-portrait_image.height*dot_pitch/2
        for row in range(portrait_image.height):
            for col in range(portrait_image.width):
                alpha = portrait_image.getpixel((col, row))
                x, y = left+(col+0.5)*dot_pitch, top+(row+0.5)*dot_pitch
                size = dot_pitch*math.sqrt(alpha/255)
                radius = size/math.sqrt(2)
                if size < minimum_feature or not inside(x, y):
                    continue
                if not clear_silk(x, y, radius):
                    continue
                if edge_clearance(x, y) < radius+0.4:
                    continue
                if any(math.hypot(x-px, y-py) <= clearance+radius for px, py, clearance in keepouts):
                    continue
                if any(abs(x-bx) < w/2+radius and abs(y-by) < h/2+radius
                       for bx, by, w, h in lettering_boxes):
                    continue
                if not hero and abs(x-center) < 21 and abs(y-image_center_y) < 21:
                    continue
                pixels.append((x-size/2, y-size/2, x+size/2, y+size/2))
        return len(pixels) > before

    portraits += portrait(center, image_center_y, 40, 0.6, hero=True)
    row = 0
    cy = min_y+11
    while cy < max_y+5:
        cx = min_x+11+(11 if row % 2 else 0)
        while cx < max_x+5:
            portraits += portrait(cx, cy, 20, 1.0)
            cx += 22
        cy += 22
        row += 1
    top_pixels = list(pixels)
    bottom_pixels = list(pixels)
    font = ImageFont.truetype(str(root / "assets/ioskeley-mono-bold.ttf"), 512)

    def clear_pixel(x, y, grid):
        return clear_silk(x, y, grid/math.sqrt(2)) and inside(x, y) and edge_clearance(x, y) > grid/math.sqrt(2)+0.4 and all(
            math.hypot(x-px, y-py) > radius+grid/math.sqrt(2) for px, py, radius in keepouts)

    def lettering(label, cx, cy, max_width, max_height, rotation=0):
        box = font.getbbox(label)
        mask = Image.new("L", (box[2]-box[0], box[3]-box[1]))
        ImageDraw.Draw(mask).text((-box[0], -box[1]), label, font=font, fill=255)
        grid = minimum_feature
        mask.thumbnail((round(max_width/grid), round(max_height/grid)), Image.Resampling.LANCZOS)
        for row in range(mask.height):
            for col in range(mask.width):
                if mask.getpixel((col, row)) < 100:
                    continue
                lx, ly = (col+0.5-mask.width/2)*grid, (row+0.5-mask.height/2)*grid
                for face, direction in [(top_pixels, 1), (bottom_pixels, -1)]:
                    x = cx+direction*lx*math.cos(rotation)+ly*math.sin(rotation)
                    y = cy-direction*lx*math.sin(rotation)+ly*math.cos(rotation)
                    clear = clear_pixel(x, y, grid)
                    assert clear, (side, label, x, y, "Lettering overlaps a pad or board edge")
                    face.append((x-grid/2, y-grid/2, x+grid/2, y+grid/2))

    for label, cy, max_width, max_height in [
        ("Fridakeys", 69.5, 34, 4), ("v1.0.0", 88, 30, 3.2), ("by @fraud", 91, 24, 2.6),
    ]:
        lettering(label, title_center, cy, max_width, max_height)
    for label, x, y, width, height, angle in original_labels:
        lettering(label, x, y, width, height, angle)
    for name, cx, cy, tx, ty in arrows:
        lettering(name, cx, cy, 10, 1.6)
        dx, dy = tx-cx, ty-cy
        length = math.hypot(dx, dy)
        ux, uy = dx/length, dy/length
        start_distance = 4.5 if abs(ux) > 0.8 else 1.4
        start = (cx+ux*start_distance, cy+uy*start_distance)
        for a, b in [(start, (tx, ty)), ((tx, ty), (tx-ux*1.1-uy*0.7, ty-uy*1.1+ux*0.7)),
                     ((tx, ty), (tx-ux*1.1+uy*0.7, ty-uy*1.1-ux*0.7))]:
            steps = math.ceil(math.dist(a, b)/0.1)
            for step in range(steps+1):
                x, y = [a[i]+(b[i]-a[i])*step/steps for i in (0, 1)]
                if clear_pixel(x, y, 0.2):
                    rect = (x-0.1, y-0.1, x+0.1, y+0.1)
                    top_pixels.append(rect)
                    bottom_pixels.append(rect)

    # Replace upstream stroke labels with portable font geometry on both faces.
    matches = list(re.finditer(r'\((?:fp_text|property)\s', text))
    for match in reversed(matches):
        depth, quoted, escaped = 0, False, False
        for end in range(match.start(), len(text)):
            character = text[end]
            if escaped:
                escaped = False
                continue
            if character == "\\" and quoted:
                escaped = True
            elif character == '"':
                quoted = not quoted
            elif not quoted:
                depth += (character == "(")-(character == ")")
                if depth == 0:
                    break
        block = text[match.start():end+1]
        node = parse(block)
        layer = child(node, "layer")
        if "hide" not in node and layer and layer[1] in ("F.SilkS", "B.SilkS"):
            block = block.replace("(effects", "hide (effects", 1)
            text = text[:match.start()]+block+text[end+1:]
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
        f'(stroke (width 0) (type default)) (fill solid) (layer "{layer}"))'
        for layer, face in [("F.SilkS", top_pixels), ("B.SilkS", bottom_pixels)]
        for x0, y0, x1, y1 in face
    )
    reference = '(property "Reference" "ART1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 1 1) (thickness 0.15))))'
    footprint = f'\n(footprint "fridakeeb:frida-silkscreen" (layer "F.Cu") (at {center} {image_center_y}) (attr board_only exclude_from_pos_files exclude_from_bom)\n{reference}\n{rectangles}\n)\n'
    closing = text.rfind(")")
    board_path.write_text(text[:closing] + footprint + text[closing:])
    pixels = top_pixels
    svg_rectangles = "".join(
        f'<rect x="{x0:.4f}" y="{y0:.4f}" width="{x1-x0:.4f}" height="{y1-y0:.4f}"/>'
        for x0, y0, x1, y1 in pixels
    )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{max_x-min_x}mm" height="{max_y-min_y}mm" viewBox="{min_x} {min_y} {max_x-min_x} {max_y-min_y}"><rect x="{min_x}" y="{min_y}" width="{max_x-min_x}" height="{max_y-min_y}" fill="white"/><g fill="black">{svg_rectangles}</g></svg>'
    (root / f"build/pcb/frida-{side}.svg").write_text(svg)
    print(json.dumps({"side": side, "rectangles": len(pixels), "minimum_feature_mm": minimum_feature,
                      "layers": ["F.SilkS", "B.SilkS"], "pad_clearance_mm": 0.3, "native_silk_clearance_mm": 0.25, "portraits": portraits, "edge_clearance_mm": 0.4}))
