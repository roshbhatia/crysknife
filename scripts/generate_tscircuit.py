import json
import math
from pathlib import Path

from kicad_sexp import child, children, parse


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build/tscircuit"
GENERATED = ROOT / "tscircuit/generated"
MODELS = ROOT / "tscircuit/models"


def point(node, name):
    return tuple(map(float, child(node, name)[1:3]))


def edge_points(node):
    start, end = point(node, "start"), point(node, "end")
    if node[0] == "gr_line":
        return [start, end]
    mid = point(node, "mid")
    ax, ay = start
    bx, by = mid
    cx, cy = end
    denominator = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    assert abs(denominator) > 1e-10, "Degenerate outline arc"
    a, b, c = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ox = (a * (by - cy) + b * (cy - ay) + c * (ay - by)) / denominator
    oy = (a * (cx - bx) + b * (ax - cx) + c * (bx - ax)) / denominator
    angles = [math.atan2(y - oy, x - ox) for x, y in (start, mid, end)]
    sweep = (angles[2] - angles[0]) % math.tau
    if (angles[1] - angles[0]) % math.tau > sweep:
        sweep -= math.tau
    radius = math.hypot(ax - ox, ay - oy)
    steps = max(2, math.ceil(abs(sweep) / (2 * math.acos(1 - min(0.005 / radius, 1)))))
    return [start] + [(ox + radius * math.cos(angles[0] + sweep * i / steps),
                      oy + radius * math.sin(angles[0] + sweep * i / steps))
                     for i in range(1, steps)] + [end]


def descriptor(side):
    source = ROOT / f"build/pcb/crysknife_{side}.kicad_pcb"
    board = parse(source.read_text())
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
            raise ValueError("Outline contains disconnected edges")
        outline.extend(edge[1:])
        edges.pop(index)
    assert math.dist(outline[0], outline[-1]) < 1e-4
    outline.pop()
    origin = [(min(p[i] for p in outline) + max(p[i] for p in outline)) / 2 for i in (0, 1)]

    def convert(p):
        return {"x": p[0] - origin[0], "y": origin[1] - p[1]}

    silkscreen = []
    for fp in children(board, "footprint"):
        if not any(p[1] == "Reference" and p[2] == "ART1" for p in children(fp, "property")):
            continue
        at = child(fp, "at")
        fx, fy = map(float, at[1:3])
        for rect in children(fp, "fp_rect"):
            layer = {"F.SilkS": "top", "B.SilkS": "bottom"}[child(rect, "layer")[1]]
            x0, y0 = point(rect, "start")
            x1, y1 = point(rect, "end")
            silkscreen.append({**convert((fx + (x0+x1)/2, fy + (y0+y1)/2)),
                               "width": x1-x0, "height": y1-y0, "layer": layer})
    assert silkscreen, "Apply artwork before generating the React model"
    pads = []
    holes = []
    for fp in children(board, "footprint"):
        if not children(fp, "pad"):
            continue
        properties = children(fp, "property")
        ref = next(p[2] for p in properties if p[1] == "Reference")
        at = child(fp, "at")
        fx, fy = map(float, at[1:3])
        angle = math.radians(float(at[3]) if len(at) > 3 else 0)
        for index, pad in enumerate(children(fp, "pad")):
            local = child(pad, "at")
            x, y = map(float, local[1:3])
            position = convert((fx + x * math.cos(angle) + y * math.sin(angle),
                                fy - x * math.sin(angle) + y * math.cos(angle)))
            size = list(map(float, child(pad, "size")[1:3]))
            drill = child(pad, "drill")
            if pad[2] == "np_thru_hole":
                assert pad[3] == "circle" and size[0] == size[1]
                holes.append({**position, "diameter": float(drill[1]), "ref": ref, "index": index})
                continue
            assert pad[2] in ("smd", "thru_hole") and pad[3] in ("rect", "circle", "oval", "roundrect")
            net = child(pad, "net")
            layers = child(pad, "layers")[1:]
            pads.append({**position, "name": f"P{len(pads) + 1}", "ref": ref,
                         "number": pad[1], "index": index, "kind": pad[2], "shape": pad[3],
                         "width": size[0], "height": size[1],
                         "radius": min(size) * float(child(pad, "roundrect_rratio")[1]) if pad[3] == "roundrect" else 0,
                         "rotation": float(local[3]) if len(local) > 3 else 0,
                         "layer": "bottom" if "B.Cu" in layers else "top",
                         "holeDiameter": float(drill[1]) if drill else None,
                         "net": net[2] if net else None, "netCode": int(net[1]) if net else 0})
    return {"side": side, "origin": origin, "pads": pads, "holes": holes,
            "outline": [convert(p) for p in outline], "silkscreen": silkscreen}


