# Marine Tracker RevA — PCB Layout Postmortem

Status: Draft — awaiting review
Scope: `hardware/RevA/marine-tracker-RevA.kicad_pcb` routing effort only
Evidence sources: `git log`/`git show`/`git diff` on this repository, `docs/STATUS.md`,
`docs/ENGINEERING_RULEBOOK.md`, `docs/ENGINEERING_INDEX.md`, `docs/CHAT_HANDOFF.md`,
`DECISION_LOG.md`, and the assistant work log for the current, uncommitted session
(referred to below as "this session"). Where a claim comes only from this session's
work log rather than a committed artifact, it is labeled **[session]**; everything
else is labeled **[git]** or **[doc]** with the source cited.

No history is invented. Where evidence was not found (e.g. a written placement
review, an ADR for the final board size), this is stated explicitly rather than
assumed.

---

## 1. Executive Summary

RevA's PCB has 4 committed routing-related commits, all made on a single day
(2026-08-07), plus a large body of additional, **never-committed** routing repair
work performed in this session (currently sitting as an 18/220-line uncommitted
diff on top of `HEAD`). Despite four separate "route" / "repair" / "fix" passes,
the board still does not have a clean, verified routing state: a dedicated,
strict audit performed late in this session (the "Commit Gate" check) discovered
that `MODEM_RESET_N`'s trunk — present since the very first commit — runs directly
through U1's entire south pin row, overlapping multiple pads at 0.000mm clearance,
including two active (non-NC) nets. This defect survived three committed passes
and two more in-session repair passes before being caught.

The project's own `docs/STATUS.md` (last updated 2026-08-06, the day before all
PCB commits) states the project is in **Phase P3 (schematic only)** with **"PCB
work remains blocked"** and **"PCB modification, PCB synchronization, routing,
and Gerber export remain forbidden."** All PCB work described in this report
happened after that status was recorded, with no evidence found of the status
being updated or the block being formally lifted.

---

## 2. Verified Timeline

### 2.1 Committed history [git]

| # | Commit | Date/time (local, +0700) | Message | Diff |
|---|---|---|---|---|
| 1 | `4fd674c` | 2026-08-07 12:46:18 | "Initial RevA hardware baseline" | full baseline add |
| 2 | `98d24f0` | 2026-08-07 13:23:50 (+37min) | "Route Batch 2 recovery circuit" | +376 / −0 |
| 3 | `c88365e` | 2026-08-07 21:50:18 (+8h27min) | "Repair RevA Batch 2 routing" | +85 / −13 |
| 4 | `0bf28dc` | 2026-08-07 22:13:51 (+23min) | "Fix RevA Batch A routing defects" | +85 / −5 |

Commit 1's message body states explicitly: *"Routing is not yet complete"* and
*"Board-wide DRC cleanup remains for the routing/validation phase."* It also
records: 115 unique footprints, no duplicate references, ERC 0/0, PCB
synchronized with schematic, board outline 73×50mm, Batch 2 recovery circuit
integrated and placed (Option 1b placement verified).

Commit 2 is a pure-addition routing pass (0 deletions) over the Batch 2 recovery
circuit placed in commit 1.

Commit 3, same day, 8.5 hours later, is a **repair** of the routing added in
commit 2 — the first sign that a routing pass did not converge cleanly on the
first attempt.

Commit 4, 23 minutes after commit 3, introduces the name "Batch A" for the first
time (commits 2–3 used "Batch 2") and fixes further routing defects. The naming
switch from "Batch 2" to "Batch A" is not explained anywhere in the commit
messages or docs found.

### 2.2 This session's work (uncommitted) [session]

Everything below happened after `0bf28dc` and is **not in git history**. It exists
only as the current working-tree diff (`git diff --stat 0bf28dc` →
`220 lines changed, 202 insertions(+), 18 deletions(-)`, confirmed touching
`PWRKEY` (8 net references), `MODEM_RESET_N` (7), `WDT_RST_TRIG` (6), and `VSYS`
(2) in the diff) plus this conversation as the work log.

