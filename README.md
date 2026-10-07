# Fridakeeb

A proposed 42-key wireless Corne with MX hotswap sockets and TrackPoint pointing input.
The user assembles it with plugs and screws, without soldering.

## Current artifacts

- `ergogen/layout.yaml`: Corney Island geometry with its MX preset selected.
- `assets/frida.png`: original transparent Frida artwork.
- `.sysinit/rfc-fridakeeb.md`: research, proposed architecture, and unresolved manufacturing requirements.
- `THIRD_PARTY.md`: pinned source attribution and license location.

The layout defines one half, and the split preview mirrors it to show both halves.
Touchpad geometry has been removed.
One TrackPoint belongs on the right half; its module, stem position, and mounting remain open.
The layout does not yet include TrackPoint mounting, gasket suspension, circuitry, routing, or manufacturing outputs.
Its inherited mounting holes describe the upstream sandwich assembly.
No PCB assembly order is ready.

## Generate the layout

```sh
nix develop path:.
npm ci
npm run layout
npm run preview
```

Outputs appear under `build/layout/`.
`build/layout/outlines/key_preview.svg` shows the board outline and keycaps.
`build/layout/split_preview.svg` shows both halves without touchpads.
The preview command also renders `build/layout/split_preview.png` for visual review.
Review the generated SVG and DXF files before changing mechanical dimensions.
Do not send these prototype plates to fabrication.

## Accepted requirements

- Three rows, six columns, and three thumb keys per half.
- Wireless connection between halves and to the computer.
- ZMK firmware, using a supported controller and USB bootloader.
- Factory-installed MX hotswap sockets.
- Plug-in batteries, pointing-device cables, and prepared controllers are acceptable.
- One right-half TrackPoint for index-finger use, retaining all 42 hotswap keys.
- The TrackPoint module and cable must arrive prepared for plug-in installation without user soldering.
- White PCB solder mask with black Frida artwork and lettering on the silkscreen.
- KingjolA title font, recovered from the Terminus Est KiCad source.
- Draft legend: `fridakeeb (corne-derived v0.1) by @fraud`.
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
Compatibility still requires a pinned ZMK build and a physical module test.

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
