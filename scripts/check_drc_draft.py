import json
from pathlib import Path
import sys


root = Path(__file__).resolve().parents[1]
routed = sys.argv[1:] == ["--routed"]
assert not sys.argv[1:] or routed
for side in ("left", "right"):
    report = json.loads((root / f"build/pcb/{side}{'-routed' if routed else ''}-drc.json").read_text())
    unexpected = [item for item in report["violations"]
                  if item["type"] != "lib_footprint_issues" or item["severity"] != "warning"]
    assert not unexpected, (side, unexpected)
    expected = 0 if routed else 72
    assert len(report["unconnected_items"]) == expected, (side, len(report["unconnected_items"]))
    print(f"{side}: no unexpected violations; {expected} unrouted connections remain")
