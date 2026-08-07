# ADR-005: Coordinated Reset Architecture

## Context

RevA has three independent reset/power-control paths: A7670 `RESET` (hard reset,
driven by U8/TPL5010, timing mismatch pending under ADR-007), A7670 `PWRKEY` (soft
power on/off, currently unautomated, addressed by ADR-003), and LC29H `RESET_N`
(GNSS reset). These have been designed as separate point solutions, not as a
coordinated system.

## Problem

SIMCom `A7670X_HW.pdf` states: **"It is forbidden to pull down both RESET key and
PWRKEY to power on the module at the same time."** If ADR-003's automatic PWRKEY
one-shot and U8's own POR/REXT-read window (which holds `~RST` low for 100–120 ms at
every `VDD_1V8` power-up, per TI `tpl5010.pdf` Table 7.5) are implemented as
independent, uncoordinated circuits, they risk overlapping at cold boot — directly
violating this documented constraint.

Separately, Quectel's LC29H has its own, much more forgiving reset requirement
(`RESET_N` low for **≥ 100 ms**, `LC29H_Series_Hardware_Design_V1.2.pdf` §4.2.2, "An
OC driver circuit... is recommended to control the RESET_N pin") — LC29H's reset does
not share A7670's 2.5 s timing problem and does not need to be part of the same
timing-critical fix, but should still be accounted for in the same coordinated
picture so GNSS resets aren't triggered unexpectedly by the same events that reset
the modem.

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. Design each reset/power-on circuit independently | ADR-003 (PWRKEY) and ADR-007 (watchdog reset stretch, pending) implemented as separate point fixes. | Simpler per-block design; real risk of violating SIMCom's explicit "forbidden simultaneous" condition at cold boot — not acceptable given it's a documented hard constraint, not a guess. |
| B. Design a single coordinated power-sequencing block | PWRKEY's power-on pulse (ADR-003) and RESET's behavior (ADR-007, once unblocked) are designed together against one shared timeline, explicitly ensuring U8's POR/REXT-read window and the auto-PWRKEY assertion window never coincide. | More upfront timing analysis; eliminates the interaction risk by construction rather than by hope. |

## Decision

**Option B — coordinated design.** ADR-003 (automatic PWRKEY) and ADR-007 (watchdog
reset strategy, currently Pending) must be designed and timing-verified together, not
as isolated circuits. LC29H's `RESET_N` path is included in the same coordinated
timeline for completeness, though its 100 ms requirement is not the binding
constraint (A7670's 2.5 s RESET requirement, under ADR-007, is).

This decision does not itself resolve ADR-007 — it establishes the *process*
constraint that ADR-007, once unblocked, must be integrated with ADR-003 rather than
implemented standalone.

## Consequences

- **Positive:** Eliminates the specific, named datasheet violation risk
  ("forbidden simultaneous RESET+PWRKEY assertion") by design rather than by
  post-hoc testing.
- **Negative:** Implementation of ADR-003 cannot be finalized independently of
  ADR-007's resolution — the two are now formally linked, which may delay ADR-003's
  implementation until ADR-007 is unblocked (OpenCPU/A7670 recovery-option research,
  see ADR-007).
- **Deliverable:** The combined timeline required by this decision is produced under
  ADR-006 (Power-On Timeline).

## References

- SIMCom `A7670X_HW.pdf` §3.2.2/§3.2.3 — "It is forbidden to pull down both RESET key
  and PWRKEY to power on the module at the same time."
- TI `tpl5010.pdf` §8.3.3 "RSTn," Table 7.5 — POR/REXT-read window, 100–120 ms,
  `~RST` low during this period.
- Quectel `LC29H_Series_Hardware_Design_V1.2.pdf` §4.2.2 "RESET_N" — ≥100 ms low
  pulse requirement, OC driver recommendation.
- Engineering Change Proposal, ECP-6 (this conversation).
- ADR-003 (Automatic PWRKEY), ADR-007 (Watchdog Strategy, Pending).

## Approval status

**APPROVED** as an architectural/process constraint. Implementation is blocked on
ADR-007 leaving Pending status (see ADR-006 for the resulting sequencing dependency).
