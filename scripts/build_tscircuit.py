from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tscircuit/node_modules/.bin/tsci"


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def export(side, stage, kind="circuit-json", extension="circuit.json"):
    run(str(CLI), "export", f"tscircuit/generated/{side}-{stage}.circuit.tsx",
        "-f", kind, "--disable-parts-engine", "-o",
        str(ROOT / f"build/tscircuit/{side}-{stage}.{extension}"))


run(sys.executable, "scripts/generate_tscircuit.py")
for side in ("left", "right"):
    export(side, "placement")
    run(sys.executable, "scripts/check_tscircuit.py", side, "placement")
    export(side, "routed")
    run("node", "tscircuit/check_routing.mjs", f"build/tscircuit/{side}-routed.circuit.json",
        f"build/tscircuit/{side}-routing-checks.json")
    run(sys.executable, "scripts/check_tscircuit.py", side, "routed")
    run(str(CLI), "export", f"build/tscircuit/{side}-routed.circuit.json", "-f", "pcb-svg",
        "-o", str(ROOT / f"build/tscircuit/{side}-routed.svg"))