In order:

1. **Batch B initial repair** — targeted fix for two crossings on `WDT_RST_TRIG`
   × `VSYS`/`PWRKEY`. Passed with disclosed residual marginal-clearance items
   (not treated as blocking at the time).
2. **Batch B expanded repair** (scope explicitly widened to authorize modifying
   `MODEM_RESET_N`) — added an 8-segment MODEM_RESET_N reroute via two "notches,"
   a 5-segment WDT_RST_TRIG detour using a B.Cu underpass at y=33.9, a 3-segment
   PWRKEY change with 2 new vias, and a 3-segment local VSYS jog near R34 pin 1.
   Reported as passing with disclosed residuals.
3. **Batch B final cleanup** — investigated 5 specific findings under a strict
   A/B/C/D classification (no finding could be waved off as "not a short").
   Fixed 3 of 5. While fixing the VSYS jog, a first attempted fix **accidentally
   introduced a new crossing against `SUPV_TRIG`**, caught only by re-running
   verification a second time; the jog was redesigned twice before landing
   clean.
4. **Batch B Commit Gate audit** (strict, read-only, forbidding language like
   "inherent tightness" or "low risk" as a basis for a pass) — **this is where
   the real root cause was found**: `MODEM_RESET_N`'s trunk, in both the
   original `0bf28dc` form and the Batch B reroute, directly overlaps multiple
   U1 pads at 0.000mm clearance, including two active (non-NC) nets
   (`USB_VBUS_FUSED` on pad 24, `GNSS_PWR_EN` on pad 26). Verdict: **BATCH B
   COMMIT GATE FAIL.**
5. **U1 Corridor Analysis** (read-only) — established that `MODEM_RESET_N`'s
   original trunk was routed directly through U1's entire south castellated pin
   row (pads 18–34, 89–94, x=7–29 at y=29–31, F.Cu-only, no gaps) — a
   **pre-existing architecture defect present since the very first commit**, not
   something Batch B introduced. Also found PWRKEY's own never-touched original
   segment independently overlapped the same row.
6. **U1 Corridor Redesign — Option B geometry planning** — iterative B.Cu
   underpass design. Verified fail counts across successive drafts, in order:
   12 → 9 → 18 (a strategy change made things temporarily worse) → 10 → 3 → 2 →
   1 → 0 real design failures, across roughly 9 distinct draft iterations before
   a clean topology (via/lane "nesting" ordering) was found. Final result: 0
   failures in newly-designed copper, but **4 residual clearance violations
   disclosed** at fixed, pre-existing anchor points that the task was not
   authorized to move (VSYS trunk proximity, GND-diagonal proximity at U10,
   U1 pad 89 proximity, C29 proximity). Reported as **GEOMETRY PLAN FAIL**
   pending those residuals.
7. **PCB Expansion Feasibility (73×50 → 73×56)** — concluded expansion does
   **not** fix the 4 residuals, because they are fixed-pad-adjacency problems
   near y≈30–33, unrelated to available board area at y≈50–56. Also flagged a
   real mechanical risk: J1 (edge-launch USB-C) sits only 3.2mm from the current
   edge and would be stranded inside the board if the edge moved without J1
   moving too. Recommended against expansion.
