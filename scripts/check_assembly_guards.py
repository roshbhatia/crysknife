import copy
import json
from pathlib import Path

from generate_assembly import inventory
from kicad_sexp import child, children, parse


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'manufacturing/parts.json').read_text())
original = parse((root/'build/pcb/crysknife_right.kicad_pcb').read_text())
inventory(original, 'right', manifest)
for case in ('missing socket', 'unmapped part', 'wrong face', 'wrong footprint'):
    board = copy.deepcopy(original)
    socket = next(fp for fp in children(board, 'footprint') if any(
        p[1:3] == ['Reference', 'S1'] for p in children(fp, 'property')))
    if case == 'missing socket':
        board.remove(socket)
    elif case == 'unmapped part':
        next(p for p in children(socket, 'property') if p[1] == 'Reference')[2] = 'UNKNOWN1'
    elif case == 'wrong face':
        child(socket, 'layer')[1] = 'F.Cu'
    else:
        socket[1] = 'wrong:Choc_socket'
    try:
        inventory(board, 'right', manifest)
    except AssertionError:
        print(f'Rejected unsafe assembly export: {case}')
    else:
        raise AssertionError(f'Accepted unsafe assembly export: {case}')
