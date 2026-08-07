# ADR-007: Watchdog Strategy (DECIDED)

## Context

U8 (TI TPL5010) is A7670's hardware watchdog: `DONE` ← A7670 GPIO1, `WAKE` → A7670
MK_IN_2, `~RST` (open-collector) → previously drove `MODEM_RESET_N` directly through
R22 (100kΩ to `VDD_1V8`).

## Problem (original defect, unchanged)

TPL5010's `~RST` output asserts low for **320ms typical** (TI `tpl5010.pdf` §7.5,
"tRSTn — RSTn Pulse width — 320 ms"). A7670's RESET pin requires **≥2s minimum
(2.5s recommended)** to actually reset the module (SIMCom `A7670X_HW.pdf` Table 12,
"Treset"). A capacitor-based stretch is explicitly forbidden by SIMCom's own text
("Do not parallel capacitors which the value is exceed 100nF on PWRKEY or RESET
pin... module power on automatically when VBAT powered").

## Decision

**TPL5010 is retained, unchanged in role and supply (`VDD_1V8`), per ADR-010.**
`~RST`'s pulse-width defect is fixed by inserting **TPS3808G09DBVR** (TI) as a
dedicated, independently-timed pulse stretcher between TPL5010's `~RST` and A7670's
RESET pin — not by modifying TPL5010 or by any capacitor on the RESET net itself.

### Circuit

```
U8 (TPL5010) pin6 ~RST (open-collector) ──── net WDT_RST_TRIG ──── U10 (TPS3808G09) pin "MR"
                                                                     (MR has an internal 70–90kΩ
                                                                      pull-up to U10's own VDD —
                                                                      no external pull-up needed
                                                                      on this net; this also means
                                                                      R22, TPL5010's old external
                                                                      pull-up, is no longer needed
                                                                      and is REMOVED)

U10 pin SENSE ──tied directly to── U10 pin VDD (net VSYS)   [disables SENSE-based tripping —
                                                               see "Why TPS3808G09" below]
U10 pin VDD ── net VSYS
U10 pin GND ── net GND
U10 pin CT  ── C_STRETCH (1µF, C0G/NP0) ── GND     [sets the stretch delay, see calculation]
U10 pin RESET (open-drain) ── net MODEM_RESET_N ── R_STRETCH_PU (100kΩ) ── net VSYS
                                                  ── TP10 (existing test point)
                                                  ── U1 (A7670) pin16 RESET (unchanged)
```

### Why TPS3808G09, not a bigger/different part

TPS3808 has a SENSE pin (independent voltage-monitoring input) in addition to MR.
Since brownout supervision is already TPS3839's (U9's) job per ADR-010, U10 must be
prevented from ever tripping on its own SENSE reading — tying SENSE directly to VDD
(net VSYS) means SENSE always reads the full VSYS voltage, which is guaranteed to
stay far above the G09 variant's ~0.84V typical threshold (`tps3808.txt`, Device
Options table) under every real operating condition. This makes U10 purely an
MR-triggered pulse generator, with SENSE contributing nothing. G09 (the lowest
practical fixed-threshold variant) was chosen specifically so this tie-to-VDD trick
works across VSYS's full 3.3–4.5V range without needing an external divider.

### Worst-case delay calculation (not "around 2.5–3.0s" — full derivation)

TPS3808's delay-setting equation (`tps3808.txt`, §8.3.2, Equation 1):
`C_T(nF) = [t_D(s) − 0.5×10⁻³(s)] × 175`

Inverting: `t_D(s) = C_T(nF)/175 + 0.5×10⁻³`

The datasheet's own example row (CT = 180nF: min 0.7s / typ 1.2s / max 1.7s,
`tps3808.txt` line 340) shows the IC's internal reference tolerance spans roughly
**58.3% to 141.7% of the typical value** — this ratio is used below as the IC's own
worst-case spread (TI does not publish a separate "±% delay accuracy" figure
independent of a specific CT example, so this ratio is my own conservative
extrapolation from their one worked example, not a directly-quoted universal spec —
flagged explicitly, not presented as more certain than it is).

