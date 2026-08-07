---
name: marine-tracker-hardware
description: Review and advance the NK Marine Tracker Rev A KiCad project under strict RF, power, marine, and manufacturing gates.
---

# Marine Tracker Hardware Skill

## Trigger

Use for any request involving the Marine Tracker schematic, PCB, RF, battery, GNSS, LTE, manufacturing files, enclosure, firmware-hardware interface, ERC/DRC, BOM or factory test.

## Workflow

1. Read `docs/PROJECT_BRIEF.md`, `PROJECT_RULES.md`, `FEATURES.md`, `ACCEPTANCE_CRITERIA.md`, `STATUS.md`.
2. Identify current lifecycle status and requested deliverable.
3. Check whether required inputs exist: exact part numbers, datasheets, stackup, battery/enclosure constraints.
4. Run read-only MCP inspection first.
5. Present a change plan and risk list.
6. Make only scoped changes.
7. Run validation using MCP/KiCad CLI.
8. Update `STATUS.md`, feature checkboxes and changelog only when evidence exists.
9. Report checks run, checks skipped and remaining blockers.

## Forbidden

- Python or text rewriting of KiCad CAD files
- Guessing RF width/matching values
- Claiming production readiness without reports
- Adding solar/external MCU without approved requirement change
