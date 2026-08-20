# Marine Tracker RevB — Live Board Snapshot

> Cache only. This document records observations made against one known PCB
> baseline. It is not design authority and must never override the live PCB,
> schematic, `docs/STATUS.md`, or `docs/ENGINEERING_RULEBOOK.md`.

## Binding and invalidation

- Project baseline SHA: `5d6bd24f11acae4e13fa866dfe5abe1d2549f176`
- Board: `hardware/RevB/marine-tracker-RevB.kicad_pcb`
- Revision state: RevB ACTIVE; RevA FROZEN
- Snapshot date: 2026-08-20
- Konnect version: `0.2.2` (LIVE_RUNTIME)
- Konnect source/build commit: `c157d70a201c4a1ecfdd66413b6e240e904faa3b` (SOURCE_BASELINE; local starter-kit patch was built)
- KiCad version: UNKNOWN

### SNAPSHOT VALID ONLY WHEN

1. Marine Tracker HEAD matches the recorded baseline SHA; and
2. `marine-tracker-RevB.kicad_pcb` has no tracked modification relative to
   that baseline; and
3. no uncheckpointed PCB write occurred in the current session.

If any condition fails, routing geometry/counts, pad coordinates, rule-area
geometry, and collision findings are STALE. Schematic connectivity may be
reused only if the schematic itself is unchanged. Live state remains
authoritative.

## Provenance labels

`DOCUMENTED` = project authority documentation; `LIVE_PCB` = native live PCB
query; `LIVE_KICAD` = native KiCad metadata/query; `OWNER_AUTHORITY` = explicit
owner routing decision; `UNKNOWN` = not exposed or not safely established.

## Board and fabrication snapshot

| Field | Value | Provenance |
|---|---|---|
| Board dimensions | 65 × 58 mm | DOCUMENTED (`docs/STATUS.md`) |
| Copper layer count | 4 | DOCUMENTED |
| Layer strategy | L1 components/RF/high-current/signals; L2 solid GND; L3 power/slow signals; L4 slow signals/GND | DOCUMENTED |
| Layer names/order | F.Cu, In1.Cu, In2.Cu, B.Cu | LIVE_PCB observations / DOCUMENTED strategy |
| Fabrication stack | JLCPCB JLC04161H-7628 | DOCUMENTED |
| L1–L2 dielectric | 0.21040 mm, Dk 4.4 | DOCUMENTED |
| Outer copper | 0.035 mm, 1 oz | DOCUMENTED |
| Inner copper | 0.0152 mm | DOCUMENTED |
| Board thickness | UNKNOWN | UNKNOWN |
| Live board title | marine-tracker-RevB | LIVE_KICAD |
| Native board layer-count response | 0 / unusable | LIVE_KICAD; not accepted as design truth |
| Global native design rules | UNKNOWN; endpoint returned NULL values | LIVE_KICAD; not accepted as design truth |

## Owner routing policy snapshot

The following is OWNER_AUTHORITY, not inferred from blank PCB pad-net fields.

### POWER_HIGH

`BAT_PACK_POS`, `BAT_PROTECTED`, `BAT_CELL`: width 1.00 mm; clearance 0.25
mm; via 0.80/0.40 mm only if unavoidable; prefer F.Cu, short/direct paths,
and avoid vias.

### POWER_MEDIUM

`USB_VBUS_RAW`, `USB_VBUS_FUSED`: width 0.50 mm; clearance 0.25 mm; via
0.60/0.30 mm if required.

### ANALOG_SENSE

`BAT_SENSE`, `VBAT_ADC_SENSE`, `CHG_TS`: width 0.25 mm; clearance 0.20 mm.

### LOGIC_CONTROL

`BAT_GATE`, `ILIM_SET`, `ISET_SET`, `ITERM_SET`, `TMR_SET`, `CHG_EN1`,
`CHG_EN2`, `CHG_PGOOD`, `CHG_STATUS`: width 0.25 mm; clearance 0.20 mm; via
0.60/0.30 mm if required.

- `PWR_FLAG`: WITHHELD.
- `VDD_1V8`: EXCLUDED.

## Component and pad cache

