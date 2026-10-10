import csv
import json
import math
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
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)


def supplier_placement(part, corrections):
    rule = corrections['parts'][part['lcsc']]
    assert part['footprint'] == rule['footprint'], part['reference']
    assert part['layer'] == rule['layer'], part['reference']
    angle = part['rotation_deg']
    radians = math.radians(angle)
    dx, dy = rule['local_offset_mm']
    return {**part,
            'x_mm': part['x_mm'] + dx*math.cos(radians) - dy*math.sin(radians),
            'y_mm': part['y_mm'] + dx*math.sin(radians) + dy*math.cos(radians),
            'rotation_deg': (rule['angle_sign']*angle + rule['angle_offset_deg']) % 360}


def main():
    manifest = json.loads((ROOT/'manufacturing/parts.json').read_text())
    corrections = json.loads((ROOT/'manufacturing/jlcpcb/placement-corrections.json').read_text())
    output = ROOT/'build/manufacturing/assembly'
    output.mkdir(parents=True, exist_ok=True)
    for side in ('left', 'right'):
        source = ROOT/f'build/pcb/crysknife_{side}.kicad_pcb'
        parts, _ = inventory(parse(source.read_text()), side, manifest)
        placements = [supplier_placement(p, corrections) for p in parts]
        groups = {}
        for p in parts:
            groups.setdefault(p['lcsc'], []).append(p)
        write_csv(output/f'{side}-bom.csv', ['Comment', 'Designator', 'Footprint', 'LCSC Part #'],
                  [[p[0]['mpn'], ','.join(i['reference'] for i in p), p[0]['footprint'], code]
                   for code, p in sorted(groups.items())])
        write_csv(output/f'{side}-cpl.csv', ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'],
                  [[p['reference'], f"{p['x_mm']:.6f}", f"{p['y_mm']:.6f}", p['layer'],
                    f"{p['rotation_deg']:.6f}"] for p in placements])
        write_csv(output/f'{side}-part-evidence.csv', ['Designator', 'Manufacturer', 'MPN', 'LCSC Part #', 'Source'],
                  [[p['reference'], p['manufacturer'], p['mpn'], p['lcsc'], p['source']] for p in parts])
        print(f'{side}: BOM/CPL covers {len(parts)} factory parts')


if __name__ == '__main__':
    main()
