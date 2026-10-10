# Assembly

Each half has 21 keys, a nice!nano V2 controller, and a protected 2000 mAh battery.
JLCPCB installs 47 parts per board: 21 MX sockets, 21 diodes, two controller receivers, power/reset switches, and a battery connector.
Buy the controllers, male headers, switches, keycaps, batteries, and M2 hardware separately.

| Part | Quantity for both halves |
| --- | ---: |
| nice!nano V2 | 2 |
| Mill-Max 350-10-112-00-006000 male header, 12 round pins | 4 |
| Adafruit 2011, protected 3.7 V 2000 mAh battery | 2 |
| MX switches and 1U keycaps | 42 each |

[parts.json](parts.json) lists factory components. [JLCPCB](jlcpcb/README.md), [JLC3DP](jlc3dp/README.md), and [SendCutSend](sendcutsend/README.md) have separate file packages.
[Reference keyboards](reference-builds.md) document the circuit and pin mapping.

## Controllers

Mount each nice!nano face up beneath the PCB, with USB toward the open rear edge.
Solder two male strips to each module: 24 joints per half, 48 total.
The factory-installed HCTL PM254-1-12-Z-3.0-C receivers face down; module pins point up into them.
The footprint name `crysknife:MillMax_315_1x12` identifies the retained geometry, while the BOM selects HCTL receivers.

Use round pins, not the square headers supplied with nice!nano.
The selected male pins measure 0.4064–0.508 mm across their tolerance range; receivers accept 0.40–0.56 mm.
Both use 2.54 mm pitch and 12 contacts. [header-fit.json](header-fit.json) records the drawings and dimensions.
The minimum body stack is 7.434 mm. The case reserves an 8 mm controller gap and 16 mm below the PCB.
Measure the seated stack and USB cable clearance during assembly.

Seat receiver strips evenly on their metal shoulders. Keep both rows parallel and contacts clear of solder and flux.
The receiver soldering limit is 260°C for 10 seconds.
Fit module headers with a fixture that keeps solder out of the receiver contacts.
The carrier uses RAW and GND; leave the extra B+ and B− holes beside USB empty.
[controller-reference.json](controller-reference.json) records all 24 contact positions and functions.

## Batteries

Use one protected, single-cell 3.7 V battery per half.
The selected Adafruit 2011 pack is nominally 60 × 36 × 7 mm.
The case reserves 64 × 40 × 8.5 mm beside the controller. Secure the cell with foam and an insulating cover.
Keep wires clear of screw heads, switch pins, and case edges.

Leave both nice!nano BOOST bridges open for nominal 100 mA charging.
The battery path passes through the ALPS SSSS811101 power switch, rated 300 mA; the 500 mA setting exceeds that rating.
JST1 pin 1 is GND; pin 2 is BAT_P. Check the real plug polarity with a meter before connecting it.
The power switch connects BAT_P to RAW, so charging requires PWR on.
USB powers the controller even with PWR off. [battery.json](battery.json) records the selected pack and charge settings.

## Case and startup

Use four M2 mounts per half. The [plate guide](sendcutsend/README.md) lists the standoffs, spacers, washers, and screw lengths.
The [printed case guide](jlc3dp/README.md) covers resin plates and the removable TPU sleeve.
Assemble the rigid sandwich first, then stretch the sleeve around it and roll its lip over the plate edge.

Flash and test the key matrix over USB before connecting batteries.
Follow the [firmware guide](../out/firmware/README.md) and [startup checks](physical-tests.md).
The assembled controller fit, charging, wireless operation, and typing feel have not been physically tested.

## Generate assembly files

Run in the repository Nix shell after generating the PCBs:

```sh
python3 scripts/generate_assembly.py
python3 scripts/check_assembly_guards.py
python3 scripts/check_supplier_placement.py
```

BOM, CPL, and part-source CSVs go into `build/manufacturing/assembly/`.
The generator checks references, footprint families, copper faces, and all 47 factory parts per board.
Supplier-model offsets and rotations come from `jlcpcb/placement-corrections.json`.
