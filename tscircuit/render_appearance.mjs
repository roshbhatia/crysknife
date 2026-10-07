import { readFileSync, writeFileSync } from "node:fs"
import { convertCircuitJsonToPcbSvg } from "circuit-to-svg"

for (const side of ["left", "right"]) {
  const input = new URL(`../build/tscircuit/${side}-routed.circuit.json`, import.meta.url)
  const data = JSON.parse(readFileSync(input, "utf8"))
  const svg = convertCircuitJsonToPcbSvg(data, {
    layer: "top",
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
  writeFileSync(new URL(`../build/tscircuit/${side}-appearance.svg`, import.meta.url), svg)
}
