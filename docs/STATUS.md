# Marine Tracker RevB — Current Status

Version: RevB
Status Owner: Project Architecture
Last Updated: 2026-08-09

> This file is the single source of truth for current phase,
> current batch, progress, blockers, and next action.

## Current Phase

P4 — PCB Layout and Routing

RevB is the active hardware revision.
RevA is reference-only and MUST NOT be modified.

## Active Project

Project:
hardware/RevB/marine-tracker-RevB.kicad_pro

Schematic:
hardware/RevB/marine-tracker-RevB.kicad_sch

PCB:
hardware/RevB/marine-tracker-RevB.kicad_pcb

## Current Hardware

Main modem:
SIMCom A7670G-LABE

PCB:
4 layers
65 × 58 mm

Footprints:
108 schematic / 108 PCB
Component-count consistency CLOSED.

R22 and TP14–TP19 are intentionally absent from RevB.
Do not reopen this issue unless the schematic changes.

## Placement Status

RevB placement accepted.

U1 is the primary placement anchor.

U1 south routing corridor:
approximately 5.50 mm usable central corridor.

RF / GNSS placement strategy is accepted.

Do not repeat placement analysis unless routing reveals
a genuine structural blocker.

## Routing Status

Completed:

Batch 1 — POWER
- VBAT_MODEM — routed
- VSYS — routed

Batch 2 — CONTROLLED IMPEDANCE & RF
- RF_50 netclass applied (W = 0.32 mm, G = 0.25 mm)
- USB_90D netclass applied (W = 0.25 mm, S = 0.15 mm)
- CELL_ANT (LTE RF) — routed
- GNSS_ANT & RF_IN (GNSS RF) — routed
- USB_DP_CONN & USB_DM_CONN (USB 90-ohm pair) — routed

Batch 3 — SIM INTERFACE
- SIM_VDD — routed
- SIM_RST — routed
- SIM_CLK — routed
- SIM_DATA — routed
- SIM_DET — routed

Pending:

- Recovery / Control Routing
- Power distribution (Remaining power nets)
- UART / GNSS / low-speed signals
- Ground stitching / pours

## Current Fabrication Baseline

PCB manufacturer:
JLCPCB

Target:
4-layer controlled-impedance PCB (JLC04161H-7628)

Layer strategy:

L1 — Components / RF / high-current / signals
L2 — Solid uninterrupted GND reference
L3 — Power / slow signals
L4 — Slow signals / GND

Controlled-impedance parameters (JLCPCB JLC04161H-7628):
- L1-L2 dielectric: 0.21040 mm, Dk = 4.4
- Outer copper: 0.035 mm (1 oz)
- Inner copper: 0.0152 mm
- RF_50: 50.15 ohm (W = 0.320 mm, G = 0.250 mm)
- USB_90D: 90.42 ohm (W = 0.250 mm, S = 0.150 mm)

## Active Constraints

- KiCad modifications through approved KiCad GUI / Konnect MCP / IPC only.
- Direct Konnect MCP calls are preferred.
- Python MUST NOT orchestrate KiCad operations.
- No Python MCP wrappers/proxies.
- Do not modify RevA.
- Do not autoroute.
- Do not move accepted placement unless explicitly authorized.
- Do not modify unrelated nets.
- Do not repeatedly verify unchanged state.
- Do not commit or push unless explicitly authorized.

## Next Action

Start next routing batch:
Recovery / Control Routing

## Current Stop Condition

Awaiting approval to begin Recovery / Control Routing batch.