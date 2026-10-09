import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from kicad_sexp import parse, children, child
from generate_tscircuit import edge_points

from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box
from shapely.ops import unary_union
from shapely.affinity import rotate, scale, translate
from shapely.prepared import prep


root = Path(__file__).resolve().parents[1]
source = root / "assets/knife.svg"
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
raster = root / "build/knife-source.png"
raster.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(["rsvg-convert", str(source), "-o", str(raster)], check=True)
minimum_feature = 0.2
artwork_alpha = Image.open(raster).convert("RGBA").getchannel("A")
artwork_alpha = artwork_alpha.crop(artwork_alpha.getbbox())

font = ImageFont.truetype(str(root / "assets/kingjola.ttf"), 512)


branding_font = ImageFont.truetype(str(root / "assets/ibm-plex-mono-bold.ttf"), 512)


def glyph_pixels(label, max_width, max_height, typeface=font):
    parts = []
    pen = 0
    for character in label:
        selected = typeface
        if not character.isspace() and typeface.getmask(character).getbbox() is None:
            selected = branding_font
        bounds = selected.getbbox(character)
        parts.append((character, selected, pen, bounds))
        pen += typeface.getlength(character)
    left = min(pen+bounds[0] for _, _, pen, bounds in parts)
    top = min(bounds[1] for _, _, _, bounds in parts)
    right = max(pen+bounds[2] for _, _, pen, bounds in parts)
    bottom = max(bounds[3] for _, _, _, bounds in parts)
    mask = Image.new("L", (math.ceil(right-left), bottom-top))
    for character, selected, pen, _ in parts:
        ImageDraw.Draw(mask).text((pen-left, -top), character, font=selected, fill=255)
    assert mask.getbbox(), (label, "No printable lettering")
    mask = mask.crop(mask.getbbox())
    grid = minimum_feature
    mask.thumbnail((round(max_width/grid), round(max_height/grid)), Image.Resampling.LANCZOS)
    return [((col+0.5-mask.width/2)*grid, (row+0.5-mask.height/2)*grid)
            for row in range(mask.height) for col in range(mask.width) if mask.getpixel((col,row)) >= 100]


