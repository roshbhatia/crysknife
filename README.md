# crysknife

A 42-key wireless split keyboard with MX hotswap sockets, ZMK firmware, and a 2000 mAh battery in each half.
It uses nice!nano V2 controllers, white PCBs, and black knife artwork on both sides.

![Left PCB](previews/left.png)
![Right PCB](previews/right.png)

## Case

A clear acrylic top plate sits above a flat aluminum bottom plate.
Four standoffs hold each half together. A flat rubber layer is intended to damp vibration above the metal floor.
The top plate covers the controllers. USB, power, and reset remain accessible from the side.

![Case](previews/case-left.png)

## Edit the design

- [Layout](ergogen/layout.yaml): key spacing and column stagger.
- [PCB models](tscircuit/README.md#edit-the-models): open either half in the tscircuit editor.
- [Case model](case/sandwich.scad): open in OpenSCAD; dimensions live in [parameters.scad](case/parameters.scad).
- [Artwork](assets/knife.svg): the original knife illustration. PCB text uses IBM Plex Mono Bold.

[previews/](previews/) contains images of both PCB faces and the case.
[out/](out/README.md) contains checked KiCad projects, schematics, firmware, and 3D models.

## Build

Enter the Nix shell, then install the locked dependencies:

```sh
nix develop .
npm ci
npm ci --prefix tscircuit
```

Generate the boards, artwork, routing, schematics, and case:

```sh
npm run pcb
python3 scripts/add_artwork.py
npm run route
python3 scripts/check_electrical.py
python3 scripts/generate_schematic.py
python3 scripts/generate_assembly.py
python3 scripts/check_assembly_guards.py
npm run case
python3 scripts/check_case_models.py
python3 scripts/save_previews.py
```

Ergogen generates the layout. tscircuit routes the boards. KiCad checks the finished copper and schematic in GitHub Actions.
A separate workflow builds the left, right, and settings-reset firmware.

## Assembly and ordering

JLCPCB files are in [manufacturing/jlcpcb/](manufacturing/jlcpcb/README.md).
SendCutSend files are in [manufacturing/sendcutsend/](manufacturing/sendcutsend/README.md).
The [assembly guide](manufacturing/README.md) lists parts, controller headers, battery connections, and soldering work.

The design still needs supplier approval and a physical prototype test before ordering a production batch.
The remaining checks cover controller fit, charging, wireless operation, and plate fit.
