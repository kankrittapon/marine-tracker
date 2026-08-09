# Marine Tracker RevB

# ENGINEERING_RULEBOOK.md

Version: RevB

Status: Mandatory

Priority: Highest

---

# Purpose

This document defines the mandatory engineering rules for the project.

`STATUS.md` defines the current execution phase, progress, accepted checkpoint,
and next authorized work. This rulebook defines mandatory engineering,
electrical, safety, manufacturing, and tooling constraints. `STATUS.md` may not
override those constraints.

If `STATUS.md` and this rulebook genuinely conflict, **STOP and report the
conflict**. Do not resolve a conflict by silently giving either document blanket
precedence.

---

# Core Principles

1. Engineering correctness is more important than implementation speed.
2. Datasheets override assumptions.
3. Verification before implementation for Level A items. Level B items may proceed
   on a documented, conservative estimate, with verification completed on the
   bench — see **Verification Model** below.
4. Every engineering decision must be reproducible.
5. Unknown information shall be marked **Needs Verification** (Level A) or
   **Needs Bench Verification** (Level B) — see **Verification Model**.

---

# Project Rules

- Only one active hardware project exists:

```
hardware/RevB/
```

- RevB is the active engineering revision.
- RevA is frozen and reference-only. No RevA modification is permitted.
- Other archived projects are read-only.
- Architecture changes require an approved ADR.
- Electrical changes require an approved ECP.
- Do not add or remove features after Architecture Freeze without approval.

---

# Requirements

Every implementation shall reference:

- Requirement (RTM)
- ADR
- Datasheet
- Verification Method

No undocumented circuit is allowed. For a Level B item, "Verification Method"
may be recorded as **Needs Bench Verification** — this satisfies the requirement;
it is not an exemption from it.

---

# Datasheet Policy

Preferred reference order:

1. Manufacturer Datasheet
2. Hardware Design Guide
3. Reference Design
4. Application Note

Community discussions may provide hints but shall not override manufacturer
documentation.

This policy is unchanged by the Verification Model below: a Level B item still
requires a manufacturer-sourced, conservative estimate — never a guess. The
Verification Model changes *when* the final bench-confirmed number is required,
not *what sources* an estimate may be based on.

---

# Electrical Rules

Never guess:

- resistor values
- capacitor values
- inductor values
- timing
- voltage levels
- impedance
- power sequencing

Every electrical value shall have engineering justification. A justified,
conservative, datasheet-derived estimate for a Level B item (see Verification
Model) is not a guess and may proceed; an unjustified value is a guess and is
forbidden under any level.

---

# Recovery Rules

Firmware recovery shall be attempted before hardware recovery whenever possible.

Brownout recovery shall be hardware verified.

---

# KiCad Rules

Only the following are permitted to modify KiCad source files:

- KiCad GUI
- kicad-cli
- Approved KiCad MCP Server

For agent-executed KiCad work, use the native Konnect MCP tools directly. Do
not wrap, proxy, or orchestrate KiCad operations through Python, Bash,
PowerShell, or another scripting shell.

Forbidden:

- Python editing
- Regex editing
- sed
- awk
- Perl
- Manual S-expression editing
- Text replacement

Shells and scripts may be used for ordinary documentation work, but never to
modify, wrap, proxy, or orchestrate KiCad project, schematic, or PCB changes.

Python may only be used for:

- calculations
- reports
- documentation
- BOM analysis
- verification scripts

---

# PCB Rules

Do not begin routing until:

- ERC = 0
- Placement Review completed

Do not generate manufacturing files until:

- ERC = 0
- DRC = 0
- Manufacturing Review approved

## Incremental Routing DRC Policy

During an authorized incremental PCB-routing phase:

- Existing baseline DRC findings caused by incomplete routing are allowed and
  do not constitute an unconditional Level A hard stop by themselves.
- A baseline finding is not automatically considered acceptable merely because
  it existed before the current task.
- Any confirmed electrical short, unsafe power connection, RF-critical defect,
  or manufacturing-critical defect remains a hard stop regardless of age.
- Findings caused by the current authorized work must be investigated.
- A new Level A electrical, safety, or manufacturing violation introduced by
  the current work is a hard stop.
- Unrelated baseline findings must not be automatically repaired or used to
  expand the authorized scope.
- Global DRC cleanup occurs only during the dedicated verification/cleanup
  phase authorized by `STATUS.md`.

## Protected Completed RevB Routing

The following accepted RevB routing groups are protected and must not be
modified by later routing batches unless `STATUS.md` explicitly reopens them:

- VBAT_MODEM
- VSYS
- LTE RF
- GNSS RF
- USB differential pair
- SIM interface

---

# Component Selection

Every new component shall be evaluated against:

- Function
- Availability
- Lifecycle
- PCB Area
- Power Consumption
- Marine Suitability

Never select a component only because it existed in a previous revision.

---

# Verification Model

Not every open question carries the same risk. This model replaces a single
undifferentiated stop list with two levels, so engineering effort is spent
where it protects hardware safety, and does not stall where it doesn't.

## Level A — Hard Stop

Stop immediately. Do not proceed, implement, or enter values into KiCad until
resolved.

Examples:

- ERC > 0
- A new electrical, safety, or manufacturing DRC violation introduced by the
  current authorized work
- Undefined voltage domain
- Undefined power rail
- Missing safety-critical datasheet
- RF uncertainty
- Architecture conflict (including conflicts between approved ADRs)

## Level B — Proceed with Documentation

Document the open item as **Needs Bench Verification** and continue, provided
all of the following hold:

- safety is unaffected
- functionality is preserved
- sufficient design margin exists
- prototype testing is already planned

Examples:

- Timing optimization
- Glue logic optimization
- RC fine tuning
- Propagation delay optimization
- Component value refinement
- Bench calibration

## Classifying an item

If an item is not clearly one of the examples above and cannot be confidently
classified, treat it as **Level A** until classified. Level B is a documented,
justified exception to stopping — it is never the default for an unclassified
item.

A Level B classification does not remove the Requirements-section obligation
to reference an RTM entry, ADR, datasheet basis, and verification method for
the value in question.

---

# Definition of Done

Marine Tracker RevB is complete only when:

- Architecture Frozen
- ADR Complete
- RTM Complete
- ERC = 0
- DRC = 0
- RF Review Passed
- Manufacturing Package Complete
- Prototype Validated
- Documentation Complete

Every item logged as Needs Bench Verification (Level B) must be closed —
confirmed on the bench or superseded — before Documentation is considered
Complete. Level B defers *when* a value is confirmed; it does not exempt any
value from ever being confirmed.

---

# Golden Rule

Evidence → Analysis → Verification → Implementation.

For Level A items, verification precedes implementation without exception.

For Level B items, implementation may precede final verification, provided the
implemented value is the documented conservative estimate required above —
verification then happens on the bench, not on paper, before release.

Never optimize before the design is correct.

Never manufacture before the design is verified.

---

# MCP Safety Rules

Before every schematic modification:

- Create a KiCad MCP Snapshot.

After every completed batch:

- Run ERC.

Never modify the PCB before schematic implementation is complete.

---

# Session Reporting

The end-of-session report template is defined once, in `CLAUDE.md`. This file
does not restate it.