**Selected: C_STRETCH = 1µF, C0G/NP0 dielectric** (per the datasheet's own
recommendation: "a low-leakage type capacitor such as a ceramic should be used...
stray capacitance... may cause errors").

- Nominal: t_D = 1000/175 + 0.0005 = **5.71s**
- Worst-case-low, stacking BOTH capacitor tolerance (−10%, conservative even for
  X7R; C0G is typically tighter) AND the IC's own 58.3% ratio:
  C_T(low) = 900nF → t_D,typ(900nF) = 900/175+0.0005 = 5.14s → ×0.583 = **3.00s**
- Worst-case-low with a tighter −5% capacitor tolerance (realistic for C0G):
  C_T(low) = 950nF → t_D,typ = 5.43s → ×0.583 = **3.17s**
- **Both worst-case-low results clear the 2.5s design target and the 2.0s SIMCom
  absolute minimum with real margin** (0.5–0.67s of headroom even in the
  conservative −10% case).
- Worst-case-high (for completeness, not a hard requirement): C_T=1100nF (+10%) →
  t_D,typ=6.29s → ×1.417(IC max ratio) = **8.9s**. A rare watchdog-triggered reset
  taking up to ~9s worst-case to complete is acceptable — this is not a
  frequently-exercised path.

**No large capacitor is connected to A7670's RESET pin at any point** — `C_STRETCH`
sits on U10's CT pin, an entirely separate node from `MODEM_RESET_N`.

### R22 removal

R22 (100kΩ, formerly pulling `MODEM_RESET_N` up to `VDD_1V8`) is **removed**. Its
function is superseded by `R_STRETCH_PU` (100kΩ, pulling the same net up to `VSYS`
instead). This is also a correctness improvement, not just a relocation: A7670's
RESET pin thresholds (`VIH`/`VIL`) are defined relative to **VBAT**, not `VDD_1V8`
(SIMCom `A7670X_HW.pdf` Table 12) — a `VSYS`-referenced pull-up matches the pin's
actual voltage domain more directly than the old `VDD_1V8`-referenced one did.

## Interaction with ADR-003 (auto-PWRKEY) and cold-boot safety

See `docs/RECOVERY_TIMING_REQUIREMENTS.md` and
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` for the full combined timeline. In
summary: U10 (TPS3808) also asserts its own RESET output during a normal cold boot
(any time VSYS ramps from 0 up through the SENSE-is-always-satisfied condition, its
POR behavior holds RESET low for one `t_D` pulse) — this is proven, in the combined
timing diagram, to be sequenced so it never overlaps with the auto-PWRKEY pulse
(ADR-003/U9), satisfying SIMCom's "never assert RESET and PWRKEY simultaneously"
rule.

## Consequences

- **Positive:** The original ADR-007 defect is closed with a fully-calculated,
  worst-case-verified margin, using a part family (TI TPS380x) already established
  elsewhere in this design (TPS3839), keeping vendor/tooling consistency. R22's
  removal is a net simplification, not just an addition.
- **Negative / open items:** The 58.3–141.7% IC-tolerance ratio used above is an
  extrapolation from one datasheet example, not a directly-published spec for
  arbitrary CT values — recommend bench-verifying actual t_D with the selected
  1µF C0G capacitor before treating this as final for production (not required to
  block prototype-stage schematic entry, given the calculated margin).
- **Sleep current:** U10 adds 2.4–2.7µA typical (`tps3808.txt` electrical
  characteristics table, VDD=3.3V/6.5V rows) — combined with U8 (35nA) and U9
  (150nA typ/500nA max), total added supervisory-circuit current is
  **≈3.2µA worst-case**, still negligible against the 20µA VBAT-off floor already
  accepted (ADR-002).

## References

- TI `tpl5010.pdf` §7.5 — tRSTn = 320ms typical (unchanged from original problem
  statement).
- SIMCom `A7670X_HW.pdf` Table 12 — Treset min 2s / typ 2.5s; VIH/VIL defined
  relative to VBAT.
- SIMCom `A7670X_HW.pdf` §3.2.2/§3.2.3 — anti-parallel-capacitor warning (basis for
  ruling out a direct-cap fix); "never assert RESET and PWRKEY simultaneously."
- TI `tps3808.txt` (`tps3808.pdf`) — Equation 1 (CT-to-delay formula), Device
  Options table (G09 = 0.84V typical threshold), Electrical Characteristics (IDD
  2.4/2.7µA typ, MR pull-up 70–90kΩ), §8.3.2 (low-leakage capacitor
  recommendation), 6-pin SOT-23 (DBV) package.
- ADR-009, ADR-010 — required-functions framing and the TPL5010/TPS3839 selections
  this decision builds on.
- LCSC — TPS3808G09DBVR (C24584, verified this session).

## Approval status

**DECIDED, pending KiCad implementation approval.** No schematic or PCB file has
been modified — this ADR records the final component-level recommendation for
`docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` to implement.
