# ADR-008: Recovery Architecture

## Status of ADR-007

**ADR-007 (Watchdog Strategy) implementation is suspended.** No OpenCPU research has
been performed for this document, per instruction. This ADR evaluates recovery
mechanisms at an architectural level, using only: (a) primary-source hardware facts
already verified during the Power Architecture Review and ECP-1 (SIMCom
`A7670X_HW.pdf`, TI `tpl5010.pdf`), and (b) general embedded-systems engineering
principles that hold regardless of SIMCom's specific OpenCPU API surface. Anywhere
this document would need an OpenCPU-specific fact I don't already have verified, it
is marked **Unknown — deferred to ADR-007**, not guessed.

## Context

RevA currently has exactly one recovery mechanism designed: a hardware watchdog
(U8/TPL5010) driving A7670's RESET pin, and it has a known timing defect (ADR-007,
Pending). Before continuing to fix that single mechanism, this ADR steps back and
asks whether a hardware watchdog is even the right primary layer, and what a
complete recovery strategy — covering firmware, protocol-stack, GNSS, and power-level
failures — should look like.

## Problem

A marine asset tracker is unattended for long periods. It must recover autonomously
from failures at every layer: application firmware, cellular protocol stack, GNSS
subsystem, and power delivery. No single recovery mechanism covers all of these.
Committing hardware design effort (ADR-007) to one layer before understanding the
full failure landscape risks under- or over-building that one layer relative to what
the complete system actually needs.

## Alternatives: Recovery Mechanisms Evaluated

### 1. Software Watchdog (firmware-internal timer)

| Attribute | Assessment |
|---|---|
| Detection method | A firmware timer/task must be periodically "kicked" by application logic; failure to kick within a timeout triggers a firmware-level recovery action (task restart, soft reboot request). |
| Recovery latency | Configurable in firmware, typically seconds. |
| Hardware required | None. |
| Firmware required | Yes — kick logic, ideally running independently of the task(s) being supervised. |
| Power impact | Negligible. |
| Complexity | Low. |
| Reliability | **Low-medium standalone.** Fundamental limitation (general RTOS/embedded principle, not SIMCom-specific): a pure software watchdog cannot recover from a failure that stops the scheduler/interrupt system itself, or from firmware that's alive enough to kick a naive "did the OS tick" watchdog while the actual application task is deadlocked. Only as reliable as what it actually checks. |
| Marine suitability | Necessary as a fast, cheap first layer for task-level hangs, but insufficient alone for an unattended marine deployment. |

### 2. OpenCPU Internal Recovery (platform-level exception/crash handling)

| Attribute | Assessment |
|---|---|
| Detection method | **Unknown — deferred to ADR-007.** Generally, platforms of this class catch hard faults/exceptions at the OS/kernel level; this is architecturally distinct from catching a silent deadlock (no fault occurs in a deadlock, so a pure exception handler class of mechanism does not generally catch it — a general property of this mechanism *class*, not a SIMCom-specific claim). |
| Recovery latency | Unknown. |
| Hardware required | None additional, if it exists. |
| Firmware required | Unknown — may require opt-in configuration. |
| Power impact | Negligible if present. |
| Complexity | Low from our side if it exists as a usable platform feature — unverified. |
| Reliability | Unknown magnitude; architecturally bounded to fault-detectable failures by the general nature of this mechanism class, not to logic deadlocks. |
| Marine suitability | Potentially a good complementary layer for crash-class failures once verified; must not be assumed to cover deadlock-class failures (TCP/MQTT hangs, GNSS timeout) without confirmation. |

### 3. Hardware RESET (external supervisor driving A7670's dedicated RESET pin)

