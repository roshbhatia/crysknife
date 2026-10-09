import csv
import json
import math
from pathlib import Path

from kicad_sexp import child, children, parse

ROOT = Path(__file__).resolve().parents[1]
readback = json.loads((ROOT/'manufacturing/jlcpcb/placement-readback.json').read_text())
for side in ('left', 'right'):
    path = ROOT/f'build/manufacturing/quote-only/{side}-quote-cpl.csv'
    with path.open() as stream:
        exported = {p['Designator']: p for p in csv.DictReader(stream)}
    live = {p['reference']: p for p in readback['boards'][side]}
    assert exported.keys() == live.keys() and len(live) == 47
    for ref, actual in live.items():
        expected = exported[ref]
        assert actual['selected'], (side, ref, 'Not selected')
        assert actual['layer'] == {'Top': 'T', 'Bottom': 'B'}[expected['Layer']]
        for key, field in [('x', 'Mid X'), ('y', 'Mid Y'), ('rotation', 'Rotation')]:
            assert abs(actual[key]-float(expected[field])) < 0.0015, (side, ref, field)
    with (ROOT/f'build/manufacturing/quote-only/{side}-quote-bom.csv').open() as stream:
        for group in csv.DictReader(stream):
            for ref in group['Designator'].split(','):
                assert live[ref]['lcsc'] == group['LCSC Part #'], (side, ref)
    board = parse((ROOT/f'build/pcb/crysknife_{side}.kicad_pcb').read_text())
    count = 0
    for fp in children(board, 'footprint'):
        if fp[1] != 'ceoloide:switch_mx':
            continue
        ref = next(p[2] for p in children(fp, 'property') if p[1] == 'Reference')
        pads = [p for p in children(fp, 'pad') if p[2] == 'smd']
        assert len(pads) == 2
        dx = sum(float(child(p, 'at')[1]) for p in pads)/2
        dy = -sum(float(child(p, 'at')[2]) for p in pads)/2
        at = child(fp, 'at')
        angle = math.radians(float(at[3]) if len(at) > 3 else 0)
        x = float(at[1])+dx*math.cos(angle)-dy*math.sin(angle)
        y = -float(at[2])+dx*math.sin(angle)+dy*math.cos(angle)
        assert abs(x-float(exported[ref]['Mid X'])) < 0.000002, (side, ref, 'Pad midpoint X')
        assert abs(y-float(exported[ref]['Mid Y'])) < 0.000002, (side, ref, 'Pad midpoint Y')
        count += 1
    assert count == 21
    print(f'{side}: 47 saved supplier placements match exports; 21 socket origins match native solder-pad midpoints')
