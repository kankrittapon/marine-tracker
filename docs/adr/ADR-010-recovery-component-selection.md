# ADR-010: Recovery Component Selection

## Status of ADR-007

**Superseded by ADR-007's decided status.** This ADR selected TPL5010 (retained)
+ TPS3839 (added) for the watchdog and brownout-supervision functions.
ADR-007 has since resumed and closed the remaining wiring/timing gap (the RESET
pulse-stretcher, TPS3808G09) using the same component-search rigor established
here — see `docs/adr/ADR-007-watchdog-strategy.md` for that follow-on selection and
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` for the full, combined BOM.

## Context

ADR-009 established *why* external hardware is justified (two disjoint failure
classes: brownout, which needs an independently-powered supervisor, and
powered-but-stuck firmware, which needs a watchdog timer) without naming parts. This
ADR does the part selection, explicitly without assuming the incumbent TPL5010 is
the answer.

## Problem

Committing to specific silicon before comparing it against real alternatives risks
carrying forward a component choice made for reasons (already in the BOM, already
documented) that aren't actually engineering requirements. `CLAUDE.md`'s Component
Policy also requires preferring LCSC/JLCPCB-available, non-obsolete parts — this
needs to be checked, not assumed, for every candidate including the incumbent.

## Required functions

Defined and detailed in `docs/COMPONENT_SELECTION_MATRIX.md`: (1) independent
watchdog, (2) brownout supervision, (3) recovery trigger, (4) low sleep current,
(5) marine reliability. No candidate is scored against anything outside these five
functions plus the supporting engineering attributes the user specified (supply
voltage, voltage domains, sleep current, package, PCB area, cost, LCSC availability,
vendor support, long-term availability, failure modes, marine suitability).

## Alternatives: Candidates evaluated

Full comparison and the weighted decision matrix are in
`docs/COMPONENT_SELECTION_MATRIX.md`. Summary of what was researched, from primary
manufacturer datasheets wherever accessible this session:

- **Single-chip solutions:** TPS3813xxx (TI, window-watchdog + supervisor — primary
  datasheet obtained and extracted), MAX16152-155 (ADI/Maxim, nanopower combined
  supervisor+watchdog — primary datasheet **inaccessible this session**, see note
  below), MAX823/824/825 (ADI/Maxim — same access issue), MCP1316 family (Microchip
  — secondary-source specs, but LCSC pricing/stock independently verified).
- **Watchdog-only ICs:** TPL5010 (TI, incumbent — primary datasheet re-verified this
  session), MAX6369-MAX6374 (ADI/Maxim — access issue).
- **Supervisor-only ICs:** TPS3839/TPS383x family (TI — primary datasheet obtained
  and extracted).
- **Two-chip / hybrid implementations:** TPL5010 + TPS3839, evaluated as a combined
  architecture, not two independent scores.

**Primary-source access note:** Analog Devices/Maxim's datasheet server
(`analog.com`) refused or timed out every fetch attempt this session (both a direct
download and a `WebFetch` product-page request hung on TLS renegotiation and
returned zero bytes). This is reported honestly as an access failure for this
session, not as evidence against those parts. All ADI/Maxim and Microchip figures in
the comparison are marked 🟡 Needs Verification and are capped at a maximum score of
3/5 on any criterion in the weighted matrix as a result — they are not scored as
inferior on their merits, only on unverifiability.

## Weighted decision matrix (summary — full worksheet in COMPONENT_SELECTION_MATRIX.md)

| Architecture | Weighted score (out of 5) |
|---|---:|
| TPL5010 alone (watchdog-only) | 3.45 |
| TPS3839 alone (supervisor-only) | 3.30 |
| TPS3813 alone (single-chip combo) | 3.30 |
| MAX16152-155 alone (single-chip combo) 🟡 | 2.75 |
| MAX823 alone (single-chip combo) 🟡 | 2.90 |
| MCP1316 alone (single-chip combo) 🟡 | 2.35 |
| MAX6369 alone (watchdog-only) 🟡 | 2.55 |
| **TPL5010 + TPS3839 (two-chip hybrid)** | **4.90** |

The hybrid wins on every individual weighted criterion, not just the total —
functional coverage, sleep current, voltage-domain safety, marine
reliability/single-point-of-failure, cost/availability, and maintainability all
independently favor it. This is a structural result of matching each of ADR-009's
two required capabilities to a part built specifically for that job, rather than
compromising on one part that does both adequately.

## Decision

**Recommended: two-chip hybrid — retain TPL5010 (TI) for the independent watchdog
function, and add TPS3839 (TI, TPS383x family) for the brownout supervision
function.**

This is not a default retention of the incumbent design:
- TPL5010 is retained because it **wins on verified merit** specifically on the two
  criteria that matter most for its role — lowest verified sleep current of any
  watchdog-capable candidate (35nA, vs. TPS3813's verified 9µA — a ~257× difference)
  and a resistor-programmable timeout range (100ms-7200s, `tpl5010.pdf`) that
  actually fits a multi-minute periodic-report application, unlike TPS3813's
  verified short/fixed watchdog window. It is not being kept because it was already
  there — TPS3813, its most directly comparable primary-verified single-chip
  alternative, was rejected on its own datasheet's numbers.
- TPS3839 is a **new addition**, not a historical carryover — selected because it is
  the only primary-verified candidate purpose-built for exactly the brownout-
  supervision role ADR-009 requires (150nA IQ, factory-trimmed threshold, valid
  reset behavior maintained down to VDD>0.6V, tiny 3-pin/4-pin package), and because
  its independence from `VDD_1V8` (it can be referenced to VSYS directly, unlike
  TPL5010 as currently wired) closes exactly the gap ADR-008 first identified.
  **Correction to this ADR's original text:** the exact threshold variant and the
  full worst-case nuisance-trip calculation were deferred at the time this ADR was
  first written (which incorrectly described the "K33" suffix as a "3.3V-threshold
  variant" — TI's real Device Options table, verified subsequently, shows
  **TPS3839K33's threshold is actually 2.93V typical**, not 3.3V). The corrected,
  fully-calculated selection is **TPS3839K33DBZR**, with the complete worst-case
  derivation in `docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md`.
- **Single-chip combo options are not recommended**, for two different reasons
  depending on which one: TPS3813 is disqualified on verified sleep current and
  timing-range grounds; the ADI/Maxim and Microchip combo options cannot be
  recommended this session because they could not be verified against primary
  documentation, and MCP1316 additionally carries a verified, concrete sourcing risk
  (91 units in stock, $0.64/unit on LCSC — notably worse than either TI part).

## Consequences

- **Positive:** Component selection is now justified against real, mostly
  primary-verified data rather than an assumed continuation of the existing BOM.
  Combined sleep current impact (185nA) remains negligible against the already-
  accepted 20µA VBAT-off floor (ADR-002). Each part's independent failure only
  removes one of the two required functions, not both — a genuine reliability
  improvement over any single-chip option.
- **Negative / open items:** MAX16152-155 in particular is a plausible competitive
  alternative to the TI two-chip pair (a genuine single-chip nanopower
  supervisor+watchdog, per its description) that could not be evaluated on equal
  footing this session due to a datasheet access failure, not a technical
  shortfall — this should be revisited if ADI's documentation becomes reachable,
  since a verified single-chip win would reduce part count/PCB area further.
- **Effect on ADR-007:** Resumes with parts now fixed (TPL5010 unchanged in role,
  TPS3839 added), narrowing its remaining scope to exactly: TPL5010's RESET
  pulse-width fix (the original defect), TPS3839's exact VSYS connection and its
  output's path into the recovery-trigger circuit (interacting with ADR-003's
  auto-PWRKEY design), and the full timing/state-machine documentation this whole
  investigation was building toward.

## References

- ADR-008 (Recovery Architecture) — origin of the two-failure-class framing.
- ADR-009 (External Watchdog Justification) — the five required functions and the
  FMEA this ADR's functional-coverage scoring is built on.
- TI `tpl5010.pdf` §7.5, line 1088 — IDD 35nA typ, VDD range 1.8-5.5V, 0.1µF X7R
  bypass recommendation, 6-pin SOT23 package (all re-verified this session).
- TI `tps3839.pdf` — IQ 150nA typ, VDD range 0.9-6.5V, valid reset for VDD>0.6V,
  200ms reset pulse typ, 3-pin SOT23/4-pin X2SON package (verified this session).
- TI `tps3813.pdf` — IDD 9µA typ, VDD range 2-6.5V, watchdog time-out upper limit
  ~2-3 (short/fixed window), 6-pin SOT23 (verified this session).
- LCSC Electronics — TPL5010DDCR/DDCT (C473912/C125800), TPS3839K33DBZR (C96333),
  MCP1316T-29LE/OT (C625214) pricing/stock, verified via search this session.
- `CLAUDE.md` — Component Policy (LCSC/JLCPCB preference, avoid obsolete/
  hard-to-source parts).

## Approval status

**APPROVED with engineering conditions** (threshold-variant correction above; full
worst-case calculation completed in the ADR-007 follow-on and
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md`).