| Attribute | Assessment |
|---|---|
| Detection method | Independent IC (currently U8/TPL5010) requires a periodic "alive" pulse (`DONE`) from firmware; absence triggers assertion of the RESET pin. |
| Recovery latency | Bounded by the supervisor's configured interval, plus the RESET pulse duration itself. **Verified defect:** TPL5010's `~RST` pulse is 320ms typical (TI `tpl5010.pdf` §7.5) vs. A7670's documented minimum RESET requirement of 2s (typ. 2.5s recommended, SIMCom `A7670X_HW.pdf` Table 12) — this is the ADR-007 gap, unresolved regardless of this ADR's outcome unless this layer is dropped from the final architecture. |
| Hardware required | Yes — external supervisor IC (already present) with correctly engineered pulse timing (pending). |
| Firmware required | Minimal in principle (periodic pulse), but the pulse-source task must genuinely represent whole-system health, not just "the RTOS tick is alive" — a common real-world watchdog-defeating implementation bug, independent of hardware correctness. |
| Power impact | TPL5010 IQ = 35nA typical (verified, TI `tpl5010.pdf` §7.5) — negligible. |
| Complexity | Medium — correct pulse-width engineering plus correct firmware "aliveness" semantics. |
| Reliability | **High for firmware/task-level hangs**, once the pulse-width defect is fixed — this is the only layer evaluated so far that is driven by silicon independent of the (possibly hung) A7670 itself. **Verified limitation:** U8 is currently powered from `VDD_1V8`, which is an A7670-*internal* output rail (SIMCom symbol data, previously confirmed `power_out`) — so if A7670 itself browns out or loses power, U8 loses power too. This mechanism cannot recover from a brownout as currently powered. |
| Marine suitability | Important layer for firmware hangs; not sufficient alone for brownout-class failures given its current power source. |

### 4. PWRKEY Restart (soft power-cycle via the module's PWRKEY pin)

