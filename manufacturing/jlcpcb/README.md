# JLCPCB review files

Each half has a Gerber/drill ZIP, BOM CSV, and component-placement CSV.
Use two separate board designs. Do not mirror or combine their assembly files.
Select 2-layer, 1.6 mm FR4, white solder mask, and black silkscreen on both faces.

Each carrier has 47 factory parts: 21 MX sockets, 21 diodes, two controller receiver strips, power/reset switches, and a battery connector.
Use [Standard PCB Assembly](https://jlcpcb.com/help/article/pcb-assembly-faqs) for two-face SMT and through-hole assembly.
The nice!nano modules, batteries, and matching male headers are separate purchases.

The CSV positions use the selected JLC supplier model origins and rotations.
The generator applies the rules in `placement-corrections.json`; native KiCad footprints remain unchanged.
Both rendered previews were checked on 2026-10-09. See [prototype changes](prototype-changes.md).
JLC production-file review and physical tests remain required.
Confirm diode cathodes, connector polarity, socket alignment, and the bottom battery connector in the assembly viewer.
Ask JLCPCB to approve all footprints against current manufacturer drawings.
Confirm C5156451 HCTL receiver sourcing and its solder process before accepting the quote.
The [part manifest](../parts.json) contains exact parts and catalog evidence.
The [header record](../header-fit.json) covers drawing fit; actual insertion and controller height remain untested.

Request acceptance of the 0.2 mm black artwork features without removing the knife illustration or the title.
Confirm tooling and fiducial placement with JLCPCB. Keep the four finished M2 mounting holes unchanged.
Request bare-board electrical testing, AOI, and assembly inspection.
Confirm stock, MOQ, consignment, pickup positions, rotations, and any substitutions for both halves.

Prepare two genuine nice!nano V2 modules with four specified male strips: 48 solder joints total.
Leave both BOOST bridges OPEN for nominal 100 mA charging. The power switch is rated 300 mA maximum.
Test continuity, polarity, insertion, and charging current before fitting batteries.

KiCad ERC and routed DRC passed for the revision recorded in [validation.json](../../out/validation.json).
These checks do not establish factory acceptance or physical function.
Read `readiness.json` and the [prototype test plan](../physical-tests.md).
These files are for supplier review. No accepted quote or production order exists.

Receiver strips must seat on their metal shoulders, with openings facing away from the carrier.
Do not force shoulders into plated holes or the plastic housing flush. Keep contacts free of solder and flux.
Receiver soldering limit: 260°C for 10 seconds. Verify JST1 pin 1 is GND and pin 2 is BAT_P.
