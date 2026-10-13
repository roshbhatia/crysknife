# Startup checks

## Before power

- Inspect factory joints, socket orientation, diode cathode marks, and receiver alignment.
- Check all 24 controller contacts against the schematic, including RAW, GND, RST, and VCC.
- Check BAT_P/GND and RAW/GND for shorts.
- Confirm battery red reaches JST1 pin 2 and black reaches pin 1 with a meter.
- Fit the controllers face up below the carrier. Check full seating, USB access, and clearance above the bottom plate.
- Fit all switches and keycaps. Check latch retention, full travel, screw clearance, and sleeve installation.
- Measure the protected pack against the assumed 54 × 38 × 5 mm bounds and the 64 × 40 × 6.5 mm reservation.
- Secure batteries without cell pressure or trapped wires; fit the leads in the reserved corridor without folding or tension.
- Check the floor PET liner, protected terminals, and loose end tabs. Do not add foam layers to force fit.
- Check all four loaded feet, floor flex, screw clearances, and actual 12 mm standoff/2 mm shim heights.
- A larger pack or cable needs a taller/larger case; do not force it into this prototype.

## USB and Bluetooth

Flash the matching left/right UF2 files and test all 42 keys over USB before connecting batteries.
Check rows, columns, layers, modifiers, and simultaneous keys for wrong or phantom events.
Test reset, double-tap bootloader entry, and settings-reset recovery.
Pair both halves and the host, then check reconnect and wake from sleep.
The right half is the central. Test it over USB with the left half wireless.
Check side access to USB, power, and reset with the case installed.

On battery power, leave both halves idle for more than 15 minutes.
Test each key as a local wake source, then check split and host reconnection without clearing bonds.
Check whether the wake press reaches the host, and record the reconnect delay.
Use only right keys for 15 minutes, then wake the left locally and verify its keys.
Repeat with right USB power: the right must stay awake; the battery-powered left can sleep.

## Charging

Leave BOOST open on both modules for nominal 100 mA charging.
Measure charging current, battery voltage, and temperature at low, middle, and near-full charge.
For this prototype, start charging at 10–35°C ambient; stop at 40°C cell temperature or a 10°C rise.
These are conservative test assumptions, not published pack ratings. Check that charge termination does not exceed 4.2 V.
Replace a visibly swollen or damaged pack. The growth allowance is not a permission to continue using a damaged cell.
Check charge termination, low-battery recovery, and power-off behavior.
Measure current during typing, idle, sleep, and reconnect to estimate runtime.
Record measurements with the PCB and firmware revisions used for the test.
