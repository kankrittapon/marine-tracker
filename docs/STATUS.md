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

This closure does not authorize WDT_WAKE, SUPV_TRIG, PWRKEY,
MODEM_RESET_N, or any other CONTROL net. Any further Recovery/Control net
requires its own separate planning and write authorization.

## WDT_DONE — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

History: this net was planned under PromptID 041 and written under PromptID 042.

Verified closure:

- Native Konnect preflight (get_routing_geometry, check_route_clearance,
  check_via_clearance) passed for all 4 trace segments and both vias
  immediately before write.
- Route was written through approved native Konnect/KiCad IPC tooling only
  (route_trace, add_via) — no direct file editing.
- The In1.Cu GND zone was refilled through native `refill_zones` after
  writing, as required for antipad regeneration around the two new vias.
- Board was saved through native Konnect/KiCad IPC.
- Post-write DRC was executed (429 total violations, matching the pre-existing
  baseline; 0 violations attributable to WDT_DONE).
- Connectivity verified complete between U8.4 and U1.19.
- Expected route geometry is present and matches the final written route below
  exactly.
- Protected routing (VBAT_MODEM, VSYS, LTE RF, GNSS RF, USB pair, SIM,
  WDT_DELAY, WDT_RST_TRIG) remained unchanged.
- No In1.Cu signal routing was introduced; In1.Cu remains GND-only, with
  antipads at the two new through-via crossings.
- No component movement occurred.

Final written route (authoritative reference for future work):

- U8.4 (2.950, 35.3625) --F.Cu--> (4.500, 35.3625) --F.Cu--> Via A (4.500, 30.000)
- Via A (4.500, 30.000) --In2.Cu--> Via B (11.000, 30.000)
- Via B (11.000, 30.000) --F.Cu--> U1.19 (11.000, 32.100)

Final route geometry:

- Trace width: 0.20 mm
- Clearance target: 0.20 mm
- Via diameter / drill: 0.60 / 0.30 mm
- Via count: 2 (Via A, Via B — both through vias, F.Cu/In1.Cu/In2.Cu/B.Cu)
- Trace segment count: 4
- Approximate total route length: 11.97 mm
- Signal layers: F.Cu + In2.Cu only
- In1.Cu signal routing: NONE (In1.Cu remains GND plane with antipads at
  the two through-via crossings)

## Current Stop Condition

WDT_DELAY: CLOSED — WRITE-PASS VERIFIED. Hard stop cleared.

WDT_RST_TRIG: CLOSED — WRITE-PASS VERIFIED. Hard stop cleared.

WDT_DONE: CLOSED — WRITE-PASS VERIFIED. Hard stop cleared.

All other Recovery / Control routing (PWRKEY, MODEM_RESET_N, SUPV_TRIG,
WDT_WAKE) remains not authorized for write. No read-only planning
authorization beyond what was already established elsewhere in this
document is granted or expanded by this closure.

## WDT_WAKE / WDT_RST_TRIG — Limited Local Repack Write Authorization

Status: CONDITIONAL WRITE AUTHORIZATION — FRESH NATIVE RE-PREFLIGHT REQUIRED

This limited authorization applies only to the exact local repack geometry
below. It does not reopen any other CONTROL net or authorize unrelated PCB
changes.

WDT_RST_TRIG local reopening scope:

- Remove only the F.Cu segment U8.6 (1.050, 35.3625) to (1.050, 33.300).
- Remove only the WDT_RST_TRIG through via at (1.050, 33.300).
- Preserve the existing In2.Cu trunk from (1.050, 33.300) to (35.200, 40.200)
  and its R34.1 / U10.3 branches.

WDT_RST_TRIG replacement:

- F.Cu: (1.050, 35.3625) to (0.800, 32.500).
- Through via: (0.800, 32.500), 0.60 mm diameter / 0.30 mm drill.
- In2.Cu: (0.800, 32.500) to (1.050, 33.300).

WDT_WAKE limited B.Cu route:

- F.Cu: U8.5 (2.000, 35.3625) to (2.000, 34.000).
- F.Cu: (2.000, 34.000) to (3.500, 32.000).
- Through via: (3.500, 32.000), 0.60 mm diameter / 0.30 mm drill.
- B.Cu: (3.500, 32.000) to (31.500, 16.100).
- Through via: (31.500, 16.100), 0.60 mm diameter / 0.30 mm drill.
- F.Cu: (31.500, 16.100) to U1.47 (30.000, 16.100).

All listed CONTROL traces use 0.20 mm width and 0.20 mm clearance. In1.Cu
remains GND-only. Native via preflight positively verified the required In1.Cu
GND antipad at each planned via with a 0.50 mm required antipad radius.

Execution conditions:

- Re-run native route and via preflight immediately before writing.
- Write one net at a time and stop on any failed preflight or new Level-A
  violation.
- No WDT_WAKE or WDT_RST_TRIG write is authorized outside the exact geometry
  listed above.
- WDT_DELAY, WDT_DONE, VSYS, VBAT_MODEM, USB, LTE RF, GNSS RF, and SIM remain
  protected and must not be modified.
- No component movement, zone-definition change, or unrelated copper deletion
  is authorized.

## WDT_WAKE — B4 Local Reroute (PromptID 088) — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

Root cause: the original B4 segment (B.Cu, (3.500, 32.000) to (31.500,
16.100)) crossed an intentional footprint-owned keepout embedded in U1's
footprint definition — rule-area KIID `796b2ba7-9cb9-4d09-8a5b-5e8150cda63b`
(owner: footprint U1, layers F.Cu/B.Cu, `keepout_tracks = true`, bounds
approximately x 19.475-21.525 mm / y 22.175-24.225 mm). This was identified
using the native `query_rule_areas` capability added to Konnect for exactly
this purpose.

Verified closure:

- Native rule-area-aware `check_route_clearance` (Konnect commit
  `c157d70a201c4a1ecfdd66413b6e240e904faa3b`, deployed SHA256
  `e3aafc71b6867d5b8ed6af503f0dfe4b7eb4d87c30ba0903b3fa6588456c1e95`)
  reproduced the original B4 failure live, attributing it precisely to the
  U1 rule area above.
- Old B4 track (KIID `26bc9078-447c-498b-ae73-188198d0b675`) was removed via
  native `delete_trace`. Removal verified immediately: WDT_WAKE dropped to 3
  traces / 2 vias, B1/B2/B3/B5/B6 unaffected.
- The replacement was freshly re-preflighted against the real post-deletion
  board (not merely the pre-deletion plan) and passed 4/4 with
  `rule_areas_clear = true` on every segment before any write occurred.
- Replacement written one segment at a time via native `route_trace`, with
  live verification after each write:
  - C1: B.Cu (3.500, 32.000) to (17.500, 24.050)
  - C2: B.Cu (17.500, 24.050) to (18.700, 21.600)
  - C3: B.Cu (18.700, 21.600) to (22.000, 21.600) — the segment closest to
    the U1 keepout
  - C4: B.Cu (22.000, 21.600) to (31.500, 16.100)
  - All segments: 0.20 mm width, 0.20 mm required clearance.
- No new vias. B3 ((3.500, 32.000)) and B5 ((31.500, 16.100)) through vias
  are unchanged (same KIIDs, positions, 0.60/0.30 mm).
- In1.Cu GND zone was refilled via native `refill_zones` after writing; C1-C4
  and B1/B2/B3/B5/B6 confirmed unchanged after refill.
- Board saved through native Konnect/KiCad IPC.
- Post-write authoritative DRC: `items_not_allowed` count dropped from 5 to
  4. The removed identity is exactly the old WDT_WAKE B4 violation (KIID
  `26bc9078-447c-498b-ae73-188198d0b675`); zero WDT_WAKE violations of any
  kind remain. The 4 remaining `items_not_allowed` violations
  (SIM_DET, USB_DP_CONN, USB_DM_CONN, LTE_RF_CONN) are pre-existing,
  unrelated to this intervention, and out of scope — unchanged before and
  after this write.
