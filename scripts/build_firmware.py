import argparse
from pathlib import Path
import shutil
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("shield", choices=["fridakeeb_left", "fridakeeb_right", "settings_reset"])
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
workspace = root / "build/firmware/workspace"
workspace.mkdir(parents=True, exist_ok=True)
config = workspace / "config"
shutil.copytree(root / "firmware/config", config, dirs_exist_ok=True)


def run(*command):
    subprocess.run(command, cwd=workspace, check=True)


if not (workspace / ".west").exists():
    run("west", "init", "-l", str(config))
run("west", "update", "--fetch-opt=--filter=tree:0")
run("west", "zephyr-export")
output = root / "build/firmware" / args.shield
run("west", "build", "-p", "always", "-s", str(workspace / "zmk/app"),
    "-d", str(output), "-b", "nice_nano@2.0.0/nrf52840/zmk", "--",
    f"-DZMK_CONFIG={config}", f"-DSHIELD={args.shield}",
    f"-DZMK_EXTRA_MODULES={root / 'firmware'}")
artifacts = root / "build/firmware/artifacts" / args.shield
artifacts.mkdir(parents=True, exist_ok=True)
for name in ["zmk.uf2", "zephyr.dts", ".config"]:
    shutil.copy2(output / "zephyr" / name, artifacts / name)
with (artifacts / "west-frozen.yml").open("w") as manifest:
    subprocess.run(["west", "manifest", "--freeze"], cwd=workspace, stdout=manifest, check=True)
