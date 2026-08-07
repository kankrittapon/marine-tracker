# ADR-003: Automatic PWRKEY Generation

## Context

The `PWRKEY` net currently has only a test point (TP9) and A7670 (U1) pin 1 attached
— no circuit exists to assert PWRKEY automatically. SIMCom's hardware design guide
specifies PWRKEY must be pulled active-low for **Ton ≥ 50 ms typical** to power the
module on (`A7670X_HW.pdf`, Table 10).

## Problem

Without an automatic drive circuit, the tracker cannot self-start after a battery
disconnect/reconnect (shipping, storage, field battery swap) — a human must
physically assert PWRKEY. This conflicts with the product's marine/field-deployment
intent (`PROJECT_BRIEF.md`: sealed IP67/IP68 enclosure) since a physical button may
not even be user-accessible once sealed.

A critical constraint from the same datasheet applies to any fix: **"It is forbidden
to pull down both RESET key and PWRKEY to power on the module at the same time"**
— any automatic PWRKEY circuit must be verified not to overlap with RESET assertion
at cold boot (see ADR-005).

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. Manual button only (status quo) | No hardware change. | Zero cost/complexity; device cannot self-start after power interruption — field-reliability risk. |
| B. RC power-on generator, actively driven | `VSYS` rise triggers an RC + transistor one-shot that pulls PWRKEY low for ~100–200 ms (comfortably above the 50 ms minimum), then releases. | Low parts count; simple, well-understood topology; must be timing-coordinated with U8's own POR window (ADR-005) to avoid the "simultaneous RESET+PWRKEY" violation. |
| C. Reuse TPL5010's WAKE output | TPL5010 (U8) already produces periodic WAKE pulses (20 ms typical). Gate this once at cold start to also drive PWRKEY. | WAKE is periodic for the device's whole life, not a one-time cold-start signal — would need additional gating logic to fire only once, net *more* complexity than Option B, not less. |
| D. Dedicated POR/supervisor IC | A small, purpose-built power-on-reset IC with fixed/programmable delay driving PWRKEY. | Same sourcing/verification burden as any new IC — no specific part has been verified against a datasheet in this session; not recommended without further research. |

## Decision

**Option B — RC-based active one-shot on PWRKEY**, structurally similar to (and a
candidate to share a component family with) the reset-stretch circuit under
consideration for ADR-007/ECP-1. Exact R/C and transistor values are a follow-up
sizing task, not decided by this ADR — this ADR approves the *architecture*
(active-driven RC one-shot), not final component values.

This circuit MUST be designed and verified alongside ADR-005 (Coordinated Reset
Architecture) so that its assertion window never coincides with U8's POR/REXT-read
`~RST`-low window (100–120 ms, per TPL5010 `tpl5010.pdf` §8.3.3).

## Consequences

- **Positive:** Enables unattended field operation and automatic recovery after power
  interruption, matching the product's field-deployment intent.
- **Negative:** Adds parts (transistor + 2–3 passives), adds PCB area (small, a few
  mm²), and introduces a new interaction risk with the RESET path that must be
  explicitly verified (not merely assumed safe) before implementation.
- **Dependency:** Implementation is gated on ADR-005's coordinated timeline being
  worked out first — do not implement ADR-003 in isolation.

## References

- SIMCom `A7670X_HW.pdf`, Table 10 "Power on timing and electronic characteristic"
  — Ton (PWRKEY active-low pulse) = 50 ms typical.
- SIMCom `A7670X_HW.pdf` §3.2.2/§3.2.3 — "It is forbidden to pull down both RESET key
  and PWRKEY to power on the module at the same time."
- TI `tpl5010.pdf` §8.3.3 "RSTn" and Table 7.5 — POR/REXT-read behavior, `~RST` held
  low during this window.
- Engineering Change Proposal, ECP-2 (this conversation).

## Approval status

**APPROVED** — architecture approved; component-level sizing and the ADR-005
coordination check must be completed before schematic implementation.