| Attribute | Assessment |
|---|---|
| Detection method | Triggered by whichever layer decides recovery is needed (software watchdog, external supervisor, or firmware logic) — not a detector itself. |
| Recovery latency | SIMCom's power-off sequence requires PWRKEY held low ≥2.5s (Table 11, `Toff`), then a full cold power-on sequence (`Ton(status)`≈7s, `Ton(uart)`≈8s, `Ton(usb)`≈9s, Table 10) — roughly **10-12+ seconds total** for a full cycle. |
| Hardware required | An automatic drive circuit (subject of ADR-003; currently only a manual test point exists). |
| Firmware required | Logic to decide when a full restart (vs. a lighter recovery) is warranted. |
| Power impact | Transient only, negligible beyond the cycle's own duration. |
| Complexity | Low-medium (shared with ADR-003's implementation). |
| Reliability | **Good, and explicitly preferred by SIMCom for planned recovery over RESET pin:** "It is strongly recommended that the customer use PWRKEY or 'AT+CPOF' to shut down" (`A7670X_HW.pdf` §3.2.2), while the RESET pin is explicitly scoped as an *emergency-only* path: "It is recommended to use the reset pin only in case of emergency, such as the module is not responding" (same doc, Table 12 note). This is a direct, verified manufacturer preference ordering between mechanisms 3 and 4. |
| Marine suitability | Strong candidate for the primary "module not responding but not fully dead" recovery path; shares the same brownout blind spot as mechanism 3 if its trigger circuit depends on an A7670-derived rail. |

### 5. VBAT Power Cycle (full battery-rail removal/reapplication)

| Attribute | Assessment |
|---|---|
| Detection method | Requires a supervisor independent of A7670 entirely (referenced to VSYS/battery, not any A7670-generated rail) — RevA currently has no such element; ADR-002 explicitly chose an always-on VBAT architecture with no switch. |
| Recovery latency | Longest of all options evaluated — full cold boot from true power-off, plus whatever off-dwell time the strategy uses. |
| Hardware required | A 2A-rated load switch (previously declined under ADR-002) plus a battery-referenced supervisor — a materially bigger hardware lift than any other option here. |
| Firmware required | None for the cycle itself if hardware-autonomous; firmware could also request it. |
| Power impact | The switch + independent supervisor add continuous quiescent draw — **directly in tension with this ADR's priority #2 (battery life)** and with ADR-002's already-approved decision. |
| Complexity | High — reopens ADR-002, new parts, new independent power domain to design. |
| Reliability | **Highest of all options** — the only mechanism that can recover from any state, including scenarios where mechanisms 3/4 are themselves powered-down or non-functional, because it acts at the true power source. |
| Marine suitability | Most robust in the abstract, but its cost/complexity/battery-life impact make it unsuitable as a primary or frequent-use layer; better suited as a rare, last-resort layer if included at all. |

### 6. External Watchdog (supervisor powered independently of A7670's own output rails)

| Attribute | Assessment |
|---|---|
| Detection method | Same DONE-pulse-timeout concept as mechanism 3, but critically **powered from `VSYS` or `VBAT` directly, not `VDD_1V8`.** |
| Recovery latency | Same class as mechanism 3. |
| Hardware required | Either a new supervisor IC, **or** — the lower-cost option — repowering the *existing* U8 from `VSYS` instead of `VDD_1V8`. This is a modest change relative to mechanism 5's full redesign. |
| Firmware required | Same DONE-feed requirement as mechanism 3. |
| Power impact | Small additional continuous draw, same nA-class order of magnitude as TPL5010's existing 35nA if the same part is simply repowered. |
| Complexity | **Medium, but notably lower than mechanism 5** for a similar reliability gain in the specific brownout scenario, since it can potentially reuse the already-selected U8 rather than adding new silicon and a new switched domain. |
| Reliability | **High, and specifically closes the brownout gap that mechanism 3 (as currently wired) cannot** — VSYS is upstream of A7670's own internal regulators, so it survives an A7670-internal brownout that collapses `VDD_1V8`. |
| Marine suitability | **Strong candidate — likely the best reliability-per-unit-complexity option among the independent-recovery mechanisms.** |

### 7. Combined / Layered Recovery Strategy

Not a single mechanism — the synthesis of the above. See **Decision**, below.

---

## Failure Mode Coverage Matrix

Legend: **✓** = primary/effective layer for this failure · **~** = partial or secondary coverage · **✗** = not applicable / cannot address · **?** = Unknown, deferred to ADR-007 (OpenCPU-specific) · *(note)* = important caveat

| Failure mode | SW Watchdog | OpenCPU Internal | HW RESET (mech. 3) | PWRKEY Restart | VBAT Cycle | External WD (mech. 6) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| OpenCPU firmware lock | ~ *(only if scheduler alive)* | ? | ✓ | ✓ | ✓ | ✓ |
| LTE registration timeout | ✓ *(firmware retry/backoff is the real fix)* | ✗ | ~ *(last resort only)* | ~ | ✗ | ~ |
| PDP activation failure | ✓ *(firmware retry logic, not a reset event)* | ✗ | ~ | ~ | ✗ | ~ |
| TCP deadlock | ~ *(if the right task is monitored)* | ? | ✓ | ✓ | ✓ | ✓ |
| MQTT deadlock | ~ | ? | ✓ | ✓ | ✓ | ✓ |
| GNSS timeout | ✗ *(needs its own detection — firmware UART/NMEA timeout, not A7670 watchdog)* | ✗ | ✗ *(resets modem, not GNSS)* | ✗ | ✗ | ✗ |
| SIM removal | ✗ *(this is a hardware event via USIM_DET pin, not a hang — needs a firmware event handler, not a reset)* | ✗ | ✗ | ✗ | ✗ | ✗ |
| Brownout | ✗ | ? | ✗ *(verified: loses power alongside A7670)* | ✗ *(same power dependency)* | ✓ | ✓ *(if repowered from VSYS)* |
| Flash corruption | ~ *(detects the symptom — boot loop/hang — not the cause)* | ? | ~ *(same)* | ~ *(same)* | ~ *(same)* | ~ *(same — none can repair corrupted flash; needs firmware-level image redundancy)* |
| Memory exhaustion | ~ | ? | ✓ | ✓ | ✓ | ✓ |
| Boot loop | ✗ *(can make this WORSE without backoff logic — see Decision)* | ? | ✗ *(same risk)* | ✗ *(same risk)* | ✗ *(same risk)* | ✗ *(same risk)* |
| Unexpected reset (diagnostic classification) | ✗ *(not a recovery target — a logging/diagnostic need)* | ? | ✗ | ✗ | ✗ | ✗ |

**Key observations from the matrix:**
- No single mechanism covers every failure mode — confirms the premise of this ADR.
- Network/protocol failures (LTE registration, PDP activation) are primarily **firmware retry-logic problems**, not reset-hardware problems; escalating straight to a hardware reset for these is disproportionate and should be a last resort, not the first response.
- GNSS timeout and SIM removal are **architecturally distinct** — they need their own, separate handling (LC29H's own `RESET_N`, and a USIM_DET interrupt handler respectively), not coverage from A7670's recovery chain.
- Brownout is the one failure mode where mechanism 3 (as currently wired) provides **zero** coverage — this is the strongest evidence for mechanism 6 (externally-powered watchdog) over the status quo.
- Boot loop is a **hazard multiplier**, not just another row — any of the reset-capable mechanisms (3/4/5/6), applied naively without escalating backoff, can turn a single failure into a rapid, battery-draining crash-reset cycle. This must be an explicit design requirement on the final architecture, not an assumed side effect of "having a watchdog."
- Flash corruption cannot be *fixed* by any of the recovery mechanisms evaluated here — only firmware-level image redundancy can address it; all this ADR's mechanisms can do is detect the resulting symptom.

---

## Decision: Recommended Layered Recovery Architecture

Prioritized per instruction: **(1) reliability, (2) battery life, (3) low hardware
complexity, (4) maintainability.**

**Layer 0 — Firmware-level, proportionate response (no hardware, out of scope for
KiCad but a required architectural expectation on firmware):** LTE registration
timeout and PDP activation failure should be handled by firmware retry/backoff logic
first. SIM removal is a hardware-interrupt-driven graceful-degradation event, not a
reset trigger. GNSS timeout should trigger LC29H's own `RESET_N` (100ms per Quectel,
ADR-004), not A7670's recovery chain. This layer resolves the failure modes that a
reset-based approach would handle disproportionately or not at all.

**Layer 1 — Software watchdog (mechanism 1):** Fast, free, first line of defense
against task-level hangs (TCP/MQTT deadlock, memory exhaustion) while the RTOS
scheduler is still alive. Cheapest possible layer; catches the common case quickly
without waiting for a slower external layer.

**Layer 2 — Externally-powered hardware watchdog (mechanism 6, not mechanism 3 as
currently wired):** The recommended fix for ADR-007, once resumed, is not merely
correcting TPL5010's RESET pulse width, but **also repowering U8 from `VSYS` instead
of `VDD_1V8`**, so this layer survives an A7670-internal brownout and can independently
assert a correctly-timed RESET when Layer 1 fails to escalate (e.g., because the
scheduler itself is down). This directly addresses the matrix's starkest gap
(brownout) at materially lower complexity/cost than mechanism 5, satisfying
priorities 1 and 3 together.

**Layer 3 — PWRKEY restart (mechanism 4), preferred over repeated RESET-pin
assertion:** Per SIMCom's own explicit guidance, RESET is an emergency-only
mechanism and PWRKEY/`AT+CPOF` is the recommended path for planned power-cycling.
If Layer 2's RESET-triggered recovery fails to bring the module back within N
attempts, escalate to a full PWRKEY power-cycle rather than repeatedly hammering
RESET — this matches the manufacturer's own preference ordering and gives a
materially more thorough recovery (full re-init) at a modest additional time cost.

**Layer 4 — VBAT power cycle (mechanism 5): explicitly NOT recommended as a
standard layer.** Given priority 2 (battery life) and priority 3 (low hardware
complexity), the added always-on quiescent draw and new switched-power hardware
required for this layer are not justified when Layer 2 (repowered from VSYS) already
closes the brownout gap that would otherwise be VBAT-cycle's unique justification.
Recommend **not** implementing this layer for RevA; revisit only if field data from
prototype units shows Layers 1-3 are insufufficient.

**Boot-loop protection (cross-cutting requirement on Layers 2-3):** Whatever
firmware implements the DONE-feed and PWRKEY-escalation logic must include a
non-volatile reset counter with backoff (e.g., escalating delay or falling back to a
minimal/safe mode after N rapid reset cycles) — without this, layering 2 and 3 as
described risks turning a single fault into a fast, battery-draining crash loop,
which the matrix identifies as a hazard multiplier, not a minor detail.

**Layer 5 — OpenCPU internal recovery (mechanism 2):** Treated as an unverified
*bonus* layer, not a planned/relied-upon one, until ADR-007 resumes and its actual
capabilities are confirmed. Do not architect Layers 1-4 assuming it exists or
behaves any particular way.

**Diagnostics (maintainability, priority 4):** Whatever reset-reason information the
platform can provide (post-mortem classification of *why* a reset happened — Layer 0
retry, watchdog Layer 1/2, or PWRKEY Layer 3) should be logged/reported once
connectivity is restored — an "Unexpected reset" event is a diagnostic requirement
threaded through every other layer, not a mechanism of its own.

## Consequences

- **Positive:** This architecture explicitly avoids over-investing in the highest-cost,
  highest-battery-impact mechanism (VBAT cycle) while still closing the most severe
  verified gap (brownout) at low incremental cost by repowering existing hardware
  (U8) rather than adding new hardware. It also correctly routes network/protocol
  failures to firmware retry logic instead of disproportionate hardware resets, and
  separates GNSS/SIM handling from the modem's own recovery chain.
- **Negative / open items:** This ADR does not resolve ADR-007's pulse-width defect —
  it changes the target design (repower U8 from VSYS *and* fix the pulse width)
  rather than closing the ticket. Several matrix cells remain genuinely Unknown
  (OpenCPU internal recovery's actual behavior) until ADR-007 resumes. Boot-loop
  backoff logic is a firmware requirement this ADR imposes but cannot itself satisfy
  (firmware implementation remains blocked by CLAUDE.md's ERC-first policy anyway).
- **Effect on ADR-007:** ADR-007 may resume once this ADR is approved, but its scope
  is now expanded from "fix the RSTn pulse width" to "fix the pulse width AND
  evaluate repowering U8 from VSYS," per Layer 2 above.

## References

- SIMCom `A7670X_HW.pdf`, Table 10 (power-on timing), Table 11 (power-off sequence,
  `Toff` ≥2.5s), Table 12 (RESET pin, `Treset` ≥2s/2.5s typ.), §3.2.2 ("strongly
  recommended... use PWRKEY or 'AT+CPOF'"), §3.2.3 ("recommended to use the reset pin
  only in case of emergency, such as the module is not responding"), §3.2.2 (listing
  "Over-voltage or under-voltage automatic power off" as a native A7670 shutdown
  method).
- TI `tpl5010.pdf` §7.5 (IDD 35nA typical, tRSTn 320ms typical), §8.3.3 (RSTn
  behavior).
- Quectel `LC29H_Series_Hardware_Design_V1.2.pdf` §4.2.2 (RESET_N ≥100ms).
- ADR-002 (VBAT Always-On Architecture) — the prior decision this ADR's Layer 4
  recommendation is consistent with, not a proposal to reopen it.
- ADR-004 (GNSS Power Sequencing) — LC29H reset handling referenced in Layer 0.
- ADR-007 (Watchdog Strategy, Pending) — this ADR's direct predecessor/blocker.
- General embedded-systems watchdog/supervisor design principles (mechanism-class
  reasoning for software watchdog and exception-handler limitations) — not vendor-
  specific, standard practice, not sourced from a single citable document.

## Approval status

**PENDING APPROVAL.** Per instruction, ADR-007 remains suspended and no OpenCPU
research is to be performed until this ADR (ADR-008) is approved. Once approved,
ADR-007's scope is updated per the "Effect on ADR-007" consequence above before its
research phase resumes.