- WDT_DELAY (7 traces / 3 vias), WDT_RST_TRIG (7 traces / 2 vias), and
  WDT_DONE (4 traces / 2 vias) verified unchanged before and after this
  write.
- In1.Cu CONTROL trace count remains 0.
- No component movement. No rule-area/keepout modification. No unrelated
  copper deletion.

Final WDT_WAKE geometry (authoritative reference for future work):

- B1: F.Cu (2.000, 35.3625) to (2.000, 34.000)
- B2: F.Cu (2.000, 34.000) to (3.500, 32.000)
- B3: through via (3.500, 32.000), 0.60/0.30 mm
- C1: B.Cu (3.500, 32.000) to (17.500, 24.050)
- C2: B.Cu (17.500, 24.050) to (18.700, 21.600)
- C3: B.Cu (18.700, 21.600) to (22.000, 21.600)
- C4: B.Cu (22.000, 21.600) to (31.500, 16.100)
- B5: through via (31.500, 16.100), 0.60/0.30 mm
- B6: F.Cu (31.500, 16.100) to U1.47 (30.000, 16.100)
- Trace count: 7. Via count: 2. All CONTROL traces 0.20 mm width.

WDT_RST_TRIG Plan A was reverified unchanged throughout this work (7 traces /
2 vias, exact geometry preserved) and remains CLOSED — WRITE-PASS VERIFIED
per its own section above; this closure does not restate or reopen it.

## Remaining Recovery / Control Routing Order (Project-Owner Decision, PromptID 091)

STATUS.md previously listed PWRKEY, MODEM_RESET_N, and SUPV_TRIG as an
unordered group with no documented sequencing. The project owner has now
explicitly selected an order:

1. SUPV_TRIG
2. PWRKEY
3. MODEM_RESET_N

This is a new ordering decision, not a restatement of prior authority.

## SUPV_TRIG (PromptID 092) — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

Endpoints: U12.1 (44.100, 37.750) — U9.2 (58.0625, 26.050). U9 is the
TPS3839K33DBZR brownout supervisor (RESET output); U12 is the
SN74LVC2G08DCUR dual AND gate, gate 1 (`PWRKEY_ARM = SUPV_TRIG AND
MODEM_RESET_N`).

Verified closure:

- Native rule-area query found zero rule areas relevant to this corridor
  (nearest keepout, J4's, is far from the routing region).
- Endpoint escape planning found the first candidate via site for U12.1,
  (44.600, 37.750), collided with U12 pad 2 (MODEM_RESET_N) at only 0.025 mm
  clearance — U12 is a VSSOP-8 with 0.5 mm pin pitch. Relocated the via to
  (44.100, 37.250), which passed native preflight cleanly.
- Native `check_route_clearance`/`check_via_clearance` passed for all three
  trace segments and both vias, fresh, immediately before write.
- Route was written through native Konnect/KiCad IPC only (`route_trace`,
  `add_via`) — no direct file editing. Verified after each individual write.
- In1.Cu GND zone was refilled via native `refill_zones` after writing.
- Board saved through native Konnect/KiCad IPC.
- Post-write DRC: total 428 (errors 214 / warnings 214). The 4 pre-existing
  `items_not_allowed` violations (SIM_DET, USB_DP_CONN, USB_DM_CONN,
  LTE_RF_CONN) are unchanged. No new WDT_WAKE, WDT_RST_TRIG, WDT_DELAY, or
  WDT_DONE violation.
- Post-write DRC also surfaced a `clearance` error between U12 pad 1
  (SUPV_TRIG) and pad 2 (MODEM_RESET_N): actual 0.15 mm vs the CONTROL
  netclass's required 0.20 mm. This is **not attributable to this write** —
  an identical clearance error exists between U12 pad 2 (MODEM_RESET_N) and
  pad 3 (PWRKEY_TRIG), a pad pair this write never touched, proving the
  finding is a systemic property of U12's fixed 0.5 mm pad pitch (0.35 mm
  pad height leaves exactly 0.15 mm between every adjacent pad) versus the
  CONTROL netclass's 0.20 mm requirement — present regardless of routing and
  not fixable by any route choice. This is tracked here as a known,
  pre-existing, out-of-scope footprint/netclass-geometry finding, separate
  from the four historical `items_not_allowed` violations, and does not
  block this closure.
