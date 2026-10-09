from collections import Counter
from pathlib import Path

import pcbnew


root = Path(__file__).resolve().parents[1]
boards = {}
switches = {}
controllers = {}
for side in ("left", "right"):
    board = pcbnew.LoadBoard(str(root / f"build/pcb/crysknife_{side}.kicad_pcb"))
    boards[side] = board
    artwork = [fp for fp in board.GetFootprints() if fp.GetReference() == "ART1"]
    assert len(artwork) <= 1
    if artwork:
        assert len(list(artwork[0].Pads())) == 0
        assert artwork[0].GetLayer() == pcbnew.F_Cu
    footprints = [fp for fp in board.GetFootprints() if fp.GetReference() != "ART1"]
    assert len(footprints) == 52, (side, len(footprints))
    mounts = [fp for fp in footprints if fp.GetReference().startswith("MH")]
    assert len(mounts) == 4
    for fp in mounts:
        pads = list(fp.Pads())
        assert len(pads) == 1 and pads[0].GetAttribute() == pcbnew.PAD_ATTRIB_NPTH
        assert pads[0].GetDrillSize().x == pcbnew.FromMM(5)
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
    sockets = [next(fp for fp in footprints if fp.GetReference() == ref) for ref in ("MCU1A", "MCU1B")]
    controllers[side] = sockets
    assert controller.GetLayer() == pcbnew.F_Cu
    assert not list(controller.Pads())
    assert all(fp.GetLayer() == pcbnew.B_Cu and len(list(fp.Pads())) == 12 for fp in sockets)
    pads = [pad for socket in sockets for pad in socket.Pads()]
    assert len(pads) == 24
    assert {p.GetNumber() for p in pads} == {str(n) for n in range(1, 25)}
    assert all(p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH for p in pads)
    assert all(p.GetDrillSize().x == pcbnew.FromMM(1) for p in pads)
    center = controller.GetPosition()
    for pad in pads:
        number = int(pad.GetNumber())
        column = 7.62 if number <= 12 else -7.62
        row = number-1 if number <= 12 else 24-number
        assert abs(pad.GetPosition().x-center.x-pcbnew.FromMM(column)) <= 1
        assert abs(pad.GetPosition().y-center.y-pcbnew.FromMM(-12.7+2.54*row)) <= 1
    switches[side] = {fp.GetReference(): fp for fp in keys}
    print(f"{side}: 21 bottom-side MX sockets, 21 polarized diodes, two bottom-side factory-soldered controller sockets")

left_pins = {p.GetNumber(): p.GetNetname() for fp in controllers["left"] for p in fp.Pads()}
right_pins = {p.GetNumber(): p.GetNetname() for fp in controllers["right"] for p in fp.Pads()}
assert left_pins == right_pins
assert set(left_pins.values()) >= {
    "C0", "C1", "C2", "C3", "C4", "C5", "R0", "R1", "R2", "R3",
    "P2", "P3", "P4", "RAW", "GND", "VCC", "RST",
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

for index, ref in enumerate(("S2", "S5", "S8", "S11", "S14", "S17")):
    position = switches["left"][ref].GetPosition()
    assert position.x == pcbnew.FromMM(100 + 20 * index), (ref, "column spacing")
    assert position.y == pcbnew.FromMM((80, 80, 68, 63, 68, 70)[index]), (ref, "column stagger")
for ref in ("S1", "S4", "S7", "S10", "S13", "S16"):
    number = int(ref[1:])
    lower = switches["left"][ref].GetPosition().y
    home = switches["left"][f"S{number+1}"].GetPosition().y
    upper = switches["left"][f"S{number+2}"].GetPosition().y
    assert lower - home == home - upper == pcbnew.FromMM(20)
print("MX layout: 20 mm pitch and 12/5/-5/-2 mm stagger confirmed")
