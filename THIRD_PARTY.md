# Upstream sources

`ergogen/layout.yaml` derives from [Corney Island](https://github.com/ceoloide/corney-island/blob/b7cadab700a4a198a7217d05b6692b787136d043/ergogen/config.yaml).
The source revision is `b7cadab700a4a198a7217d05b6692b787136d043`.
Its MIT license is preserved in `ergogen/LICENSE.corney-island`.

The layout source retains upstream points and outlines, selects MX dimensions, and excludes upstream electronics and case generation.
The upstream build scripts are not included.
Upstream updates require explicit review and permission.

PCB generation loads [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints/tree/48935f54b456ff1503d78d6b17d9d146b54e8ade) from the pinned Nix input.
Revision `48935f54b456ff1503d78d6b17d9d146b54e8ade` remains in the immutable dependency source.
Its selected footprints use MIT and CC BY-NC-SA 4.0 licenses, as declared in each source file.
Diode, controller, and power-switch sources use CC BY-NC-SA 4.0.
MX socket, battery, and reset footprints use MIT.
No upstream footprint source files are edited or vendored.
The `out/` snapshots embed generated KiCad footprint geometry for editing.
The local controller adapter preserves pin positions and nets, sets 1 mm drills, and splits contacts into two factory socket footprints.

`assets/knife.svg` is an unchanged copy of the user's `bike-decals/assets/blade.svg`.
It depicts a hand holding a knife and was supplied through the user's sticker project.
`scripts/add_artwork.py` converts it to solid black silkscreen geometry on both PCB faces.

`assets/kingjola.ttf` is the user's KingjolA Regular font from the `bike-decals` project.
Poem lines and component labels use this face as portable silkscreen geometry.
IBM Plex Mono supplies braces that Kingjola does not contain.
No font license was supplied with this asset.

`assets/ibm-plex-mono-bold.ttf` comes from [Google Fonts](https://github.com/google/fonts/tree/2eb0b48d5f760f62e286216f0859a8c540dbc1bd/ofl/ibmplexmono).
The signature uses IBM Plex Mono Bold. Its OFL is preserved in `assets/LICENSE.ibm-plex-mono`.

Column stagger dimensions are measured from the [Piantor left PCB](https://github.com/beekeeb/piantor/blob/cd847afb4f9a86e8c1c8e36f243140644013afb2/pcb/left/keyboard_pcb.kicad_pcb).
The source uses 18 mm horizontal and 17 mm vertical pitch; this design uses 20 mm MX pitch.
Its measured 12, 5, -5, and -2 mm offsets inform a 12, 5, -5, and -2 mm adaptation.
Upstream PCB, circuit, and case files are not included. Its repository uses GPL-3.0.

The controller socket adapter retains the pinned nice!nano net mapping and splits its pads into two factory assembly footprints.
Socket dimensions reference the [Mill-Max 315-43-112-41-003000 manufacturer drawing](https://static6.arrow.com/aropdfconversion/2e225be7d9212620894362dafa7ce735623fe9ca/315-43-112-41-003000.pdf).

The four case mounts follow the distributed pattern in the [Corne MX plate](https://github.com/foostan/crkbd/blob/63366fb7f51cf2a796462fdd90527e99dd126055/plates/3x6/pcb/plate-top-cherrymx.kicad_pcb).
Their positions are adapted to this layout, with 5 mm carrier holes around 4 mm standoffs and 2.2 mm plate screw holes.
The mounting-hole footprint comes from the same pinned ceoloide library and uses MIT.
No Corne PCB or plate source is vendored.