- Protected routing (VBAT_MODEM, VSYS, LTE RF, GNSS RF, USB pair, SIM,
  WDT_DELAY, WDT_RST_TRIG, WDT_DONE, WDT_WAKE) remained unchanged. PWRKEY and
  MODEM_RESET_N remain unrouted and untouched.
- No In1.Cu signal routing was introduced; In1.Cu remains GND-only.
- No component movement, rule-area modification, or unrelated copper
  deletion occurred.

Final written route (authoritative reference for future work):

- S1: F.Cu U12.1 (44.100, 37.750) to Via A (44.100, 37.250)
- S2: In2.Cu Via A (44.100, 37.250) to Via B (57.500, 26.050)
- S3: F.Cu Via B (57.500, 26.050) to U9.2 (58.0625, 26.050)
- Trace width: 0.20 mm. Via diameter/drill: 0.60/0.30 mm. Via count: 2
  (both through vias, F.Cu/In1.Cu/In2.Cu/B.Cu). Trace count: 3.
- Signal layers: F.Cu + In2.Cu only. No B.Cu, no In1.Cu.

PWRKEY and MODEM_RESET_N remain unrouted and are not authorized by this
closure.

## PWRKEY (PromptID 095) — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

PWRKEY is a three-terminal net: Q2 (MMBT2222A) collector — TP9 (existing
testpoint) — U1 (A7670 modem) pin 1 PWRKEY. Q2's collector sinks PWRKEY when
driven by the auto-PWRKEY interlock (U11/U12/U13); TP9 is a bench test point.
Distinct from PWRKEY_TRIG / PWRKEY_ARM / PWRKEY_ARM_DLY / PWRKEY_ARM_DLY_N,
which are separate nets not part of the CONTROL netclass authorization and
were not touched.

Verified closure:

- Live endpoint discovery (native `get_routing_geometry`/`get_component_pads`,
  not memorized coordinates) found U1.1 (6.000, 12.100) sitting close to U1's
  own footprint keepout (7.1-9.15, 10.9-13.3); the escape was planned
  leftward, away from it, and verified clear via native
  `check_route_clearance`.
- The route runs entirely clear of U12, so MODEM_RESET_N's future escape
  corridor near U12 was not consumed or disturbed by this write.
- Native rule-area-aware `check_route_clearance`/`check_via_clearance` passed
  for all four segments and both vias, fresh, immediately before write.
- Route was written through native Konnect/KiCad IPC only (`route_trace`,
  `add_via`) — no direct file editing. Verified after each individual write.
- Three-terminal connectivity confirmed by shared endpoint coordinates: S1
  connects U1.1 to Via A; S2 (In2.Cu trunk) connects Via A to Via B; S3 and
  S4 both originate at Via B, connecting it to Q2.3 and TP9.1 respectively.
  No dangling branch.
- In1.Cu GND zone was refilled via native `refill_zones` after writing.
- Board saved through native Konnect/KiCad IPC.
- Post-write DRC: total 427 (errors 213 / warnings 214). The only PWRKEY
  mention is a pre-existing `silk_over_copper` **warning** between TP9's pad
  and J2's silkscreen — neither object was touched by this write, and it is
  a warning, not an error. The 4 pre-existing `items_not_allowed` violations
  are unchanged. MODEM_RESET_N's DRC mentions are the same pre-existing
  systemic U12 pad-pitch findings documented under SUPV_TRIG (PromptID 093)
  plus one pre-existing TP10 silk warning — identical identities, no
  regression. The total-count dip from 428 to 427 matches the run-to-run DRC
  count variance already documented under WDT_DELAY's closure, independent
  of PCB modification.
