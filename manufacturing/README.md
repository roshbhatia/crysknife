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
The left inventory has 45 parts; the right has 51.
Each contains 21 bottom-face MX hotswap sockets and 21 bottom-face diodes.
The right adds a ribbon connector, three resistors, and two capacitors.
The two controllers remain explicit external assembly requirements.

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

## Controller contact requirements

Both carrier footprints specify 24 plated holes at 0.85 mm nominal.
[Typeractive spring headers](https://typeractive.xyz/products/no-solder-spring-headers) require 0.8–0.9 mm finished holes and provide 5 mm height.
[JLCPCB standard PTH tolerance](https://jlcpcb.com/capabilities/pcb-capabilities/) permits 0.77–0.98 mm at this nominal diameter.
That range does not guarantee spring contact.
The listed ±0.05 mm press-fit option applies to multilayer ENIG boards.
The current two-layer board has no accepted precision-hole quote.

The assembly supplier needs to confirm one of these paths:

- Guarantee 0.80–0.90 mm finished diameter for the named MCU1 holes, with inspection evidence.
- Factory-install a verified controller connection and supply any separately prepared controller pins.

The second path can require footprint and case changes.
A bare nice!nano with loose ordinary headers does not meet the no-solder requirement.
The user must not need to solder pins or bridges.

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
