from pathlib import Path
import subprocess
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews'
OUT.mkdir(exist_ok=True)
subprocess.run(['node', 'tscircuit/render_appearance.mjs'], cwd=ROOT, check=True)
for side in ('left', 'right'):
    for face in ('', '-bottom'):
        source = ROOT / f'build/tscircuit/{side}{face}-appearance.svg'
        subprocess.run(['rsvg-convert', str(source), '-o', str(OUT/f'{side}{face}.png')], check=True)
print('Updated four PCB previews from the current routed circuit JSON')

render_env = os.environ.copy()
if sys.platform.startswith('linux'):
    render_env['QT_QPA_PLATFORM'] = 'offscreen'
for side in ('left', 'right'):
    subprocess.run(['openscad', '-o', str(OUT/f'case-{side}.png'), '--render',
                    '--imgsize=1200,900', '--viewall', '--autocenter', '--colorscheme=Tomorrow',
                    '-D', f'side="{side}"', str(ROOT/'case/sandwich.scad')], check=True, env=render_env)
print('Updated both case assembly previews from the committed OpenSCAD model')
