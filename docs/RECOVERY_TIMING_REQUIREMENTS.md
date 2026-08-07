# Recovery Circuit Timing Requirements

Consolidated reference for every timing number governing RevA's watchdog/supervisor/
recovery circuitry (ADR-007, ADR-009, ADR-010). Every value is tagged Verified
(primary datasheet, quoted) or Needs Verification. See
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` for how these combine into the
actual BOM and `docs/adr/ADR-007-watchdog-strategy.md` for the worst-case derivation.

## A7670 (SIMCom `A7670X_HW.pdf`) — Verified

| Parameter | Min | Typ | Max | Unit | Source |
|---|---|---|---|---|---|
| PWRKEY active-low pulse to power on (Ton) | — | 50 | — | ms | Table 10 |
| Time to STATUS high (Ton(status)) | — | 7 | — | s | Table 10 |
| Time to UART ready (Ton(uart)) | — | 8 | — | s | Table 10 |
| Time to USB ready (Ton(usb)) | — | 9 | — | s | Table 10 |
| RESET active-low pulse to reset module (Treset) | 2.0 | 2.5 | — | s | Table 12 |
| PWRKEY active-low pulse to power off (Toff) | 2.5 | — | — | s | Table 11 |
| VBAT operating range | 3.4 | 3.8 | 4.2 | V | Table 8 |
| VBAT peak current | — | — | 2 | A | Table 8 |
| VBAT power-off leakage | — | — | 20 | µA | Table 8 |
| Max recommended VBAT ripple during 2A burst | — | — | 300 | mV | §3.1.1 (system design guidance, not a component spec) |
| Max parallel capacitance on PWRKEY/RESET pins | — | — | 100 | nF | §3.2.2 (exceeding this risks unintended auto power-on) |
| Special note: RESET pin also performs power-on function on the **very first** valid-supply event only; loses this function after first power-on | — | — | — | — | §3.2.3 |

## BQ24074 (TI `bq24074.pdf`) — Verified

| Parameter | Min | Typ | Max | Unit | Source |
|---|---|---|---|---|---|
| OUT (VSYS) regulation, input present | 4.3 | 4.4 | 4.5 | V | Electrical Characteristics |
| VDO(BAT-OUT), battery-only, IOUT=1A | — | 50 | 100 | mV | Electrical Characteristics (no verified figure at 2A) |
| → Derived worst-case VSYS floor (battery-only, near VBAT min) | **≈3.3** | — | — | V | 3.4V(VBAT min) − ≤100mV drop |

## TPL5010 (TI `tpl5010.pdf`) — Verified

| Parameter | Min | Typ | Max | Unit |
|---|---|---|---|---|
| VDD operating range | 1.8 | — | 5.5 | V |
| IDD | — | 35 | 50 | nA |
| RSTn pulse width | — | 320 | — | ms |
| DONE pulse width required | 100 | — | — | ns |
| WAKE pulse width | — | 20 | — | ms |
| Time to convert REXT (power-up) | — | 100–120 | — | ms |

## TPS3839K33 (TI `tps3839.pdf`) — Verified

| Parameter | Min | Typ | Max | Unit |
|---|---|---|---|---|
| VDD operating range | 0.9 | — | 6.5 | V |
| IDD | — | 150 | 500 | nA |
| VIT− (K33 variant, negative-going threshold) | 2.857 | **2.93** | 2.974 | V |
| Vhys (K33) | — | 29 | — | mV |
| Reset delay (td) | 120 | 200 | 350 | ms |
| MR pull-up | 10 | 20 | 30 | kΩ |

**Worst-case VSYS nuisance-trip margin:** legitimate VSYS floor (≈3.3V battery-only,
conservatively reduced to **3.1V** using SIMCom's 300mV max-sag design guidance
applied to VSYS) minus K33's worst-case-high trip point (2.974V) = **126mV positive
margin.** TPS3839G33 (VIT− max 3.126V) was evaluated and rejected — it exceeds the
3.1V floor and would risk nuisance trips.

## TPS3808G09 (TI `tps3808.pdf`) — Verified

| Parameter | Min | Typ | Max | Unit |
|---|---|---|---|---|
| VDD operating range | 1.7 | — | 6.5 | V |
| IDD (RESET not asserted) | — | 2.4–2.7 | 5–6 | µA |
| VIT− (G09) | — | 0.84 | — | V |
| MR pull-up | 70 | — | 90 | kΩ |
| Propagation delay MR→RESET | — | 150 | — | ns |
| CT-to-delay formula | `t_D(s) = C_T(nF)/175 + 0.5×10⁻³` | | | |
| Delay tolerance ratio (derived from the one published CT=180nF example) | 58.3% | 100% | 141.7% | of typical |

**Selected C_STRETCH = 1µF C0G/NP0 → worst-case-low delay 3.00–3.17s** (stacking
capacitor tolerance and the IC's own ratio — see ADR-007 for full derivation).

## SN74LVC1G123 (TI) — REJECTED for the PWRKEY pulse role (see ADR-level decision in COMPONENT_SELECTION_MATRIX.md)

Primary datasheet `sn74lvc1g123.pdf` (SCES586E, revised March 2024) re-inspected
directly (rendered page images, this session) specifically to resolve whether a
REXT/CEXT pair can be proven — from the primary source, with tolerance and
temperature accounted for — to guarantee a minimum pulse exceeding the 50ms
PWRKEY floor. **It cannot.** This closes the "Needs Bench Verification" status
left open in the prior session as a rejection, not a resolution.

| Item | Status | Finding |
|---|---|---|
| VCC operating range | ✅ Verified | 1.65–5.5V |
| Function table (CLR/A/B → Q behavior) | ✅ Verified | Table 7-1 — see below (kept for historical record; not applicable once the part is dropped) |
| Rext/Cext-to-pulse-width relationship | ✅ Verified **that no closed-form equation exists** | §8.2.3 provides only graphical curves (Figs 8-2–8-4, log-log, parameterized by Rext: 1k/5k/10k/100k/200kΩ) |
| **Guaranteed (MIN/MAX) timing coverage** | ✅ Verified — **and it stops far short of what's needed** | §5.8/5.9 Switching Characteristics tables give real MIN/MAX `t_wOUT` bounds for exactly two REXT/CEXT points, over the full −40°C to 125°C range: **Rext=10kΩ, Cext=0.01µF → 100–110µs**; **Rext=10kΩ, Cext=0.1µF → 1.0–1.1ms**. Both are TI's own guaranteed bounds. Neither reaches 50ms — the larger one is **45× short**. |
| Pulse duration for any REXT/CEXT combination giving ~50ms+ | 🔴 **Not derivable from the primary source at all** | Beyond the two guaranteed points above, TI publishes only §5.11/§8.2.3 "Typical Characteristics" — log-log curves **at T_A=25°C only**, with **no stated tolerance, no min curve, no max curve, no unit-to-unit variation figure**. Reading a "minimum" off a typical-only curve would be fabricating a spec TI never published, not deriving one. |
| IQ | Not queried — moot, part rejected | — |

**Conclusion:** Option A (derive a schematic-ready REXT/CEXT pair with a proven
minimum pulse > 50ms) is **not achievable** for this part from TI's primary
datasheet. The datasheet's own guaranteed-timing coverage caps out at 1.1ms;
everything in the 50ms–1s range this design needs lives only in an
unbounded, room-temperature-only typical curve. See
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` "Blocker 1" and
`docs/COMPONENT_SELECTION_MATRIX.md` for the replacement decision.

