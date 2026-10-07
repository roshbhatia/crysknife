import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
for side in ("left", "right"):
    report = json.loads((root / f"build/pcb/{side}-drc.json").read_text())
    unexpected = [item for item in report["violations"] if item["type"] != "lib_footprint_issues"]
    assert not unexpected, (side, unexpected)
    assert len(report["unconnected_items"]) == 72, (side, len(report["unconnected_items"]))
    print(f"{side}: no unexpected violations; 72 unrouted connections remain")
