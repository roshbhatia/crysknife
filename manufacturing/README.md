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

`parts.json` binds references to exact catalog parts and sources checked on 2026-10-08.
Catalog presence does not establish stock, footprint approval, or factory acceptance.
The MX candidate is CPG151101S11-1, C5184526.
The selected socket and its exact variant drawing still need comparison with the original Ergogen land pattern.
The side power switch is ALPS SSSS811101, C109335.
The side reset button is Panasonic EVQPUC02K, C79174, including its two locating bosses.
The JST PH connector is a through-hole part, not a pick-and-place-only SMT part.
Standard assembly must cover both faces and the through-hole connector.
The right JST1 ground pad connects directly to the ground pour; its soldering heat profile needs assembler review.

## Controller assembly requirements

Use one genuine nice!nano V2 per half, mounted face up beneath the carrier PCB.
The user permits limited soldering on these two modules.
JLCPCB must solder all four receiver socket strips onto the bottom faces of the carrier PCBs.
Receiver openings face down. The module header pins point up into them.
Keep the module face up; turning it over changes the pin mapping.
Each socket is Mill-Max 315-43-112-41-003000, [JLCPCB C5504443](https://jlcpcb.com/partdetail/6420580-315_43_112_41003000/C5504443).
Catalog presence does not guarantee stock; pre-order or consignment acceptance remains required.
The socket footprint retains the original controller contact positions and net numbers.
The [independent controller comparison](controller-reference.json) checks all 24 positions against the pinned bstiq library and compiled ZMK GPIO map.
The libraries use different pad numbers; the comparison uses physical positions and pin functions.
The upstream 3D model represents a Pro Micro and does not establish nice!nano V2 fit.
MCU1 is the controller outline; MCU1A and MCU1B are the physical socket references.
The CPL uses the center of each 12-pin strip, rather than the controller center.

The [manufacturer socket drawing](https://static6.arrow.com/aropdfconversion/2e225be7d9212620894362dafa7ce735623fe9ca/315-43-112-41-003000.pdf) specifies 2.54 mm pitch and a 0.762 mm solder tail.
Its standard ±0.051 mm diameter tolerance gives a maximum 0.813 mm tail.
[JLCPCB standard PTH tolerance](https://jlcpcb.com/capabilities/pcb-capabilities/) gives a minimum 0.92 mm hole at the selected 1 mm nominal diameter.
The socket tail can enter that hole; solder establishes electrical contact.
The removable contact is inside the manufactured socket, so it does not depend on a spring pin gripping the carrier hole.
Supplier land-pattern approval, soldering, alignment, and insertion tests remain required.

Purchase two nice!nano V2 modules and four complete 12-pin round-pin header strips.
Mill-Max 350-10-112-00-006000 is the selected prototype mating header.
Its exact manufacturer drawing specifies 0.018 inch round pins on both ends.
With ±0.002 inch diameter tolerance, the 0.4064–0.508 mm pin range fits the receiver's 0.381–0.5588 mm range.
The 2.54 mm pitch and 12-contact count match. See `header-fit.json` for drawing sources and arithmetic.
The 4.5974 mm insulator sum is only a lower bound on the assembled controller gap.
Confirm insertion depth and full seating using sample parts before ordering the complete build.
The socket accepts 0.381–0.559 mm diameter mating pins.
The ordinary square headers supplied with nice!nano are unsuitable for these machine sockets.
The [controller manufacturer explicitly documents this restriction](https://nicekeyboards.com/docs/nice-nano/getting-started/).
Do not substitute a header based only on 2.54 mm pitch.
Do not populate the extra B+ or B- holes beside USB; the carrier uses RAW and GND.

The user solders two complete strips to each module: 24 joints per half, 48 total.
A builder can prepare the modules instead; [beekeeb advertises custom soldering](https://shop.beekeeb.com/), but no quote is accepted.
Switch sockets, diodes, side power/reset controls, battery connectors, and receiver sockets remain factory-installed.
Ask the assembler to prepare supplied nice!nano modules and their BOOST bridges where it supports this service.
Confirm the matched header orientation and use a fixture that prevents solder entering the receiver contacts.
Verify continuity, absence of shorts, and face-up pin mapping before fitting the modules.
Measure the resulting underside gap, USB height, and connector-latch access before cutting the case.
The current 5 mm controller gap is a mechanical reservation, not a verified mating-stack dimension.

## Battery and factory acceptance

Each half needs a protected, single-cell 3.7 V rechargeable battery with the correct PH plug polarity.
The selected prototype SKU is Adafruit 2011: 2000 mAh, nominal 60 × 36 × 7 mm, with protection and a JST-PH plug.
The case reserves 64 × 40 × 8.5 mm below the key field.
Use the nice!nano 500 mA BOOST setting, within its published 2000 mAh guidance.
This requires one additional solder bridge per module unless a supplier prepares it.
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
