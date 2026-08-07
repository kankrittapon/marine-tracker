# ADR-009: External Watchdog Justification

## Status of ADR-007

**ADR-007 is suspended again.** This ADR answers a more fundamental question than
ADR-007's "how should the watchdog be wired": whether any external
watchdog/supervisor hardware is justified at all, before any wiring, pulse-width, or
power-domain decision is made. ADR-007 does not resume until this ADR is approved.

## Context

The prior session converged on a specific hardware fix (repower/split U8's role
across two domain-appropriate ICs) without first establishing, from a clean-sheet
comparison, whether external hardware is the right answer at all versus a
firmware-only approach. This ADR corrects that ordering: it evaluates necessity
before implementation.

## Problem

Every external IC added to RevA costs sleep current, PCB area, BOM cost, sourcing
risk, and long-term maintainability burden — all things `CLAUDE.md`'s Power Policy,
Component Policy, and Manufacturing Policy explicitly ask to minimize. Before
committing any of that budget to watchdog/supervisor hardware, the actual failure
landscape (established in ADR-008) must be checked against what firmware alone can
and cannot cover. If firmware alone is sufficient, no hardware should be added. If
not, the *specific* gap firmware cannot close should drive exactly how much hardware
is justified — no more, no less.

## Method

This ADR reuses ADR-008's 12 failure modes for the FMEA and evaluates 5 candidate
architectures against 12 engineering dimensions. Where a dimension requires a
specific component's data (IQ, price, LCSC stock), and no specific part has been
selected/verified in this session, it is marked **Needs Verification** rather than
estimated — consistent with this project's no-guessing rule for component values.
General reliability/architecture reasoning (e.g., "a hung scheduler cannot run its
own recovery code") is treated as established embedded-systems principle, not a
datasheet claim, and is labeled as such.

## Alternatives: Architecture Comparison

| Dimension | A. Firmware only | B. Firmware + TPL5010 | C. Firmware + Supervisor IC | D. Firmware + Supervisor + Watchdog | E. Alternative modern (combined) solution |
|---|---|---|---|---|---|
| Reliability | Low for full lockup/brownout — nothing runs to detect or act (general principle) | Medium-high for firmware/task hangs once pulse-width is fixed (ADR-007); **zero for brownout** (verified: U8 powered from `VDD_1V8`, an A7670-internal rail) | High for brownout/voltage-fault class; **zero for firmware-hang class** (a voltage supervisor has no concept of "is the application logic stuck") | Highest of the realistic, currently-specified options — each fault class covered by the mechanism naturally suited to it | Potentially equal to D in a single part — **unverified**, no specific part researched this session |
| Brownout handling | None | None (verified — same power domain as A7670 itself) | Yes, if the supervisor is VSYS/VBAT-referenced (not VDD_1V8) | Yes (via the supervisor element) | Needs Verification — depends on the specific part's own supply pin |
| Firmware complexity | Same baseline complexity as all other options (software watchdog task, retry/backoff logic) — this cost exists regardless of hardware choice | Baseline + DONE-feed logic | Baseline only (no feed protocol needed for a pure voltage supervisor) | Baseline + DONE-feed logic | Depends on part; likely similar to D |
| Hardware complexity | None | Low (1 IC, already in BOM, already documented) | Low (typically a 3-5 pin voltage supervisor) | Medium (2 small ICs + passives) | Needs Verification |
| PCB area | None | Small (existing footprint) | Small | Small-medium (two small footprints) | Potentially smaller than D if genuinely combined — Needs Verification |
| Sleep current | Best possible (zero added) | TPL5010 IQ = 35nA typical (verified, `tpl5010.pdf` §7.5) | Typically nA-class for a basic supervisor — **Needs Verification**, no specific part sourced yet | Sum of B + C, still very low order of magnitude if reasonable parts are chosen — Needs Verification for the exact sum | Needs Verification |
| Component count | 0 added | ~7 (U8 + R21/R22/R23 + decoupling, already placed) | Low (supervisor + 1-2 passives) — Needs Verification | Highest among specified options | Potentially lowest of B/C/D if one part replaces two — Needs Verification |
| BOM cost | $0 | Low — TPL5010 already selected/priced | Needs Verification | Sum of B + C — Needs Verification | Needs Verification |
| LCSC availability | N/A | **Needs Verification** — TPL5010 is a TI part; availability/pricing as an LCSC/JLCPCB line item not confirmed this session | Needs Verification — no specific part chosen | Needs Verification (both parts) | Needs Verification |
| Marine suitability | Poor specifically for unattended-failure recovery (no physical access assumed in the field) | Good for firmware-hang class only | Good for brownout class only | Best coverage of the identified failure landscape among specified options | Potentially equal to D — unverified |
| Production risk | Lowest (nothing new to qualify) | Low-medium (single point of failure: TPL5010 itself; still needs the pulse-width fix to be production-worthy) | Low (simple part class, but unselected) | Moderate (two parts to qualify instead of one) | Needs Verification (new part class to qualify) |
| Maintainability | Simplest hardware-wise, but pushes all risk onto firmware validation, which is harder to exhaustively test for edge cases | Well precedented — extensively documented in this project's own history (ADR-007, ECP-1, Power Architecture Report) | Simple in isolation, undocumented in this project | More moving parts to document than B or C alone, but each is individually simple | Fewer parts than D, but a wholly new part to document from scratch |

## FMEA — Recovery Capability by Failure Mode

| Failure mode | Can firmware recover? | Can hardware recover? | Is external hardware required? |
|---|---|---|---|
| OpenCPU firmware lock | Partial — only if the scheduler itself is still alive and only the offending task is stuck (software watchdog can restart a task, not revive a dead scheduler) | Yes — an independent watchdog (DONE-timeout class) recovers regardless of the internal cause | **Yes**, for the full-lockup case; software watchdog alone is not sufficient for a scheduler-level freeze |
| LTE registration timeout | Yes — protocol-layer condition, module is not hung, firmware retry/backoff is the correct and sufficient response | N/A — wrong tool for this failure mode | No |
| PDP activation failure | Yes — same reasoning as LTE registration | N/A | No |
| TCP deadlock | Partial — software watchdog can catch it only if it's monitoring the actually-relevant task and the scheduler is still running | Yes — watchdog-timer class catches it via DONE-timeout regardless | **Yes**, as a backstop behind firmware's first attempt (matches ADR-008's Layer 1→Layer 2 escalation) |
| MQTT deadlock | Partial — same reasoning as TCP deadlock | Yes | **Yes**, as a backstop |
| GNSS timeout | Yes — firmware detects via UART/NMEA timeout and recovers via LC29H's own `RESET_N` (ADR-004's path, not part of the A7670-recovery chain this ADR evaluates) | N/A to this ADR's scope | No — already a separately-handled path |
| SIM removal | Yes — hardware event (USIM_DET interrupt) handled by a firmware event handler, not a hang requiring reset | N/A — not a hang | No — the pin already exists; no *new* hardware needed for this ADR's question |
| Brownout | **No** — by definition, firmware execution (and the software watchdog checking it) is what's absent or failing | Yes, but **only** if that hardware is independently powered — i.e., not referenced to `VDD_1V8` (verified: A7670-internal rail) | **Yes** — this is the one failure mode with zero firmware-only coverage by physical necessity, and the one existing-hardware element (U8/TPL5010) also cannot cover it as currently powered |
| Flash corruption | Partial — can detect the resulting symptom (boot failure) *if* an image/CRC-check strategy exists; cannot repair corruption itself | Partial — can detect the resulting hang/boot-loop symptom; cannot repair flash | No, not for the corruption itself (needs firmware-level image redundancy, out of this ADR's scope); the resulting symptom is covered by the same hardware as "Boot loop," below |
| Memory exhaustion | Partial — same class as TCP/MQTT deadlock | Yes | **Yes**, as a backstop |
| Boot loop | Partial/risky — a naive watchdog layered without persistent-counter backoff logic can make this *worse* (established in ADR-008); this specific protection is a firmware requirement regardless of which hardware architecture (A-E) is chosen | Not sufficient alone, for the same reason | Hardware does not resolve this by itself either way — firmware backoff logic is mandatory regardless of the architecture chosen elsewhere in this ADR |
| Unexpected reset (diagnostic classification) | Yes, if reset-cause is queryable (**Needs Verification** — deferred to ADR-007's OpenCPU research) | N/A — this is a logging/diagnostic need, not a recovery action | No |

## Decision

**External hardware beyond firmware alone is justified — specifically, and only, for
two disjoint reasons revealed by the FMEA, not because "more hardware is generally
more reliable":**

1. **Brownout / A7670 self-shutdown has zero firmware-only coverage, by physical
   necessity.** This alone justifies at minimum an independently-powered (VSYS/VBAT-
   referenced) supervisor element — Architecture C's core capability.
2. **Task/protocol-deadlock-while-powered (OpenCPU lock, TCP/MQTT deadlock, memory
   exhaustion) benefit from a hardware backstop because a purely firmware-internal
   software watchdog has a well-known structural limitation: it cannot recover from
   a failure that also takes down the mechanism doing the recovering** (the scheduler
   itself). This justifies at minimum a watchdog-timer element — Architecture B's
   core capability — as a *second* line of defense behind firmware's own first
   attempt (per ADR-008's Layer 0/1 ordering), not as a replacement for it.

**Neither capability subsumes the other.** A supervisor alone (C) does not detect a
powered-but-stuck firmware; a watchdog-timer alone (B), as currently wired, does not
survive the one scenario that most needs it. This is why **Architecture D** (or its
single-part equivalent, E, if a suitable part is verified) is the recommended
direction — justified by the FMEA's disjoint coverage of two genuinely separate
failure classes, not by a general preference for more hardware.

**Architecture A (firmware only) is rejected** specifically and only because of the
Brownout row of the FMEA — every other row has at least partial firmware coverage,
but brownout has none, and CLAUDE.md's "High reliability" design goal combined with
the marine/unattended-deployment context (`PROJECT_BRIEF.md`) makes an unrecoverable
failure mode with no field-accessible remedy unacceptable to leave entirely
uncovered.

**Architecture E is not rejected, but not yet selectable** — no specific combined
supervisor+watchdog part has been researched against primary documentation this
session. It should be evaluated as a genuine candidate for reducing D's part
count/PCB area during ADR-007's resumed work, provided it can be verified to
independently satisfy both the Brownout row and the deadlock-backstop row of this
FMEA — the bar is the FMEA coverage, not the part count.

**This ADR deliberately does not specify wiring, pulse widths, power-domain
assignment for specific pins, or a selected part number for any option.** That is
ADR-007's job, once resumed.

## Consequences

- **Positive:** Hardware scope is now justified against a specific, disjoint pair of
  uncoverable failure modes rather than assumed. This gives ADR-007 a narrower,
  better-justified mandate: solve exactly these two gaps, not "build a general
  watchdog."
- **Negative / open items:** Several dimensions remain Needs Verification (LCSC
  availability and IQ for any specific supervisor part, and Architecture E's
  viability entirely) — ADR-007's resumed work must close these before finalizing
  a bill of materials.
- **Effect on ADR-007:** Scope is now: (a) confirm/select a supervisor element
  satisfying the Brownout row, independently powered from VSYS/VBAT; (b) fix
  TPL5010's (or equivalent watchdog-timer element's) RESET pulse-width defect for
  the deadlock-backstop row; (c) evaluate whether a single Architecture-E part can
  satisfy both before finalizing two separate ICs. The specific wiring/voltage-
  domain-compatibility work already reasoned through in the prior (suspended)
  session remains valid input for step (b) once ADR-007 resumes, but is not restated
  or re-approved here.

## References

- ADR-008 (Recovery Architecture) — source of the 12 failure modes and the original
  Layer 0-5 escalation ordering this ADR's FMEA is built on.
- TI `tpl5010.pdf` §7.5 — IDD = 35nA typical (Architecture B's verified sleep-current
  figure).
- SIMCom `A7670X_HW.pdf` — `VDD_1V8` as an A7670-internal LDO output (basis for the
  verified Brownout-row finding that U8, as currently wired, cannot cover brownout).
- `CLAUDE.md` — Power Policy, Component Policy, Manufacturing Policy (basis for
  treating added hardware as a cost to justify, not a default).
- `docs/PROJECT_BRIEF.md` — unattended marine deployment context (basis for
  rejecting Architecture A on the Brownout row alone).
- General embedded-systems watchdog/supervisor architecture principles (scheduler-
  level lockup reasoning) — standard practice, not sourced from a single citable
  document, labeled as such throughout.

## Approval status

**PENDING APPROVAL.** ADR-007 remains suspended until this ADR is approved. Once
approved, ADR-007 resumes under the narrowed scope defined in "Effect on ADR-007"
above.
