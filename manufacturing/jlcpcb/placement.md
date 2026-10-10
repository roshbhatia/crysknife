# Supplier placement

`placement-corrections.json` defines supplier-specific origins and angles. The generator applies them to the unchanged KiCad footprints.
Socket pickup origins move to the midpoint of the two solder pads. Local translation is −0.6215 mm X, +3.81 mm Y.
That translation rotates with each native footprint, including the thumb keys. Socket supplier angles are `(180 - native_angle) % 360`. This includes bottom-side mirroring and the corrected body orientation.
Diodes and receivers also need supplier angle changes. Power switches rotate 90 degrees; reset switches rotate 180 degrees.
JST connectors retain their native positions. These rules apply only to the selected supplier models.

The [socket manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/d953a8b0b623247f3341ebcfbaa2e88f.pdf?productCode=C41430893) specifies 6.35 mm horizontal and 2.54 mm vertical opening spacing.
Those dimensions match the native footprint. The [diode drawing](https://datasheet.lcsc.com/datasheet/pdf/8abd7fc00ebe41ffb03ad1383c10753b.pdf?productCode=C81598) identifies the band as cathode/pin 1.
All 42 native cathode pads connect to rows; anode pads connect to the corresponding switch nets.
Rendered cathode bands match those pads, including all four angled diodes. Diode rotations remain unchanged.

Both faces of both halves were checked in the JLC viewer on October 9, 2026.
Checks covered terminals, locating holes, receiver rows, diode cathodes, and side switch actuators, including angled thumb components.
All 94 saved placements match the generated CPL within 0.0015 mm, including layer, part code, position, and angle.
`placement-readback.json` stores the saved positions.
These corrections change assembly exports; native PCB pads, copper, schematic, and controller orientation stay unchanged.
