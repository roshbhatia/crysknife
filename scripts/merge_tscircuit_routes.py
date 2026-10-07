import json
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
    output = ROOT / f"build/pcb/fridakeeb_{side}_routed.kicad_pcb"
    pcbnew.SaveBoard(str(output), board)
    print(f"{side}: merged {segments} copper segments and {len(vias)} vias into original KiCad geometry")