**Function Table 7-1 (verified, kept for historical record):**

| CLR | Ā (A) | B | Q |
|---|---|---|---|
| L | X | X | L |
| X | H | X | L (steady-state) |
| X | X | L | L (steady-state) |
| H | L | ↑ | pulse |
| H | ↓ | H | pulse |
| ↑ | L | H | **pulse** ← the interlock condition this design still needs, now reconstructed with TPL5111 + glue logic (see below) |

## TPL5111 (TI) — SELECTED replacement for the auto-PWRKEY pulse generator — Verified

Primary datasheet `tpl5111.pdf` (SNAS659B, revised September 2018) downloaded and
read directly (rendered page images) this session.

| Parameter | Min | Typ | Max | Unit | Source |
|---|---|---|---|---|---|
| VDD operating range | 1.8 | — | 5.5 | V | §6.3 Recommended Operating Ratings |
| IDD, operation mode | — | 35 | **50** | nA | §6.5 Electrical Characteristics |
| t_IP (selectable time interval) | 100ms | — | 7200s | — | §6.5; 1650 discrete steps via REXT |
| Time interval setting accuracy (excl. REXT precision) | — | — | ±0.6% | — | §6.5 note (5) |
| Oscillator accuracy at 25°C | −0.5% | — | +0.5% | — | §6.5 |
| Oscillator accuracy over temperature (−40 to 105°C) | — | — | ±400 | ppm/°C | §6.5 note (6) |
| Oscillator accuracy over supply voltage | — | — | ±0.4 | %/V | §6.5 |
| Oscillator accuracy over lifetime (10yr equivalent) | — | — | ±0.24% | — | §6.5 note (7) |
| t_DRVn (DRVn pulse width, DONE not received) | — | t_IP − 50ms | — | ms | §6.5 — this is our operating case (DONE tied permanently low) |
| t_M_DRV (valid manual-trigger pulse into DELAY/M_DRV) | **20** | — | — | ms | §6.6 Timing Requirements — a real guaranteed minimum, unlike anything 1G123 could offer |
| t_R_EXT (REXT read time at POR) | 100 | — | 120 | ms | §6.5 |

**REXT equation (§7.5.3, Equation 1, quoted verbatim):**

```
R_EXT = 100 × [ −b + √(b² − 4a(c − 100T)) ] / (2a)
```

