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
