# Assembly quote preparation

The files in this directory describe candidate parts and factory requirements.
They do not authorize fabrication or establish that the hardware works.

Generate the quote inventory after PCB generation and artwork:

```sh
nix develop . --command python3 scripts/generate_assembly.py
nix develop . --command python3 scripts/check_assembly_guards.py
```

Outputs appear under `build/manufacturing/quote-only/`.
Each half has a quote BOM, a quote CPL, and catalog evidence for every factory part.
The left inventory has 47 parts; the right has 53.
Each contains 21 bottom-face MX hotswap sockets and 21 bottom-face diodes.
The right adds a ribbon connector, three resistors, and two capacitors.
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

Use one genuine nice!nano V2 per half, mounted face up.
The user permits limited soldering on these two modules.
JLCPCB must solder all four receiver socket strips onto the carrier PCBs.
Each socket is Mill-Max 315-43-112-41-003000, [JLCPCB C5504443](https://jlcpcb.com/partdetail/6420580-315_43_112_41003000/C5504443).
Catalog presence does not guarantee stock; pre-order or consignment acceptance remains required.
The socket footprint retains the original controller contact positions and net numbers.
MCU1 is the controller outline; MCU1A and MCU1B are the physical socket references.
The CPL uses the center of each 12-pin strip, rather than the controller center.

The [manufacturer socket drawing](https://static6.arrow.com/aropdfconversion/2e225be7d9212620894362dafa7ce735623fe9ca/315-43-112-41-003000.pdf) specifies 2.54 mm pitch and a 0.762 mm solder tail.
Its standard ±0.051 mm diameter tolerance gives a maximum 0.813 mm tail.
[JLCPCB standard PTH tolerance](https://jlcpcb.com/capabilities/pcb-capabilities/) gives a minimum 0.92 mm hole at the selected 1 mm nominal diameter.
The socket tail can enter that hole; solder establishes electrical contact.
The removable contact is inside the manufactured socket, so it does not depend on a spring pin gripping the carrier hole.
Supplier land-pattern approval, soldering, alignment, and insertion tests remain required.

Purchase two nice!nano V2 modules and four complete 12-pin round-pin header strips.
Mill-Max 350-10-112-00-006000 is the mating-header candidate; compare its current drawing and insertion depth before purchase.
The socket accepts 0.381–0.559 mm diameter mating pins.
The ordinary square headers supplied with nice!nano are unsuitable for these machine sockets.
The [controller manufacturer explicitly documents this restriction](https://nicekeyboards.com/docs/nice-nano/getting-started/).
Do not substitute a header based only on 2.54 mm pitch.
Do not populate the extra B+ or B- holes beside USB; the carrier uses RAW and GND.

The user solders two complete strips to each module: 24 joints per half, 48 total.
A builder can prepare the modules instead; [beekeeb advertises custom soldering](https://shop.beekeeb.com/), but no quote is accepted.
Switch sockets, diodes, side power/reset controls, battery connectors, and TrackPoint support components remain factory-installed.
The TrackPoint must still arrive with its connector prepared; user soldering is limited to the controller headers.
Confirm the matched header orientation and use a fixture that prevents solder entering the receiver contacts.
Verify continuity, absence of shorts, and face-up pin mapping before fitting the modules.
Measure the resulting underside gap, USB height, and connector-latch access before cutting the case.
The current 5 mm controller gap is a mechanical reservation, not a verified mating-stack dimension.

## Prepared TrackPoint requirements

The candidate is Sprintek SK8707-01-005 at 3.3 V, with the method-3 bottom ribbon connector installed by the supplier.
The [manufacturer datasheet](https://docs.holykeebs.com/datasheets/SK8707-01.pdf) says the connector is optional and not installed by default.
The module must arrive with its matching cable and connector already prepared.
The cable must map pin 1 to pin 1 through pin 8 to pin 8.
Contact-side orientation and latch fit must be confirmed for both installed connectors.
The keyboard connector is Hirose FH12-8S-1SH(55): eight contacts, 1 mm pitch, 0.3 mm ribbon thickness.
The current engineering drawing and the assembled connector orientation remain supplier review items.

| Pin | Signal | Carrier connection |
| --- | --- | --- |
| 1 | DATA | nice!nano P2; 4.7 kΩ pull-up to VCC |
| 2 | RST | nice!nano P4; active high; 10 kΩ and 100 nF to GND |
| 3 | MIDDLE | Unconnected; mouse buttons use the keyboard keymap |
| 4 | RIGHT | Unconnected |
| 5 | LEFT | Unconnected |
| 6 | CLK | nice!nano P3; 4.7 kΩ pull-up to VCC |
| 7 | GND | GND |
| 8 | VCC | nice!nano switched 3.3 V output; 100 nF local decoupling |

The socketed nice!nano sits above the interface components.
The user plugs in the ribbon before seating the controller.
The proposed pinout is checked against generated PCB pads and firmware source.
The cable and module must pass a physical continuity and powered communication test.
Stem placement, mount, keycap travel, and gasket travel remain open.

## Battery and factory acceptance

Each half needs a protected, single-cell 3.7 V rechargeable battery with the correct PH plug polarity.
The exact SKU, charging rating, lead length, and retention remain unselected.
A 301230 cell reserves 3 × 12 × 30 mm; this is a fit candidate, not an approved battery specification.
The carrier's JST1 pin 1 is GND; pin 2 is BAT_P.
Confirm polarity with a meter before connecting a battery.
The power switch connects BAT_P to nice!nano RAW.
This arrangement requires the power switch on for battery charging through the controller.
USB can power the controller even when its battery switch is off.

Factory acceptance needs all 42 key positions tested without ghosting, both Bluetooth halves paired, and firmware reset/USB recovery checked.
It also needs TrackPoint motion, click/scroll layers, battery charging, power-off behavior, and current measurements.
AOI and bare-PCB flying-probe tests alone cannot prove these behaviors.
Record the actual firmware revision, fixture, results, and serial identification for each supplied half.

`readiness.json` lists the open gates beside every generated quote inventory.
The pipeline does not produce an order release while these gates remain open.