8. **Placement + Routing Feasibility (Option A/B/C)** — proposed Option B
   (move C29 by 0.7mm, a small ~2mm local VSYS jog, a small local GND segment
   reshape) to resolve 3 of the 4 residuals. The 4th (MODEM_RESET_N's approach
   near U1 pad 89, blocked by a fully-packed U6 pad row with no usable gap) has
   **no identified low-risk fix** — closing it would require a larger,
   higher-risk Option C (moving U6/R22/R23, re-verifying U6's SPI traces).

No PCB write ever occurred during steps 4–8 (all explicitly read-only tasks);
steps 1–3 are the source of the current uncommitted diff.

---

## 3. Governance / Process Findings

- **`docs/STATUS.md`** (Last Updated: 2026-08-06) states: Current Phase
  **"P3 — Schematic Implementation and Freeze,"** and under Active Constraints:
  *"PCB modification, PCB synchronization, routing, and Gerber export remain
  forbidden."* No later revision of this file was found. All four committed
  PCB commits, plus this session's routing work, post-date this status.
- **`docs/ENGINEERING_RULEBOOK.md`** ("PCB Rules"): *"Do not begin routing
  until: ERC = 0, Placement Review completed."* and ("MCP Safety Rules"):
  *"Never modify the PCB before schematic implementation is complete."* Commit
  1's own message confirms ERC was 0/0 at that point, but **no written
  Placement Review artifact was found** anywhere in `docs/` — meaning there is
  no discoverable evidence the row-crossing conflict (found only much later by
  the Commit Gate audit) was ever checked for at the placement stage, which is
  exactly the review step the rulebook requires before routing starts.
- No ADR or `DECISION_LOG.md` entry was found authorizing the transition out of
  Phase P3 into PCB routing work. `DECISION_LOG.md` contains only three entries
  (D001–D003), none related to PCB routing or phase transition.

**Finding**: the PCB routing work that produced RevA's current state proceeded
without a visible, logged placement review and without the project's own status
document being updated to reflect it — a documentation/governance gap, not just
a routing-technique gap.

---

## 4. Board Size Drift

- **`docs/CHAT_HANDOFF.md`** records an original target of **60×45mm, maximum
  65×50mm**.
- The actual board (`Edge.Cuts`, confirmed by direct inspection of the
  `.kicad_pcb` file: `gr_rect (0 0) → (73 50)`) is **73×50mm** — 8mm wider than
  the stated maximum.
- The board's own silkscreen text (`gr_text` on `F.SilkS`) still reads
  **"MARINE TRACKER V1.3 / NO SOLAR / 65x50mm"** — stale, not matching the
  actual 73mm width.
- No ADR or `DECISION_LOG.md` entry was found explaining or approving the
  60×45 → 65×50 → 73×50 growth.

**Finding**: the board grew past its own documented maximum with no recorded
justification, and the on-board silkscreen was never updated to match — a
second, independent documentation-drift symptom from the same root cause as
Section 3 (status/decision records not kept current as the design evolved).

---

## 5. Repeated Problems — Verified Attempt Counts

### 5.1 U1 south-row crossing (MODEM_RESET_N)

Verified passes that did **not** catch this defect, in order: commit 1
(baseline), commit 2 (Batch 2 routing), commit 3 (Batch 2 repair), commit 4
(Batch A fix), this session's Batch B initial repair, this session's Batch B
expanded repair, this session's Batch B final cleanup (which investigated 5
specific findings, none of which was this one). **7 separate commits/tasks**
passed or partially cleaned up the board before the defect was found, on the
8th pass (the dedicated Commit Gate audit). This is the single largest source
of rework in the whole effort.

### 5.2 Corridor geometry convergence (this session)

Within the single Option-B geometry-planning task, **9 distinct draft
iterations** were run through deterministic geometric verification before
reaching 0 real design failures (fail counts, in order: 12, 9, 18, 10, 3, 2, 1,
0 — two verification passes, draft 3 and draft "9", produced 0/low counts only
after the underlying via/lane topology rule was derived analytically). The
draft-3 attempt ("dive south early") is notable for making things temporarily
**worse** (9 → 18 failures) before the design direction was corrected.

### 5.3 VSYS local jog (Batch B final cleanup)

Fixed, broke (introduced a new `SUPV_TRIG` crossing), then fixed again — 2
verified attempts for one localized change, caught only because a second
verification pass was run rather than trusting the first fix.

