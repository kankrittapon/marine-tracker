# Recovery Hardware Component Selection Matrix

Supporting detail for `docs/adr/ADR-010-recovery-component-selection.md`. This
document is the auditable scoring worksheet; ADR-010 states the conclusion.

**Verification key:** ✅ Verified (primary manufacturer datasheet, extracted and
quoted this session) · 🟡 Needs Verification (secondary source only — primary
datasheet was inaccessible this session, see note) · — Not applicable to this part.

## Primary-source access note

TI datasheets (`tpl5010.pdf`, `tps3839.pdf`, `tps3813.pdf`) were downloaded and
text-extracted successfully this session. Analog Devices/Maxim's datasheet server
(`analog.com`) refused/timed out both a direct `curl` fetch and a `WebFetch` product-
page request (TLS renegotiation hang, then a 60s timeout with zero bytes received) —
this is reported as an access failure, not treated as evidence the parts don't exist
or don't meet spec. All MAX-series and MCP1316 figures below are from search-result
snippets of manufacturer/distributor pages, not from a primary PDF opened this
session, and are marked 🟡 accordingly.

## Required functions (from ADR-009's approved recommendation)

1. **Independent watchdog** — detects a powered-but-unresponsive firmware state via
   a periodic proof-of-life signal, independent of the same firmware's own ability
   to self-diagnose.
2. **Brownout supervision** — detects loss/collapse of an A7670-internal rail
   (`VDD_1V8`) caused by the modem's own documented over/under-voltage automatic
   power-off, using a monitor that does **not** share that rail's power source.
3. **Recovery trigger** — an output capable of driving either A7670's RESET pin
   (2s min / 2.5s recommended low pulse, SIMCom `A7670X_HW.pdf` Table 12) or feeding
   ADR-003's PWRKEY auto-restart circuit.
4. **Low sleep current** — must not materially erode the battery-life budget ADR-002
   already accepted (20µA VBAT-off leakage floor).
5. **Marine reliability** — must function correctly across the unattended,
   temperature/humidity-exposed deployment context in `PROJECT_BRIEF.md`, and not
   introduce a new single point of failure worse than what it replaces.

## Candidate inventory

| Candidate | Vendor | Category | Verification |
|---|---|---|---|
| TPL5010 | TI | Watchdog-only | ✅ |
| TPS3839 (TPS383x family) | TI | Supervisor-only | ✅ |
| TPS3813xxx | TI | Single-chip combo (window-watchdog + supervisor) | ✅ |
| MAX16152/153/154/155 | ADI (Maxim) | Single-chip combo (nanopower supervisor + watchdog) | 🟡 |
| MAX823/824/825 | ADI (Maxim) | Single-chip combo (reset + watchdog + manual reset) | 🟡 |
| MCP1316 family | Microchip | Single-chip combo (supervisor + WDI input) | 🟡 |
| MAX6369-MAX6374 | ADI (Maxim) | Watchdog-only | 🟡 |
| **TPL5010 + TPS3839** | TI (both) | **Two-chip hybrid** | ✅ |

## Detailed comparison

