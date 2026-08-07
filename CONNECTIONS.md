# Rev A connection specification

## Power and charging

| Net | Source | Loads | Protection/filtering |
|---|---|---|---|
| USB_5V_RAW | J1 USB-C VBUS | F1 | USB TVS at J1 |
| USB_5V_FUSED | F1 | U3 BQ24074 IN | 4.7 uF + 100 nF |
| BAT+ | J2 protected 1S cell | U3 BAT | cell NTC required |
| VSYS | U3 OUT | A7670 rail, U4 input | 100 uF bulk |
| VBAT_MODEM | FB1/0R from VSYS | U1 VBAT pins | 1000 uF + 100 uF + 10 uF + 100 nF close to U1 |
| GNSS_3V3 | U4 TPS7A2033 | U2 VCC | 10 uF input/output + 100 nF close to U2 |
| GNSS_BCKP | GNSS_3V3 through 0R | U2 pin 22 V_BCKP | optional supercap circuit DNP |

BQ24074 preliminary settings: ISET sized for 1.0 A charge, ILIM sized for USB source policy, TS connected to the pack NTC. Exact resistor values depend on the selected battery and thermal test.

## LC29H-AA verified pins

| Pin | Signal | Rev A connection |
|---:|---|---|
| 5 | D_SEL1 | configuration strap; value pending current truth table |
| 6 | D_SEL2 | configuration strap; value pending current truth table |
| 7 | VDD_EXT 2.8 V output | level-shifter reference and test point only |
| 8 | RESET_N | open-drain reset from A7670 GPIO plus test pad |
| 11 | RF_IN | GNSS SAW/matching/DC block to J4 |
| 14 | ANT_ON | active-antenna PMOS/NPN control |
| 15 | TXD2 | GNSS debug test pad |
| 16 | RXD2 | GNSS debug test pad through protected header |
| 18 | I2C_SDA/SPI_CS | leave accessible; DNP pull-up |
| 19 | I2C_SCL/SPI_CLK | leave accessible; DNP pull-up |
| 20 | TXD1 | UART level shifter to A7670 GNSS_RX |
| 21 | RXD1 | UART level shifter from A7670 GNSS_TX |
| 22 | V_BCKP | GNSS_BCKP |
| 23 | VCC | GNSS_3V3 |
| 24 | GND | solid ground plane |

All other GND pins connect directly to the uninterrupted L2 ground plane. Reserved pins are no-connect unless a newer Quectel document explicitly states otherwise.

## A7670SA interface allocation

The following are **logical nets**, not frozen pin numbers. Pin numbers remain a release blocker until the exact OpenCPU hardware manual is obtained.

| Logical function | Connection |
|---|---|
| VBAT[3] | VBAT_MODEM |
| GND | solid ground and thermal via array |
| RF_MAIN | pi match + low-cap ESD + J3 LTE antenna |
| SIM_VDD/DATA/CLK/RST/DET | J5 nano-SIM through ESD array |
| USB_DP/USB_DM | J1 through USB ESD and optional common-mode choke footprint |
| PWRKEY | pushbutton/test pad and power-on RC/open-drain circuit |
| RESET_N | test pad; never driven push-pull high |
| UART_GNSS_TX/RX | bidirectional level translation to U2 UART1 |
| GPIO_GNSS_RESET | open-drain transistor to U2 RESET_N |
| GPIO_WATCHDOG | watchdog/service test point |
| ADC_BAT | switched battery divider |
| STATUS/NETLIGHT | test pads; LEDs DNP in low-power build |

## RF constraints

- J3 LTE and J4 GNSS are U.FL/MHF1.
- Place U2, GNSS SAW and J4 in one shieldable quiet zone.
- No switch-mode converter, USB pair or high-speed clock under/adjacent to the GNSS zone.
- L2 must remain solid beneath both RF feeds; no power-plane split crossing.
- Obtain the 50-ohm geometry from the PCB fabricator's actual four-layer stack-up.
- Tune matching in the final sealed enclosure with battery and production antenna cables installed.

