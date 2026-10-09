import json
import re
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from kicad_sexp import child, children, parse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/schematic'
OUT.mkdir(parents=True, exist_ok=True)
NAMES = ['outer', 'pinky', 'ring', 'middle', 'index', 'inner']
CONTROLLER = {'1': 'RAW', '2': 'GND', '3': 'RST', '4': 'VCC',
              **{str(n+5): f'C{n}' for n in range(6)},
              '11': None, '12': None, '13': None, '14': 'R3', '15': 'R2',
              '16': 'R1', '17': 'R0', **{str(n): None for n in (18, 19, 20, 23, 24)},
              '21': 'GND', '22': 'GND'}


def uid(value):
    return str(uuid5(NAMESPACE_URL, 'https://github.com/roshbhatia/crysknife/schematic/'+value))


def property_text(name, value, x, y, hide=False):
    return f'(property "{name}" "{value}" (at {x} {y} 0) (effects (font (size 1 1))'+(' (hide yes)' if hide else '')+'))'


for side in ('left', 'right'):
    sheet = uid(side)
    symbols, placed, wires, labels, connections, texts = [], [], [], [], {}, []

    def component(ref, value, pins, x, y, footprint='', module=False, flag=False):
        x, y = (round(v / 1.27) * 1.27 for v in (x, y))
        footprint = 'crysknife:'+ref if footprint else ''
        name = ref.replace('#', '')
        identifier = 'crysknife:'+name
        height = max(2.54, (len(pins)+1)*2.54)
        geometry = f'(rectangle (start -3.81 {height/2}) (end 3.81 {-height/2}) (stroke (width 0.254) (type default)) (fill (type background)))'
        if flag:
            geometry = '(polyline (pts (xy 0 0) (xy 0 2.54) (xy -1.27 1.27) (xy 0 0) (xy 1.27 1.27) (xy 0 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))'
        pin_text, positions = [], []
        for index, (number, net) in enumerate(pins.items()):
            py = ((len(pins)-1)/2-index)*2.54
            px = -6.35
            kind = 'passive'
            label = number
            if module:
                label = {'1':'RAW/BAT+', '2':'GND', '3':'RST', '4':'3V3_OUT', '21':'GND', '22':'GND'}.get(number, net or 'unused GPIO')
                kind = 'power_in' if number in ('1','2','21','22') else 'input' if number == '3' else 'power_out' if number == '4' else 'output' if net and net.startswith('C') else 'bidirectional'
            if flag:
                kind, px, py = 'power_out', 0, 0
            pin_text.append(f'(pin {kind} line (at {px} {py} 0) (length {0 if flag else 2.54}) (name "{label}" (effects (font (size 0.8 0.8)))) (number "{number}" (effects (font (size 0.8 0.8)))))')
            positions.append((number, net, x+px, y-py))
        lib = f'(symbol "{identifier}" (pin_names (offset 0.5)) (in_bom yes) (on_board yes) {property_text("Reference", ref, 0, height/2+1.27)} {property_text("Value", value, 0, -height/2-1.27)} (symbol "{name}_0_1" {geometry}) (symbol "{name}_1_1" {" ".join(pin_text)}))'
        symbols.append(lib)
        props = ' '.join([property_text('Reference', ref, x, y-height/2-1.27), property_text('Value', value, x, y+height/2+1.27), property_text('Footprint', footprint, x, y, True)])
        pin_ids = ' '.join(f'(pin "{n}" (uuid {uid(side+ref+n)}))' for n in pins)
        placed.append(f'(symbol (lib_id "{identifier}") (at {x} {y} 0) (unit 1) (in_bom {"no" if module or flag else "yes"}) (on_board {"no" if module or flag else "yes"}) (dnp no) (uuid {uid(side+ref)}) {props} {pin_ids} (instances (project "crysknife_{side}" (path "/{sheet}" (reference "{ref}") (unit 1)))))')
        for number, net, px, py in positions:
            if net is None:
                wires.append(f'(no_connect (at {px} {py}) (uuid {uid(side+ref+number+"nc")}))')
            else:
                lx = px-2.54
                wires.append(f'(wire (pts (xy {px} {py}) (xy {lx} {py})) (stroke (width 0) (type default)) (uuid {uid(side+ref+number+"wire")}))')
                labels.append(f'(label "{net}" (at {lx} {py} 0) (effects (font (size 0.8 0.8)) (justify left bottom)) (uuid {uid(side+ref+number+"label")}))')
                if not module and not flag:
                    connections[(ref, number)] = net
        if not module and not flag:
            for n, net in pins.items():
                if net is None:
                    connections[(ref, n)] = None

    for column, name in enumerate(NAMES):
        for row, position in enumerate(('bottom', 'home', 'top')):
            n = column*3+row+1
            net = ('mirror_' if side == 'right' else '')+name+'_'+position+'_SW'
            x, y = 35+column*45, 40+(2-row)*45
            component(f'S{n}', 'MX hotswap', {'1': f'C{column}', '2': net}, x, y, 'ceoloide:switch_mx')
            component(f'D{n}', '1N4148W (1=K, 2=A)', {'1': f'R{2-row}', '2': net}, x, y+17.78, 'ceoloide:diode_tht_sod123')
    for n, name in enumerate(('near', 'mid', 'far'), 19):
        net = ('mirror_' if side == 'right' else '')+name+'_home_SW'
        x = 170+(n-19)*45
        component(f'S{n}', 'MX hotswap', {'1': f'C{n-16}', '2': net}, x, 175, 'ceoloide:switch_mx')
        component(f'D{n}', '1N4148W (1=K, 2=A)', {'1':'R3', '2': net}, x, 192.78, 'ceoloide:diode_tht_sod123')
    component('MCU1A', '315-43-112-41-003000', {str(n):CONTROLLER[str(n)] for n in range(24,12,-1)}, 345, 55, 'crysknife:MillMax_315_1x12')
    component('MCU1B', '315-43-112-41-003000', {str(n):CONTROLLER[str(n)] for n in range(1,13)}, 390, 55, 'crysknife:MillMax_315_1x12')
    component('U1', 'nice!nano V2 external module', CONTROLLER, 345, 160, module=True)
    component('PWR1', 'SSSS811101', {'1':'BAT_P', '2':'RAW', '3':None}, 45, 235, 'ceoloide:power_switch_smd_side')
    component('RST1', 'EVQPUC02K', {'1':'GND', '2':'RST', '3':'GND', '4':'RST'}, 100, 235, 'ceoloide:reset_switch_smd_side')
    component('JST1', 'PH2: 1=GND, 2=BAT+', {'1':'GND', '2':'BAT_P'}, 170, 235, 'ceoloide:battery_connector_jst_ph_2')
    for i, net in enumerate(('RAW','GND')):
        component(f'#FLG0{i+1}', 'external supply', {'1':net}, 230+i*40, 240, flag=True)
    text = 'External module provides USB charging; PWR must be ON to charge. Carrier has no charger.\nUnused GPIO and power-switch throw have explicit no-connects. Diode pad 1 is cathode.\nSwitch pin 1 -> column; pin 2 -> diode anode; cathode -> row. Right half is ZMK central.'
    texts.append(f'(text {json.dumps(text)} (at 25 265 0) (effects (font (size 1 1)) (justify left)) (uuid {uid(side+"notes")}))')
    body = f'(kicad_sch (version 20250114) (generator "crysknife") (uuid {sheet}) (paper "A3") (title_block (title "crysknife {side}") (rev "1.0.0") (company "by @roshbhatia")) (lib_symbols {" ".join(symbols)}) {" ".join(wires+labels+placed+texts)} (sheet_instances (path "/" (page "1"))))\n'
    (OUT/f'crysknife_{side}.kicad_sch').write_text(body)
    (OUT/f'crysknife_{side}.kicad_pro').write_text(json.dumps({'meta': {'version': 1}})+'\n')
    libdir = OUT
    (libdir/'crysknife.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "crysknife") '+' '.join(s.replace('"crysknife:', '"') for s in symbols)+')\n')
    board = parse((ROOT/f'build/pcb/crysknife_{side}.kicad_pcb').read_text())
    pretty = OUT/'crysknife.pretty'
    pretty.mkdir(exist_ok=True)
    source = (ROOT/f'build/pcb/crysknife_{side}.kicad_pcb').read_text()
    tokens = list(re.finditer(r'\"(?:\\.|[^\"\\])*\"|[()]|[^\s()]+', source))
    for i, token in enumerate(tokens):
        if token.group() != 'footprint' or tokens[i-1].group() != '(':
            continue
        depth, end = 1, None
        for following in tokens[i+1:]:
            depth += (following.group() == '(') - (following.group() == ')')
            if depth == 0:
                end = following.end()
                break
        text = source[tokens[i-1].start():end]
        fp = parse(text)
        ref = next(p[2] for p in children(fp, 'property') if p[1] == 'Reference')
        if not children(fp, 'pad'):
            continue
        text = re.sub(r'^\(footprint\s+\"[^\"]*\"', '(footprint '+json.dumps(ref), text, count=1)
        (pretty/f'{ref}.kicad_mod').write_text(text+'\n')
    observed = {}
    for fp in children(board,'footprint'):
        ref = next(p[2] for p in children(fp,'property') if p[1]=='Reference')
        for pad in children(fp,'pad'):
            if not pad[1]:
                continue
            net = child(pad,'net')
            observed[(ref,pad[1])] = net[2] if net else None
    assert set(observed) == set(connections), (side, set(observed)^set(connections))
    for pin, net in connections.items():
        if net is None and pin[0].startswith('MCU'):
            assert observed[pin].startswith('P'), (pin, observed[pin])
        else:
            assert observed[pin] == net, (side, pin, observed[pin], net)
    (OUT/f'{side}-expected-nets.json').write_text(json.dumps({f'{ref}.{pin}':net for (ref,pin),net in connections.items()},indent=2)+'\n')
    print(f'{side}: independent schematic design matches {len(connections)} carrier pins; typed controller and explicit unused pins')

(OUT/"sym-lib-table").write_text('(sym_lib_table (version 7) (lib (name "crysknife") (type "KiCad") (uri "${KIPRJMOD}/crysknife.kicad_sym") (options "") (descr "Local carrier symbols and typed external module")))\n')

(OUT/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name \"crysknife\") (type \"KiCad\") (uri \"${KIPRJMOD}/crysknife.pretty\") (options \"\") (descr \"Generated carrier footprints\")))\n')
