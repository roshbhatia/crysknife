import json
import math
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]
LAYERS = {"top": pcbnew.F_Cu, "bottom": pcbnew.B_Cu}


for side in ("left", "right"):
    expected = json.loads((ROOT / f"build/tscircuit/{side}.json").read_text())
    data = json.loads((ROOT / f"build/tscircuit/{side}-routed.circuit.json").read_text())
    board = pcbnew.LoadBoard(str(ROOT / f"build/pcb/fridakeeb_{side}.kicad_pcb"))
    assert len(list(board.GetTracks())) == 0, "Regenerate the placement before merging routes"
    names = sorted({p["net"] for p in expected["pads"] if p["net"]})
    net_codes = {p["net"]: p["netCode"] for p in expected["pads"] if p["net"]}
    source_nets = {n["source_net_id"]: names[int(n["name"][1:])]
                   for n in data if n["type"] == "source_net"}
    traces = {n["source_trace_id"]: n for n in data if n["type"] == "source_trace"}
    routed = [n for n in data if n["type"] == "pcb_trace"]

    def position(p):
        return pcbnew.VECTOR2I(pcbnew.FromMM(p["x"] + expected["origin"][0]),
                              pcbnew.FromMM(expected["origin"][1] - p["y"]))

    route_codes = {}
    segments = 0
    for trace in routed:
        connected = traces[trace["source_trace_id"]]["connected_source_net_ids"]
        assert len(connected) == 1
        code = net_codes[source_nets[connected[0]]]
        route_codes[trace["pcb_trace_id"]] = code
        route = trace["route"]
        for a, b in zip(route, route[1:]):
            assert a["route_type"] in ("wire", "via") and b["route_type"] in ("wire", "via"), (a, b)
            if position(a) == position(b):
                continue
            wire = a if a["route_type"] == "wire" else b
            assert wire["route_type"] == "wire"
            if a["route_type"] == b["route_type"] == "wire":
                assert a["layer"] == b["layer"] and a["width"] == b["width"]
            assert not any(k in wire for k in ("start_width", "end_width")), "Tapered traces need a dedicated converter"
            track = pcbnew.PCB_TRACK(board)
            track.SetStart(position(a))
            track.SetEnd(position(b))
            track.SetWidth(pcbnew.FromMM(wire["width"]))
            track.SetLayer(LAYERS[wire["layer"]])
            track.SetNetCode(code)
            board.Add(track)
            segments += 1
    vias = [n for n in data if n["type"] == "pcb_via"]
    created_vias = []
    for source in vias:
        assert set(source["layers"]) == {"top", "bottom"}
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(position(source))
        via.SetWidth(pcbnew.FromMM(source["outer_diameter"]))
        via.SetDrill(pcbnew.FromMM(source["hole_diameter"]))
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        via.SetNetCode(route_codes[source["pcb_trace_id"]])
        board.Add(via)
        created_vias.append((source, via))

    def move_via(via, target, code):
        old, new = via.GetPosition(), position(target)
        connected = 0
        for track in board.GetTracks():
            if isinstance(track, pcbnew.PCB_VIA):
                continue
            for getter, setter in [(track.GetStart, track.SetStart), (track.GetEnd, track.SetEnd)]:
                if getter() == old:
                    assert track.GetNetCode() == code
                    setter(new)
                    connected += 1
        assert connected == 2, (side, "Unexpected via escape connectivity", connected)
        via.SetPosition(new)

    def coordinates(via):
        p = via.GetPosition()
        return {"x": pcbnew.ToMM(p.x)-expected["origin"][0], "y": expected["origin"][1]-pcbnew.ToMM(p.y)}

    finishing = []
    for net, own_number, other_number, delta_y in [("GND", "3", "4", -0.7), ("RST", "4", "3", 0.7)]:
        own = next(p for p in expected["pads"] if p["ref"] == "RST1" and p["number"] == own_number)
        other = next(p for p in expected["pads"] if p["ref"] == "RST1" and p["number"] == other_number)
        assert own["net"] == net and other["net"] != net
        assert own["shape"] == other["shape"] == "rect"
        assert own["rotation"] % 180 == other["rotation"] % 180 == 0

        def pad_gap(point, pad, diameter):
            dx = max(0, abs(point["x"]-pad["x"])-pad["width"]/2)
            dy = max(0, abs(point["y"]-pad["y"])-pad["height"]/2)
            return math.hypot(dx, dy)-diameter/2

        for source, via in created_vias:
            if via.GetNetCode() != net_codes[net]:
                continue
            if math.hypot(source["x"]-own["x"], source["y"]-own["y"]) > 1.4:
                continue
            before = pad_gap(source, other, source["outer_diameter"])
            if before >= 0.25:
                continue
            target = {"x": own["x"]-own["width"]/2-source["outer_diameter"]/2-0.1,
                      "y": own["y"]+delta_y}
            after = pad_gap(target, other, source["outer_diameter"])
            assert after >= 0.25 and pad_gap(target, own, source["outer_diameter"]) >= 0.1
            move_via(via, target, net_codes[net])
            finishing.append({"reference": "RST1", "net": net, "via": source["pcb_via_id"],
                              "from": {axis: source[axis] for axis in ("x", "y")}, "to": target,
                              "opposite_pad_clearance_before_mm": before, "opposite_pad_clearance_after_mm": after})
        assert len(finishing) <= 2, "Unexpected extra reset escape vias"
    for index, (source, first) in enumerate(created_vias):
        for other_source, second in created_vias[index+1:]:
            if first.GetNetCode() == second.GetNetCode():
                continue
            a, b = coordinates(first), coordinates(second)
            radii = pcbnew.ToMM(first.GetWidth()+second.GetWidth())/2
            distance = math.hypot(a["x"]-b["x"], a["y"]-b["y"])
            before = distance-radii
            if before >= 0.25:
                continue
            assert {first.GetNetname(), second.GetNetname()} == {"RAW", "GND"}, "Unrecognized via clearance defect"
            if first.GetNetname() == "GND":
                moving, fixed, moving_source = first, second, source
            else:
                moving, fixed, moving_source = second, first, other_source
            start, anchor = coordinates(moving), coordinates(fixed)
            scale = (radii+0.3)/distance
            target = {axis: anchor[axis]+(start[axis]-anchor[axis])*scale for axis in ("x", "y")}
            move_via(moving, target, net_codes["GND"])
            after = math.dist(tuple(coordinates(moving).values()), tuple(coordinates(fixed).values()))-radii
            assert after >= 0.29999
            finishing.append({"net": "GND", "via": moving_source["pcb_via_id"], "from": start, "to": target,
                              "opposite_net": "RAW", "via_clearance_before_mm": before, "via_clearance_after_mm": after})
    for index, (_, first) in enumerate(created_vias):
        for _, second in created_vias[index+1:]:
            if first.GetNetCode() != second.GetNetCode():
                gap = math.dist(tuple(coordinates(first).values()), tuple(coordinates(second).values()))-pcbnew.ToMM(first.GetWidth()+second.GetWidth())/2
                assert gap >= 0.24999, (side, "Via finishing introduced another clearance defect", gap)
    (ROOT / f"build/pcb/{side}-route-finishing.json").write_text(json.dumps(finishing, indent=2)+"\n")
    output = ROOT / f"build/pcb/fridakeeb_{side}_routed.kicad_pcb"
    pcbnew.SaveBoard(str(output), board)
    print(f"{side}: merged {segments} copper segments and {len(vias)} vias into original KiCad geometry")
