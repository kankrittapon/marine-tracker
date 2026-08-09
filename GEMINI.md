# Gemini / Antigravity Instructions — Marine Tracker

## Startup

Before every engineering task:

1. Read `AGENTS.md`.
2. Read `docs/STATUS.md`.
3. Read `docs/ENGINEERING_INDEX.md`.
4. Load only documents required for the current task.
5. Read `docs/REVA_POSTMORTEM.md` when working on RevB PCB placement/routing.

Use the repository as project memory.
Do not reconstruct project state from assumptions or prior chat.

## Active Hardware Revision

The active revision is defined by `docs/STATUS.md`.

Current work must use the existing RevB project.
RevA is reference-only unless explicitly authorized otherwise.

Never:
- create another RevB
- copy RevA over RevB
- modify RevA while working on RevB

## KiCad Tooling

Use Konnect / KiCad MCP / KiCad IPC API directly for engineering modifications.

Before modifying KiCad:
- confirm Konnect is connected
- confirm the correct project is open
- confirm the active PCB/schematic paths

Never modify KiCad source using:
- Python
- Bash
- PowerShell
- sed/awk/regex
- S-expression rewriting
- direct text editing

Python may be used only for read-only calculations or geometry analysis.

Do not create Python wrappers or proxy scripts to invoke MCP write operations.
Call Konnect MCP tools directly.

## KiCad Geometry

For PCB placement decisions:
- use actual KiCad F.CrtYd geometry
- do not trust generic MCP bounding boxes when text/F.Fab may be included
- use pads/courtyards/board geometry from KiCad as engineering ground truth

## Workflow Discipline

Do not repeatedly verify unchanged state.

Default:
1. Verify baseline once.
2. Perform the authorized change.
3. Verify the changed area once.
4. Save.
5. Report and STOP.

Do not automatically start the next engineering task.

If the same structural problem survives two attempts:
STOP.
Report the blocker.
Do not continue patching around it.

Never expand the authorized scope just to make a check pass.

## Routing / Placement

Placement and routing are separate phases.

Do not route during placement-only tasks.
Do not move components during routing-only tasks unless explicitly authorized.

Do not autoroute.

Preserve intentionally protected:
- RF geometry
- antenna areas
- power architecture
- validated critical nets

unless the task explicitly authorizes changes.

## Schematic / PCB Consistency

Do not create PCB-only engineering components to hide schematic drift.

If schematic and PCB disagree:
STOP and identify the mismatch.

Schematic → PCB synchronization requires explicit authorization.

## Git

Do not commit unless explicitly instructed.
Do not push unless explicitly instructed.
Never rewrite repository history.

Before a requested commit:
- report modified files
- confirm scope
- confirm no unexpected files

## Reporting

End engineering tasks with:

- Objective
- Work Completed
- Files Modified
- Verification
- Open Issues / Risks
- Next Recommended Action

Keep reports concise.

Do not repeat previously established facts unless they changed.