import json
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]


def polygon(zone, points):
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in points:
        outline.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))


for side in ("left", "right"):
    path = ROOT / f"build/pcb/crysknife_{side}_routed.kicad_pcb"
    board = pcbnew.LoadBoard(str(path))
    assert not list(board.Zones()), "Regenerate routes before adding ground zones"
    data = json.loads((ROOT / f"build/tscircuit/{side}.json").read_text())
    points = [(p["x"] + data["origin"][0], data["origin"][1] - p["y"]) for p in data["outline"]]
    controller = next(fp for fp in board.GetFootprints() if fp.GetReference() == "MCU1")
    cx, cy = [pcbnew.ToMM(v) for v in (controller.GetPosition().x, controller.GetPosition().y)]
    exclusion = [(cx-14, cy-23), (cx+14, cy-23), (cx+14, cy+23), (cx-14, cy+23)]
    ground_codes = {p.GetNetCode() for fp in board.GetFootprints()
                    if fp.GetReference() in ("MCU1A", "MCU1B")
                    for p in fp.Pads() if p.GetNetname() == "GND"}
    assert len(ground_codes) == 1, "Controller sockets must share the GND net"
    ground_code = ground_codes.pop()
    if side == "right":
        battery = next(fp for fp in board.GetFootprints() if fp.GetReference() == "JST1")
        ground_pad = next(p for p in battery.Pads() if p.GetNumber() == "1")
        assert ground_pad.GetNetname() == "GND"
        ground_pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    board.GetDesignSettings().m_CopperEdgeClearance = pcbnew.FromMM(0.55)
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        keepout = pcbnew.ZONE(board)
        keepout.SetLayer(layer)
        keepout.SetZoneName("nice!nano body and antenna: no ground pour")
        keepout.SetIsRuleArea(True)
        keepout.SetDoNotAllowZoneFills(True)
        keepout.SetDoNotAllowTracks(False)
        keepout.SetDoNotAllowVias(False)
        keepout.SetDoNotAllowPads(False)
        keepout.SetDoNotAllowFootprints(False)
        polygon(keepout, exclusion)
        board.Add(keepout)
        zone = pcbnew.ZONE(board)
        zone.SetLayer(layer)
        zone.SetZoneName("GND")
        zone.SetNetCode(ground_code)
        zone.SetLocalClearance(pcbnew.FromMM(0.3))
        zone.SetMinThickness(pcbnew.FromMM(0.25))
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.SetThermalReliefGap(pcbnew.FromMM(0.3))
        zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
        zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        polygon(zone, points)
        zone.Outline().Deflate(pcbnew.FromMM(0.65), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,
                               pcbnew.FromMM(0.005))
        assert zone.Outline().OutlineCount() == 1
        board.Add(zone)
    board.BuildConnectivity()
    assert pcbnew.ZONE_FILLER(board).Fill(board.Zones()), "Ground fill failed"
    pcbnew.SaveBoard(str(path), board)
    saved = pcbnew.LoadBoard(str(path))
    if side == "right":
        battery = next(fp for fp in saved.GetFootprints() if fp.GetReference() == "JST1")
        assert next(p for p in battery.Pads() if p.GetNumber() == "1").GetLocalZoneConnection() == pcbnew.ZONE_CONNECTION_FULL
    zones = [z for z in saved.Zones() if not z.GetIsRuleArea()]
    assert len(zones) == 2 and {z.GetLayer() for z in zones} == {pcbnew.F_Cu, pcbnew.B_Cu}
    evidence = []
    for zone in zones:
        layer = zone.GetLayer()
        assert zone.GetNetname() == "GND" and zone.HasFilledPolysForLayer(layer)
        assert zone.GetIslandRemovalMode() == pcbnew.ISLAND_REMOVAL_MODE_ALWAYS
        for x in range(-13, 14):
            for y in range(-22, 23):
                point = pcbnew.VECTOR2I(pcbnew.FromMM(cx+x), pcbnew.FromMM(cy+y))
                assert not zone.HitTestFilledArea(layer, point), "Ground pour beneath controller exclusion"
        polys = zone.GetFilledPolysList(layer)
        assert polys.OutlineCount() > 0
        evidence.append({"layer": saved.GetLayerName(layer), "net": zone.GetNetname(),
                         "filled_polygons": polys.OutlineCount(), "clearance_mm": 0.3,
                         "board_outline_inset_mm": 0.65,
                         "battery_ground_connection": "solid" if side == "right" else "thermal",
                         "island_removal": "always", "controller_exclusion_mm": exclusion})
    (ROOT / f"build/pcb/{side}-ground-fill.json").write_text(json.dumps(evidence, indent=2)+"\n")
    print(f"{side}: filled GND on both faces; saved fill and controller exclusion verified")
