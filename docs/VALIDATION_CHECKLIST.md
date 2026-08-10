# Marine Tracker RevB

# VALIDATION_CHECKLIST.md

Version: RevB

Status: Living Document

Target: Marine Tracker RevB

Active PCB: `hardware/RevB/marine-tracker-RevB.kicad_pcb`

Board: 65 × 58 mm, 4 layers

Main modem / U1: SIMCom A7670G-LABE

RevA is frozen, historical, and reference-only.

---

# Purpose and Governance

This document defines the mandatory engineering validation gates for RevB.

`STATUS.md` is the sole authority for the live phase, active routing batch,
completed work, blockers, and next authorized action. This checklist defines
the validation criteria applicable to that phase. `ENGINEERING_RULEBOOK.md`
defines the mandatory safety and incremental-routing DRC policy.

Failure of an applicable gate or a Level A stop condition requires work to
stop. A gate that is not yet due does not prohibit an incremental task that is
explicitly authorized by `STATUS.md` and permitted by the rulebook.

---

# Current RevB Routing Context

Current phase: incremental PCB routing, as controlled by `STATUS.md`.

Completed and protected routing groups:

- VBAT_MODEM
- VSYS
- LTE RF
- GNSS RF
- USB differential pair
- SIM interface

Next eligible routing batch: Recovery / Control route planning and routing,
pending the approval required by `STATUS.md`.

Protected completed routing must not be modified unless `STATUS.md` explicitly
reopens it.

---

# Project Status

| Phase | Validation state |
|---|---|
| Architecture | Retain approved RevB records |
| Electrical Review | Retain approved RevB records |
| Schematic | Frozen prerequisite; final ERC remains mandatory |
| PCB Placement | Accepted per `STATUS.md` |
| PCB Routing | In progress incrementally |
| RF Review | Final acceptance pending |
| Manufacturing | Pending |
| Prototype | Pending |
| Validation | Pending |

---

# GATE 1 — Architecture Freeze

## Documents

- [ ] PROJECT_BRIEF.md
- [ ] SYSTEM_REQUIREMENTS.md
- [ ] DESIGN_SPECIFICATION.md
- [ ] REQUIREMENTS_TRACEABILITY_MATRIX.md
- [ ] FMEA.md
- [ ] TEST_PLAN.md

## ADR and requirements

- [ ] Applicable ADRs approved
- [ ] Every implementation requirement traced to an ADR
- [ ] Every ADR traced to a requirement
- [ ] No unresolved architecture conflict

Result: PASS / FAIL

Reviewer: ____________

Date: ____________

---

# GATE 2 — Electrical Design Review

## Power and recovery

- [ ] Power tree verified
- [ ] Battery architecture verified
- [ ] Brownout strategy verified
- [ ] Recovery strategy verified
- [ ] Energy budget reviewed

## Signals

- [ ] USB reviewed
- [ ] SIM reviewed
- [ ] GNSS reviewed
- [ ] LTE reviewed
- [ ] Flash reviewed
- [ ] Reset reviewed
- [ ] Boot reviewed

## Protection

- [ ] ESD reviewed
- [ ] TVS reviewed
- [ ] Reverse-polarity protection reviewed
- [ ] Battery protection reviewed

Result: PASS / FAIL

---

# GATE 3 — Schematic Freeze

## ERC

- [ ] ERC = 0
- [ ] No undocumented warnings

## Components and documentation

- [ ] Every IC, pin, capacitor, pull-up/down, power rail, and test point reviewed
- [ ] Datasheets linked
- [ ] ADRs linked
- [ ] RTM links complete

Result: PASS / FAIL

---

# GATE 4 — PCB Placement Review

## Placement

- [ ] Mechanical fit
- [ ] Battery location
- [ ] GNSS placement
- [ ] LTE placement
- [ ] RF separation
- [ ] USB placement
- [ ] SIM placement
- [ ] Programming pads

## Thermal and manufacturing

- [ ] Heat sources reviewed
- [ ] Copper area reviewed
- [ ] Assembly clearance
- [ ] Courtyard clearance
- [ ] Mounting holes

RevB placement is accepted according to `STATUS.md`. Reopen this gate only when
an authorized change or a genuine routing blocker invalidates the accepted
placement.

Result: PASS / FAIL

---

# GATE 5 — PCB Routing

## Incremental routing policy

During an incremental PCB-routing phase explicitly authorized by `STATUS.md`:

- Baseline DRC findings caused by incomplete routing may remain and are not an
  unconditional Level A stop solely because routing is incomplete.