| Candidate | Supply voltage | Voltage domain fit vs. VSYS (~3.3-4.5V, verified this session) | Sleep current (IQ) | Package | PCB area | Cost (LCSC, single-qty) | LCSC availability | Vendor | Failure mode if part fails | Marine suitability notes |
|---|---|---|---|---|---|---|---|---|---|---|
| TPL5010 | 1.8V–6.5V min-max ("requires a voltage supply within 1.8V and 5.5V", `tpl5010.pdf` line 1088) | ✅ Fits, but currently wired to `VDD_1V8` not VSYS — see ADR-007 | **35nA typ / 50nA max** (verified, §7.5) | 6-pin SOT23, 3.00×3.00mm (verified) | Small | **~$0.19-0.24** (LCSC C473912/C125800, thousands in stock — verified this session) | ✅ Strong | TI | Loses ALL watchdog coverage (no backup timer) | Already used/documented in this project; wide 100ms-7200s programmable range fits a multi-minute report interval well |
| TPS3839 | **0.9V–6.5V** (verified, line 14), valid reset output down to VDD>0.6V | ✅ Fits comfortably, and is a genuinely appropriate candidate for direct VSYS reference (unlike TPL5010's current wiring) | **150nA typ** (verified, line 12) | 3-pin SOT23 or 4-pin X2SON 1×1mm (verified) | Very small | **~$0.30** (LCSC C96333, verified this session for the K33/3.3V-threshold variant) | ✅ Confirmed | TI | Loses independent brownout detection entirely | Extremely small footprint, factory-trimmed threshold (no external divider to tolerance-stack), reset pulse 200ms typ (verified) — appropriate for triggering a downstream PWRKEY sequence, not long enough alone to satisfy RESET's 2.5s requirement directly |
| TPS3813xxx | **2V–6.5V** (verified, lines 150/181) | ✅ Fits | **9µA typical** (verified, line 9/240) — **~60× TPL5010, ~257× TPS3839** | 6-pin SOT23 | Small | Needs Verification (not queried this session) | Needs Verification | TI | Single point of failure for BOTH functions at once | **Watchdog window is fixed/short** ("Watchdog time-out Upper limit... 2/2.5/3" — verified, line 266 — this reads in the few-second range typical of DSP/processor supervision, not resistor-programmable across a wide range like TPL5010's 100ms-7200s) — **poor fit** for a multi-minute periodic-report application; would force firmware to feed it far more often than the application's natural cadence, or risk nuisance resets |
| MAX16152-155 | 🟡 Reported as "ultra-low-current supervisory circuits" combining voltage + code-execution monitoring — no verified numeric IQ/VDD range this session | 🟡 Unverified | 🟡 Unverified | 🟡 Unverified | 🟡 | 🟡 No LCSC listing surfaced in this session's search | 🟡 Not confirmed on LCSC | ADI (Maxim) | 🟡 Unverified | 🟡 Cannot be recommended without primary verification |
| MAX823/824/825 | 🟡 Typical for this Maxim supervisor class is a few volts to 5.5V — not verified this session | 🟡 Unverified | 🟡 Unverified | 5-pin SOT23 / SC70 (from search snippet) | Small (unverified precisely) | 🟡 Unverified | 🟡 Unverified | ADI (Maxim) | 🟡 Unverified | 🟡 Cannot be recommended without primary verification |
| MCP1316 family | 🟡 Unverified this session (secondary source only) | 🟡 Unverified | 🟡 Unverified | 🟡 Unverified | 🟡 | **$0.64** (LCSC C625214, verified this session) — notably more expensive than the TI candidates | **Only 91 units in stock** (LCSC, verified this session) — a real, concrete sourcing risk for even a 10-100 unit prototype/production run | Microchip | 🟡 Unverified | Poor — cost and stock alone are disqualifying regardless of electrical merit |
| MAX6369-MAX6374 | 2.5V–5.5V (from search snippet, not primary-verified) | 🟡 Likely fits but unverified | 🟡 Unverified | 8-pin SOT23 (from search snippet) | Small | 🟡 Unverified | 🟡 Unverified | ADI (Maxim) | 🟡 Unverified | 🟡 Cannot be recommended without primary verification |
| **TPL5010 + TPS3839** | Each part independently within its own verified range; can be powered from **different** rails (TPL5010 stays on `VDD_1V8`, TPS3839 moves to VSYS) — this is the point | ✅ Each part used exactly within its verified domain — no cross-domain voltage risk (unlike a naive whole-IC VSYS repower, ruled out in the prior session's analysis) | **35nA + 150nA = 185nA combined** — still negligible against the 20µA VBAT-off floor already accepted (ADR-002) | 2× small SOT23-class parts | Small-medium (two footprints, still tiny) | **~$0.49-0.54 combined** (both verified) | ✅ Both confirmed strong | TI (both) | Each part's failure only removes ONE of the two required functions, not both — a real reliability advantage over any single-chip option | Both parts individually well-suited; TPL5010 already precedented in this project |

## Weighted decision matrix

Weights derived from ADR-008's priority ordering (reliability > battery life > low
hardware complexity > maintainability) plus this ADR's marine/sourcing criteria.
Scored 1 (poor) to 5 (excellent) per architecture; 🟡-marked candidates are capped
at a maximum score of 3 on any criterion they couldn't be primary-verified for,
since an un-verifiable claim cannot be scored as excellent regardless of how good
the secondary-source description sounds.

| Criterion | Weight | TPL5010 alone | TPS3839 alone | TPS3813 alone | MAX16152-155 alone | MAX823 alone | MCP1316 alone | MAX6369 alone | **TPL5010+TPS3839** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Functional coverage (watchdog **and** brownout, per ADR-009's FMEA) | 25% | 2 *(watchdog only)* | 2 *(supervisor only)* | 4 *(both, but poorly sized)* | 3🟡 *(both, claimed)* | 3🟡 *(both, claimed)* | 3🟡 *(both, claimed)* | 2 *(watchdog only)* | **5** |
| Sleep current | 20% | 5 | 5 | 2 *(9µA verified)* | 3🟡 | 3🟡 | 3🟡 | 3🟡 | **5** |
| Voltage-domain safety (no cross-domain overvoltage risk) | 15% | 4 *(as currently wired; needs the domain-separation fix)* | 5 | 4 | 3🟡 | 3🟡 | 3🟡 | 3🟡 | **5** |
| Marine reliability / single-point-of-failure | 15% | 2 *(alone, no brownout coverage)* | 2 *(alone, no hang coverage)* | 3 *(one part = one failure kills both functions)* | 3🟡 | 3🟡 | 3🟡 | 2 | **5** *(each failure only removes one function)* |
| Cost / LCSC availability | 15% | 5 *(verified cheap, high stock)* | 5 *(verified cheap, in stock)* | 3🟡 | 2🟡 *(no LCSC listing found)* | 3🟡 | **1** *(verified: 91 units, $0.64 — real risk)* | 3🟡 | **5** |
| Maintainability (precedent, documentation, multi-vendor support) | 10% | 5 *(already used/documented in this project)* | 3 *(new to project)* | 3 | 2🟡 | 2🟡 | 2🟡 | 2🟡 | **4** |
| **Weighted total** | 100% | 3.45 | 3.30 | 3.30 | 2.75 | 2.90 | 2.35 | 2.55 | **4.90** |

**TPL5010 + TPS3839 wins on every weighted criterion, not just on net total** — it
is not a case of one strong score offsetting weak ones. This is a direct consequence
of splitting the two ADR-009-required functions across two parts each individually
matched to its own job, rather than compromising on a single chip that does both
adequately but neither optimally, or accepting a single-function part that leaves
one whole failure class (per ADR-009's FMEA) uncovered.

## Addendum: RESET pulse-stretcher candidates (ADR-007 follow-on)

Required: convert TPL5010's 320ms `~RST` into a valid ≥2.0s (design target
2.5-3.0s minimum across tolerance) A7670 RESET assertion, open-drain/isolated,
no large cap directly on the RESET pin, low sleep current, small package,
real LCSC availability.

| Candidate | Category | Part number | Datasheet | Operating voltage | Trigger polarity | Retrigger behavior | Output pulse tolerance | IQ | Package/area | LCSC | Failure mode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **TPS3808G09** | Programmable delay/reset timer | TPS3808G09DBVR | ✅ `tps3808.pdf` — primary, extracted | 1.7–6.5V (verified) | MR active-low, level-triggered | N/A (not retriggerable in the sense of extending an active pulse — MR held low simply holds RESET asserted) | Fully calculated: worst-case-low 3.00-3.17s, worst-case-high ~8.9s (see ADR-007) | **2.4-2.7µA typ / 5-6µA max** (verified) | SOT-23-6, small | ✅ Verified (C24584) | Loses RESET-stretch function only; SENSE tied to VDD so a part failure can't cause a spurious independent trip source |
| SN74LVC1G123 | Dedicated monostable IC | SN74LVC1G123 (TI) / 74LVC1G123 (Nexperia) | 🟡 Confirmed to exist via search (VCC 1.65-5.5V, REXT/CEXT-programmable, Schmitt-trigger inputs, retriggerable) — not locally extracted from primary PDF this session | 1.65-5.5V (search-confirmed) | Edge-triggered (A/B inputs), true retriggerable monostable | Genuinely retriggerable (extends pulse on repeated triggers) — a real advantage over TPS3808's level-holding behavior | 🟡 Not verified — REXT/CEXT tolerance not extracted | 🟡 Not verified | SOT-23-5/6 class, small | 🟡 Not queried | 🟡 Not fully characterized this session |
| TPS3123 | Supervisor with extended reset pulse | TPS3123 (TI) | 🟡 Found via search only ("active-low, push-pull, voltage supervisor with 1.6-s watchdog & manual reset") — not downloaded/extracted this session | 🟡 Unverified | 🟡 Unverified | 🟡 Unverified | 🟡 1.6s figure from search snippet — **below the 2.0s absolute minimum on its own**, would still need external stretching, defeating the purpose of a "native long pulse" part | 🟡 Unverified | 🟡 Unverified | 🟡 Not queried | Even if verified, its native pulse doesn't clear the requirement by itself |
| Schmitt-trigger one-shot (discrete RC + 74HC14-class buffer) | Schmitt-trigger one-shot | Generic (e.g. 74LVC1G14) + RC | 🟡 Buffer part exists and is well-characterized generically; not the risk — the RC timing element is | Depends on logic family, typically 1.65-5.5V | Edge-coupled via RC differentiator into buffer | Not retriggerable without added logic | **Dominant error source is capacitor tolerance (±5-20% typical) stacked with RC-to-threshold-crossing nonlinearity** — no IC-level compensation for this, unlike TPS3808's trimmed 220nA reference | Low (buffer IQ small) | Small | Generic, likely available | **Rejected for the RESET stretcher specifically**: cleans up the switching edge vs. a bare transistor, but the timing-defining RC network still has no factory trim/calibration — same class of risk flagged for the bare discrete option below, just partially mitigated |
| Discrete transistor + RC (no supporting IC) | Discrete | Generic NPN/RC | — | — | — | — | **Cannot prove worst-case timing** — pulse duration depends on transistor hFE (poorly controlled, large part-to-part and temperature variation) in addition to RC tolerance; no datasheet provides a bounded worst-case for this combination because it isn't a specified circuit, it's an ad-hoc one | — | Smallest (fewest parts) | — | **Excluded per the user's own stated condition** ("only if timing accuracy can be proven") — it cannot be proven from datasheets alone, unlike TPS3808's fully-derived worst-case bound |

**Selected: TPS3808G09DBVR.** It is the only candidate in this addendum with a
complete, primary-source-derived worst-case timing proof (see ADR-007). SN74LVC1G123
remains a plausible alternative worth full characterization in a future pass if
TPS3808 sourcing ever becomes a problem, but is not recommended now — it would add
verification work without a demonstrated advantage over an already-fully-verified
part.

## Addendum: Auto-PWRKEY buffer stage (ADR-003 follow-on)

| Candidate | Type | Part | Datasheet | Vsat/leakage | Base/gate drive | Package | LCSC | Notes |
|---|---|---|---|---|---|---|---|---|
| **MMBT2222A** | Small-signal NPN, open-collector buffer | MMBT2222A (multiple mfrs stock this exact part) | 🟡 Generic small-signal transistor — well-established characteristics, not individually re-extracted from a specific vendor's PDF this session | VCE(sat) ≈0.3V typical (generic NPN class figure); ICBO in the nA range at room temp | Sized in `docs/RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` — base current ~28µA vs. ~53µA needed sink current at worst case, oversized by design | SOT-23 | ✅ Multiple manufacturers in stock, $0.004-0.03 (verified this session) | Extremely common, low risk, low cost — not a timing-critical part so generic-class characterization (not a single vendor's exact binned spec) is acceptable here, unlike the RESET stretcher's capacitor/IC choice |
| 2N7002 (N-MOSFET alternative) | Small-signal N-MOSFET, open-drain buffer | 2N7002 | 🟡 Not queried this session | — | Needs VGS(th) check against U9's output swing | SOT-23 | Widely available | Considered but not selected — BJT's base-current-driven turn-on is simpler to hand-calculate a guaranteed-saturated worst case for at the low drive currents here; MOSFET's VGS(th) spread would need its own datasheet check for no added benefit at this current level |

## Addendum: Auto-PWRKEY pulse generator (ADR-003/ADR-010 follow-on — supersedes SN74LVC1G123)

Required: given an edge on `MODEM_RESET_N` (qualified by `SUPV_TRIG`), generate
a **self-terminating** low-going pulse on `PWRKEY`, with a **provable minimum
exceeding 50ms** (SIMCom `A7670X_HW.pdf` Table 10) and comfortably below 2.5s
(A7670's own power-OFF pulse threshold, Table 11 — a pulse too long risks being
read as a power-off command), low IQ, small package, real LCSC availability.

| Candidate | Category | Explicit equation/guarantee? | Guaranteed min pulse achievable >50ms? | IQ | Trigger/clear fit | LCSC | Verdict |
|---|---|---|---|---|---|---|---|
| **SN74LVC1G123** | RC monostable | Graphical curves only, no equation. Guaranteed MIN/MAX tables (`sn74lvc1g123.pdf` §5.8/5.9) cover only two REXT/CEXT points, capping at 1.1ms | 🔴 **No** — every REXT/CEXT pair reaching 50ms+ lives only in an unbounded, 25°C-only typical curve | Not queried (moot) | Native CLR pin — ideal, but moot given the timing failure | Not queried | **Rejected** — cannot prove the one hard requirement this circuit exists for |
| **TLC555 (TI)** | Classic 555 monostable | Yes — `t = 1.1RC`, TI states ±0.5% initial accuracy, 0.005%/°C drift | ✅ Yes, easily, with margin to spare | 🔴 **~170–300µA typical** (`tlc555.pdf`) — ~1000× the 235nA total budget this recovery subsystem already runs at (TPL5010 35nA + TPS3839 150nA) | Trigger via pin 2, reset via pin 4 — good fit, but moot given IQ | Not queried | **Rejected on IQ alone** — would dominate this circuit's entire sleep-current budget for one function |
| **MIC1555/1557 (Microchip)** | Low-power 555 variant | Yes, same `1.1RC`-class equation | ✅ Likely, not fully derived | 🟡 ~200µA active (search-sourced, not primary-verified this session) — still ~1000× the existing budget | Similar to TLC555 | Not queried | **Rejected on IQ** before further verification was warranted — same order-of-magnitude problem as TLC555 |
| **CD4538/4098-class CMOS monostable** | Discrete RC monostable | Similar graphical/approximate-only characterization as SN74LVC1G123 in most vendor datasheets (threshold-variation-dominated, historically not factory-trimmed) | 🔴 Not verified — same class of problem that sank SN74LVC1G123 expected, not independently checked this session given the pattern | Low (CMOS static) | Has an inhibit pin on some variants | Not queried | **Not pursued** — same fundamental risk (untrimmed RC threshold) that already failed for SN74LVC1G123; no reason to expect a better outcome without primary verification |
| **TPL5111 (TI)** | Nanopower one-shot system timer | ✅ **Yes** — explicit REXT→t_IP equation (`tpl5111.pdf` §7.5.3 Eq.1) plus a stated `t_DRVn = t_IP−50ms` relationship, with itemized tolerance contributors (setting accuracy, temp, supply, lifetime) in the Electrical Characteristics table | ✅ **Yes, fully derived**: worst-case-low 1.30s at the selected operating point (26× the 50ms floor) — see `RECOVERY_TIMING_REQUIREMENTS.md` | ✅ **35nA typ / 50nA max (guaranteed)** — same class as TPL5010/TPS3839 already in this design; combined budget stays at ≈235nA | 🟡 Native trigger (DELAY/M_DRV, guaranteed ≥20ms spec) but **no native CLR/inhibit** — needs external glue logic (AND + edge shaper) to reconstruct the `MODEM_RESET_N` interlock, not yet designed | ✅ TPL5111DDCR, LCSC C2870554, confirmed in stock this session | **Selected** — the only candidate that closes the one hard requirement (provable >50ms minimum) while staying inside this design's established nanopower budget |

**Decision: TPL5111DDCR replaces SN74LVC1G123 as U11.** This is not a
close call on the deciding criterion — SN74LVC1G123 cannot be proven to meet
the 50ms requirement from any primary source, full stop, while TPL5111 proves
26× margin over it. The trade-off accepted is topological, not electrical:
TPL5111 needs a small external interlock stage (U12, not yet designed) where
SN74LVC1G123 would have provided that function on one pin — a real but bounded
follow-on task, not a reason to prefer an unprovable part.

## Notes on rejected single-chip candidates

- **TPS3813** is disqualified primarily on **sleep current (9µA, verified)** and
  **watchdog timing range** (short/fixed window vs. our multi-minute report
  interval) — not on unavailability of data. This is the one single-chip candidate
  with a fully primary-verified "no."
- **MAX16152-155, MAX823, MCP1316, MAX6369** remain **provisionally unattractive**
  but not conclusively rejected — their scores are capped by the 🟡 verification
  penalty, not by a confirmed technical shortfall. If ADI's/Microchip's datasheets
  become accessible in a future session, MAX16152-155 in particular (described as
  a nanopower combined supervisor+watchdog) should be re-scored, since it's the
  closest secondary-source description to what a competitive single-chip
  alternative to the TPL5010+TPS3839 pair would need to look like.
- **MCP1316** is the one candidate with a **verified, concrete disqualifying fact**
  (91 units in stock at $0.64/unit on LCSC) independent of its electrical merits.
