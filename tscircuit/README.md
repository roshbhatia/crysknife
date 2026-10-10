# React routing pipeline

CLI 0.1.2258 is locked in this directory.
Ergogen supplies key positions and KiCad footprints.
`scripts/generate_tscircuit.py` generates React boards for both complete 21-key halves.
The model includes every copper pad, non-plated hole, net, and artwork rectangle from the placement source.
Single-pad nets remain reserved contacts; they need no copper connection.
These React boards are routing models. They are not a completed electrical schematic or assembly BOM.

Run from the repository Nix shell:

```sh
npm ci
npm ci --prefix tscircuit
npm run pcb
python3 scripts/add_artwork.py
npm run route
```

Editable JSX is committed in `tscircuit/generated/`.
Artwork arrays are committed once per half in `tscircuit/models/`.
A clean checkout can open either board without regenerating it.
Circuit JSON, previews, and check reports live in `build/tscircuit/`.
`left-appearance.svg` and `right-appearance.svg` show white mask and black knife artwork and lettering.
The corresponding `*-bottom-appearance.svg` files show the back faces as viewed after flipping the boards.
Both faces use Ioskeley Mono Bold for poems, component labels, and edge-aligned branding.
The React board color properties and KiCad stackup also specify white mask and black silkscreen.
The editor can retain its layer colors in the 2D routing view.
Select white mask and black silkscreen when creating the fabrication order.
`index.circuit.tsx` opens the left board by default.
`left.circuit.tsx` and `right.circuit.tsx` provide separate named preview entries.
Both use local autorouting and disable automatic part searches.

Start the live preview from the repository Nix shell:

```sh
tscircuit/node_modules/.bin/tsci dev tscircuit/index.circuit.tsx --port 3020
```

Open [left PCB](http://localhost:3020/#file=tscircuit%2Fleft.circuit.tsx)
or [right PCB](http://localhost:3020/#file=tscircuit%2Fright.circuit.tsx).
Regenerate the routing models after editing Ergogen geometry.
The development server watches the React files for changes.

The adapter places each pad at its explicit world coordinate.
It avoids the direct converter's bottom-side mirroring error.
It retains pad dimensions, rotations, assembly sides, drills, and net membership.
Outline arcs are sampled with a maximum 0.005 mm chord error for routing.
KiCad retains the original exact outline and silkscreen.
Routing uses 0.3 mm clearance to holes, 0.25 mm between via and pad edges, and 0.55 mm to the board edge.
These exceed KiCad's default 0.25 mm hole and 0.5 mm edge constraints.

The build first checks every pad and hole against the descriptor.
Up to five placement diagnostics per half use overlapping bounding boxes for separated shapes.
The check calculates exact circle and rotated-rectangle clearance for those diagnostics.
It rejects clearance below 0.2 mm and records the measured values.
Only after this check does routing disable tscircuit's placement diagnostics.

The rounded battery pad specifies zero drill offsets explicitly.
Undefined offsets crash the live copper checks; JSON serialization drops those fields and can conceal the cause.
The build renders both named React entries and checks their live, unmodified database before JSON serialization.
Runtime errors, routing errors, and copper shorts fail the build.
Post-build checks validate the finished routes.
Warnings about generic pad symbols and missing manufacturer metadata remain visible.

The KiCad job independently checks every descriptor against `pcbnew`.
It merges only tracks and vias into the original boards.
KiCad finishes reset-button escapes when the autorouter leaves a GND or RST via too close to the opposite pad.
This step moves the via outside its own pad, keeps both connected tracks, and records its clearance before and after.
It also separates conflicting vias on different nets to a 0.3 mm copper-edge gap, retaining both connected trace endpoints.
The router's drill-spacing setting checks these gaps but does not change the offending routes.
The final KiCad DRC validates the finished route. React previews remain autorouter drafts.
It preserves footprint references, solder mask, paste, exact outlines, and knife artwork.
The routed board check requires zero unconnected items and no violations except library-resolution warnings.
KiCad independently checks the complete schematic and its exported netlist against all carrier pins.

References: [board and autorouter](https://docs.tscircuit.com/elements/board),
[CLI export](https://docs.tscircuit.com/command-line/tsci-export),
[AI skill](https://github.com/tscircuit/skill),
[KiCad exporter silk issue](https://github.com/tscircuit/circuit-json-to-kicad/issues/362).

## Edit the models

Enter `nix develop .` and run `npm ci --prefix tscircuit` once.
Start `tsci dev` with the command above, then select the left or right entry.
Edit the corresponding `generated/*-board.circuit.tsx` to experiment with board geometry, pad placement, colors, or routing constraints.
The `models/*-artwork.ts` arrays contain `[x, y, width, height, layer]` rectangles in millimeters.
Both placement and routed entries share one board component and one artwork array per half.

The generated files are editable snapshots. `npm run route` replaces them from the Ergogen sources and artwork generator.
For lasting changes, edit `ergogen/layout.yaml`, `ergogen/pcb.yaml`, `scripts/add_artwork.py`, or `scripts/generate_tscircuit.py`.
Copy an entry before experimenting if you want to keep changes outside regeneration.
Changes made only in React do not alter the original KiCad footprints or manufacturing BOM.
Run the full pipeline and its independent KiCad checks before treating an experiment as fabrication input.

Fresh front and back PNGs are committed in [`../previews/`](../previews/).
Run `nix develop . --command python3 scripts/save_previews.py` after routing to refresh them.
Open [`../case/sandwich.scad`](../case/sandwich.scad) in OpenSCAD for the editable mechanical assembly.
Its geometry is committed beside it, so no ignored build directory is needed.
The case model shows reserved envelopes. Controller, socket, switch, and battery fit still need physical checks.

Checked KiCad projects and 3D exports live in [`../out/`](../out/README.md).
Vendor files have separate directories under `manufacturing/`.