Coordinates and pad layers below are LIVE_PCB observations. PCB pad-net fields
were blank in the native component-pad response; logical membership comes from
the native schematic cache below.

| Ref | Identity/value | Position / rotation | Pad | Coordinate | Layer |
|---|---|---|---|---|---|
| J2 | BATTERY | (56.0, 51.5) / UNKNOWN | 1 | (56.0, 51.5) | F.Cu |
| Q1 | AO3401A_REVERSE_POLARITY | (50.0, 51.5) / 90° | 2 | (50.95, 52.4375) | F.Cu |
| Q1 | AO3401A_REVERSE_POLARITY | (50.0, 51.5) / 90° | 3 | (50.0, 50.5625) | F.Cu |
| Q2 | UNKNOWN | (50.0, 45.0) / UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| F2 | 2.0A_PTC_BAT | (46.0, 50.0) / UNKNOWN | 1 | (44.6, 50.0) | F.Cu |
| F2 | 2.0A_PTC_BAT | (46.0, 50.0) / UNKNOWN | 2 | (47.4, 50.0) | F.Cu |
| U3 | BQ24074RGTR | (8.5, 37.0) / UNKNOWN | 2 | (6.8025, 36.75) | F.Cu |
| U3 | BQ24074RGTR | (8.5, 37.0) / UNKNOWN | 3 | (6.8025, 37.25) | F.Cu |
| R19 | UNKNOWN | (54.0, 41.0) / UNKNOWN | 1 | (53.49, 41.0) | F.Cu |
| TP3 | UNKNOWN | (31.5, 55.0) / UNKNOWN | 1 | (31.5, 55.0) | F.Cu |
| TP4 | UNKNOWN | (43.5, 55.0) / UNKNOWN | 1 | (43.5, 55.0) | F.Cu |

Additional repeatedly queried branch pads:

- C3.1: `(63.0,24.68)`, F.Cu.
- R16.1: `(38.69,14.6)`, F.Cu.

## Native schematic connectivity cache

Provenance is NATIVE_SCHEMATIC; PCB reference/pad correspondence is
CROSS_CONFIRMED where the live pad query returned the matching reference and
number.

- `BAT_PACK_POS`: Q1.3 (D), TP3.1 (TP_BAT_PACK_POS), J2.1 (Pin_1).
- `BAT_PROTECTED`: Q1.2 (S), F2.1.
- `BAT_CELL`: U3.2 (BAT), U3.3 (BAT), C3.1, TP4.1 (TP_BAT_CELL), F2.2,
  R16.1.

The cache does not include every closed-net membership; live native queries
remain required before writes.

## Routing checkpoint snapshot

Counts are `traces / vias`, and are SNAPSHOT STATE only:

| Net | Count |
|---|---:|
| WDT_DELAY | 7 / 3 |
| WDT_RST_TRIG | 7 / 2 |
| WDT_DONE | 4 / 2 |
| WDT_WAKE | 7 / 2 |
| SUPV_TRIG | 3 / 2 |
| PWRKEY | 4 / 2 |
| MODEM_RESET_N | 11 / 5 |
| BAT_GATE | 4 / 2 |
| BAT_PACK_POS | 0 / 0 |
| BAT_PROTECTED | 0 / 0 |
| BAT_CELL | 0 / 0 |

In1.Cu signal traces: 0.

These counts must be live-verified after any PCB write or baseline SHA change.

## Closed geometry cache

Partial cache; object UUIDs were not retained.

### BAT_GATE — LIVE_PCB

- F.Cu: `(49.05,52.4375)` → `(49.05,53.8)`.
- In2.Cu: `(49.05,53.8)` → `(55.0,46.0)`.
- In2.Cu: `(55.0,46.0)` → `(53.7,42.0)`.
- F.Cu: `(53.7,42.0)` → `(53.49,41.0)`.
- Vias: `(49.05,53.8)` and `(53.7,42.0)`; exact cached size/drill: UNKNOWN.

### PWRKEY — LIVE_PCB

- F.Cu branches include `(52.0,45.0)` → `(53.5,55.0)` and
  `(52.0,45.0)` → `(50.9375,45.0)`.
