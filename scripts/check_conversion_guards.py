import copy
import json
from pathlib import Path
import tempfile

import check_tscircuit


source = check_tscircuit.ROOT
original = json.loads((source / "build/tscircuit/left-placement.circuit.json").read_text())
with tempfile.TemporaryDirectory() as directory:
    check_tscircuit.ROOT = Path(directory)
    output = check_tscircuit.ROOT / "build/tscircuit"
    output.mkdir(parents=True)
    (output / "left.json").write_text((source / "build/tscircuit/left.json").read_text())
    cases = {}
    for label, kind, field, value in [
        ("mirrored socket", "pcb_smtpad", "x", 0),
        ("wrong assembly side", "pcb_smtpad", "layer", "top"),
        ("wrong controller drill", "pcb_plated_hole", "hole_diameter", 0.6),
    ]:
        data = copy.deepcopy(original)
        next(n for n in data if n["type"] == kind)[field] = value
        cases[label] = data
    data = copy.deepcopy(original)
    data.remove(next(n for n in data if n["type"] == "source_net"))
    cases["lost complete net"] = data
    data = copy.deepcopy(original)
    data.remove(next(n for n in data if n["type"] == "pcb_hole"))
    cases["lost mounting hole"] = data
    for label, data in cases.items():
        (output / "left-placement.circuit.json").write_text(json.dumps(data))
        try:
            check_tscircuit.check("left", "placement")
        except AssertionError:
            print(f"Rejected unsafe conversion: {label}")
        else:
            raise AssertionError(f"Accepted unsafe conversion: {label}")
