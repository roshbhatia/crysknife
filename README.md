# Fridakeys

A proposed 42-key wireless split keyboard with MX hotswap sockets and TrackPoint pointing input.
The user assembles it with plugs and screws, without soldering.

## Current artifacts

- `ergogen/layout.yaml`: Corney Island geometry with its MX preset selected.
- `ergogen/pcb.yaml`: separate left and right electrical placement prototypes.
- `assets/frida.png`: original transparent Frida artwork.
- `.sysinit/rfc-fridakeeb.md`: research, proposed architecture, and unresolved manufacturing requirements.
- `THIRD_PARTY.md`: pinned source attribution and license location.

The layout defines one half, and the split preview mirrors it to show both halves.
The Piantor-inspired column offsets rise 10 mm from pinky to ring, then 5 mm to middle.
Index drops 5 mm from middle; the inner column drops another 2 mm.
MX spacing is 20 mm in both directions, 1 mm wider than the initial Corne draft.
The stagger is milder than Piantor’s 12 mm and 5 mm rises.
This draft uses the user’s successful Corne and 3x6 Voyager experience as fit context.
Comfort remains unverified until the physical prototype.
The Piantor Pro aluminum case is the visual reference for a silver surround and covered components.
MX switches, the battery, and the TrackPoint set this design's final height.
Touchpad geometry has been removed.
One TrackPoint belongs on the right half; its module, stem position, and mounting remain open.
The OpenSCAD case draft includes perimeter gasket suspension.
TrackPoint mounting remains incomplete.
PCB placement includes switches, diodes, controller contacts, power, reset, and battery connectors.
The right PCB includes an eight-pin TrackPoint ribbon connector and its support circuit.
The electrical schematic remains incomplete.
Quote-only BOM and placement inventories are generated under `build/manufacturing/quote-only/`.
The tscircuit pipeline routes the existing matrix and power placement drafts.
The PCB has no case mounting holes; the OpenSCAD sandwich uses six external standoffs per half.
No PCB assembly order is ready.

## Generate the layout

```sh
nix develop .
npm ci
npm run layout
npm run preview
npm run pcb
python3 scripts/add_artwork.py
```

Outputs appear under `build/layout/`.
`build/layout/outlines/key_preview.svg` shows the board outline and keycaps.
`build/layout/split_preview.svg` shows both halves without touchpads.
The preview command also renders `build/layout/split_preview.png` for visual review.
Review the generated SVG and DXF files before changing mechanical dimensions.
Do not send these prototype plates to fabrication.

