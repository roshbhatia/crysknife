import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/schematic'
for side in ('left', 'right'):
    report = json.loads((OUT/f'{side}-erc.json').read_text())
    issues = [issue for sheet in report['sheets'] for issue in sheet['violations']]
    assert not issues, (side, issues)
    expected = json.loads((OUT/f'{side}-expected-nets.json').read_text())
    exported = ET.parse(OUT/f'{side}.net').getroot()
    observed = {}
    for net in exported.find('nets'):
        name = net.attrib['name'].lstrip('/')
        for node in net.findall('node'):
            pin = node.attrib['ref']+'.'+node.attrib['pin']
            if pin not in expected:
                assert node.attrib['ref'] == 'U1' or node.attrib['ref'].startswith('#FLG'), pin
                continue
            assert pin not in observed, ('Pin on multiple nets', pin)
            observed[pin] = None if name.startswith('unconnected-') else name
    for pin, net in expected.items():
        assert observed.get(pin) == net, (side, pin, observed.get(pin), net)
    assert set(observed) <= set(expected)
    print(f'{side}: zero ERC issues; exported schematic connectivity matches all {len(expected)} carrier pins')
