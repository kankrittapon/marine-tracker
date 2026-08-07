# Marine Tracker RevA — Current Status

Version: RevA
Status Owner: Project Architecture
Last Updated: 2026-08-06

> This file is the **single source of truth** for current phase, current batch, progress, blockers, and next action.
> Other documents SHALL reference this file and SHALL NOT duplicate live project status.

---

## Current Phase

**P3 — Schematic Implementation and Freeze**

Architecture Freeze and Electrical Design Review are complete. PCB work remains blocked.

## Current Batch

**Coordinated Boot and Recovery Schematic Change**

Approved implementation scope:

- ADR-003 — Automatic PWRKEY
- ADR-005 — Coordinated Reset Architecture
- ADR-006 — Power-On Timeline
- ADR-007 — Watchdog Strategy
- ADR-010 — Recovery Component Selection

These ADRs form one electrically coordinated circuit and SHALL NOT be implemented as separate, incompatible point fixes.

## Completed

- Single active hardware project consolidated under `hardware/RevA/`
- ADR-001 through ADR-010 approved or decided
- Power architecture review completed
- Recovery architecture and component selection completed
- Recovery implementation specification completed
- KiCad 10 IPC MCP backend connected and schematic readable
- Baseline ERC verified: **0 errors, 0 warnings**
- Filesystem backup created and SHA-256 verified before schematic implementation
- ADR-004 GNSS backup sequencing verified; no schematic change required

## Active Constraints

- Modify KiCad only through KiCad GUI, `kicad-cli`, or approved KiCad MCP tools
- No raw text or S-expression editing of KiCad files
- PCB modification, PCB synchronization, routing, and Gerber export remain forbidden
- Run ERC after every logical schematic change
- Stop immediately on unexpected net, pin, voltage-domain, or ERC regression

## Open Verification Items

These are prototype/bench validation items and do not authorize guessed schematic values:

- Bench verification of SN74LVC1G123 timing against the datasheet graph-based design method
- Recovery timing and no-overlap behavior to be validated on prototype hardware
- Final power consumption to be measured after prototype assembly

## Current Blockers

**No unresolved architecture blocker.**

Implementation may proceed only from the approved coordinated recovery specification.

## Next Action

Implement the coordinated Boot/Recovery schematic circuit through the approved KiCad MCP schematic tools, one logical change at a time, saving and running ERC after each change.

## Phase Exit Criteria

P3 is complete only when:

- All approved schematic changes are implemented
- ERC = 0 errors
- ERC = 0 undocumented warnings
- Pin, voltage-domain, reset, boot, and recovery reviews are complete
- Schematic is formally frozen before PCB synchronization