PCB drafts appear under `build/pcb/` with 21 hotswap sockets and 21 SMD diodes per half.
Both use dedicated controller footprints without reversible solder jumpers.
The controller generator adapts upstream 1 mm holes to a nominal 0.85 mm for spring headers.
[Typeractive specifies 0.8–0.9 mm finished holes](https://typeractive.xyz/products/no-solder-spring-headers).
[JLCPCB lists standard PTH tolerance as +0.13/−0.08 mm](https://jlcpcb.com/capabilities/pcb-capabilities/).
At 0.85 mm nominal, that permits 0.77–0.98 mm and cannot guarantee the contact fit.
Its ±0.05 mm press-fit option lists multilayer ENIG boards; the current board has two copper layers.
Supplier acceptance of tighter finished holes or a factory-soldered controller connection remains required.
The right PCB mirrors key positions while preserving component pin orientation and assembly sides.

KiCad CLI runs in its official container, pinned in `tools.lock.json`.
It requires the host Docker service and makes no network connections during checks.
For example:

```sh
python3 scripts/kicad.py pcb drc --format json \
  --output build/pcb/left-drc.json build/pcb/fridakeeb_left.kicad_pcb
python3 scripts/kicad.py --python scripts/check_placement.py
```

Read the report: KiCad can exit successfully while reporting violations or unconnected pads.
The unrouted drafts are expected to have unconnected nets and are not ready for assembly.
The placement check reads KiCad pads to verify matrix topology, diode polarity, socket assembly sides, mirroring, and controller hole dimensions.
It does not replace electrical, routing, or physical validation.

`scripts/add_artwork.py` repeats Frida's halftone on the front and back silkscreen.
The 44 mm hero portrait uses 0.3 mm sampling; repeated 26 mm portraits use 0.4 mm sampling.
The hero sits lower to preserve Frida's open mouth, with its right-half image mirrored.
Adjacent ink cells merge into rectangular runs without changing their outline.
All artwork features measure at least 0.2 mm.
Ioskeley Mono Bold supplies all visible PCB text, including controller pin labels.
Arrows use `{PWR}`, `{RST}`, `{BTY}`, and `{CPU}` labels.
Back-side lettering reads correctly when the board is flipped.
It reserves 0.3 mm clearance from conservative pad envelopes.
It also protects existing socket outlines and diode symbols with 0.25 mm clearance.
The original artwork remains unchanged; small dots are resampled for printing.
The PCB workflow checks artwork with KiCad and uploads silkscreen previews.
These checks allow the known unrouted connections and footprint-library warnings.
They do not establish manufacturing readiness.

## React routing and KiCad validation

```sh
npm ci --prefix tscircuit
npm run route
python3 scripts/kicad.py --python scripts/check_tscircuit_source.py
python3 scripts/kicad.py --python scripts/merge_tscircuit_routes.py
python3 scripts/kicad.py --python scripts/fill_ground.py
```

Run these after generating the PCB placement and artwork.
Ergogen supplies geometry; tscircuit performs local autorouting; KiCad preserves original footprints and checks the final copper.
Generated React files appear under `tscircuit/generated/`.
Routing evidence appears under `build/tscircuit/`.
KiCad outputs are `build/pcb/fridakeeb_left_routed.kicad_pcb` and the corresponding right board.
The GitHub workflow runs this pipeline without a local Docker service.
KiCad fills GND on both copper faces after merging routes.
The zones use 0.3 mm clearance, 0.3 mm thermal spokes, and removal of disconnected islands.
Their outlines sit 0.65 mm inside the PCB boundary, preserving the 0.55 mm copper-edge requirement.
A 28 by 46 mm exclusion around each controller prevents ground pours below the module and antenna.
This exclusion does not prohibit existing signal traces; RF performance still requires prototype testing.
Its routed DRC gate requires zero unconnected items and no unexpected violations.
Read [the pipeline details](tscircuit/README.md) for conversion checks and known upstream limitations.
These checks do not prove TrackPoint operation, mechanical fit, or factory acceptance.

## Firmware draft

`firmware/` defines a nice!nano v2 shield with the right half as the central.
Its pin assignment matches the PCB matrix draft.
The right half connects the TrackPoint data, clock, and reset to P2, P3, and P4.
The keymap provides QWERTY, symbols, Bluetooth selection, and mouse buttons.
The GitHub Actions workflow builds both halves and a settings-reset image.
It pins ZMK, the external PS/2 driver, the build container, and action revisions.
`firmware/config/west.lock.yml` freezes all active dependencies from the verified build.
The build script uses this lock instead of resolving upstream branches again.
Artifacts include UF2 files, compiled devicetree, Kconfig, and resolved dependency revisions.
These are integration drafts until the builds and physical hardware tests pass.

`nix develop . --command python3 scripts/check_electrical.py` checks the PCB against the firmware source.
It verifies all 42 matrix coordinates, diode direction, nice!nano pin assignments, battery power, and reset wiring.
The right circuit adds 4.7 kΩ clock/data pull-ups to VCC, a 10 kΩ reset pull-down, and 100 nF reset capacitance.
Another 100 nF capacitor decouples VCC beside the ribbon interface.
The connector uses Sprintek method 3: DATA, RST, unused MIDDLE, unused RIGHT, unused LEFT, CLK, GND, VCC.
Mouse buttons come from the keyboard keymap.
The Hirose FH12-8S-1SH(55) candidate accepts eight-conductor, 1 mm pitch, 0.3 mm thick ribbon.
Its [JLCPCB identifier is C596711](https://jlcpcb.com/partdetail/HRS_Hirose-FH12_8S_1SH_55/C596711).
The local land pattern follows the manufacturer catalog; the current engineering drawing still needs supplier acceptance.
The connector and passives sit below the raised nice!nano, clear of the switch holes.
Plug in the prepared ribbon before inserting the controller.
Cable contact orientation, pin-to-pin continuity, latch access, and module clearance require physical verification.
The controller bay retains its `{CPU}` arrow but omits hidden pin lettering on the populated right half.

## Sandwich case draft

```sh
nix develop . --command npm run case
```

`case/sandwich.scad` uses geometry from the actual generated PCBs.
It exports left and right bottom plates, spacer rings, switch plates, gaskets, and bezels as DXF and SVG.
Assembly CSG files and dimension checks appear under `build/case/`.
No printed parts are required.
The floating switch plate and PCB sit between compressed perimeter gaskets.
Six M2 standoffs sit outside each PCB, keeping bolts clear of copper and sockets.
An open electronics bay provides side access to USB, power, and reset.
The nominal stack uses a 3 mm acrylic bottom, three 3 mm spacer rings, and a 1.5 mm switch plate.
The lower and upper gaskets compress to 1 mm and 0.5 mm respectively.
The bezel is 3 mm thick; nominal standoffs are 12 mm above the bottom plate.
Use nonconductive bottoms and spacers around the Bluetooth module.
Anti-slip feet attach below the bottom plate.

Outemu Medium-Low Black switches retain the standard MX socket footprint.
[ZSA tested the MX-compatible Medium-Low family](https://blog.zsa.io/diy-low-profile-moonlander/).
The plate has 14 mm openings, with a configurable 3.5 mm gap above the PCB and 1.5 mm thickness.
These vertical dimensions need measurement on the user's switch batch before plate fabrication.
The 4.9 mm underside clearance is a reserved envelope, not proof of battery or connector fit.
The controller and TrackPoint need mechanical clearance checks with their exact supplied parts.
Supplier material thickness and cut tolerances must match the final dimensions.

## Factory assembly options

[Assembly quote requirements](manufacturing/README.md) define the candidate BOM, prepared parts, and acceptance tests.
`nix develop . --command python3 scripts/generate_assembly.py` exports separate quote BOM/CPL files.
These include every factory socket and diode, but require pickup-origin and rotation review.

[JLCPCB Standard assembly](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) supports both PCB faces and through-hole connectors.
The factory must install all 42 MX sockets, diodes, power switches, reset buttons, and battery connectors.
The [Kailh CPG151101S11-1 catalog entry](https://jlcpcb.com/partdetail/Kailh-CPG151101S111/C5184526) is Standard Only.
Catalog presence does not confirm stock, footprint fit, or an accepted assembly quote.
[Flying-probe and functional testing](https://jlcpcb.com/help/article/smt-inspection-and-testing-capabilities) can support the acceptance plan.
Test scope and fixtures need a supplier quote; AOI alone cannot prove wireless operation.
Prepared nice!nano modules and spring headers remain a plug-in assembly path to verify.
Each half uses its own rechargeable battery and USB charging port.
An inter-half USB-C cable is not supported by the current electrical design or firmware.

## Accepted requirements

- Three rows, six columns, and three thumb keys per half.
- Wireless connection between halves and to the computer.
- ZMK firmware, using a supported controller and USB bootloader.
- Factory-installed MX hotswap sockets.
- Outemu Medium-Low Black switches with standard MX pin geometry.
- Plug-in batteries, pointing-device cables, and prepared controllers are acceptable.
- One right-half TrackPoint for index-finger use, retaining all 42 hotswap keys.
- The TrackPoint module and cable must arrive prepared for plug-in installation without user soldering.
- White PCB solder mask with repeated black Frida portraits and lettering on both silkscreen faces.
- Ioskeley Mono Bold for all PCB text.
- Draft legend: `Fridakeys v1.0.0 by @fraud`.
- JLCPCB assembly and SendCutSend plates.
- Gasket suspension and anti-slip feet.
- A sandwich case with side access to power, reset, and charging.

The revision identifies this project, rather than claiming an upstream Corne release.

## TrackPoint sourcing evidence

The proposed route uses one integrated Sprintek SK8707-01-005 module with a factory-installed ribbon connector.
This remains a candidate, rather than an accepted part or a completed integration.
The [manufacturer store](https://store.sprintek.com/products) lists the integrated 3.3 V model.
The [manufacturer datasheet](https://docs.holykeebs.com/datasheets/SK8707-01.pdf), revision 1.04, documents optional connector installation on request.
The order needs supplier confirmation of the connector, matching cable, preparation, and availability.
The standard module cannot be assumed to include that connector.

The drawing specifies a 23 mm wide, 29.55 mm long module and an 11.5 mm stem.
These dimensions describe the module; they do not establish clearance with MX sockets or a plate.
The detached SK8707-01-004 sold by Holykeebs needs additional assembly and has a shorter stem.
It does not satisfy the plug-in requirement by itself.

The right half is the proposed ZMK central.
This keeps the TrackPoint connection local to the half that sends mouse reports to the computer.
[Current ZMK](https://zmk.dev/docs/hardware-integration/pointing) also supports pointing input from peripherals.
The proposed central placement simplifies integration but is not a firmware restriction.
The [badjeff PS/2 driver](https://github.com/badjeff/kb_zmk_ps2_mouse_trackpoint_driver/tree/7ab7846a95b233c3ada0e0605b972f36353e7bc4) emits Zephyr input events.
Compatibility still requires a physical module test.

Both halves and the reset image [passed the pinned firmware build](https://github.com/roshbhatia/fridakeys/actions/runs/37675127728).
The physical module test remains open.
A [Corne TrackPoint build](https://github.com/joh/crkbd-trackpoint/tree/e7f2f0581cea261c441d9648132b6b4fd5f9d41f) places its stem between Y, U, H, and J.
It provides a mounting case, stem adapter, and a jig for modifying those four keycaps.
Its wired QMK electronics and soldered wiring do not satisfy this project's requirements.
Its mechanical approach is a reference; its files use CC BY-NC-SA 4.0.
The Fridakeys stem position still needs selection and a fit test.

## Manufacturing gates

- Confirm the exact prepared TrackPoint module, cable, stem, and mounting hardware.
- Prove controller spring-header fit, finished-hole tolerance, battery polarity, and charging behavior.
- Generate separate left and right PCBs with every MX socket installed by the factory.
- Complete the schematic, routing, and KiCad electrical and board checks.
- Build firmware for both halves and test all keys, wireless pairing, and pointing input.
- Verify gasket travel, socket clearance, plate fit, and TrackPoint reach with a prototype.
- Convert Frida and the title to silkscreen geometry and check supplier minimum features.
- Obtain JLCPCB acceptance of the exact assembly BOM and placement files.
- Export and review full-scale SendCutSend plate files after the mechanical checks.

These gates remain open. Layout generation alone does not establish manufacturing readiness.
