# Startup checks

## Before power

- Inspect factory joints, socket orientation, diode cathode marks, and receiver alignment.
- Check all 24 controller contacts against the schematic, including RAW, GND, RST, and VCC.
- Check BAT_P/GND and RAW/GND for shorts.
- Confirm battery red reaches JST1 pin 2 and black reaches pin 1 with a meter.
- Fit the controllers face up below the carrier. Check full seating, USB access, and clearance above the bottom plate.
- Fit all switches and keycaps. Check latch retention, full travel, screw clearance, and sleeve installation.
- Secure batteries without cell pressure or trapped wires.

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
Use the battery's specified temperature and voltage limits.
Check charge termination, low-battery recovery, and power-off behavior.
Measure current during typing, idle, sleep, and reconnect to estimate runtime.
Record measurements with the PCB and firmware revisions used for the test.
