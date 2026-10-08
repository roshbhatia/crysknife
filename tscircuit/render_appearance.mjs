import { readFileSync, writeFileSync } from "node:fs"
import { convertCircuitJsonToPcbSvg } from "circuit-to-svg"

for (const side of ["left", "right"]) {
  const input = new URL(`../build/tscircuit/${side}-routed.circuit.json`, import.meta.url)
  const data = JSON.parse(readFileSync(input, "utf8"))
  for (const layer of ["top", "bottom"]) {
    let svg = convertCircuitJsonToPcbSvg(data, {
      layer,
      width: 800,
      height: 600,
      backgroundColor: "#fafafa",
      showSolderMask: true,
      showPinNumbers: false,
      drawPaddingOutsideBoard: true,
      colorOverrides: {
        soldermask: { top: "#fafafa", bottom: "#fafafa" },
        soldermaskOverCopper: { top: "#f0f0f0", bottom: "#f0f0f0" },
        soldermaskWithCopperUnderneath: { top: "#f0f0f0", bottom: "#f0f0f0" },
        silkscreen: { top: "#111111", bottom: "#111111" },
        copper: { top: "#c9a44c", bottom: "#c9a44c" },
        substrate: "#fafafa",
        drill: "#303030",
        boardOutline: "#999999",
      },
    })
    if (layer === "bottom") {
      svg = svg.replace(/(<svg[^>]*>)/, '$1<g transform="translate(800 0) scale(-1 1)">')
        .replace("</svg>", "</g></svg>")
    }
    const filename = layer === "top" ? `${side}-appearance.svg` : `${side}-bottom-appearance.svg`
    writeFileSync(new URL(`../build/tscircuit/${filename}`, import.meta.url), svg)
  }
}
