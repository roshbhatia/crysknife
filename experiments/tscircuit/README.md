# tscircuit conversion experiment

This experiment tests CLI 0.1.2258 against one generated MX hotswap footprint.
It does not generate production keyboard PCBs.
The existing Ergogen and KiCad pipeline remains the design source.

`MxHotswap.tsx` derives from ceoloide's switch_mx footprint at the revision in `flake.lock`.
The source came from the generated left PCB, with its placement reset to zero.
KiCad's legacy bare `hide` token was converted to `(hide yes)` before `tsci convert`.
The converter rejected the original syntax.
The upstream MIT license remains in the pinned Nix footprint source.

The pilot has one bottom-side MX socket and one SOD123 diode.
Local autorouting completes their single connection at 0.25 mm width.
Circuit JSON and KiCad PCB export both complete.
The imported socket's asymmetric geometry does not preserve the source coordinates when placed on the bottom side.
The KiCad exporter also places its silkscreen on F.SilkS.
These results prevent adopting this direct conversion for fabrication.
They do not establish that every tscircuit design has the same problems.

Run commands from the repository Nix shell:

```sh
npm ci --prefix experiments/tscircuit
experiments/tscircuit/node_modules/.bin/tsci export experiments/tscircuit/index.circuit.tsx \
  -f circuit-json -o "$PWD/build/research/tscircuit-pilot.json"
experiments/tscircuit/node_modules/.bin/tsci export experiments/tscircuit/index.circuit.tsx \
  -f kicad_pcb -o "$PWD/build/research/tscircuit-pilot.kicad_pcb"
python3 experiments/tscircuit/check_geometry.py
```

The geometry check currently exits 1 and prints the coordinate differences.
Retest the exact tool versions after any conversion correction.
Before adopting the pipeline, compare pad identities, holes, layers, outlines, artwork, and net connectivity with KiCad.

References: [conversion](https://docs.tscircuit.com/command-line/tsci-convert),
[local autorouting](https://docs.tscircuit.com/elements/board#setting-the-autorouter),
[AI skill](https://github.com/tscircuit/skill),
[bottom-side silk issue](https://github.com/tscircuit/circuit-json-to-kicad/issues/362).
