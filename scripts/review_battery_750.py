from pathlib import Path
import json
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REV = '5b51501fead672c41b5cfb396f3dafe0894bf4e9'
PARAM = {name: float(value) for name, value in re.findall(
    r'(\w+)\s*=\s*([0-9.]+);', (ROOT / 'case/parameters.scad').read_text())}
BATTERY = json.loads((ROOT / 'manufacturing/battery.json').read_text())


def runtime(capacity, central, asleep):
    current = capacity * 1000 * .05 / (30 * 24) + 18
    awake = (490 + 23 + 380 * .02) if central else (20 + 365 * .02)
    current += awake * (1 - asleep)
    average = capacity * .85 * 1000 / current / 24
    worst = capacity * .80 * 1000 / (current * 1.20) / 24
    return {'current_uA': round(current, 4), 'average_days': round(average, 2),
            'profiler_range_days': [round(worst, 2), round(2 * average - worst, 2)]}


under = PARAM['standoff_height'] + PARAM['standoff_shim']
reservation = BATTERY['case_reservation_mm'][2]
nominal = BATTERY['nominal_dimensions_mm'][2]
extra = reservation - nominal
candidate_reservation = 4 + extra
candidate_under = under - (nominal - 4)
fixed = 4.4 + .5 + .5 + PARAM['damping_thickness']
margin = candidate_under - fixed - candidate_reservation
controller_floor = candidate_under - PARAM['controller_gap'] - PARAM['controller_board_thickness'] - PARAM['damping_thickness']
assert round(margin, 4) == round(under - fixed - reservation, 4)
assert controller_floor >= 1
profiles = []
for name, floor, clearance, cell in [
    ('Current 2000 / 3.175 mm floor', PARAM['bottom_thickness'], under, nominal),
    ('Conditional 750 / 3.175 mm floor', PARAM['bottom_thickness'], candidate_under, 4),
    ('Conditional 750 / thin E floor', PARAM['plate_thickness'], candidate_under, 4),
]:
    plate = 2.5 + floor + clearance + PARAM['pcb_thickness'] + PARAM['plate_to_pcb_gap'] + PARAM['plate_thickness']
    profiles.append({'name': name, 'floor_mm': floor, 'under_pcb_mm': clearance,
                     'nominal_cell_mm': cell, 'desk_to_plate_mm': round(plate, 4)})
report = {
    'status': 'candidate only; adoption blocked by missing supplied-pack specifications',
    'selected_battery': BATTERY['sku'], 'candidate': 'Typeractive Liter 403450 750 mAh',
    'nominal_dimensions_mm': [50, 34, 4], 'connector': '2-pin JST-PH 2.0 mm',
    'carrier_polarity': {'1': 'GND', '2': 'BAT_P'},
    'polarity_evidence': 'Product photo suggests matching wiring; supplied plug requires meter confirmation',
    'protection_evidence': 'Liter 403450 listing specifies protection; Typeractive photo shows a circuit board. Exact supplied assembly is not documented.',
    'missing': ['Supplied-pack standard/maximum charge current and temperature limits',
                'Protected-pack maximum dimensions, cable length and bend allowance',
                'Supplied-pack polarity and protection cutoffs'],
    'charging': {'current_mA': BATTERY['charge_current_mA'], 'BOOST': 'OPEN'},
    'conditional_stack': {'battery_reservation_mm': candidate_reservation,
        'battery_xy_reservation_mm': BATTERY['case_reservation_mm'][:2],
        'under_pcb_mm': candidate_under, 'reserved_stack_margin_mm': round(margin, 4),
        'controller_to_floor_pad_mm': round(controller_floor, 4),
        'height_reduction_mm': under - candidate_under,
        'manufacturing_geometry_changed': False, 'physical_tested': False},
    'profiles': profiles,
    'runtime_assumptions': {'zmk_revision': REV, 'nice_nano': 2, 'host_profiles': 1,
        'typing_fraction_awake': .02, 'lights_and_display': False,
        'board_quiescent_uA': 18, 'self_discharge_percent_per_30_days': 5,
        'effective_capacity_fraction': .85, 'worst_capacity_fraction': .80,
        'worst_current_multiplier': 1.20, 'range': 'average +/- (average - worst); not a statistical confidence interval',
        'sleep_model': '8 hours awake and 16 hours actually asleep; excludes entry delay and wake bursts',
        'measured_on_crysknife': False},
    'runtime': {str(cap): {role: {mode: runtime(cap, role == 'right_central', asleep)
        for mode, asleep in [('no_sleep', 0), ('8h_awake_16h_sleep', 2/3)]}
        for role in ['right_central', 'left_peripheral']} for cap in [750, 2000]},
    'sources': ['https://typeractive.xyz/products/lithium-battery-750mah',
        'https://bihuade.com/products/37v-403450-750mah-liter-energy-battery-rechargeable-battery-for-smart-phone-dvd-mp3-mp4-led-lamp-camera',
        'https://www.jst-mfg.com/product/pdf/eng/ePH.pdf',
        'https://nicekeyboards.com/docs/nice-nano/getting-started/',
        f'https://github.com/zmkfirmware/zmk/blob/{REV}/docs/src/data/power.js',
        f'https://github.com/zmkfirmware/zmk/blob/{REV}/docs/src/components/power-estimate.js']}
