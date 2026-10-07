import { type ChipProps } from "tscircuit"
export const MxHotswap = (props: ChipProps) => (
  <chip
    footprint={<footprint>
        <hole pcbX="0mm" pcbY="0mm" diameter="4.1mm" />
<hole pcbX="5.08mm" pcbY="0mm" diameter="1.9mm" />
<hole pcbX="-5.08mm" pcbY="0mm" diameter="1.9mm" />
<hole pcbX="2.54mm" pcbY="5.08mm" diameter="3mm" />
<hole pcbX="-3.81mm" pcbY="2.54mm" diameter="3mm" />
<smtpad portHints={["1"]} pcbX="-7.085mm" pcbY="2.54mm" layer="bottom" width="2.55mm" height="2.5mm" shape="rect" />
<smtpad portHints={["2"]} pcbX="5.842mm" pcbY="5.08mm" layer="bottom" width="2.55mm" height="2.5mm" shape="rect" />
<silkscreenpath route={[{"x":-3.6,"y":6.5},{"x":-3.8,"y":6.5},{"x":-4.1,"y":6.45},{"x":-4.4,"y":6.35},{"x":-4.6,"y":6.25},{"x":-4.75,"y":6.15},{"x":-4.95,"y":6},{"x":-5.1,"y":5.85},{"x":-5.25,"y":5.65},{"x":-5.4,"y":5.4},{"x":-5.5,"y":5},{"x":-5.5,"y":4.6},{"x":-5.35,"y":4.5},{"x":-5.2,"y":4.4},{"x":-4.75,"y":4.65},{"x":-4.5,"y":4.75},{"x":-4.05,"y":4.85},{"x":-3.55,"y":4.85},{"x":-2.95,"y":4.7},{"x":-2.45,"y":4.4},{"x":-2.15,"y":4.15},{"x":-1.75,"y":3.6},{"x":-1.55,"y":3.05},{"x":-1.5,"y":2.6},{"x":-1.25,"y":2.8},{"x":-0.9,"y":2.9},{"x":-0.4,"y":2.95},{"x":1.65,"y":2.95},{"x":1.2,"y":3.2},{"x":0.95,"y":3.4},{"x":0.65,"y":3.75},{"x":0.5,"y":4},{"x":0.35,"y":4.35},{"x":0.25,"y":4.75},{"x":0.25,"y":5.05},{"x":0.25,"y":5.4},{"x":0.3,"y":5.65},{"x":0.45,"y":6.05},{"x":0.75,"y":6.5}]} strokeWidth={0.4} layer="bottom" />
      </footprint>}
    {...props}
  />
)