- Baseline findings are not automatically acceptable and must not be silently
  repaired outside the authorized scope.
- Any confirmed electrical short, unsafe power connection, RF-critical defect,
  or manufacturing-critical defect is a hard stop regardless of age.
- Findings introduced by the current authorized work must be investigated.
- Any new Level A electrical, safety, or manufacturing violation introduced by
  the current work is a hard stop.
- Global DRC cleanup occurs only in the verification/cleanup phase authorized
  by `STATUS.md`.

## Routing progress

- [x] VBAT_MODEM
- [x] VSYS
- [x] LTE RF
- [x] GNSS RF
- [x] USB differential pair
- [x] SIM interface
- [ ] Recovery / Control
- [ ] Remaining power nets
- [ ] UART / GNSS / low-speed signals
- [ ] Ground stitching and pours

## Final routing acceptance

These requirements are not waived by incremental routing:

- [ ] All required nets routed and reviewed
- [ ] Ground planes, stitching, return paths, and required separation reviewed
- [ ] Protected controlled-impedance and RF routing remains compliant
- [ ] ERC = 0
- [ ] DRC = 0
- [ ] No undocumented DRC warnings or accepted deviations

Result: PASS / FAIL

---

# GATE 6 — RF Validation

- [ ] LTE RF
- [ ] GNSS RF
- [ ] 50 Ω review
- [ ] Keep-outs verified
- [ ] Via fences
- [ ] Matching networks
- [ ] Antenna placement

Result: PASS / FAIL

---

# GATE 7 — Manufacturing Review

Manufacturing output is prohibited until the rulebook prerequisites and this
gate are satisfied.

## Final electrical/layout acceptance

- [ ] ERC = 0
- [ ] DRC = 0
- [ ] DFM review passed
- [ ] Manufacturing-critical findings closed
- [ ] RF review passed

## BOM

- [ ] Complete
- [ ] Availability reviewed
- [ ] No obsolete parts without approved disposition
- [ ] Alternatives defined where required

## Production package

- [ ] Gerbers
- [ ] Drill files
- [ ] STEP
- [ ] CPL
- [ ] BOM
- [ ] Assembly drawing
- [ ] Fabrication notes

## Programming

- [ ] UART
- [ ] USB
- [ ] BOOT
- [ ] Factory jig

Result: PASS / FAIL

---

# GATE 8 — Prototype Validation

## Electrical and functional

- [ ] Power
- [ ] Sleep current
- [ ] Boot time
- [ ] Current profile
- [ ] LTE
- [ ] MQTT
- [ ] TCP
- [ ] GNSS
- [ ] SIM
- [ ] Recovery

## Environmental and mechanical

- [ ] Temperature
- [ ] Humidity
- [ ] Salt air
- [ ] Enclosure fit
- [ ] Connector access
- [ ] Battery fit

Result: PASS / FAIL

---

# GATE 9 — Release Approval

## Engineering

- [ ] All gates passed
- [ ] RTM complete
- [ ] ADRs frozen
- [ ] Documentation complete
- [ ] ERC = 0
- [ ] DRC = 0
- [ ] DFM and manufacturing review accepted
- [ ] Release tag created

## Prototype

- [ ] Required prototype build completed
- [ ] All acceptance units boot
- [ ] Factory programming successful
- [ ] No critical failure

Final approval:

Engineering Lead: ____________

Hardware Lead: ____________

Firmware Lead: ____________

Project Owner: ____________

Release Version: ____________

Release Date: ____________

---

# Stop Conditions

Engineering must stop immediately for any applicable Level A condition,
including:

- A new electrical, safety, or manufacturing DRC violation introduced by the
  current authorized work
- A confirmed short or unsafe power, RF-critical, or manufacturing-critical
  defect, whether new or baseline
- ERC > 0 when ERC is required by the applicable gate or batch checkpoint
- Requirement without required verification traceability
- ADR conflict or datasheet contradiction
- Undefined power rail or voltage domain
- Unresolved RF impedance uncertainty
- Missing safety-critical component information
- Undefined brownout recovery, boot sequence, or recovery architecture

Incomplete-routing baseline DRC findings are governed by Gate 5 and the
`ENGINEERING_RULEBOOK.md`; they do not waive final DRC = 0.

---

# Definition of Done

Marine Tracker RevB is complete only when:

- Architecture and requirements are frozen
- Applicable ADRs and RTM are complete
- ERC = 0
- DRC = 0
- RF review passed
- DFM and manufacturing review passed
- Manufacturing package complete
- Prototype built and validated
- Documentation complete

Only then may RevB be released for manufacturing.