---

## 6. KiCad / Konnect / MCP / Tooling Issues Encountered [session]

- **Inconsistent path handling**: `mcp__konnect__get_component_pads`,
  `get_board_info`, and `get_board_extents` failed with `"The system cannot
  find the path specified (os error 3)"` when given the board's repo-relative
  path (which `query_traces` accepted without issue), and only succeeded once
  given the full absolute Windows path. This cost extra round-trips every time
  a new tool in this family was first used in a session.
- **`get_board_extents` does not return the board outline.** It returns the
  bounding box of populated copper/footprints. Confirmed directly: it reported
  `62.0 × 44.57mm` (x:1–63, y:2.2–46.77) while the actual `Edge.Cuts` rectangle,
  found only by reading the file directly, is `73 × 50mm` at `(0,0)–(73,50)`.
  Anyone trusting this tool alone for board size would get a materially wrong
  answer.
- **`get_board_info` returned `layer_count: 0, net_count: 0`** against a valid,
  open board — effectively non-functional for this project every time it was
  tried.
- **`kicad-cli` DRC non-determinism**: established repeatedly across the
  engagement — identical, unchanged files produced different violation
  counts/sets on repeated runs. This forced a shift to direct, deterministic
  geometric computation (custom distance/clearance functions run against
  cached pad/track/via data) as the primary verification method, with DRC used
  only as a secondary cross-check rather than a trusted source of truth.
- **Self-inflicted verification bug** [session]: the custom Python
  segment-to-pad distance helper used throughout the corridor planning work
  had a bug — it checked only one segment endpoint against each pad's edges,
  not both — which produced at least one **false PASS** (a MODEM_RESET_N stub
  against U1 pad 89, reported as `+0.183mm` margin by the buggy version and
  `-0.125mm` — an actual violation — once fixed). This was caught only by an
  incidental manual spot-check, not by any systematic self-test of the
  verification tooling itself.

---

## 7. Final Root Causes Preventing Convergence

1. **`MODEM_RESET_N`'s original trunk topology** (present since commit 1) was
   routed directly through U1's entire south pin row. This is a placement/
   routing-topology defect from the very first "baseline," not something any
   later Batch introduced — and it was not caught by ERC (which does not check
   copper geometry), nor by any of the four committed routing passes, nor by
   three of this session's four repair/cleanup passes.
2. **Fixed-geometry pinch points** independent of routing choices: U10's own
   adjacent pins sit close enough together that its GND trace and
   WDT_RST_TRIG's trace inherently start near each other; the VSYS trunk
   passes close to a necessary via anchor point; C28/C29 sit close to
   WDT_RST_TRIG's natural approach; U1's pin16/17 stack and U6's pad row
   (which has no usable gap anywhere across its 4.17mm width) box in
   MODEM_RESET_N's approach to U1 pin 16. None of these are fixable by routing
   cleverness alone — they require either accepting the residual or a small,
   deliberate placement change (Section 8 of the placement-feasibility
   analysis, not yet approved or executed).
3. **No placement review artifact exists** (Section 3) that would have caught
   #1 before routing began, and no process step in the four committed passes
   included a full pad-by-pad geometric audit — that step (the "Commit Gate")
   was only introduced late, in this session, well after the defect had
   already survived four commits.

---

## 8. Workflow Mistakes That Caused Unnecessary Repeated Loops

- **Full geometric audits happened too late.** The Commit Gate method (a
  strict, read-only, pad-by-pad clearance audit disallowing soft
  language like "inherent tightness") is what finally found the U1-row
  defect — but it was only run after 4 commits and 3 in-session repair passes
  had already occurred. Running it once, early (e.g., right after commit 2's
  first routing pass), would very likely have caught the same defect for a
  fraction of the total rework.
