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

## Approved Recovery / Control Netclass

Netclass:
CONTROL

Approved routing geometry:
- Trace width: 0.20 mm
- Clearance: 0.20 mm
- Via diameter: 0.60 mm
- Via drill: 0.30 mm

Authorized nets only:
- PWRKEY
- MODEM_RESET_N
- SUPV_TRIG
- WDT_RST_TRIG
- WDT_DONE
- WDT_WAKE
- WDT_DELAY

Applicability:
- Low-speed Recovery / Control signals only.
- Does not apply to RF, USB, power, SIM, or other protected nets.
- Values exceed the selected JLCPCB fabrication minima while remaining
  appropriate for the dense RevB recovery-routing area.

Implementation state:
- Engineering approval: APPROVED
- KiCad netclass creation: BLOCKED — the currently exposed native Konnect
  `create_netclass` tool directly rewrites `.kicad_pcb` instead of using KiCad
  IPC.
- Seven-net assignment: BLOCKED — the currently exposed native Konnect
  `assign_net_to_class` tool directly rewrites `.kicad_pcb` instead of using
  KiCad IPC.
- Do not create or assign CONTROL through those handlers under the current
  engineering rulebook.

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

## Recovery / Control Authorization

Recovery / Control Route Planning: AUTHORIZED

Recovery / Control Write Routing: HARD STOP — ZONE REFILL VALIDATION ONLY

## Recovery / Control — Limited Placement Correction

Status: COMPLETED AND VALIDATED

Placement checkpoint:

1. R21
   - Final center: (2.050, 47.500).
   - Final rotation: 90 degrees.
   - R21.1 / WDT_DELAY: (2.050, 48.010).
   - R21.2 / GND: (2.050, 46.990).
   - Live placement validation: PASS.
   - New Level A violations introduced: NO.

2. R34
   - Final center: (38.000, 38.700).
   - Final rotation: 0 degrees.
   - R34.1 / WDT_RST_TRIG: (37.490, 38.700).
   - R34.2 / VSYS: (38.510, 38.700).
   - Live placement validation: PASS.
   - New Level A violations introduced: NO.

Protected routing was unchanged. No routing or vias were created during the
placement correction.

## Recovery / Control — WDT Write Routing Batch 1

Status: HARD STOP AFTER WDT_DELAY WRITE

Current written WDT_DELAY state:

- Three WDT_DELAY through vias are present and correctly assigned.
- Via diameter: 0.60 mm.
- Via drill: 0.30 mm.
- WDT_DELAY connectivity is complete.
- No WDT_DELAY signal trace exists on In1.Cu.
- Post-write DRC introduced three In1.Cu GND filled-zone clearance violations
  and three hole-clearance violations.
- Read-only diagnosis found the existing In1.Cu GND fill predates the new vias
  and stale fill is the likely root cause.

Original batch order, currently suspended:

1. WDT_DELAY
2. WDT_RST_TRIG

No CONTROL net is currently authorized for additional write routing.

Required CONTROL geometry:

- Trace width: 0.20 mm.
- Clearance: 0.20 mm.
- Via diameter: 0.60 mm.
- Via drill: 0.30 mm.

Layer policy:

- F.Cu: endpoint and local escape only.
- In1.Cu: GND plane only; CONTROL traces are prohibited.
- In2.Cu: preferred CONTROL trunk layer.
- B.Cu: only if required and positively verified.

Mandatory write procedure for each authorized net:

1. Re-query live geometry before writing.
2. Re-run trace-clearance checks on the final candidate.
3. Re-run every via-site preflight.
4. Route one net at a time.
5. Save after each completed net.
6. Re-query the written copper.
7. Run DRC after each net.
8. Distinguish pre-existing baseline findings from findings caused by the
   current routing.
9. Treat any new Level A violation as a hard stop.

WDT_RST_TRIG and all additional CONTROL write routing are NOT AUTHORIZED while
this hard stop is active.

Explicitly not authorized:

- Write routing PWRKEY, MODEM_RESET_N, SUPV_TRIG, WDT_DONE, or WDT_WAKE.
- Moving components.
- Modifying VSYS, USB, SIM, RF, zones, stackup, or netclasses.
- Modifying the schematic.
- Unrelated DRC cleanup.
- Accessing or modifying RevA.
- Commit or push.

Post-batch gate:

- After WDT_DELAY and WDT_RST_TRIG are routed and validated, stop.
- Do not proceed automatically to the remaining five CONTROL nets.
- The validated written WDT copper becomes the live-board geometry baseline
  for the next route-planning phase.

## WDT_DELAY — Control Zone Refill Validation

Status: AUTHORIZED

Purpose:
Regenerate the existing In1.Cu GND filled copper so KiCad creates normal
antipads around the three already-written WDT_DELAY vias.

Authorized operations only:

- Run native KiCad IPC `refill_zones`.
- Save through the approved native KiCad / Konnect IPC path after refill.
- Run DRC after refill.
- Perform read-only geometry and connectivity inspection.

This authorization does not permit:

- Changing the zone outline, net, clearance, priority, or any zone setting.
- Deleting or recreating the zone.
- Adding or removing vias or traces.
- Routing WDT_RST_TRIG or any other CONTROL net.
- Moving components.
- Modifying protected routing, stackup, netclasses, or the schematic.
- Unrelated DRC cleanup.
- Commit or push.

Post-refill gate:

- Retest all six newly introduced WDT_DELAY via/zone-related errors.
- Success requires all three new zone-clearance violations and all three new
  hole-clearance violations to disappear.
- No new Level A violation may be introduced.
- WDT_DELAY connectivity must remain complete.
- The In1.Cu GND zone outline and settings must remain unchanged.
- If any of the six errors remain, the hard stop remains active and no further
  routing may proceed.

