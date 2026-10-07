import React from "react"
import { RootCircuit } from "tscircuit"
import { writeFileSync } from "node:fs"

globalThis.React = React

for (const side of ["left", "right"]) {
  const { default: Board } = await import(`./${side}.circuit.tsx`)
  const circuit = new RootCircuit({ platform: { partsEngineDisabled: true } })
  circuit.add(React.createElement(Board))
  await circuit.renderUntilSettled()
  const data = circuit.db.toArray()
  const errors = data.filter((item) => item.type.endsWith("_error"))
  const pads = data.filter((item) => item.type === "pcb_plated_hole" && item.shape === "circular_hole_with_rect_pad")
  if (pads.some((pad) => pad.hole_offset_x !== 0 || pad.hole_offset_y !== 0)) {
    throw new Error(`${side}: centered battery drills need explicit zero offsets`)
  }
  const report = { side, liveDrcErrors: errors, roundedDrillOffsetsDefined: true }
  writeFileSync(new URL(`../build/tscircuit/${side}-live-checks.json`, import.meta.url), JSON.stringify(report, null, 2) + "\n")
  if (errors.length) throw new Error(JSON.stringify(errors))
  console.log(`${side}: live React entry renders with zero DRC errors`)
}
