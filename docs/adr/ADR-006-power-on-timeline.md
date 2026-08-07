# ADR-006: Power-On Timeline

## Context

No single documented timeline currently exists tying together: battery/USB present →
`VSYS` valid → PWRKEY assertion (ADR-003) → A7670 boot (`STATUS` high ~7 s, UART ready
~8 s, USB ready ~9 s, per SIMCom `A7670X_HW.pdf` Table 10) → GPIO2 available for GNSS
enable → `GNSS_3V3` sequencing (ADR-004) → watchdog (U8) coming alive on `VDD_1V8` →
U8's first POR/REXT-read window (100–120 ms, `~RST` low) → steady-state supervised
operation. This is the synthesis item across ADR-002 through ADR-005 and (once
unblocked) ADR-007.

## Problem

Without one shared, explicit timeline, each of ADR-002 through ADR-005's decisions
were verified against their own individual datasheet requirements, but never checked
against each other on a common clock. The specific, already-identified risk this
creates is the ADR-005 "simultaneous RESET+PWRKEY" violation — but other, as-yet
unidentified interactions may exist between, e.g., GPIO2's availability timing
(dependent on A7670 boot completion) and U7/GNSS turn-on, or between U8's periodic
WAKE cadence and any future firmware-driven sleep/wake cycling.

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. No integrated timeline; rely on each ADR's individual verification | Faster to "complete" on paper. | Leaves cross-ADR interaction risks unverified — exactly the class of risk ADR-005 was created to close for one specific case; doesn't generalize to catch others. |
| B. Produce a single power-on sequence diagram/table spanning all rails and control signals on one shared timeline, with margins against every datasheet minimum cited across ADR-001 through ADR-005 | Requires dedicated integration effort. | Surfaces interaction risks before implementation rather than after; becomes the acceptance artifact for the whole reset/power-on rework. |

## Decision

**Option B.** A single, explicit power-on sequence diagram/table must be produced
before ADR-003 or ADR-007 are implemented in KiCad. It must show, on one timeline:

- Battery/USB presence and `VSYS` rise
- PWRKEY assertion window (ADR-003, once sized)
- A7670 boot milestones (`STATUS`/UART/USB ready times, SIMCom Table 10)
- `VDD_1V8` availability and U8's POR/REXT-read window (100–120 ms)
- GPIO2 availability and `GNSS_PWR_EN`/`GNSS_3V3` turn-on (ADR-004)
- RESET assertion windows, both cold-boot-incidental (if any) and watchdog-triggered
  (ADR-007, once unblocked)

This is a documentation deliverable, not a schematic change, and does not itself
authorize any KiCad edit.

## Consequences

- **Positive:** Becomes the single acceptance reference for verifying ADR-003 and
  ADR-007 don't conflict with each other or with A7670/LC29H boot timing, before any
  component is placed.
- **Negative:** Adds a documentation step before implementation can begin; the
  diagram cannot be finalized until ADR-007 leaves Pending status, since the
  watchdog's actual reset behavior is one of the timeline's inputs.
- **Gating relationship:** This ADR's deliverable is a prerequisite for implementing
  ADR-003, and is fully completable only after ADR-007 is resolved.

## References

- SIMCom `A7670X_HW.pdf`, Table 10 "Power on timing and electronic characteristic."
- TI `tpl5010.pdf` Table 7.5, §8.3.3.
- Quectel `LC29H_Series_Hardware_Design_V1.2.pdf` §3.4.
- Engineering Change Proposal, ECP-7 (this conversation).
- ADR-003, ADR-004, ADR-005, ADR-007.

## Approval status

**APPROVED** as a required documentation deliverable. Cannot be fully completed until
ADR-007 resolves out of Pending status.
