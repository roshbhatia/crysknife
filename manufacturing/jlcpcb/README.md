# JLCPCB

Upload each half separately using its `*-gerbers.zip`, `*-bom.csv`, and `*-cpl.csv`.
Select 2-layer, 1.6 mm FR4, white solder mask, black silkscreen, and ENIG.
Use Standard PCBA on both sides for SMT and through-hole parts.
The board outline is approximately 144.862 × 103.224 mm; process rails add to the manufacturing envelope.

Each board has 47 factory parts across six component types.
The nice!nano controllers, male headers, and batteries are separate purchases.
[parts.json](../parts.json) contains the selected manufacturers and part codes.

## Placement

The CPL uses millimeters, X right, Y up, and PCB origin 0,0.
`placement-corrections.json` applies supplier-model offsets and angles to the native KiCad footprints.
Both faces of both halves were reviewed in JLC's viewer on October 9, 2026.
[placement.md](placement.md) describes the corrections; `placement-readback.json` records all 94 saved positions.

Check terminals, locating holes, and polarity in the assembly viewer after importing the files.
Diode cathodes connect to rows. JST1 pin 1 is GND; pin 2 is BAT_P.
Receiver openings face away from the carrier and seat on their metal shoulders.
Keep contacts free of solder and flux. Receiver soldering limit: 260°C for 10 seconds.
The right JST1 ground pad connects directly to the ground pour.

Enable production-file confirmation and disable automatic confirmation.
Keep the four finished M2 holes unchanged when adding tooling or fiducials.
Select bare-board electrical testing and assembly inspection.

See the [assembly guide](../README.md) for controller headers, battery polarity, and the 100 mA charging configuration.
[validation.json](../../out/validation.json) records KiCad ERC/DRC results and board hashes.