- Protected routing (VBAT_MODEM, VSYS, LTE RF, GNSS RF, USB pair, SIM,
  WDT_DELAY, WDT_RST_TRIG, WDT_DONE, WDT_WAKE, SUPV_TRIG) remained unchanged.
  MODEM_RESET_N remains unrouted and untouched (0 traces / 0 vias).
- No In1.Cu signal routing was introduced; In1.Cu remains GND-only.
- No component movement, rule-area modification, or unrelated copper
  deletion occurred.

Final written route (authoritative reference for future work):

- S1: F.Cu U1.1 (6.000, 12.100) to Via A (4.500, 12.100)
- S2: In2.Cu Via A (4.500, 12.100) to Via B (52.000, 45.000)
- S3: F.Cu Via B (52.000, 45.000) to Q2.3 (50.9375, 45.000)
- S4: F.Cu Via B (52.000, 45.000) to TP9.1 (53.500, 55.000)
- Trace width: 0.20 mm. Via diameter/drill: 0.60/0.30 mm. Via count: 2
  (both through vias, F.Cu/In1.Cu/In2.Cu/B.Cu). Trace count: 4.
- Signal layers: F.Cu + In2.Cu only. No B.Cu, no In1.Cu.

Remaining owner-selected routing order (superseded — see MODEM_RESET_N
closure below):

1. MODEM_RESET_N

## MODEM_RESET_N (PromptID 098) — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

MODEM_RESET_N is a five-terminal net: U10.1 (TPS3808 RESET pulse-stretcher
open-drain output, active-low) — R30.1 (100kΩ pull-up to VSYS) — U12.2 (AND
gate interlock input) — TP10.1 (testpoint) — U1.16 (A7670 modem RESET pin).
Live endpoint discovery (not memorized coordinates) confirmed all five.

Verified closure:

- Native rule-area query found no keepout relevant to any endpoint or
  corridor.
- U12.2 escape: first candidates toward U12.1/U12.3's y-pitch were avoided
  entirely by escaping east along pad2's own row (0.5 mm VSSOP-8 pitch,
  same intrinsic condition documented under SUPV_TRIG/PWRKEY, not
  reopened or modified here).
- U10.1 escape: two directions (west, north) failed against WDT_RST_TRIG's
  existing F.Cu geometry — a closed net, correctly left untouched. East
  escape passed.
- R30.1 escape: north failed against R31's GND pad. East escape passed.
- Trunk routing: a direct In2.Cu path from ViaU1 to ViaU10 collided with
  WDT_DONE's via — resolved with a dogleg routed outside WDT_DONE's x-range,
  not through it. Direct In2.Cu trunks from ViaU10/ViaU12 to ViaU12/ViaR30/
  ViaTP10 all collided with SUPV_TRIG's and PWRKEY's existing In2.Cu trunks
  (same-layer crossing of an existing trace is illegal regardless of
  dogleg). Resolved by routing those three legs on B.Cu instead — natively
  verified clear, and confirmed clear of WDT_WAKE's B.Cu geometry (which
  stays at x < 32, no overlap). No closed net was deleted, rerouted, or
  moved to make room.
- Native `check_route_clearance`/`check_via_clearance` passed for all 11
  segments and 5 vias, fresh, immediately before write.
- Route was written through native Konnect/KiCad IPC only (`route_trace`,
  `add_via`), one object at a time, each verified immediately after
  creation.
- Five-endpoint connectivity confirmed by shared coordinates forming one
  tree: U1.16 - E1 - ViaU1 - T1a - T1b - T1c - ViaU10 - {E2 - U10.1;
  T2 - ViaU12 - {E3 - U12.2; T3 - ViaR30 - E4 - R30.1;
  T4 - ViaTP10 - E5 - TP10.1}}. No dangling branch.
