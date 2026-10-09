# fridakeys

42-key Bluetooth split keyboard with standard MX hotswap sockets, ZMK, and one protected 2000 mAh battery per half.
The layout uses 20 mm pitch and 12/5/-5/-2 mm stagger for Outemu Medium-Low Black switches.
No pointing device is fitted.

The design remains a prototype candidate. Supplier acceptance and physical tests remain open.

## Build

Use the repository shell. `nix develop .` excludes ignored Node dependencies from its source snapshot.
Do not use `nix develop path:.`.

```sh
nix develop . --command npm ci
nix develop . --command npm run pcb
nix develop . --command python3 scripts/add_artwork.py
nix develop . --command npm ci --prefix tscircuit
nix develop . --command npm run route
nix develop . --command python3 scripts/check_electrical.py
nix develop . --command python3 scripts/generate_schematic.py
nix develop . --command python3 scripts/generate_assembly.py
nix develop . --command python3 scripts/check_assembly_guards.py
nix develop . --command npm run case
```

Ergogen supplies geometry and pinned footprints. Generated React models use tscircuit for routing.
KiCad merges copper into the original footprints, fills ground pours, and checks final DRC.
GitHub Actions runs the pinned KiCad container and builds all three ZMK images.
Local KiCad container commands need a running Docker service; generation does not.

Generated artifacts stay under `build/`:

- `pcb/`: placement PCBs, routed PCBs, DRC reports, and silkscreen previews.
- `tscircuit/`: React routing evidence and white PCB appearance previews for both faces.
- `schematic/`: separate KiCad schematics, independent pin mapping, ERC reports, netlists, and PDFs.
- `manufacturing/quote-only/`: BOM/CPL candidates with explicit unresolved supplier requirements.
- `case/`: five flat sandwich layers per half in DXF/SVG and OpenSCAD assembly files.

## Electronics and assembly

Each carrier has 21 Kailh MX hotswap sockets, 21 diodes, side power/reset switches, one JST-PH battery connector, and two controller receiver sockets.
All 47 carrier components per half are specified for factory assembly.
Two-face SMT and through-hole assembly are required; a pick-and-place-only quote is insufficient.
The controller uses genuine nice!nano V2, face up, with matching round-pin headers.
The factory may prepare the controllers if it accepts supplied modules; this remains a quote option.
The fallback user work is 48 controller header joints and two BOOST solder bridges across the complete keyboard.
The controller's built-in charge/status LEDs remain available through the open electronics bay.
No additional RGB lighting is fitted.

The battery selection is [Adafruit 2011](https://www.adafruit.com/product/2011): protected 1S 3.7 V, 2000 mAh, JST-PH plug.
The 500 mA charging option requires the BOOST bridge on each nice!nano.
Check plug polarity: JST1 pin 1 is GND; pin 2 is battery positive.
The power switch must be ON for charging. USB can power a controller with its battery switch OFF.
See [assembly requirements](manufacturing/README.md), [battery selection](manufacturing/battery.json), and [prototype tests](manufacturing/physical-tests.md).

## Schematic and firmware checks

The independent schematic design defines all 21 switch/diode paths, both 12-pin sockets, battery, power, and reset connections.
The external nice!nano symbol uses power and GPIO electrical types; unused pins have explicit no-connect markers.
The generation check compares all 117 carrier pin connections with each PCB.
CI runs KiCad ERC and compares the exported schematic netlist with those connections.
ERC and DRC cannot prove assembly quality, switch fit, charging temperature, or Bluetooth operation.

The right half remains ZMK central. The keymap provides QWERTY, symbols, navigation, function keys, and five Bluetooth profiles.
ZMK and its dependencies remain pinned in `firmware/config/west.lock.yml`.
The firmware workflow builds left, right, and settings-reset images, with compiled devicetree and Kconfig evidence.
The former PS/2 driver and TrackPoint circuit have been removed.

## PCB artwork

White solder mask and black Frida silkscreen cover both faces.
Each face repeats 31 portraits; a larger portrait is positioned around its open mouth rather than a switch hole.
The generator checks its sampled mouth region against pad, drill, title, and edge exclusions.
Artwork features are at least 0.2 mm, with 0.3 mm pad and 0.25 mm native silkscreen clearances.
The original transparent image remains unchanged.

All visible PCB lettering uses IBM Plex Mono Bold, including native controller labels.
The legend reads `fridakeys v1.0.0 by @roshbhatia`.
Arrows identify `{CPU}`, `{RST}`, `{PWR}`, and `{BTY}`.
Back lettering reads correctly when the board is flipped.
Installed keycaps and components can cover artwork; the PCB previews show bare boards.

## Sandwich case

OpenSCAD exports flat bottom, spacer, plate, gasket, and bezel contours; no printed parts are needed.
Six external M2 standoffs hold each assembly. The floating plate/PCB use perimeter gaskets.
USB, power, and reset remain accessible from the side.

The large battery adds 9 mm to the previous case reservation.
The nominal stack has a 3 mm nonconductive bottom, six 3 mm spacer rings, a 1.5 mm switch plate, and a 3 mm bezel.
PCB underside clearance is 13.9 mm; plate-to-PCB clearance is 3.5 mm.
Compressed gaskets measure 1 mm below the plate and 0.5 mm above it.
The battery's 64 × 40 × 8.5 mm reservation sits beneath the key field, clear of the controller RF exclusion.
A foam retainer and insulating cover must prevent movement and contact with switch pins.
Actual supplier material thickness, component protrusion, cell dimensions, and gasket travel require a prototype measurement.
Cutting exports are dimensional drafts until SendCutSend accepts the selected materials and tolerances.

## Release gates

- Matched header insertion and assembled controller height verified.
- Fresh KiCad ERC/DRC and all firmware builds passed for the proposed revision.
- JLCPCB approves sourcing, footprint geometry, pickup positions, rotations, and mixed assembly.
- SendCutSend approves actual materials, thicknesses, bolt holes, and cut tolerances.
- Physical prototype passes all 42 keys, wireless pairing/reconnect, charging, controls, and mechanical travel tests.

There is no accepted supplier quote or physical prototype result yet.
No production order is authorized by these files.