## WDT_DELAY — Verified Closure (Geometric DRC Audit)

Status: WRITE-PASS YES — HARD STOP CLEARED

Verified current state:

- Routed: YES.
- Connectivity complete: YES (U8.3 / R21.1 / R23.1, confirmed live via
  `query_traces` and `get_net_pads`).
- Trace width: 0.20 mm.
- Vias: 3.
- Via geometry: 0.60 / 0.30 mm.
- In1.Cu signal routing introduced: NO (In1.Cu remains GND-only).
- Stale In1.Cu GND-zone fill was corrected using native `refill_zones`.
- The six stale-fill via/zone findings (3 zone-clearance, 3 hole-clearance)
  remain absent after refill.
- A fresh geometric DRC audit found no WDT_DELAY-attributable Level-A
  finding: no current violation coincides with WDT_DELAY via bodies, trace
  centerlines, or endpoint pad geometry.
- WDT_DELAY WRITE-PASS: YES.
- WDT_DELAY hard stop: CLEARED.

Attribution method note:

The currently active DRC interface does NOT expose the rich
KIID / resolved-net / resolved-layer / footprint-pad attribution that a
prior task expected. Violations return only type, severity, message text,
and an (x, y) location. The WDT_DELAY pass above was therefore established
by cross-referencing live WDT_DELAY geometry (vias, trace segments, endpoint
pads queried directly from the board) against DRC violation coordinates,
not by native per-violation net/KIID resolution.

Aggregate DRC count note:

Two consecutive read-only DRC queries with no PCB change between them
returned different totals (428 vs. 427; all variance confined to
`shorting_items` / `tracks_crossing` / `clearance` counts, none near
WDT_DELAY geometry). Aggregate DRC error/warning counts have demonstrated
run-to-run variance independent of PCB modification and must not alone be
used to attribute a new violation to a specific net or write.

## WDT_RST_TRIG — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

History (superseded — kept for traceability only, not current
authorization): this net was originally opened for read-only planning
under WDT_DELAY closure, then given a limited write authorization gated on
a passing live re-preflight immediately before write. Both steps completed
and are now closed out below.

Verified closure:

- Native Konnect preflight (get_routing_geometry, check_route_clearance,
  check_via_clearance) passed for all 6 trace segments and both vias
  immediately before write.
- Route was written through approved native Konnect/KiCad IPC tooling only
  (route_trace, add_via) — no direct file editing.
- The In1.Cu GND zone was refilled through native `refill_zones` after
  writing, as required for antipad regeneration around the two new vias.
- Board was saved through native Konnect/KiCad IPC.
- Post-write DRC was executed (213 errors / 214 warnings, 427 total —
  matching the pre-existing baseline; no delta attributable to this write).
- An independent, separate post-write checkpoint task re-verified the live
  board from scratch and returned CHECKPOINT-PASS = YES.
- All three endpoints are connected: U8.6, R34.1, U10.3, all live net
  WDT_RST_TRIG.
- Expected route geometry is present and matches the final written route
  below exactly.
- No new WDT_RST_TRIG-route-attributable Level-A DRC violation exists. The
  only DRC findings touching WDT_RST_TRIG, R34, or U10 are pre-existing,
  placement-driven items (R34/U10 courtyard overlap; cosmetic
  silk-over-copper between R34's pads and U10's silkscreen) tied to
  component positions that were never changed by this routing work.
- Protected routing (VBAT_MODEM, VSYS, LTE RF, GNSS RF, USB pair, SIM)
  remained unchanged.
- R34.2 / VSYS remained unchanged and unconnected to WDT_RST_TRIG.
- No In1.Cu signal routing was introduced; In1.Cu remains GND-only, with
  antipads at the two new through-via crossings.
- No unrelated component movement occurred; R34, U10, and U8 positions are
  unchanged from the accepted placement checkpoint.

Final written route (authoritative reference for future work):

- U8.6 (1.050, 35.3625) --F.Cu--> Via A (1.050, 33.300)
- Via A (1.050, 33.300) --In2.Cu--> Via B (35.200, 40.200)
- Via B (35.200, 40.200) --F.Cu--> (35.200, 38.700) --F.Cu--> R34.1 (37.490, 38.700)
- Via B (35.200, 40.200) --F.Cu--> (35.200, 41.450) --F.Cu--> U10.3 (36.8625, 41.450)

Final route geometry:

- Trace width: 0.20 mm
- Clearance target: 0.20 mm
- Via diameter / drill: 0.60 / 0.30 mm
- Via count: 2 (Via A, Via B — both through vias, F.Cu/In1.Cu/In2.Cu/B.Cu)
- Trace segment count: 6
- Approximate total route length: 43.61 mm
- Signal layers: F.Cu + In2.Cu only
- In1.Cu signal routing: NONE (In1.Cu remains GND plane with antipads at
  the two through-via crossings)

Placement checkpoint referenced (unchanged by this routing work):

- R34 center: (38.000, 38.700), rotation 0°.
- R34.2: VSYS.

This closure does not authorize WDT_DONE, WDT_WAKE, SUPV_TRIG, PWRKEY,
MODEM_RESET_N, or any other CONTROL net. Any further Recovery/Control net
requires its own separate planning and write authorization.

## Current Stop Condition

WDT_DELAY: CLOSED — WRITE-PASS VERIFIED. Hard stop cleared.

WDT_RST_TRIG: CLOSED — WRITE-PASS VERIFIED. Hard stop cleared.

All other Recovery / Control routing (PWRKEY, MODEM_RESET_N, SUPV_TRIG,
WDT_DONE, WDT_WAKE) remains not authorized for write. No read-only planning
authorization beyond what was already established elsewhere in this
document is granted or expanded by this closure.