- In1.Cu GND zone was refilled via native `refill_zones` after writing.
- Board saved through native Konnect/KiCad IPC.
- Post-write DRC: total 429 (errors 215 / warnings 214). All 3
  MODEM_RESET_N-related findings are pre-existing and unrelated to this
  route: the U12.1↔U12.2 and U12.2↔U12.3 intrinsic pad-pitch findings
  (unchanged, documented since PromptID 093), and a pre-existing
  TP10↔J2 silk_over_copper warning. Zero findings involve any of the 11
  new traces or 5 new vias. The 4 historical `items_not_allowed`
  violations are unchanged. SUPV_TRIG and PWRKEY mentions unchanged (1
  each, same pre-existing findings) — zero regression.
- Protected routing (VBAT_MODEM, VSYS, LTE RF, GNSS RF, USB pair, SIM,
  WDT_DELAY, WDT_RST_TRIG, WDT_DONE, WDT_WAKE, SUPV_TRIG, PWRKEY) remained
  unchanged throughout.
- No component movement, rule-area modification, or unrelated copper
  deletion occurred.

Final written route (authoritative reference for future work):

- E1: F.Cu U1.16 (6.000, 27.100) to ViaU1 (4.500, 27.100)
- T1a: In2.Cu ViaU1 (4.500, 27.100) to (15.000, 27.100)
- T1b: In2.Cu (15.000, 27.100) to (15.000, 33.000)
- T1c: In2.Cu (15.000, 33.000) to ViaU10 (37.900, 39.550)
- E2: F.Cu U10.1 (36.8625, 39.550) to ViaU10 (37.900, 39.550)
- T2: B.Cu ViaU10 (37.900, 39.550) to ViaU12 (45.500, 38.250)
- E3: F.Cu U12.2 (44.100, 38.250) to ViaU12 (45.500, 38.250)
- T3: B.Cu ViaU12 (45.500, 38.250) to ViaR30 (43.300, 25.710)
- E4: F.Cu R30.1 (42.500, 25.710) to ViaR30 (43.300, 25.710)
- T4: B.Cu ViaU12 (45.500, 38.250) to ViaTP10 (54.500, 53.500)
- E5: F.Cu TP10.1 (56.000, 55.000) to ViaTP10 (54.500, 53.500)
- Trace width: 0.20 mm. Via diameter/drill: 0.60/0.30 mm. Via count: 5
  (all through vias, F.Cu/In1.Cu/In2.Cu/B.Cu). Trace count: 11.
- Signal layers: F.Cu (5 traces) + In2.Cu (3 traces) + B.Cu (3 traces).
  No In1.Cu signal routing.

The owner-selected Recovery/Control routing sequence (SUPV_TRIG, PWRKEY,
MODEM_RESET_N) is now complete. The known U12 intrinsic adjacent-pad
0.15 mm / required 0.20 mm condition (all six adjacent pad pairs) remains
unresolved and out of scope — not modified, not waived, not excluded. The
four historical `items_not_allowed` violations (SIM_DET, USB_DP_CONN,
USB_DM_CONN, LTE_RF_CONN) also remain unresolved and out of scope. This
closure does not claim total board DRC is clean.

MODEM_RESET_N remains unrouted and is not authorized by this closure.

## Recovery/Control: COMPLETE — Power/Charger Completion (Owner Decision, PromptID 101–103)

Recovery/Control routing (WDT_DELAY, WDT_RST_TRIG, WDT_DONE, WDT_WAKE,
SUPV_TRIG, PWRKEY, MODEM_RESET_N) is COMPLETE as of commit
`c22513f9bb6a3dad663782335a68a68a2e93ceb5`.

The project owner has selected the next Recovery/Control-adjacent work item
as a new batch: **POWER / CHARGER COMPLETION** (PromptID 101). This is a new
owner decision recorded here for the first time — it was not previously
established by any prior STATUS.md authority.