- **Partial, targeted fixes were repeatedly declared "passing" with disclosed
  residuals**, and each subsequent task treated the prior task's residuals as
  settled background rather than re-examining them from first principles. It
  took a dedicated, differently-scoped audit task (explicitly forbidding
  soft-pedaling language) to break that pattern.
- **Trial-and-error coordinate picking before deriving the underlying rule.**
  The corridor geometry planning task spent its first several drafts (12 → 9 →
  18 failures) adjusting individual coordinates without a general topological
  rule for how three nets' via/lane layout must be ordered to avoid mutual
  crossings. Once that rule (dive-column X-order must match lane Y-order) was
  derived analytically, the remaining drafts converged in 3 iterations instead
  of many more.
- **Documentation not kept current** (Sections 3–4): `STATUS.md`, the board
  silkscreen, and any decision record for the board-size growth were all left
  stale, so anyone consulting the docs (rather than the actual files) would be
  misled about both project phase and board dimensions.

---

## 9. Lessons — DO NOT REPEAT IN REVB

1. **Do not begin routing without a written placement review** that explicitly
   checks every net's start/end pads against every nearby fixed pad row/
   footprint — not just an ERC=0 result. ERC does not check copper geometry.
2. **Do not declare a routing pass "fixed" based on a targeted/partial check.**
   Run a full pad-by-pad geometric audit (the Commit Gate method) before every
   commit that touches routing, not after several rounds of partial repair.
3. **Do not let `STATUS.md` drift from reality.** Update it at every phase
   transition, especially schematic-freeze → PCB-routing, so there is an
   auditable authorization trail. If PCB work is starting, `STATUS.md` should
   say so before or at the same time the first PCB commit lands.
4. **Do not let board outline size change without a logged decision** (ADR or
   `DECISION_LOG.md` entry). RevA's 60×45 → 65×50 → 73×50 growth has no
   recorded justification for the final step.
5. **Do not trust `get_board_extents` / `get_board_info`** from this Konnect
   MCP version as sources of board-size or layer/net-count truth — verify
   `Edge.Cuts` and net counts by direct file inspection or `kicad-cli` until
   the tools are confirmed fixed. Use absolute file paths with Konnect
   component/pad tools, since relative paths failed inconsistently.
6. **Do not trust a single `kicad-cli` DRC run as final proof of a clean
   board** — violation counts were non-deterministic on this setup.
   Corroborate with direct geometric computation before declaring a design
   passing.
7. **Do not route a net's trunk through a component's own pin row just
   because the routed-copper view looks empty there.** F.Cu-only pad rows are
   invisible obstacles unless pad geometry is checked explicitly — this exact
   mistake is RevA's single largest source of rework.
8. **Build the full geometric audit into the process as a required, early
   step** — not as a late-stage discovery task. The same defect surviving
   seven prior passes before an eighth caught it is the clearest evidence in
   this report that "no complaint from the tool" was being treated as "known
   clean," when it was not.
9. **If a custom verification script is used for clearance checking, spot-test
   it against at least one known-violating case before trusting its PASS
   output at scale.** A single-endpoint-only bug in this session's homemade
   distance function produced at least one false pass.

---

## 10. Open Items Not Yet Resolved

- The 4 disclosed residual clearance violations from the Option-B corridor
  geometry plan (VSYS-anchor, GND-diagonal-at-U10, U1-pad-89, C29 proximity)
  remain unresolved on the current uncommitted PCB. Three have a proposed
  low-risk fix (Placement Feasibility Option B); one (U1-pad-89, blocked by
  U6's fully-packed pad row) does not yet have a low-risk fix identified.
- The current working tree remains uncommitted and does not match any
  committed state. Whatever RevA does next (continue repairing, or abandon in
  favor of RevB) should explicitly decide whether to commit, discard, or
  archive this in-progress diff rather than leaving it in limbo.
- No written Placement Review artifact exists for RevA. If a RevB effort
  reuses RevA's placement, this gap should be closed before routing begins
  again, per Lesson 1 above.
