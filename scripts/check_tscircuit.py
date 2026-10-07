import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def close(actual, expected):
    assert math.isclose(actual, expected, abs_tol=0.001), (actual, expected)


def check(side, stage):
    expected = json.loads((ROOT / f"build/tscircuit/{side}.json").read_text())
    data = json.loads((ROOT / f"build/tscircuit/{side}-{stage}.circuit.json").read_text())
    components = {n["source_component_id"]: n["name"] for n in data if n["type"] == "source_component"}
    pcb_components = {n["pcb_component_id"]: components[n["source_component_id"]]
                      for n in data if n["type"] == "pcb_component"}
    pads = {pcb_components[n["pcb_component_id"]]: n for n in data
            if n["type"] in ("pcb_smtpad", "pcb_plated_hole")}
    assert len(pads) == len(expected["pads"]) == 121
    ports = {components[n["source_component_id"]]: n for n in data if n["type"] == "source_port"}
    nets = {n["name"]: n["subcircuit_connectivity_map_key"] for n in data if n["type"] == "source_net"}
    names = sorted({p["net"] for p in expected["pads"] if p["net"]})
    net_keys = {net: nets[f"N{i}"] for i, net in enumerate(names) if f"N{i}" in nets}
    for source in expected["pads"]:
        actual = pads[source["name"]]
        for axis in ("x", "y"):
            close(actual[axis], source[axis])
        if source["kind"] == "smd":
            assert actual["type"] == "pcb_smtpad" and actual["layer"] == source["layer"]
            for dimension in ("width", "height"):
                close(actual[dimension], source[dimension])
            close((actual.get("ccw_rotation", 0) - source["rotation"]) % 180, 0)
        else:
            assert actual["type"] == "pcb_plated_hole" and set(actual["layers"]) == {"top", "bottom"}
            if source["shape"] == "circle":
                close(actual["outer_diameter"], source["width"])
                close(actual["hole_diameter"], source["holeDiameter"])
            elif source["shape"] == "oval":
                close(actual["outer_width"], source["width"])
                close(actual["outer_height"], source["height"])
                close(actual["hole_width"], source["holeDiameter"])
                close(actual["hole_height"], source["holeDiameter"])
                close((actual.get("ccw_rotation", 0) - source["rotation"]) % 180, 0)
            else:
                close(actual["rect_pad_width"], source["width"])
                close(actual["rect_pad_height"], source["height"])
                close(actual["hole_diameter"], source["holeDiameter"])
                close(actual["rect_border_radius"], source["radius"])
                close((actual.get("rect_ccw_rotation", 0) - source["rotation"]) % 180, 0)
        key = ports[source["name"]].get("subcircuit_connectivity_map_key")
        if source["net"] in net_keys:
            assert key == net_keys[source["net"]], (source, key)
        else:
            assert key not in net_keys.values(), source
    holes = [n for n in data if n["type"] == "pcb_hole"]
    assert len(holes) == len(expected["holes"]) == 109
    for source, actual in zip(expected["holes"], holes):
        for axis in ("x", "y"):
            close(actual[axis], source[axis])
        close(actual["hole_diameter"], source["diameter"])
    board = next(n for n in data if n["type"] == "pcb_board")
    close(board["thickness"], 1.6)
    assert len(board["outline"]) == len(expected["outline"])
    for a, b in zip(board["outline"], expected["outline"]):
        for axis in ("x", "y"):
            close(a[axis], b[axis])
    errors = [n for n in data if n["type"].endswith("_error")]
    by_id = {n.get("pcb_hole_id", n.get("pcb_smtpad_id")): n for n in data
             if n["type"] in ("pcb_hole", "pcb_smtpad")}
    diagnostics = []
    for error in errors:
        if error["type"] == "source_runtime_error" and stage == "routed":
            assert error["phase_name"] == "PcbDesignRuleChecks"
            assert error["message"] == "DRC could not complete (routing): Illegal Parameters"
            report = json.loads((ROOT / f"build/tscircuit/{side}-routing-checks.json").read_text())
            assert report == [], report
            continue
        assert error["type"] == "pcb_footprint_overlap_error", error
        ids = error.get("pcb_hole_ids", []) + error.get("pcb_smtpad_ids", [])
        assert len(ids) == 2, error
        a, b = [by_id[i] for i in ids]
        assert a["type"] == "pcb_hole", error
        dx, dy = a["x"] - b["x"], a["y"] - b["y"]
        if b["type"] == "pcb_hole":
            clearance = math.hypot(dx, dy) - (a["hole_diameter"] + b["hole_diameter"]) / 2
        else:
            angle = math.radians(b.get("ccw_rotation", 0))
            x, y = dx * math.cos(angle) + dy * math.sin(angle), -dx * math.sin(angle) + dy * math.cos(angle)
            clearance = math.hypot(max(abs(x) - b["width"] / 2, 0),
                                   max(abs(y) - b["height"] / 2, 0)) - a["hole_diameter"] / 2
        assert clearance >= 0.2, (error, clearance)
        diagnostics.append({"error_id": error["pcb_error_id"], "exact_clearance_mm": clearance})
    (ROOT / f"build/tscircuit/{side}-{stage}-parity.json").write_text(
        json.dumps({"pads": len(pads), "holes": len(holes), "verified_overlap_diagnostics": diagnostics}, indent=2))
    print(f"{side} {stage}: all 121 pads, 109 holes, outline, and net memberships match")


if __name__ == "__main__":
    check(sys.argv[1], sys.argv[2])
