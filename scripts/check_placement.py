from collections import Counter
from pathlib import Path

import pcbnew


root = Path(__file__).resolve().parents[1]
boards = {}
switches = {}
controllers = {}
for side in ("left", "right"):
    board = pcbnew.LoadBoard(str(root / f"build/pcb/fridakeeb_{side}.kicad_pcb"))
    boards[side] = board
    footprints = [fp for fp in board.GetFootprints()
                  if fp.GetFPID().GetLibItemName() != "frida-silkscreen"]
    assert len(footprints) == 46, (side, len(footprints))
    keys = [fp for fp in footprints if fp.GetReference().startswith("S")]
    diodes = [fp for fp in footprints if fp.GetReference().startswith("D")]
    assert len(keys) == len(diodes) == 21
    internal_nets = Counter()
    column_nets = Counter()
    row_nets = Counter()
    for fp in keys:
        assert fp.GetLayer() == pcbnew.B_Cu
        pads = {p.GetNumber(): p for p in fp.Pads() if p.GetNumber()}
        assert set(pads) == {"1", "2"}
        assert all(p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD for p in pads.values())
        assert all(p.IsOnLayer(pcbnew.B_Paste) for p in pads.values())
        column_nets[pads["1"].GetNetname()] += 1
        internal_nets[pads["2"].GetNetname()] += 1
    diode_internal_nets = Counter()
    for fp in diodes:
        pads = {p.GetNumber(): p for p in fp.Pads()}
        assert set(pads) == {"1", "2"}
        assert all(p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD for p in pads.values())
        assert all(p.IsOnLayer(pcbnew.B_Paste) for p in pads.values())
        row_nets[pads["1"].GetNetname()] += 1
        diode_internal_nets[pads["2"].GetNetname()] += 1
    assert internal_nets == diode_internal_nets
    assert len(internal_nets) == 21 and set(internal_nets.values()) == {1}
    assert column_nets == {"C0": 3, "C1": 3, "C2": 3, "C3": 4, "C4": 4, "C5": 4}
    assert row_nets == {"R0": 6, "R1": 6, "R2": 6, "R3": 3}
    controller = next(fp for fp in footprints if fp.GetReference() == "MCU1")
    controllers[side] = controller
    assert controller.GetLayer() == pcbnew.F_Cu
    pads = list(controller.Pads())
    assert len(pads) == 24
    assert {p.GetNumber() for p in pads} == {str(n) for n in range(1, 25)}
    assert all(p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH for p in pads)
    assert all(p.GetDrillSize().x == pcbnew.FromMM(0.85) for p in pads)
    switches[side] = {fp.GetReference(): fp for fp in keys}
    print(f"{side}: 21 bottom-side MX sockets, 21 polarized diodes, 24 spring-header contacts")

left_pins = {p.GetNumber(): p.GetNetname() for p in controllers["left"].Pads()}
right_pins = {p.GetNumber(): p.GetNetname() for p in controllers["right"].Pads()}
assert left_pins == right_pins
assert set(left_pins.values()) >= {
    "C0", "C1", "C2", "C3", "C4", "C5", "R0", "R1", "R2", "R3",
    "TP_DATA", "TP_CLK", "TP_RST", "RAW", "GND", "VCC", "RST",
}
for ref, left in switches["left"].items():
    right = switches["right"][ref]
    assert abs(left.GetPosition().x + right.GetPosition().x - pcbnew.FromMM(335)) <= 1
    assert abs(left.GetPosition().y - right.GetPosition().y) <= 1
    assert abs((left.GetOrientationDegrees() + right.GetOrientationDegrees()) % 360) < 0.0001
left_box = boards["left"].GetBoardEdgesBoundingBox()
right_box = boards["right"].GetBoardEdgesBoundingBox()
outline_tolerance = pcbnew.FromMM(0.001)
assert abs(left_box.GetWidth() - right_box.GetWidth()) <= outline_tolerance
assert abs(left_box.GetHeight() - right_box.GetHeight()) <= outline_tolerance
print("Mirrored key positions, board dimensions within 0.001 mm, and controller pad-to-net mapping verified.")
print("Placement checks do not prove routing, supplier assembly, or physical fit.")
