import json
import math
from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parents[1]


def close(actual, expected):
    assert math.isclose(actual, expected, abs_tol=0.001), (actual, expected)


for side in ("left", "right"):
    data = json.loads((ROOT / f"build/tscircuit/{side}.json").read_text())
    board = pcbnew.LoadBoard(str(ROOT / f"build/pcb/fridakeeb_{side}.kicad_pcb"))
    pads = {(fp.GetReference(), i): pad for fp in board.GetFootprints() for i, pad in enumerate(fp.Pads())}
    count = 230 if side == "left" else 250
    assert len(pads) == len(data["pads"]) + len(data["holes"]) == count
    for expected in data["pads"] + data["holes"]:
        actual = pads[(expected["ref"], expected["index"])]
        close(pcbnew.ToMM(actual.GetPosition().x), expected["x"] + data["origin"][0])
        close(pcbnew.ToMM(actual.GetPosition().y), data["origin"][1] - expected["y"])
        if "diameter" in expected:
            assert actual.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH
            close(pcbnew.ToMM(actual.GetDrillSize().x), expected["diameter"])
            close(pcbnew.ToMM(actual.GetDrillSize().y), expected["diameter"])
            continue
        assert actual.GetNumber() == expected["number"]
        assert actual.GetNetname() == (expected["net"] or "")
        assert actual.GetNetCode() == expected["netCode"]
        close(pcbnew.ToMM(actual.GetSize().x), expected["width"])
        close(pcbnew.ToMM(actual.GetSize().y), expected["height"])
        close((actual.GetOrientationDegrees() - expected["rotation"] + 90) % 180 - 90, 0)
        assert actual.GetShape() == {"circle": pcbnew.PAD_SHAPE_CIRCLE, "rect": pcbnew.PAD_SHAPE_RECT,
                                     "oval": pcbnew.PAD_SHAPE_OVAL, "roundrect": pcbnew.PAD_SHAPE_ROUNDRECT}[expected["shape"]]
        if expected["holeDiameter"]:
            assert actual.GetAttribute() == pcbnew.PAD_ATTRIB_PTH
            for axis in (actual.GetDrillSize().x, actual.GetDrillSize().y):
                close(pcbnew.ToMM(axis), expected["holeDiameter"])
        else:
            assert actual.GetAttribute() == pcbnew.PAD_ATTRIB_SMD
            copper = pcbnew.B_Cu if expected["layer"] == "bottom" else pcbnew.F_Cu
            opposite = pcbnew.F_Cu if copper == pcbnew.B_Cu else pcbnew.B_Cu
            assert actual.IsOnLayer(copper) and not actual.IsOnLayer(opposite), expected
    print(f"{side}: KiCad independently confirms all {count} pad/hole descriptors")
