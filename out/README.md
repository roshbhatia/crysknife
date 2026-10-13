# Engineering exports

- `kicad/`: editable routed boards, complete schematics, local libraries, schematic PDFs, and exported netlists.
- `3d/`: active 750 mAh reinforced resin tops, resin bottoms, rigid assemblies, and shortened TPU sleeves in 3MF format.
- `../manufacturing/enclosures/f-750-rigid-sandwich/`: active aluminum-floor STEP/STL/DXF, PMMA RF inserts, top plates, and hardware.
- `firmware/`: verified UF2 builds for each half and settings reset.
- `validation.json`: PCB check revision, reports, and board hashes.

Open `kicad/crysknife_left.kicad_pro` or `kicad/crysknife_right.kicad_pro` in KiCad.
Open `case/sandwich.scad` from the repository root for the parameter-based mechanical source.
The 3MF files are exported geometry. Edit the OpenSCAD source to change the case.
Read `tscircuit/README.md` for live React editing.

Regeneration replaces these snapshots. Keep lasting changes in the source generators and parameter files.
Fresh images live in `previews/`. Supplier files live in `manufacturing/jlcpcb/`, `manufacturing/jlc3dp/`, and `manufacturing/sendcutsend/`.
