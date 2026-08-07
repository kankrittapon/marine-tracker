# ADR-001: Protected Battery Pack (No Board-Level Protection IC)

## Context

RevA's only battery-path protection element is Q1, a single FET whose gate (`BAT_GATE`)
is tied to GND through R19 alone — a passive, self-biased reverse-polarity blocking
stage. There is no active overcurrent, overvoltage, or over-discharge protection IC on
the board. `PROJECT_BRIEF.md` specifies "Battery: Li-ion/LiPo 1S แบบชาร์จได้"
(rechargeable 1S) without mandating an on-board protection IC, and no specific
cell/pack part has been selected yet (`docs/STATUS.md`: "ยังไม่ยืนยัน: ... battery
capacity").

## Problem

Whether the board is adequately protected against over-discharge, charge overcurrent
beyond F2's fuse rating, and cell overvoltage depends entirely on a component (the
battery pack) that has not yet been selected. Deciding now which protection strategy
to design for is a prerequisite for finalizing the BOM and for battery-pack sourcing.

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. Rely on a protected battery pack | Select only cell/pack SKUs with integrated PCM (over-current, over-voltage, over-discharge). Q1 remains as reverse-polarity-only protection. | Zero added parts/cost/area; constrains BOM to protected-pack SKUs only; protection quality varies by vendor. |
| B. Add a dedicated board-level protection IC | e.g. a DW01-class dual-FET driver + sense IC, or an integrated part such as the TI BQ2970x family, in series with Q1. | Board is safe with any cell, including an accidentally unprotected one; adds cost, qualification effort, and board area. |
| C. Both (defense in depth) | Protected pack + board-level protection IC. | Highest safety margin; highest cost/complexity/area for a 10-unit prototype run. |

## Decision

**Option A — rely on a protected battery pack.** The battery pack purchased for RevA
MUST be a protected pack (integrated PCM). Q1 remains in its current role
(reverse-polarity protection only). This is a BOM/sourcing constraint, not a schematic
change.

Rationale: lowest complexity/cost/area, consistent with CLAUDE.md's Component Policy
("Avoid difficult sourcing," "low component count") and Manufacturing Policy
("Design for 10 prototype boards... avoid expensive assembly"). Revisit for the
100-unit production run if field data suggests board-level protection is warranted.

## Consequences

- **Positive:** No schematic change, no new part to qualify, no added PCB area or cost.
- **Negative:** Battery pack selection is now a hard constraint — any pack chosen at BOM
  freeze must be verified to include integrated protection before purchase. If an
  unprotected pack is substituted later (e.g., for cost or availability reasons)
  without revisiting this ADR, the board has no board-level protection net.
- **Follow-up action:** Add "battery pack must include integrated PCM" as an explicit
  BOM acceptance criterion (see `docs/ACCEPTANCE_CRITERIA.md` item 8, "BOM ทุก fitted
  part มี exact MPN").

## References

- `docs/PROJECT_BRIEF.md` — battery chemistry requirement (1S Li-ion/LiPo rechargeable).
- `docs/STATUS.md` — battery capacity/connector/chemistry not yet frozen.
- CLAUDE.md — Component Policy, Manufacturing Policy.
- Engineering Change Proposal, ECP-3 (this conversation, Power Architecture Review phase).
- No manufacturer datasheet applies directly — no protection IC or specific cell/pack
  is in the design; this is an architectural/sourcing decision, not a datasheet
  contradiction.

## Approval status

**APPROVED** — per user decision, this conversation.
