import csv
import json
from pathlib import Path
import re

from kicad_sexp import child, children, parse


ROOT = Path(__file__).resolve().parents[1]


def inventory(board, side, manifest):
    items = []
    excluded = {}
    seen = set()
    for fp in children(board, 'footprint'):
        ref = next(p[2] for p in children(fp, 'property') if p[1] == 'Reference')
        assert ref not in seen, ('Duplicate reference', ref)
        seen.add(ref)
        if ref in manifest['excluded_references']:
            excluded[ref] = manifest['excluded_references'][ref]
            continue
        matches = [p for p in manifest['parts'] if re.fullmatch(p['reference_pattern'], ref)]
        assert len(matches) == 1, ('Unmapped or ambiguous assembly part', ref)
        part = matches[0]
        assert fp[1] == part['footprint'], (ref, fp[1], part['footprint'])
        assert child(fp, 'layer')[1] == part['side']+'.Cu', ('Wrong assembly face', ref)
        assert children(fp, 'pad'), ('Assembly part without pads', ref)
        at = child(fp, 'at')
        items.append({**part, 'reference': ref, 'x_mm': float(at[1]), 'y_mm': -float(at[2]),
                      'rotation_deg': float(at[3]) % 360 if len(at) > 3 else 0,
                      'layer': 'Top' if part['side'] == 'F' else 'Bottom'})
    assert set(excluded) == set(manifest['excluded_references']), excluded
    assert len(items) == 47, (side, len(items))
    assert {'MCU1A', 'MCU1B'} <= {p['reference'] for p in items}
    for prefix in ('S', 'D'):
        assert {p['reference'] for p in items if re.fullmatch(prefix+r'\d+', p['reference'])} == {
            f'{prefix}{n}' for n in range(1, 22)}
    return items, excluded


def write_csv(path, header, rows):
    with path.open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    manifest = json.loads((ROOT/'manufacturing/parts.json').read_text())
    output = ROOT/'build/manufacturing/quote-only'
    output.mkdir(parents=True, exist_ok=True)
    report = {'status': 'NOT ORDER READY', 'catalog_checked': manifest['catalog_checked'],
              'coordinate_system': 'KiCad footprint origin; millimeters; X right, Y up; PCB origin 0,0',
              'placement_validation': 'Pickup offsets, polarity and factory rotations require assembler review',
              'remaining_gates': manifest['remaining_gates'], 'boards': []}
    for side in ('left', 'right'):
        source = ROOT/f'build/pcb/crysknife_{side}.kicad_pcb'
        parts, excluded = inventory(parse(source.read_text()), side, manifest)
        groups = {}
        for p in parts:
            groups.setdefault(p['lcsc'], []).append(p)
        write_csv(output/f'{side}-quote-bom.csv', ['Comment', 'Designator', 'Footprint', 'LCSC Part #'],
                  [[p[0]['mpn'], ','.join(i['reference'] for i in p), p[0]['footprint'], code]
                   for code, p in sorted(groups.items())])
        write_csv(output/f'{side}-quote-cpl.csv', ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'],
                  [[p['reference'], f"{p['x_mm']:.6f}", f"{p['y_mm']:.6f}", p['layer'],
                    f"{p['rotation_deg']:.6f}"] for p in parts])
        write_csv(output/f'{side}-part-evidence.csv', ['Designator', 'Manufacturer', 'MPN', 'LCSC Part #', 'Source'],
                  [[p['reference'], p['manufacturer'], p['mpn'], p['lcsc'], p['source']] for p in parts])
        report['boards'].append({'side': side, 'factory_parts': len(parts),
                                 'factory_sockets': 21, 'factory_diodes': 21,
                                 'factory_controller_sockets': 2,
                                 'excluded': excluded, 'through_hole_battery_connector': 'JST1'})
        print(f'{side}: quote BOM/CPL covers {len(parts)} factory parts; controller stays an explicit supply gate')
    (output/'readiness.json').write_text(json.dumps(report, indent=2)+'\n')
    (output/'DO-NOT-ORDER.txt').write_text('QUOTE DRAFT ONLY. Read readiness.json. No manufacturing release or accepted assembly quote.\n')


if __name__ == '__main__':
    main()
