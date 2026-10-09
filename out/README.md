# Engineering exports

- `kicad/`: editable routed boards, complete schematics, local libraries, schematic PDFs, and exported netlists.
- `3d/`: flat top and bottom plates, case assemblies, and TPU sleeves in 3MF format.
- `firmware/`: verified UF2 builds for each half and settings reset.
- `validation.json`: PCB check revision, reports, and board hashes.

Open `kicad/crysknife_left.kicad_pro` or `kicad/crysknife_right.kicad_pro` in KiCad.
Open `case/sandwich.scad` from the repository root for the parameter-based mechanical source.
The 3MF files are exported geometry. Edit the OpenSCAD source to change the case.
Read `tscircuit/README.md` for live React editing.

Regeneration replaces these snapshots. Keep lasting changes in the source generators and parameter files.
Fresh images live in `previews/`. Supplier files live in `manufacturing/jlcpcb/` and `manufacturing/sendcutsend/`.
These exports do not authorize an order. Supplier approval and physical prototype tests remain open.
