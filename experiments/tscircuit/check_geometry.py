import json
from pathlib import Path


root = Path(__file__).resolve().parents[2]
data = json.loads((root / "build/research/tscircuit-pilot.json").read_text())
source = next(item for item in data if item["type"] == "source_component" and item["name"] == "S1")
component = next(item for item in data if item["type"] == "pcb_component"
                 and item["source_component_id"] == source["source_component_id"])
pads = [item for item in data if item["type"] == "pcb_smtpad"
        and item["pcb_component_id"] == component["pcb_component_id"]]
expected = {"1": (-9 - 7.085, 2.54), "2": (-9 + 5.842, 5.08)}
failures = []
for pad in pads:
    pin = pad["port_hints"][0]
    x, y = expected[pin]
    if abs(pad["x"] - x) > 0.001 or abs(pad["y"] - y) > 0.001 or pad["layer"] != "bottom":
        failures.append({"pin": pin, "expected": [x, y], "actual": [pad["x"], pad["y"]],
                         "layer": pad["layer"]})
print(json.dumps({"geometry_preserved": not failures, "differences": failures}, indent=2))
raise SystemExit(bool(failures))
