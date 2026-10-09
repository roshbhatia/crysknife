import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Save checked engineering models and supplier review files')
parser.add_argument('--evidence-dir', type=Path, required=True)
parser.add_argument('--run-url', required=True)
parser.add_argument('--revision', required=True)
args = parser.parse_args()
evidence = args.evidence_dir.resolve()
out = ROOT/'out'
kicad = out/'kicad'
jlc = ROOT/'manufacturing/jlcpcb'
scs = ROOT/'manufacturing/sendcutsend'
for directory in (kicad, jlc, scs, out/'3d'):
    directory.mkdir(parents=True, exist_ok=True)
verification = {'pcb_revision':args.revision, 'pcb_ci':args.run_url,
                'status':'digital checks passed; supplier and physical approval pending', 'boards':{}}
for side in ('left', 'right'):
    erc = json.loads((evidence/f'schematic/{side}-erc.json').read_text())
    assert not [v for s in erc['sheets'] for v in s['violations']], (side, 'ERC issues')
    drc = json.loads((evidence/f'pcb/{side}-routed-drc.json').read_text())
    assert not drc['unconnected_items'], (side, 'Unconnected copper')
    assert all(v['severity']=='warning' and v['type']=='lib_footprint_issues' for v in drc['violations']), (side, 'DRC issues')
    board = evidence/f'pcb/fridakeeb_{side}_routed.kicad_pcb'
    verification['boards'][side] = {'erc_issues':0, 'drc_errors':0, 'unconnected':0,
                                  'library_warnings':len(drc['violations']),
                                  'sha256':hashlib.sha256(board.read_bytes()).hexdigest()}
    shutil.copyfile(board, kicad/f'fridakeys_{side}.kicad_pcb')
    for extension in ('kicad_sch', 'kicad_pro'):
        shutil.copyfile(evidence/f'schematic/fridakeys_{side}.{extension}', kicad/f'fridakeys_{side}.{extension}')
    for extension in ('pdf', 'net'):
        shutil.copyfile(evidence/f'schematic/{side}.{extension}', kicad/f'{side}.{extension}')
    quote = evidence/'manufacturing/quote-only'
    for kind in ('bom', 'cpl'):
        shutil.copyfile(quote/f'{side}-quote-{kind}.csv', jlc/f'{side}-{kind}.csv')
    with zipfile.ZipFile(jlc/f'{side}-gerbers.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((quote/f'gerbers/{side}').iterdir()):
            archive.writestr(zipfile.ZipInfo(file.name, (1980,1,1,0,0,0)), file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    for part in ('bottom-bent','plate','damping'):
        shutil.copyfile(ROOT/f'build/case/{side}-{part}.dxf', scs/f'{side}-{part}.dxf')
    for name in ('bends.json','bend-lines.svg'):
        shutil.copyfile(ROOT/f'build/case/{side}-{name}', scs/f'{side}-{name}')
for name in ('fridakeys.kicad_sym','sym-lib-table','fp-lib-table'):
    shutil.copyfile(evidence/f'schematic/{name}', kicad/name)
shutil.copytree(evidence/'schematic/fridakeys.pretty', kicad/'fridakeys.pretty', dirs_exist_ok=True)
readiness = json.loads((evidence/'manufacturing/quote-only/readiness.json').read_text())
readiness['remaining_gates'] = [gate.replace('Complete schematic/ERC and physical prototype', 'Physical prototype') for gate in readiness['remaining_gates']]
readiness['digital_evidence'] = '../../out/validation.json'
(jlc/'readiness.json').write_text(json.dumps(readiness,indent=2)+'\n')
shutil.copyfile(ROOT/'build/case/mechanical-checks.json', scs/'mechanical-checks.json')
for extension in ('dxf','svg'):
    shutil.copyfile(ROOT/f'build/case/switch-fit-coupon.{extension}', scs/f'switch-fit-coupon.{extension}')
for side in ('left','right'):
    for part in ('assembly','bottom'):
        shutil.copyfile(ROOT/f'build/case/{side}-{part}.3mf', out/f'3d/{side}-{part}.3mf')
(out/'validation.json').write_text(json.dumps(verification,indent=2)+'\n')
for vendor in (jlc,scs):
    (vendor/'DO-NOT-ORDER.txt').write_text('SUPPLIER REVIEW ONLY. No accepted quote or physical prototype result.\n')
print('Saved checked KiCad models, 3D case models and separate vendor review files')
