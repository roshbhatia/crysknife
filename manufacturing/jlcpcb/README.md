# JLCPCB review files

Each half has a Gerber/drill ZIP, BOM CSV, and component-placement CSV.
Use two separate board designs. Do not mirror or combine their assembly files.
Select 2-layer, 1.6 mm FR4, white solder mask, and black silkscreen on both faces.

Each carrier has 47 factory parts: 21 MX sockets, 21 diodes, two controller receiver strips, power/reset switches, and a battery connector.
This requires two-face SMT and through-hole assembly.
The nice!nano modules, batteries, and matching male headers are separate purchases.

The CSV positions use footprint origins. Pickup offsets and rotations still need assembler review.
Confirm diode cathodes, connector polarity, socket alignment, and the bottom battery connector in the assembly viewer.
Ask JLCPCB to approve all footprints against current manufacturer drawings.
Confirm C5504443 Mill-Max receiver sourcing and its solder process before accepting the quote.
The [part manifest](../parts.json) contains exact parts and catalog evidence.
The [header record](../header-fit.json) covers drawing fit; actual insertion and controller height remain untested.

Request acceptance of the 0.2 mm black artwork features without removing Frida's mouth or the title.
Request bare-board electrical testing, AOI, and assembly inspection.
Confirm stock, MOQ, consignment, pickup positions, rotations, and any substitutions for both halves.

Optional service: prepare two genuine nice!nano V2 modules with the four specified male strips and both BOOST bridges.
Otherwise, solder the 48 module header joints and two BOOST bridges before inserting the modules.
Test continuity, polarity, insertion, and charging current before fitting batteries.

KiCad ERC and routed DRC passed for the revision recorded in [validation.json](../../out/validation.json).
These checks do not establish factory acceptance or physical function.
Read `readiness.json` and the [prototype test plan](../physical-tests.md).
These files are for supplier review. No accepted quote or production order exists.