Scope: 19 live-verified unrouted nets (BAT_CELL, BAT_GATE, BAT_PACK_POS,
BAT_PROTECTED, BAT_SENSE, VBAT_ADC_SENSE, CHG_EN1, CHG_EN2, CHG_PGOOD,
CHG_STATUS, CHG_TS, ILIM_SET, ISET_SET, ITERM_SET, TMR_SET, PWR_FLAG,
USB_VBUS_RAW, USB_VBUS_FUSED, VDD_1V8). PWRKEY-internal-logic nets
(PWRKEY_TRIG, PWRKEY_ARM, PWRKEY_ARM_DLY, PWRKEY_ARM_DLY_N,
AUTO_PWRKEY_BASE, AUTO_PWRKEY_DRV, STRETCH_CT, LEVEL_OE) are explicitly
excluded from this batch pending separate authorization and the still-open
U12 pad-pitch decision.

### Power/Charger Routing Authority (Owner Decision, PromptID 103)

These are new owner-established routing classes for the Power/Charger batch
only. They do not modify, extend, or reuse the existing Recovery/Control
`CONTROL` netclass, which remains scoped to its original seven named nets.

**POWER_HIGH** — BAT_PACK_POS, BAT_PROTECTED, BAT_CELL
- Width 1.00 mm, clearance 0.25 mm, via 0.80 mm / 0.40 mm drill (if
  unavoidable), preferred F.Cu, avoid vias where practical.
- Rationale: F2 (battery-path PTC fuse) is rated 2.0A. PromptID 102 derived
  ~0.80 mm from 1 oz external copper / 10°C-rise IPC-2221 reference; the
  owner selected 1.00 mm for additional margin and consistency with the
  existing VBAT_MODEM precedent.

**POWER_MEDIUM** — USB_VBUS_RAW, USB_VBUS_FUSED
- Width 0.50 mm, clearance 0.25 mm, via 0.60 mm / 0.30 mm drill (if
  unavoidable), preferred F.Cu.
- Rationale: F1 (USB input PTC fuse) is rated 1.1A; 0.50 mm matches the
  existing VSYS width precedent.

**ANALOG_SENSE** — BAT_SENSE, VBAT_ADC_SENSE, CHG_TS
- Width 0.25 mm, clearance 0.20 mm, avoid vias where practical.

**LOGIC_CONTROL** — BAT_GATE, ILIM_SET, ISET_SET, ITERM_SET, TMR_SET,
CHG_EN1, CHG_EN2, CHG_PGOOD, CHG_STATUS
- Width 0.25 mm, clearance 0.20 mm, via 0.60 mm / 0.30 mm drill if required.

**PWR_FLAG** — routing authority WITHHELD. Electrical role insufficiently
established (three modem pads share one literal net; needs schematic
clarification before planning).

**VDD_1V8** — EXCLUDED from the Power/Charger batch for now. PromptID 102
found that U6 (previously assumed to be a regulator) is actually a load
(W25Q32JW flash, 1.8V variant); the rail's actual source and total load
remain unresolved. Requires a separate cross-subsystem power-rail audit
before classification. Note: one of its loads, U8 (TPL5010 watchdog), is
the same IC used in the already-closed WDT_DELAY net.

Internal Power/Charger net order (owner-approved for planning progression;
each net still requires its own PLAN-PASS and separate WRITE
authorization):

1. BAT_GATE
2. BAT_PACK_POS / BAT_PROTECTED / BAT_CELL
3. USB_VBUS_RAW / USB_VBUS_FUSED
4. BAT_SENSE / VBAT_ADC_SENSE / CHG_TS
5. ILIM_SET / ISET_SET / ITERM_SET / TMR_SET / CHG_EN1 / CHG_EN2
6. CHG_PGOOD / CHG_STATUS

### BAT_GATE — Plan Established (PromptID 103), NOT WRITTEN

Status: PLAN-PASS — routing NOT authorized, NOT written.

BAT_GATE is the gate-control node for Q1 (AO3401A battery reverse-polarity
protection FET): R19.1 (100k pull-up resistor) to Q1.1. Live endpoints
verified: R19.1 (53.490, 41.000), Q1.1 (49.050, 52.4375), both F.Cu.

