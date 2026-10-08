# Fridakeys

A proposed 42-key wireless Corne with MX hotswap sockets and TrackPoint pointing input.
The user assembles it with plugs and screws, without soldering.

## Current artifacts

- `ergogen/layout.yaml`: Corney Island geometry with its MX preset selected.
- `ergogen/pcb.yaml`: separate left and right electrical placement prototypes.
- `assets/frida.png`: original transparent Frida artwork.
- `.sysinit/rfc-fridakeeb.md`: research, proposed architecture, and unresolved manufacturing requirements.
- `THIRD_PARTY.md`: pinned source attribution and license location.

The layout defines one half, and the split preview mirrors it to show both halves.
The Piantor-inspired column offsets rise 8 mm from pinky to ring, then 4 mm to middle.
Index drops 4 mm from middle; the inner column drops another 2 mm.
MX spacing is 20 mm in both directions, 1 mm wider than the initial Corne draft.
The stagger is milder than Piantor’s 12 mm and 5 mm rises.
This draft uses the user’s successful Corne and 3x6 Voyager experience as fit context.
Comfort remains unverified until the physical prototype.
The Piantor Pro aluminum case is the visual reference for a silver surround and covered components.
MX switches, the battery, and the TrackPoint set this design's final height.
Touchpad geometry has been removed.
One TrackPoint belongs on the right half; its module, stem position, and mounting remain open.
The layout does not yet include TrackPoint mounting or gasket suspension.
PCB placement includes switches, diodes, controller contacts, power, reset, and a battery connector.
TrackPoint circuitry, the electrical schematic, and manufacturing outputs remain incomplete.
The tscircuit pipeline routes the existing matrix and power placement drafts.
Its inherited mounting holes describe the upstream sandwich assembly.
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
Supplier tolerance and physical contact fit still need verification.
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
The hero portrait uses 0.6 mm dot spacing; the repeated portraits use 1 mm spacing.
All artwork features measure at least 0.2 mm.
Ioskeley Mono Bold supplies all visible PCB text, including controller pin labels.
One-word arrows identify power, reset, battery, and the controller brain.
Back-side lettering reads correctly when the board is flipped.
It reserves 0.3 mm clearance from conservative pad envelopes.
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
```

Run these after generating the PCB placement and artwork.
Ergogen supplies geometry; tscircuit performs local autorouting; KiCad preserves original footprints and checks the final copper.
Generated React files appear under `tscircuit/generated/`.
Routing evidence appears under `build/tscircuit/`.
KiCad outputs are `build/pcb/fridakeeb_left_routed.kicad_pcb` and the corresponding right board.
The GitHub workflow runs this pipeline without a local Docker service.
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

## Accepted requirements

- Three rows, six columns, and three thumb keys per half.
- Wireless connection between halves and to the computer.
- ZMK firmware, using a supported controller and USB bootloader.
- Factory-installed MX hotswap sockets.
- Plug-in batteries, pointing-device cables, and prepared controllers are acceptable.
- One right-half TrackPoint for index-finger use, retaining all 42 hotswap keys.
- The TrackPoint module and cable must arrive prepared for plug-in installation without user soldering.
- White PCB solder mask with repeated black Frida portraits and lettering on both silkscreen faces.
- Ioskeley Mono Bold for all PCB text.
- Draft legend: `Fridakeys v1.0.0 by @fraud`.
- JLCPCB assembly and SendCutSend plates.
- Gasket suspension and anti-slip feet.

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
