# Prototype acceptance

Scope includes the assembled keyboard, protected batteries, controller headers, switches, and sandwich case.
No physical test has been performed. Only the user's Outemu switches are currently available.
Record measurements in `prototype-results.json`; an empty result does not pass.

## Before power

1. Identify each PCB, nice!nano revision, battery SKU, firmware commit, and assembly quote.
2. Inspect all factory joints, MX socket orientation, diode cathode marks, and soldered header alignment.
3. Measure all 24 controller contacts against the schematic. Verify RAW, GND, RST, and VCC without relying on orientation alone.
4. Verify no hard short between BAT_P/GND or RAW/GND. Record resistance and meter mode.
5. Confirm battery plug red wire reaches JST1 pin 2 and black wire reaches pin 1.
6. Measure each actual battery, controller gap, pin protrusion, and USB height.
7. Fit headers without forcing or leaving any contact partly seated. Repeat insertion/removal ten times, then repeat continuity checks.
8. Fit 21 switches per half. Verify retention, complete travel, keycap clearance, and socket support during insertion.
9. Fit the battery with removable foam retention and an insulating cover. Verify no cell pressure, pin contact, trapped lead, or rattle.
10. Compress the gaskets through their full permitted travel. Maintain clearance above the battery and below the switch pins.

## Electrical and firmware

1. Start from a current-limited bench supply instead of the battery. Set 3.7 V and 100 mA limit; record boot current and RAW/VCC voltages.
2. Flash the exact left/right UF2 files. Check USB recovery and physical reset, including double-tap bootloader entry.
3. Press every key 100 times. Accept zero missed events, repeated events, or wrong coordinates across all 42 keys.
4. Check simultaneous keys across shared rows and columns, modifiers, layers, and six-key combinations. Accept zero phantom keys.
5. Pair both halves and the host. Test all Bluetooth profiles, split reconnect, host reconnect, and wake after sleep.
6. Repeat wireless tests at 1 m and 3 m with the complete case and batteries fitted. Record disconnects and visible input latency.
7. Confirm the right central half works through USB while its peripheral remains wireless.
8. Confirm power and reset can be operated from the side without removing plates.

## Charging and battery life

1. Confirm both nice!nano BOOST bridges are configured for approximately 500 mA charging; do not infer this from LED activity.
2. Measure charging current, battery voltage, and temperature on each half at low, middle, and near-full charge.
3. Charge only within the battery's documented temperature range. Stop on overheating, cell damage, swelling, or unexpected current.
4. Verify charge termination and battery voltage at completion against the supplied cell specification.
5. Confirm battery charging requires PWR ON. With PWR OFF and USB absent, measure battery leakage.
6. Measure both halves separately during active typing, idle, sleep, reconnect, and USB charging.
7. Log a representative 24-hour usage cycle. Compute usable runtime from measured average current and 80% of nominal capacity.
8. Prototype runtime target: at least 30 days per charge for the recorded usage cycle. For 2000 mAh, this requires average draw below 2.22 mA.
9. Do not report the estimate as a measured discharge result. Complete at least one charge/discharge cycle and verify low-battery recovery.

## Case and suppliers

Record actual plate thickness and switch retention after cutting.
Check minimum/maximum cut tolerances, gasket compression, standoff length, bolt clearance, and anti-slip feet.
Supplier AOI and bare-board electrical testing supplement these tests; they do not replace them.
Release only after all required results are recorded and the supplier accepts the exact revision and assembly scope.
