# Marine Tracker V1 — Electrical Design Package

Status: Rev A architecture and connection specification. **Not released for fabrication.**

## Frozen architecture

- U1: SIMCom A7670SA, LTE Cat-1, intended OpenCPU host
- U2: Quectel LC29H-AA, L1/L5 dual-band GNSS
- No ESP32 and no external application MCU
- 1-cell protected Li-ion/LiPo battery
- USB-C charging/service
- External LTE and active dual-band GNSS antennas
- Four-layer controlled-impedance PCB

## Sheet structure for schematic capture

1. `POWER`: USB-C protection, BQ24074 power-path charger, battery/NTC, A7670 rail and low-noise GNSS rail
2. `CELLULAR`: A7670SA, PWRKEY/reset/status, UART/USB test access and LTE RF matching
3. `SIM`: nano-SIM, low-capacitance ESD and optional MFF2 eSIM pads
4. `GNSS`: LC29H-AA, UART/PPS level translation, reset, backup supply and active antenna bias/filter
5. `SERVICE`: LEDs (DNP for low-power build), test points and expansion header

## Fixed electrical decisions

- A7670 VBAT connects to the charger SYS/battery domain through a ferrite bead or 0-ohm current-rated link. Route for at least 3 A transient capability.
- Place 1000 uF low-ESR polymer, 100 uF, 10 uF and 100 nF at A7670 VBAT. Final values must be reconciled against the exact A7670SA hardware revision reference design.
- LC29H receives a dedicated low-noise 3.3 V rail from TPS7A2033. Do not share its decoupling path with the LTE modem.
- LC29H UART1 is the navigation interface; UART2 remains available at test pads for firmware/debug.
- LC29H D_SEL1/D_SEL2 receive explicit straps after confirming the UART selection truth table in the current module datasheet. They must not float.
- LC29H active antenna feed uses 68 nH bias inductance, 10-ohm short protection, 100 pF DC block and a C-L-C matching reservation.
- Reserve B39162B2651P810 dual-band GNSS SAW footprint immediately before LC29H RF_IN. Confirm insertion loss and availability before assembly.
- LTE and GNSS feeds are 50 ohm controlled impedance. Antennas must demonstrate at least 20 dB isolation in the final enclosure.
- USB D+/D- are 90-ohm differential, length matched, with ESD at the connector.

## Release blockers

1. Exact A7670SA OpenCPU hardware revision, SDK and pin-multiplex table
2. A7670SA official symbol/footprint cross-check
3. Enclosure outline, mounting holes and connector locations
4. Battery capacity, connector and NTC curve
5. LTE/GNSS antenna part numbers and cable lengths
6. Quectel/SIMCom design review
7. ERC, PCB DRC, impedance calculation, RF tuning and enclosure test

The files in this directory are deliberately marked Rev A. They document every required circuit and net, but fabrication outputs must not be generated until the release blockers are closed.

