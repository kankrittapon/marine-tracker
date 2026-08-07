# Marine Tracker RevA

# ENGINEERING_INDEX.md

Version: RevA

---

# Purpose

This document routes a task to the minimum set of documents required for it.
It does document routing only — engineering rules live in
`ENGINEERING_RULEBOOK.md`, live project state lives in `STATUS.md`.

This list is a floor, not a ceiling: if a document listed below itself
references another document needed to complete the task correctly (an ADR it
depends on, a datasheet it cites, a spec it implements), load that document
too. Do not treat this index as a reason to withhold a supporting document the
task actually needs.

---

# Architecture Work

Read:

- `STATUS.md`
- `PROJECT_MASTER_PLAN.md`
- `ENGINEERING_RULEBOOK.md`
- `SYSTEM_REQUIREMENTS.md`
- Relevant ADRs only

# Electrical Review

Read:

- `STATUS.md`
- `ENGINEERING_RULEBOOK.md`
- `DESIGN_SPECIFICATION.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `FMEA.md`
- Relevant ADRs and primary manufacturer documentation

# Schematic Work

Read:

- `STATUS.md`
- `ENGINEERING_RULEBOOK.md`
- `DESIGN_SPECIFICATION.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `VALIDATION_CHECKLIST.md`
- Relevant ADRs
- `adr/IMPLEMENTATION_ROADMAP.md` when the ADRs declare implementation dependencies
- Relevant implementation specifications, including `RECOVERY_COMPONENT_IMPLEMENTATION_SPEC.md` and `RECOVERY_TIMING_REQUIREMENTS.md` for recovery circuitry

# PCB Work

Read:

- `STATUS.md`
- `ENGINEERING_RULEBOOK.md`
- `DESIGN_SPECIFICATION.md`
- `VALIDATION_CHECKLIST.md`
- Relevant ADRs and approved schematic freeze report

# RF Work

Read:

- `STATUS.md`
- `ENGINEERING_RULEBOOK.md`
- `DESIGN_SPECIFICATION.md`
- Relevant manufacturer datasheets and approved PCB stackup

# Firmware Work

Read:

- `STATUS.md`
- `SYSTEM_REQUIREMENTS.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- Relevant recovery and firmware ADRs

# Manufacturing Work

Read:

- `STATUS.md`
- `VALIDATION_CHECKLIST.md`
- `TEST_PLAN.md`
- Approved BOM, CPL, fabrication, and assembly documents

# Documentation Work

Read only the documents directly related to the requested change.
