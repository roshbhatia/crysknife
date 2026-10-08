# Upstream sources

`ergogen/layout.yaml` derives from [Corney Island](https://github.com/ceoloide/corney-island/blob/b7cadab700a4a198a7217d05b6692b787136d043/ergogen/config.yaml).
The source revision is `b7cadab700a4a198a7217d05b6692b787136d043`.
Its MIT license is preserved in `ergogen/LICENSE.corney-island`.

The layout source retains upstream points and outlines, selects MX dimensions, and excludes upstream electronics and case generation.
The upstream build scripts are not included.
Upstream updates require explicit review and permission.

PCB generation loads [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints/tree/48935f54b456ff1503d78d6b17d9d146b54e8ade) from the pinned Nix input.
Revision `48935f54b456ff1503d78d6b17d9d146b54e8ade` and its MIT license remain in the immutable dependency source.
No upstream footprint files are edited or vendored.
The local controller adapter changes only the 24 header drill diameters in generated output.

`assets/frida.png` is an unchanged copy of `/Users/roshan/Desktop/frida.png`, supplied by the user.
`scripts/add_artwork.py` resamples its halftone for draft PCB silkscreen placement.
The original source image remains unchanged.

`assets/ioskeley-mono-bold.ttf` comes from [Ioskeley Mono v2.1.0](https://github.com/ahatem/IoskeleyMono/releases/tag/v2.1.0).
It is the Normal/Unhinted Bold face from the release archive.
Its SIL Open Font License is preserved in `assets/LICENSE.ioskeley-mono`.
All PCB lettering uses this font, rasterized into portable silkscreen geometry.
The previously supplied KingjolA asset remains unused.

Column stagger dimensions are measured from the [Piantor left PCB](https://github.com/beekeeb/piantor/blob/cd847afb4f9a86e8c1c8e36f243140644013afb2/pcb/left/keyboard_pcb.kicad_pcb).
The source uses 18 mm horizontal and 17 mm vertical pitch; this design uses 20 mm MX pitch.
Its measured 12, 5, -5, and -2 mm offsets inform a milder 8, 4, -4, and -2 mm adaptation.
Upstream PCB, circuit, and case files are not included. Its repository uses GPL-3.0.