- In2.Cu trunk includes `(4.5,12.1)` → `(52.0,45.0)`.
- Via B: `(52.0,45.0)`; exact object ID/size/drill: UNKNOWN.

### MODEM_RESET_N — LIVE_PCB

- Existing F.Cu/B.Cu/In2.Cu routing spans the modem/control region;
  complete segment cache intentionally omitted.
- Trace/via count is cached above; live geometry is required before any new
  route.

## Rule-area cache

Ten rule areas were observed by native query. Cached ownership includes J3, J4,
J5, and U1. Detailed complete bounds/KIIDs were not retained for every area;
this section is PARTIAL and must not replace a fresh rule-area query.

- J5 areas: approximately x17–24, y43–53.8; F.Cu/F.CrtYd; copper/pads/
  tracks/vias restrictions observed.
- J4 top keepout: approximately x42.05–43.95, y1.21–3.3; F.Cu.
- J3 top keepout: approximately x7.05–8.95, y1.21–3.3; F.Cu.
- U1 areas: approximately x7.1–9.15, y10.9–13.3 and x19.475–21.525,
  y22.175–24.225; F.Cu/B.Cu.
- Other observed area ownership/details: UNKNOWN.

No local Q1/F2/J2/U3/TP3/TP4/C3/R16 rule-area intersection was reported in
the cached query, but this must be rechecked for any affected write.

## Known DRC baseline findings

These are KNOWN BASELINE FINDINGS, not accepted waivers and not evidence that
future regressions are acceptable.

- Historical `items_not_allowed`: SIM_DET, USB_DP_CONN, USB_DM_CONN,
  LTE_RF_CONN.
- Systemic U12 adjacent-pad condition: actual 0.15 mm versus required 0.20
  mm, affecting adjacent U12 pad pairs; footprint/rule remediation issue.

## High-current planning evidence

These are PLAN EVIDENCE, not routed state.

### BAT_PROTECTED

Native candidate accepted in 107H:

`Q1.2 → F.Cu escape → via (50.95,54.5) → In2.Cu dogleg → via (43.0,50.0) → F.Cu → F2.1`.

Verified candidate traces:

- F.Cu `(50.95,52.4375)` → `(50.95,54.5)`, 1.00 mm, minimum clearance
  1.100 mm, native PASS.
- In2.Cu `(50.95,54.5)` → `(50.95,56.0)` → `(43.0,56.0)` → `(43.0,50.0)`,
  1.00 mm, minimum clearance 1.225 mm, native PASS.
- F.Cu `(43.0,50.0)` → `(44.6,50.0)`, 1.00 mm, minimum clearance 4.449
  mm, native PASS.

Via `(50.95,54.5)` was natively PASS with 0.80/0.40 mm, minimum clearance
1.325 mm, and supported In1.Cu GND antipad. The second via site was accepted
as a candidate in the same native preflight family. No copper was written.

### BAT_PACK_POS

J2.1 is `(56.0,51.5)`. A via-only candidate at `(56.0,53.0)` passed native
via clearance, but the 1.00 mm F.Cu escape from J2.1 failed due to the
existing LTE_RF_CONN track. The endpoint remains unresolved.

### BAT_CELL

No complete accepted topology exists. Direct candidates remain blocked by
existing VSYS, SIM, MODEM_RESET_N, BAT_GATE, USB, and nearby pad geometry as
recorded in the 107G/107H reports.

## Future handshake fast path

When the snapshot baseline is valid, normally verify only:

1. Git HEAD and tracked PCB/schematic status.
2. Konnect connection and KiCad IPC health.
3. Active RevB board.
4. Target-net routing counts relevant to the next task.
5. Geometry directly involved in the next planned write.

Do not re-query the entire board by default. If the baseline differs, perform
full live verification for the affected sections. Static values from this
snapshot are accelerators only.

## Source priority

1. Owner/design authority documents for design intent and approved rules.
2. Current live PCB/schematic for actual implementation.
3. This snapshot when baseline-valid.
4. Historical session reports as supporting evidence only.

## Integrity at snapshot creation

- Authorized file written: this document only.
- PCB modified: NO.
- Schematic modified: NO.
- Rules/footprints/components modified: NO.
- STATUS modified: NO.
- Git commit/push: NO.