A direct F.Cu connection and two local F.Cu doglegs were all found to
collide with existing copper/pads in this densely-populated corner of the
board (Q1/Q2/F2/U13/C34 courtyards, and PWRKEY's F.Cu branches/via near
(52, 45)) — natively verified, not assumed. No unnecessary alternative
search was performed once collisions were confirmed.

Planned route (F.Cu escape → via → In2.Cu trunk with one dogleg → via →
F.Cu escape), all natively PASS, fresh:

- S1: F.Cu Q1.1 (49.050, 52.4375) to ViaA (49.050, 53.800)
- ViaA: (49.050, 53.800), 0.60/0.30 mm
- T: In2.Cu ViaA (49.050, 53.800) to (55.000, 46.000) to ViaB
  (53.700, 42.000) — the dogleg via (55.000, 46.000) is required to clear
  PWRKEY's via at (52.000, 45.000), which a direct line grazed at only
  0.057 mm (required 0.20 mm).
- ViaB: (53.700, 42.000), 0.60/0.30 mm
- S2: F.Cu ViaB (53.700, 42.000) to R19.1 (53.490, 41.000)
- Width 0.25 mm throughout, per the LOGIC_CONTROL class above.

This plan does not consume or block the obvious short/direct corridor
expected for BAT_PACK_POS / BAT_PROTECTED / BAT_CELL (J2 connector, Q1.2/
Q1.3, F2, U3), which remains open for its own future planning task.

No PCB write occurred. BAT_GATE remains unrouted (0 traces / 0 vias) as of
this entry.

## BAT_GATE (PromptID 104) — Closed (Write-Pass Verified)

Status: CLOSED — WRITE-PASS VERIFIED

Verified closure:

- Native rule-area-aware `check_route_clearance`/`check_via_clearance`
  passed for all four segments and both vias, fresh, immediately before
  write, matching the PromptID 103 plan exactly.
- Route was written through native Konnect/KiCad IPC only (`route_trace`,
  `add_via`), one object at a time, each verified immediately after
  creation. The T1/T2 dogleg was written as two explicit In2.Cu segments,
  not an implicit polyline.
- After writing T2, PWRKEY's Via B (52.000, 45.000) was re-queried and
  confirmed unchanged — the dogleg's 2.12 mm clearance to it held.
- In1.Cu GND zone was refilled via native `refill_zones` after writing.
- Board saved through native Konnect/KiCad IPC.
- Post-write DRC: total 427 (errors 213 / warnings 214). BAT_GATE's only
  DRC mention is a pre-existing `silk_over_copper` **warning** between
  Q1's pad 1 (the BAT_GATE endpoint itself) and TP6's silkscreen
  reference field — neither object was touched by this write. Zero
  route-attributable Level-A (error) violations. PWRKEY's only mention is
  the same pre-existing TP9/J2 finding, unchanged. Recovery/Control (all
  7 nets) reverified unchanged.
- BAT_PACK_POS, BAT_PROTECTED, and BAT_CELL remain unrouted (0/0) —
  their obvious short F.Cu corridor near J2/Q1/F2/U3 was not consumed by
  this route.
- No component movement, rule-area modification, or unrelated copper
  deletion occurred.

Final written route (authoritative reference for future work):

- S1: F.Cu Q1.1 (49.050, 52.4375) to ViaA (49.050, 53.800)
- ViaA: through via (49.050, 53.800), 0.60/0.30 mm
- T1: In2.Cu ViaA (49.050, 53.800) to (55.000, 46.000)
- T2: In2.Cu (55.000, 46.000) to ViaB (53.700, 42.000)
- ViaB: through via (53.700, 42.000), 0.60/0.30 mm
- S2: F.Cu ViaB (53.700, 42.000) to R19.1 (53.490, 41.000)
- Width 0.25 mm throughout (LOGIC_CONTROL class). Trace count: 4. Via
  count: 2. Signal layers: F.Cu + In2.Cu only. No B.Cu, no In1.Cu.

Next Power/Charger work: BAT_PACK_POS / BAT_PROTECTED / BAT_CELL (not
routed, not authorized by this closure).