where T is the desired t_IP in seconds, and (a, b, c) are selected from TI's
Table 1 by range of T. For our target range (1s < T ≤ 5s): a=0.2253,
b=−20.7654, c=570.5679.

**Selected operating point:** T (t_IP) = 1.5s → R_EXT = 6211.6Ω calculated,
**6.19kΩ 1% (E96 standard) selected** (0.35% rounding offset, absorbed into the
tolerance stack below).

**Worst-case pulse-width derivation (all terms stacked in the same
worsening direction, consistent with this project's TPS3808 stacking
convention):**

| Error source | Contribution to t_IP | Basis |
|---|---|---|
| REXT tolerance (1% resistor + 0.35% rounding ≈ 1.35%, rounded to 1.5%) × measured R→T sensitivity (~3×, numerically derived from Equation 1 near T=1.5s) | ±4.5% | Equation 1, evaluated at T=1.5s and T=1.53s |
| Time interval setting accuracy | ±0.6% | §6.5 |
| Temperature drift, 25°C→105°C worst leg (80°C span) × 400ppm/°C max | ±3.2% | §6.5 note (6) |
| Supply voltage, 2.5V test point → 4.5V worst-case VSYS × 0.4%/V | ±0.8% | §6.5, VSYS range per BQ24074 section above |
| Lifetime drift | ±0.24% | §6.5 note (7) |
| **Total (simple worst-case sum)** | **±9.34%, rounded to ±10%** | — |

- **t_DRVn nominal:** 1500ms − 50ms = **1.45s**
- **t_DRVn worst-case-low:** 1500×0.90 − 50 = **1300ms = 1.30s → 26× the 50ms PWRKEY minimum**
- **t_DRVn worst-case-high:** 1500×1.10 − 50 = **1600ms = 1.60s → 0.90s (36%) margin below the A7670's 2.5s minimum power-OFF pulse (Toff), so the auto-PWRKEY pulse cannot be mistaken for a power-off command**

This is the first fully quantified, primary-source, min/max-proven pulse-width
result in this document for the PWRKEY auto-restart function — SN74LVC1G123
could never produce this because TI never published the underlying tolerance
data for it.

**Open item — trigger/clear reconstruction:** TPL5111's DELAY/M_DRV pin
natively provides the **trigger** function (guaranteed ≥20ms pulse spec, see
table above) but has no CLR-equivalent **inhibit** pin — 1G123's single-pin
interlock against `MODEM_RESET_N` must be reconstructed with small external
gating logic. See `RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` "Blocker 1" for
the proposed approach; this remains 🟡 Needs Bench Verification / detailed
logic design, not yet schematic-ready.

## Derived circuit-level timing (this design)

| Event | Value | Basis |
|---|---|---|
| U9 (TPS3839) assertion during VSYS ramp | until VSYS > 2.93V+29mV, then +120-350ms | TPS3839 td |
| U10 (TPS3808) cold-boot RESET assertion | ~3.0s (worst-case-low) to ~8.9s (worst-case-high) | TPS3808 CT=1µF calculation |
| U10 watchdog-triggered RESET assertion | same 3.0–8.9s window, triggered by TPL5010 `~RST` via MR | same |
| Auto-PWRKEY pulse (via TPL5111, U11 replacement) | **1.30–1.60s worst-case window** (nominal 1.45s), REXT=6.19kΩ | ✅ Fully derived, see TPL5111 section above |

## Open verification items

1. **TPL5111 interlock/glue logic** — the trigger function (DELAY/M_DRV) is
   natively verified, but the CLR-equivalent inhibit against `MODEM_RESET_N` is
   not native to this part and needs a small external AND/edge-shaping stage,
   not yet fully specified — see `RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md`.
2. BQ24074 VDO(BAT-OUT) at 2A (only 1A-tested figure available) — 300mV SIMCom
   system-level guidance used as a conservative substitute.
3. TPS3808's 58.3–141.7% tolerance ratio is extrapolated from one datasheet example,
   not a universally-published spec — recommend bench verification.

## Resolved this session (previously open)

- **Cold-boot RESET/PWRKEY interlock behavior** — no longer applicable in its
  original form: the SN74LVC1G123 that provided the native CLR interlock has
  been **rejected** (see SN74LVC1G123 section above — TI's primary datasheet
  cannot prove a >50ms minimum pulse for any REXT/CEXT pair). The interlock must
  be reconstructed for the TPL5111 replacement — tracked as open item 1 above.
- **SN74LVC1G123 REXT/CEXT minimum-pulse question** — definitively closed as
  **not derivable**, not just "needs bench verification." TI's own guaranteed
  MIN/MAX timing tables stop at 1.1ms; everything above that is an unbounded,
  25°C-only typical curve. This is a hard primary-source finding, not a gap in
  this session's research.
- **TPL5111 worst-case PWRKEY pulse width** — newly **Verified**: 1.30–1.60s
  worst-case window, comfortably clearing both the 50ms floor (26× margin) and
  staying below the 2.5s power-off threshold (36% margin). See TPL5111 section
  above for the full derivation.