(ROOT / 'manufacturing/battery-750-review.json').write_text(json.dumps(report, indent=2) + '\n')
image = Image.new('RGB', (1500, 1450), '#f6f5f1')
draw = ImageDraw.Draw(image)
font = lambda size: ImageFont.truetype(str(ROOT / 'assets/ioskeley-mono-bold.ttf'), size)
draw.text((30, 20), '750 mAh candidate | conditional sections | common scale', font=font(25), fill='#24333c')
draw.text((30, 65), 'Not adopted. Current CAD and battery remain unchanged. No keycaps shown.', font=font(19), fill='#624a23')
scale = 12
for index, p in enumerate(profiles):
    desk = 460 + index * 420
    x = 50
    y = lambda z: desk - z * scale
    floor = p['floor_mm']
    pcb = 2.5 + floor + p['under_pcb_mm']
    plate = pcb + PARAM['pcb_thickness'] + PARAM['plate_to_pcb_gap']
    def rect(x1, x2, z, thickness, color):
        draw.rectangle((x + x1, y(z + thickness), x + x2, y(z)), fill=color)
    draw.line((35, desk, 700, desk), fill='#24333c', width=2)
    rect(30, 110, 0, 2.5, '#424d52')
    rect(460, 540, 0, 2.5, '#424d52')
    rect(0, 590, 2.5, floor, '#9a9d9c')
    rect(0, 590, 2.5 + floor, PARAM['damping_thickness'], '#59636b')
    rect(70, 350, 2.5 + floor + PARAM['damping_thickness'] + .5, p['nominal_cell_mm'], '#bf914b')
    rect(430, 540, pcb - PARAM['controller_gap'] - PARAM['controller_board_thickness'], PARAM['controller_board_thickness'], '#426d91')
    rect(0, 590, pcb, PARAM['pcb_thickness'], '#99b79a')
    rect(0, 590, plate, PARAM['plate_thickness'], '#b0d2dc')
    draw.text((750, desk - 190), p['name'], font=font(22), fill='#24333c')
    draw.text((750, desk - 145), f"Plate: {p['desk_to_plate_mm']:.4f} mm above desk", font=font(21), fill='#24333c')
    draw.text((750, desk - 100), f"Under PCB: {p['under_pcb_mm']:.1f} mm", font=font(20), fill='#24333c')
    draw.text((750, desk - 65), 'Reference feet: 2.5 mm installed', font=font(17), fill='#59636b')
draw.text((30, 1415), 'Schematic sections, not CAD. Gold: nominal cell. Blue: controller. Pale blue: plate.', font=font(18), fill='#24333c')
image.save(ROOT / 'previews/enclosures/heights/battery-750-conditional.png')
print(json.dumps({'stack': report['conditional_stack'], 'runtime_750': report['runtime']['750']}, indent=2))