for side in ("left", "right"):
    board_path = root / f"build/pcb/crysknife_{side}.kicad_pcb"
    text = board_path.read_text()
    assert "knife-silkscreen" not in text, "Regenerate the PCB before applying artwork."
    board = parse(text)
    middle_home = next(fp for fp in children(board, "footprint")
                       if any(p[1:3] == ["Reference", "S11"] for p in children(fp, "property")))
    center = float(child(middle_home, "at")[1]) + (-16 if side == "left" else 16)
    image_center_y = float(child(middle_home, "at")[2]) + 18.5
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
            radius = max(size)/2 if pad[3] == "circle" else math.hypot(*size)/2
            keepouts.append((px, py, radius+0.3))
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
    def clear_pixel(x, y, grid):
        return clear_silk(x, y, grid/math.sqrt(2)) and inside(x, y) and edge_clearance(x, y) > grid/math.sqrt(2)+0.4 and all(
            math.hypot(x-px, y-py) > radius+grid/math.sqrt(2) for px, py, radius in keepouts)

    title_center = 110 if side == "left" else 225
    legends = [("crys.knife", title_center, 108.8, 32, 2.0),
               ("v1.0.0-alpha", title_center+2, 110.9, 30, 1.6),
               ("by @roshbhatia", title_center+4, 112.7, 26, 1.4)]
    lettering_boxes = [(cx,cy,width+2,height+2) for _,cx,cy,width,height in legends]
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
        ("{RST}", "RST1", (0, 7), (0, 2.8)),
        ("{CPU}", "MCU1", (0, 1), (0, -5)),
        ("{BTY}", "JST1", (-6, 6), (-3, 0)),
        ("{PWR}", "PWR1", (-7, 9), (-6, 0)),
    ]:
        x, y = components[ref]
        if side == "right":
            offset = (-offset[0], offset[1])
            target_offset = (-target_offset[0], target_offset[1])
            if ref == "MCU1":
                offset, target_offset = (15, 0), (12, 0)
        arrows.append((name, x+offset[0], y+offset[1], x+target_offset[0], y+target_offset[1]))
        lettering_boxes.append((x+offset[0], y+offset[1], 12, 4))
        lettering_boxes.append((x+(offset[0]+target_offset[0])/2, y+(offset[1]+target_offset[1])/2,
                                abs(offset[0]-target_offset[0])+1.5, abs(offset[1]-target_offset[1])+1.5))
    blocked = [Point(x, y).buffer(r+0.22) for x, y, r in keepouts]
    blocked += [box(x-w/2-0.22, y-h/2-0.22, x+w/2+0.22, y+h/2+0.22)
                for x, y, w, h in lettering_boxes]
    for ref, (x, y) in components.items():
        if re.fullmatch(r"S\d+", ref):
            footprint = next(fp for fp in children(board, "footprint")
                             if any(p[1:3] == ["Reference", ref] for p in children(fp, "property")))
            at = child(footprint, "at")
            angle = float(at[3]) if len(at) > 3 else 0
            blocked.append(rotate(box(x-7.5, y-7.5, x+7.5, y+7.5), -angle, origin=(x, y)))
    blocked += [LineString((a, b)).buffer(clearance+0.22)
                for a, b, clearance in silk_segments]
    blocked += [box(*bounds).buffer(0.22) for bounds in silk_boxes]
    safe_polygon = Polygon(outline).buffer(-0.65).difference(unary_union(blocked))
    safe = prep(safe_polygon)
    sampled = artwork_alpha.resize((64, round(64*artwork_alpha.height/artwork_alpha.width)), Image.Resampling.BOX)
    silhouette = MultiPoint([(x/64-0.5, (y-sampled.height/2)/64)
                             for y in range(sampled.height) for x in range(sampled.width)
                             if sampled.getpixel((x, y)) >= 50]).convex_hull
    candidates = []
    for width in (30, 26, 22, 18, 14):
        shape = scale(silhouette, xfact=width*(-1 if side == "right" else 1), yfact=width, origin=(0, 0)).buffer(0.3)
        for cx in range(math.ceil(min_x), math.floor(max_x), 1):
            for cy in range(math.ceil(min_y), math.floor(max_y), 1):
                if safe.contains(translate(shape, xoff=cx, yoff=cy)):
                    distance = (cx-center)**2+(cy-image_center_y-18)**2
                    candidates.append((width, -distance, cx, cy))
        if candidates:
            break
    assert candidates, (side, "No unobstructed gap for knife")
    hero_width, _, center, image_center_y = max(candidates)
    blade_visibility = figure_visibility = 1.0
    hero_height = hero_width*artwork_alpha.height/artwork_alpha.width
    lettering_boxes.append((center, image_center_y, hero_width+0.5, hero_height+0.5))
    poem = [
        "Do you wrestle with dreams?",
        "Do you contend with shadows?",
        "Do you move in a kind of sleep?",
        "Time has slipped away.",
        "Your life is stolen.",
        "You tarried with trifles,",
        "Victim of your folly.",
    ]
    poem_placements = []
    poem_safe = safe_polygon.difference(box(center-hero_width/2-0.5, image_center_y-hero_height/2-0.5,
                                            center+hero_width/2+0.5, image_center_y+hero_height/2+0.5))
    for index, line in enumerate(poem):
        samples = glyph_pixels(line, 46, 4.2)
        width = max(x for x, y in samples)-min(x for x, y in samples)+minimum_feature
        height = max(y for x, y in samples)-min(y for x, y in samples)+minimum_feature
        choices = []
        target_x = min_x+(max_x-min_x)*((0.30, 0.64, 0.46, 0.72, 0.27, 0.55, 0.38)[index]
                                                   if side == "left" else (0.65, 0.35, 0.54, 0.28, 0.73, 0.45, 0.62)[index])
        target_y = min_y+(max_y-min_y)*(0.12+index*0.115)
        for cx in range(math.ceil(min_x+width/2), math.floor(max_x-width/2), 2):
            for cy in range(math.ceil(min_y+height/2), math.floor(max_y-height/2)):
                bounds = box(cx-width/2-0.3, cy-height/2-0.3, cx+width/2+0.3, cy+height/2+0.3)
                if poem_safe.contains(bounds) and all(clear_pixel(cx+direction*x, cy+y, minimum_feature)
                                                     for x, y in samples for direction in (-1, 1)):
                    choices.append(((cx-target_x)**2+(cy-target_y)**2, cx, cy, bounds))
        assert choices, (side, "No clear position for poem", line)
        _, cx, cy, bounds = min(choices, key=lambda candidate: candidate[0])
        poem_placements.append((line, cx, cy, 46, 4.2))
        lettering_boxes.append((cx, cy, width+0.6, height+0.6))
        poem_safe = poem_safe.difference(bounds.buffer(0.7))
    pixels = []
    def stamp(cx, cy, artwork_width, dot_pitch):
        artwork_image = artwork_alpha.copy()
        if side == "right":
            artwork_image = artwork_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        artwork_image = artwork_image.resize((round(artwork_width/dot_pitch),
            round(artwork_width/dot_pitch*artwork_image.height/artwork_image.width)), Image.Resampling.BOX)
        before = len(pixels)
        left = cx-artwork_image.width*dot_pitch/2
        top = cy-artwork_image.height*dot_pitch/2
        for row in range(artwork_image.height):
            for col in range(artwork_image.width):
                alpha = artwork_image.getpixel((col, row))
                x, y = left+(col+0.5)*dot_pitch, top+(row+0.5)*dot_pitch
                size = dot_pitch if alpha >= 100 else 0
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
                       for bx, by, w, h in lettering_boxes if (bx, by) != (center, image_center_y)):
                    continue
                pixels.append((x-size/2, y-size/2, x+size/2, y+size/2))
        expected = sum(alpha >= 100 for alpha in artwork_image.get_flattened_data())
        assert len(pixels)-before == expected, (side, "Knife graphic was clipped", len(pixels)-before, expected)
        return len(pixels) > before

    assert stamp(center, image_center_y, hero_width, minimum_feature), 'Single knife graphic has no printable pixels'
    stamps = 1
    top_pixels = list(pixels)
    bottom_pixels = list(pixels)
    def lettering(label, cx, cy, max_width, max_height, rotation=0, typeface=font):
        grid = minimum_feature
        for lx, ly in glyph_pixels(label, max_width, max_height, typeface):
            for face, direction in [(top_pixels, 1), (bottom_pixels, -1)]:
                x = cx+direction*lx*math.cos(rotation)+ly*math.sin(rotation)
                y = cy-direction*lx*math.sin(rotation)+ly*math.cos(rotation)
                assert clear_pixel(x, y, grid), (side, label, x, y, "Lettering overlaps a pad or board edge")
                face.append((x-grid/2, y-grid/2, x+grid/2, y+grid/2))

    for label, cx, cy, max_width, max_height in legends:
        lettering(label, cx, cy, max_width, max_height, typeface=branding_font)
    for label, cx, cy, max_width, max_height in poem_placements:
        lettering(label, cx, cy, max_width, max_height)
    for label, x, y, width, height, angle in original_labels:
        lettering(label, x, y, width, height, angle)
    for name, cx, cy, tx, ty in arrows:
        lettering(name, cx, cy, 12, 3.0)
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
    def compact(face):
        rows = {}
        for x0, y0, x1, y1 in face:
            rows.setdefault((round(y0, 4), round(y1, 4)), []).append((round(x0, 4), round(x1, 4)))
        result = []
        for (y0, y1), spans in rows.items():
            spans.sort()
            x0, x1 = spans[0]
            for start, end in spans[1:]:
                if start <= x1 + 0.00001:
                    x1 = max(x1, end)
                else:
                    result.append((x0, y0, x1, y1))
                    x0, x1 = start, end
            result.append((x0, y0, x1, y1))
        return result

    top_pixels, bottom_pixels = compact(top_pixels), compact(bottom_pixels)
    rectangles = "\n".join(
        f'(fp_rect (start {x0-center:.4f} {y0-image_center_y:.4f}) (end {x1-center:.4f} {y1-image_center_y:.4f}) '
        f'(stroke (width 0) (type default)) (fill solid) (layer "{layer}"))'
        for layer, face in [("F.SilkS", top_pixels), ("B.SilkS", bottom_pixels)]
        for x0, y0, x1, y1 in face
    )
    reference = '(property "Reference" "ART1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 1 1) (thickness 0.15))))'
    footprint = f'\n(footprint "crysknife:knife-silkscreen" (layer "F.Cu") (at {center} {image_center_y}) (attr board_only exclude_from_pos_files exclude_from_bom)\n{reference}\n{rectangles}\n)\n'
    closing = text.rfind(")")
    board_path.write_text(text[:closing] + footprint + text[closing:])
    pixels = top_pixels
    svg_rectangles = "".join(
        f'<rect x="{x0:.4f}" y="{y0:.4f}" width="{x1-x0:.4f}" height="{y1-y0:.4f}"/>'
        for x0, y0, x1, y1 in pixels
    )
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{max_x-min_x}mm" height="{max_y-min_y}mm" viewBox="{min_x} {min_y} {max_x-min_x} {max_y-min_y}"><rect x="{min_x}" y="{min_y}" width="{max_x-min_x}" height="{max_y-min_y}" fill="white"/><g fill="black">{svg_rectangles}</g></svg>'
    (root / f"build/pcb/knife-{side}.svg").write_text(svg)
    print(json.dumps({"side": side, "rectangles": len(pixels), "minimum_feature_mm": minimum_feature,
                      "layers": ["F.SilkS", "B.SilkS"], "pad_clearance_mm": 0.3, "native_silk_clearance_mm": 0.25, "stamps": stamps, "edge_clearance_mm": 0.4, "hero_blade_visibility": blade_visibility, "hero_figure_visibility": figure_visibility, "source_sha256": source_hash,
                      "hero_center_mm": [center, image_center_y], "hero_width_mm": hero_width, "poem": poem_placements}))
