import { MxHotswap } from "./MxHotswap"

export default () => (
  <board width="40mm" height="24mm" autorouter="auto-local" minTraceWidth="0.25mm">
    <MxHotswap name="S1" pcbX={-9} pcbY={0} layer="bottom" />
    <diode name="D1" footprint="sod123" pcbX={9} pcbY={0} layer="bottom" />
    <trace from=".S1 > .pin2" to=".D1 > .pin2" />
  </board>
)
