# Assembly quote preparation

The files in this directory describe candidate parts and factory requirements.
They do not authorize fabrication or establish that the hardware works.
The [reference comparison](reference-builds.md) shows which circuits match existing keyboards and which mechanics still need testing.

Generate the quote inventory after PCB generation and artwork:

```sh
nix develop . --command python3 scripts/generate_assembly.py
nix develop . --command python3 scripts/check_assembly_guards.py
```

Outputs appear under `build/manufacturing/quote-only/`.
Each half has a quote BOM, a quote CPL, and catalog evidence for every factory part.
Each half has 47 factory parts.
Each contains 21 bottom-face MX hotswap sockets and 21 bottom-face diodes.
Both inventories include two factory-soldered controller sockets, MCU1A and MCU1B.
The two nice!nano V2 modules and their four male header strips are purchased separately.

The CPL uses KiCad footprint origins, millimeters, X right, and Y up.
The PCB origin is 0,0, without a bottom-face coordinate mirror.
These origins are not validated pickup centers.
The assembler must check socket pickup offsets, diode polarity, connector pin one, and every rotation against its assembly preview.
No automatic rotation corrections are assumed.
The generator rejects missing sockets, unknown parts, wrong copper faces, and mismatched footprint families.

## Candidate parts

`parts.json` records the user-selected substitutions from the existing JLCPCB drafts on October 9, 2026.
Both live drafts passed stock checks and rendered placement review on October 9. Final production-file review remains required.
The MX socket is HanElectricity CPG151101S11-16, C41430893; its manufacturer and contact finish differ from the original Kailh part.
The power switch remains ALPS SSSS811101, C109335, rated 300 mA maximum.
The reset button is Panasonic EVQPUL02K, C79175, with bosses and 1.6 N actuation.
Its land pattern matches the original EVQPUC02K; the actuator must face the rear edge on both halves.
The JST PH connector remains a through-hole part. Standard assembly must cover both faces and through-hole parts.
The right JST1 ground pad connects directly to the ground pour; its soldering heat profile needs assembler review.

## Controller assembly requirements

Use one genuine nice!nano V2 per half, mounted face up beneath the carrier PCB.
The user permits limited soldering on these two modules.
JLCPCB must solder all four receiver socket strips onto the bottom faces of the carrier PCBs.
Receiver openings face down. The module header pins point up into them.
Keep the module face up; turning it over changes the pin mapping.
Each receiver is HCTL PM254-1-12-Z-3.0-C, C5156451. These are sockets, not controller modules.
The user provided drawing checks for tail fit in the existing 1 mm plated holes and 0.40–0.56 mm round mating pins.
Supplier-model pad and hole alignment was checked on both halves. Physical assembled fit remains unverified.
The existing `crysknife:MillMax_315_1x12` footprint name identifies retained geometry; it does not identify the ordered manufacturer.
The [controller comparison](controller-reference.json) checks all 24 contact positions and functions against the published nice!nano mapping.
MCU1 is the controller projection; MCU1A and MCU1B are physical receiver strips.
Keep both strips parallel, with openings facing away from the carrier.
Seat on the metal shoulders. Do not force shoulders into holes or press the plastic body flush.
Keep solder and flux out of the contacts. The supplied soldering limit is 260°C for 10 seconds.

Purchase two nice!nano V2 modules and four complete 12-pin round-pin header strips.
Mill-Max 350-10-112-00-006000 is the selected prototype mating header.
Its exact manufacturer drawing specifies 0.018 inch round pins on both ends.
With ±0.002 inch diameter tolerance, the 0.4064–0.508 mm pin range fits the receiver's 0.40–0.56 mm range.
The 2.54 mm pitch and 12-contact count match. See `header-fit.json` for drawing sources and arithmetic.
The 4.64 mm effective opening height plus 2.794 mm male insulator gives a 7.434 mm minimum stack.
Confirm insertion depth and full seating using sample parts before ordering the complete build.
The socket accepts 0.40–0.56 mm diameter round mating pins.
The ordinary square headers supplied with nice!nano are unsuitable for these machine sockets.
The [controller manufacturer explicitly documents this restriction](https://nicekeyboards.com/docs/nice-nano/getting-started/).
Do not substitute a header based only on 2.54 mm pitch.
Do not populate the extra B+ or B- holes beside USB; the carrier uses RAW and GND.

The user solders two complete strips to each module: 24 joints per half, 48 total.
A builder can prepare the modules instead; [beekeeb advertises custom soldering](https://shop.beekeeb.com/), but no quote is accepted.
Switch sockets, diodes, side power/reset controls, battery connectors, and receiver sockets remain factory-installed.
A separate builder may prepare the module headers. Leave BOOST OPEN on both modules.
Confirm the matched header orientation and use a fixture that prevents solder entering the receiver contacts.
Verify continuity, absence of shorts, and face-up pin mapping before fitting the modules.
Measure the resulting underside gap, USB height, and connector-latch access before cutting the case.
The model reserves an 8 mm underside controller gap. Full seating, USB cable clearance, and insulation need first-article measurements.

## Battery and factory acceptance

Each half needs a protected, single-cell 3.7 V rechargeable battery with the correct PH plug polarity.
The selected prototype SKU is Adafruit 2011: 2000 mAh, nominal 60 × 36 × 7 mm, with protection and a JST-PH plug.
The case reserves 64 × 40 × 8.5 mm below the key field.
Leave BOOST OPEN for nominal 100 mA charging. The battery path passes through a 300 mA-rated ALPS switch.
Do not enable the 500 mA setting. Bring up firmware and all matrix keys over USB before connecting the battery.
Verify actual lead length, cell dimensions, plug polarity, charging current, and retention before approval.
See `battery.json` and `physical-tests.md`.
The carrier's JST1 pin 1 is GND; pin 2 is BAT_P.
Confirm polarity with a meter before connecting a battery.
The power switch connects BAT_P to nice!nano RAW.
This arrangement requires the power switch on for battery charging through the controller.
USB can power the controller even when its battery switch is off.

Factory acceptance needs all 42 key positions tested without ghosting, both Bluetooth halves paired, and firmware reset/USB recovery checked.
It also needs battery charging, power-off behavior, and current measurements.
AOI and bare-PCB flying-probe tests alone cannot prove these behaviors.
Record the actual firmware revision, fixture, results, and serial identification for each supplied half.

`readiness.json` lists the open gates beside every generated quote inventory.
The pipeline does not produce an order release while these gates remain open.