def jsx(data):
    lines = [f'import artwork from "../models/{data["side"]}-artwork"', 'export default ({ routing = true }: { routing?: boolean }) => (',
             f'<board solderMaskColor="white" silkscreenColor="black" outline={{{json.dumps(data["outline"])}}} layers={{2}} thickness={{1.6}} '
             'autorouter="auto-local" routingDisabled={!routing} '
             'placementDrcChecksDisabled={routing} '
             'minTraceWidth={0.25} minTraceToPadEdgeClearance={0.2} minViaEdgeToPadEdgeClearance={0.25} '
             'minTraceToHoleEdgeClearance={0.3} '
             'minBoardEdgeClearance={0.55} minViaHoleDiameter={0.3} minViaPadDiameter={0.6}>']
    for pad in data["pads"]:
        common = 'portHints={["1"]}'
        if pad["kind"] == "smd":
            primitive = (f'<smtpad shape="rotated_rect" width={{{pad["width"]}}} '
                         f'height={{{pad["height"]}}} ccwRotation={{0}} '
                         f'layer="{pad["layer"]}" {common} />')
        elif pad["shape"] == "circle":
            primitive = (f'<platedhole shape="circle" outerDiameter={{{pad["width"]}}} '
                         f'holeDiameter={{{pad["holeDiameter"]}}} {common} />')
        elif pad["shape"] == "oval":
            primitive = (f'<platedhole shape="oval" outerWidth={{{pad["width"]}}} '
                         f'outerHeight={{{pad["height"]}}} holeWidth={{{pad["holeDiameter"]}}} '
                         f'holeHeight={{{pad["holeDiameter"]}}} {common} />')
        else:
            assert pad["shape"] == "roundrect"
            primitive = (f'<platedhole shape="circular_hole_with_rect_pad" '
                         f'rectPadWidth={{{pad["width"]}}} rectPadHeight={{{pad["height"]}}} '
                         f'rectBorderRadius={{{pad["radius"]}}} holeDiameter={{{pad["holeDiameter"]}}} '
                         'holeOffsetX={0} holeOffsetY={0} '
                         f'{common} />')
        lines.append(f'<chip name="{pad["name"]}" pcbX={{{pad["x"]}}} pcbY={{{pad["y"]}}} '
                     f'layer="{pad["layer"]}" pcbRotation={{{pad["rotation"]}}} '
                     f'footprint={{<footprint>{primitive}</footprint>}} />')
    for hole in data["holes"]:
        lines.append(f'<hole pcbX={{{hole["x"]}}} pcbY={{{hole["y"]}}} diameter={{{hole["diameter"]}}} />')
    lines.append('{artwork.map(([x, y, width, height, layer], index) => <silkscreenrect key={index} '
                 'pcbX={x} pcbY={y} width={width} height={height} layer={layer} '
                 'filled={true} stroke="none" strokeWidth={0} />)}')
    nets = sorted({p["net"] for p in data["pads"] if p["net"]})
    for index, net in enumerate(nets):
        selectors = [f'.{p["name"]} > .pin1' for p in data["pads"] if p["net"] == net]
        if len(selectors) > 1:
            lines.append(f'<net name="N{index}" connectsTo={{{json.dumps(selectors)}}} />')
    return '\n'.join(lines + ['</board>', ')', ''])


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    for side in ("left", "right"):
        data = descriptor(side)
        (OUTPUT / f"{side}.json").write_text(json.dumps(data, indent=2) + '\n')
        rectangles = [[round(rect[k], 6) for k in ('x', 'y', 'width', 'height')] + [rect['layer']]
                      for rect in data['silkscreen']]
        module = 'type Rectangle = [number, number, number, number, "top" | "bottom"]\nconst artwork: Rectangle[] = [\n'
        module += ',\n'.join(json.dumps(rect, separators=(',', ':')) for rect in rectangles)
        (MODELS/f'{side}-artwork.ts').write_text(module+'\n]\nexport default artwork\n')
        (GENERATED / f"{side}-board.circuit.tsx").write_text(jsx(data))
        for routing, suffix in ((False, "placement"), (True, "routed")):
            wrapper = f'import Board from "./{side}-board.circuit"\nexport default () => <Board routing={{{str(routing).lower()}}} />\n'
            (GENERATED / f"{side}-{suffix}.circuit.tsx").write_text(wrapper)
        print(f'{side}: {len(data["pads"])} copper pads, {len(data["holes"])} holes')
