import json
from pathlib import Path
import re

from kicad_sexp import child, children, parse


ROOT = Path(__file__).resolve().parents[1]
FIRMWARE = ROOT / "firmware/boards/shields/fridakeeb"
common = (FIRMWARE / "fridakeeb.dtsi").read_text()
assert 'diode-direction = "col2row"' in common
rows = re.search(r"row-gpios\s*=\s*(.*?);", common, re.S)[1]
assert re.findall(r"&pro_micro (\d+) \(GPIO_ACTIVE_HIGH \| GPIO_PULL_DOWN\)", rows) == ["5", "6", "7", "8"]
transform = {(int(row), int(column)) for row, column in re.findall(r"RC\((\d+),(\d+)\)", common)}
assert len(transform) == 42
gpio_by_pin = {5: 21, 6: 20, 7: 19, 8: 18, 9: 15, 10: 14,
               14: 8, 15: 7, 16: 6, 17: 5, 18: 4, 19: 3, 20: 2}
expected_pins = {"1": "RAW", "2": "GND", "3": "RST", "4": "VCC",
                 "5": "C0", "6": "C1", "7": "C2", "8": "C3", "9": "C4", "10": "C5",
                 "14": "R3", "15": "R2", "16": "R1", "17": "R0", "18": "TP_RST",
                 "19": "TP_CLK", "20": "TP_DATA", "21": "GND", "22": "GND"}
evidence = []
for side in ("left", "right"):
    board = parse((ROOT / f"build/pcb/fridakeeb_{side}.kicad_pcb").read_text())
    footprints = {next(p[2] for p in children(fp, "property") if p[1] == "Reference"): fp
                  for fp in children(board, "footprint")}

    def pads(ref):
        return {pad[1]: child(pad, "net")[2] if child(pad, "net") else None
                for pad in children(footprints[ref], "pad") if pad[1]}

    assert not children(footprints["MCU1"], "pad")
    assert len(pads("MCU1A")) == len(pads("MCU1B")) == 12
    assert set(pads("MCU1A")).isdisjoint(pads("MCU1B"))
    controller = {**pads("MCU1A"), **pads("MCU1B")}
    for ref in ("MCU1A", "MCU1B"):
        assert footprints[ref][1] == "fridakeys:MillMax_315_1x12"
        assert all(child(pad, "drill")[1] == "1" for pad in children(footprints[ref], "pad"))
    assert all(controller[pin] == net for pin, net in expected_pins.items()), (side, controller)
    gpio_nets = {gpio: controller[str(pin)] for pin, gpio in gpio_by_pin.items()}
    overlay = (FIRMWARE / f"fridakeeb_{side}.overlay").read_text()
    columns = list(map(int, re.findall(r"&pro_micro (\d+) GPIO_ACTIVE_HIGH",
                       re.search(r"col-gpios\s*=\s*(.*?);", overlay, re.S)[1])))
    assert len(columns) == 6
    column_index = {gpio_nets[gpio]: i for i, gpio in enumerate(columns)}
    offset = 6 if side == "right" else 0
    if offset:
        assert "col-offset = <6>" in overlay
    diode_rows = {}
    for ref in footprints:
        if re.fullmatch(r"D\d+", ref):
            diode = pads(ref)
            assert diode["1"].startswith("R") and diode["2"].endswith("_SW")
            assert diode["2"] not in diode_rows
            diode_rows[diode["2"]] = int(diode["1"][1:])
    key_coordinates = []
    for ref in footprints:
        if re.fullmatch(r"S\d+", ref):
            switch = pads(ref)
            row = diode_rows[switch["2"]]
            column = column_index[switch["1"]] + offset
            assert (row, column) in transform, (side, ref, row, column)
            key_coordinates.append((row, column))
    assert len(key_coordinates) == len(set(key_coordinates)) == 21
    assert pads("JST1") == {"1": "GND", "2": "BAT_P"}
    assert pads("PWR1") == {"1": "BAT_P", "2": "RAW", "3": None}
    assert pads("RST1") == {"1": "GND", "2": "RST", "3": "GND", "4": "RST"}
    if side == "right":
        for name, gpio in [("scl", 3), ("sda", 2), ("rst", 4)]:
            assert re.search(rf"{name}-gpios\s*=\s*<&pro_micro {gpio} GPIO_ACTIVE_HIGH>", overlay)
        assert gpio_nets[2] == "TP_DATA" and gpio_nets[3] == "TP_CLK" and gpio_nets[4] == "TP_RST"
        assert pads("TP1") == {"1": "TP_DATA", "2": "TP_RST", "3": None, "4": None,
                               "5": None, "6": "TP_CLK", "7": "GND", "8": "VCC"}
        ribbon_pads = children(footprints["TP1"], "pad")
        assert len(ribbon_pads) == 10
        for pad in ribbon_pads:
            assert child(pad, "layers")[1:] == ["F.Cu", "F.Paste", "F.Mask"]
            size = list(map(float, child(pad, "size")[1:]))
            position = list(map(float, child(pad, "at")[1:3]))
            if pad[1]:
                assert size == [0.6, 1.3] and position == [int(pad[1])-4.5, 0]
            else:
                assert size == [1.8, 2.2] and position in [[-5.9, 3.25], [5.9, 3.25]]
        for ref, value, mapping in [
            ("R1", "4.7k", {"1": "VCC", "2": "TP_DATA"}),
            ("R2", "4.7k", {"1": "VCC", "2": "TP_CLK"}),
            ("R3", "10k", {"1": "TP_RST", "2": "GND"}),
            ("C1", "100nF", {"1": "TP_RST", "2": "GND"}),
            ("C2", "100nF", {"1": "VCC", "2": "GND"}),
        ]:
            assert pads(ref) == mapping, (ref, pads(ref))
            assert next(p[2] for p in children(footprints[ref], "property") if p[1] == "Value") == value
    evidence.append({"side": side, "unique_matrix_positions": len(key_coordinates),
                     "controller_pin_mapping": "matches nice!nano v2 face-up pinout",
                     "diode_direction": "col2row; diode cathode pad 1 to row",
                     "power_path": "JST pin 2 BAT_P through PWR1 to nice!nano RAW; JST pin 1 GND",
                     "reset": "momentary RST to GND", "matrix_positions": sorted(key_coordinates),
                     "trackpoint": "8-pin FFC, 4.7k clock/data pull-ups, 10k/100nF reset and 100nF decoupling" if side == "right" else "not fitted"})
all_positions = {tuple(p) for item in evidence for p in item["matrix_positions"]}
assert all_positions == transform
keymap = (ROOT / "firmware/config/fridakeeb.keymap").read_text()
for bindings in re.findall(r"bindings\s*=\s*<(.*?)>;", keymap, re.S):
    assert len(re.findall(r"&\w+", bindings)) == 42, "Keymap layer does not cover all 42 switches"
output = ROOT / "build/pcb/electrical-checks.json"
output.write_text(json.dumps(evidence, indent=2)+"\n")
print("Electrical source audit: all 42 matrix positions, diode direction, power, reset and firmware GPIOs match")
print("Not hardware proof: TrackPoint cable/mount, controller contact fit, battery polarity and assembly remain unverified")
