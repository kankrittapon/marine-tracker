# PCB Rev A specification

## Mechanical assumptions

- Board: 80.0 mm x 45.0 mm, rectangular, 2.0 mm corner radius target
- Thickness: 1.6 mm
- Copper: 1 oz outer and inner layers; request 2 oz outer only if modem transient/thermal validation requires it
- Mounting: four M2.5 NPTH holes, hole diameter 2.8 mm, centers 3.5 mm from edges
- External connectors: USB-C on south edge; battery on east edge; LTE and GNSS U.FL on north edge
- Nano-SIM accessible from east edge
- Components on top side by default; bottom side reserved for passives/test pads where RF rules permit

## Four-layer stack-up

| Layer | Use |
|---|---|
| L1 | Components, RF, USB, high-current power and signals |
| L2 | Uninterrupted solid ground reference |
| L3 | Power islands (VBAT_MODEM, VSYS, GNSS_3V3) and slow signals |
| L4 | Slow signals and ground pour |

The fabricator must supply final dielectric values and calculate 50-ohm single-ended RF and 90-ohm differential USB geometry. Do not copy trace widths from another stack-up.

## Floorplan zones

- North-west: LTE antenna connector, pi network and A7670G-LABE. Keep the LTE feed short.
- North-east: GNSS connector, active antenna bias, SAW filter and LC29H-AA in a shieldable quiet zone.
- East-center: nano-SIM with ESD beside A7670.
- South-west: USB-C, USB ESD and charger.
- South-center: battery/power-path and modem bulk capacitance.
- South-east: low-noise GNSS LDO and service/test header.

## Mandatory clearance/keep-outs

- No switcher, USB pair or digital clock in the GNSS quiet zone.
- No copper-plane split beneath LTE/GNSS feeds or USB differential pair.
- Maintain 3 mm service clearance around LC29H.
- Keep U.FL ground pads tied to L2 with multiple adjacent vias.
- Separate LTE and GNSS antennas in the enclosure until measured isolation is >=20 dB.
- Place GNSS SAW/filter and RF ESD immediately adjacent to LC29H RF_IN/connector path.
- Put modem bulk capacitance within the shortest practical path of all VBAT pins.

## Preliminary net classes

| Class | Rule |
|---|---|
| RF_50 | Geometry supplied by board house; minimal vias; clearance >= 0.25 mm |
| USB_90D | 90-ohm differential; pair gap/width from stack-up; skew < 0.5 mm |
| MODEM_PWR | Width/plane sized for 3 A transient; use via arrays for layer changes |
| POWER | >=0.30 mm unless calculated otherwise |
| SIGNAL | 0.15 mm minimum for prototype |

## Fabrication hold points

- Replace conceptual A7670 and LC29H courtyards with manufacturer-released footprints.
- Confirm A7670G-LABE OpenCPU pin mapping and all multiplexed pins.
- Review antenna connector choice against final cable assembly (U.FL vs MHF4 vs SMA pigtail).
- Confirm enclosure, connector heights and battery location.
- Run ERC/DRC in installed KiCad and obtain vendor design review.

