# ADR-002: VBAT Always-On Architecture

## Context

`VBAT_MODEM` is wired as a direct, always-on link from `VSYS` through FB1
(ferrite bead / 0R link) to A7670 (U1) VBAT pins 55/56/57. There is no switch or
enable element on this rail — A7670 is electrically powered (VBAT present) any time
`VSYS` is up, regardless of the module's own PWRKEY-controlled power state.

## Problem

SIMCom's own hardware design guide recommends an enable-pin-controlled LDO/DC-DC on
the VBAT supply ("It is recommended to select an LDO or DC-DC chip with an enable
pin, and the enable pin is controlled by the MCU" — `A7670X_HW.pdf` §3.1.1). RevA
does not follow this recommendation. Whether that matters depends on the achievable
system sleep-current budget, which has not yet been calculated (battery capacity is
still unconfirmed per `docs/STATUS.md`).

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. Keep VBAT always-on (status quo) | Rely on A7670's own PWRKEY-controlled sleep/off states. SIMCom's datasheet gives an explicit power-off leakage spec: **IVBAT (power-off) = 20 µA typical** (Table 8, `A7670X_HW.pdf`). | Zero added parts; simpler power-on sequence (see ADR-006); matches most SIMCom reference designs; 20 µA floor whenever the battery is connected, even in the deepest "off" state. |
| B. Add a load switch on VBAT_MODEM | Insert a switch rated for the A7670's 2 A burst current between VSYS and VBAT_MODEM, controllable for a true hard-disconnect state. | Enables sub-20 µA total system sleep by fully removing VBAT; loses hot/warm-boot state; adds a new 2 A-rated part, more PCB area, and a new rail to sequence (interacts with ADR-003 and ADR-005). |

## Decision

**Option A — keep VBAT always-on.** No schematic change. SIMCom's documented 20 µA
power-off leakage is treated as the accepted sleep-current floor for RevA.

Rationale: 20 µA is small relative to a typical 1S battery's capacity (thousands of
mAh) and the design goal of "Lowest possible sleep current" (CLAUDE.md, Power Policy)
does not by itself justify the added cost/complexity/PCB area of a 2 A-rated switch
without a concrete capacity/runtime calculation showing 20 µA is unacceptable. Adding
a VBAT switch would also add another rail requiring coordination with the reset/
power-on architecture (ADR-005), increasing risk in exactly the area ADR-005 exists
to reduce.

## Consequences

- **Positive:** No new part, no new PCB area, no new sequencing risk. Matches SIMCom's
  own reference-design pattern for this family of modules.
- **Negative:** 20 µA continuous drain whenever the battery is connected, including in
  storage/shipping, is now an accepted constraint, not something the hardware can
  eliminate.
- **Revisit trigger:** If a battery capacity/runtime calculation (once the pack is
  selected per ADR-001) shows the 20 µA floor materially impacts shelf life or
  field-deployment runtime targets, this decision should be reopened and Option B
  reconsidered.

## References

- SIMCom `A7670X_HW.pdf`, Table 8 "VBAT pins electronic characteristic" — IVBAT
  (power-off leakage current) = 20 µA typical.
- SIMCom `A7670X_HW.pdf` §3.1.1 "Power Supply Design Guide" — enable-pin
  recommendation.
- CLAUDE.md — Power Policy ("Lowest possible sleep current... always prioritize
  battery life").
- Engineering Change Proposal, ECP-4 (this conversation).

## Approval status

**APPROVED** — per user decision, this conversation. Subject to the revisit trigger
noted above once battery capacity is confirmed.
