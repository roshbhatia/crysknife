import json
from pathlib import Path
import subprocess
import sys


root = Path(__file__).resolve().parents[1]
tool = json.loads((root / "tools.lock.json").read_text())["kicad"]
arguments = sys.argv[1:]
program = "kicad-cli"
if arguments[:1] == ["--python"]:
    program = "python3"
    arguments = arguments[1:]
(root / "build").mkdir(exist_ok=True)
subprocess.run([
    "docker", "run", "--rm", "--platform", tool["platform"], "--network", "none",
    "--mount", f"type=bind,source={root},target=/work,readonly",
    "--mount", f"type=bind,source={root / 'build'},target=/work/build",
    "--workdir", "/work", tool["image"], program, *arguments,
], check=True)
