# Claude Code Instructions — Marine Tracker RevA

## Startup

1. Read `docs/STATUS.md` for current phase, batch, and blockers.
2. Read `docs/ENGINEERING_INDEX.md` to find the documents required for the
   current task, and load them.
3. Follow `docs/ENGINEERING_RULEBOOK.md` for all engineering rules, including
   the Level A (hard stop) / Level B (proceed with documentation) verification
   model.

Use the repository as the only project memory. Do not rely on prior chat
context.

## Scope

- Work only on the single active hardware project under `hardware/RevA/`.
- Treat `archive/` as read-only.
- Do not create parallel copies such as `RevA_final`, `RevA_fixed`, or `RevA_new`.
- Do not define project phase or current status in this file — see `docs/STATUS.md`.

## MCP Policy

Before any KiCad MCP tool call, verify the MCP backend is connected and
responsive.

The full KiCad/MCP editing policy — permitted tools, snapshot requirements,
and the Level A / Level B verification model — is defined in
`docs/ENGINEERING_RULEBOOK.md`. This file does not restate it.

## Reporting

End each engineering session with:

- Objective
- Work Completed
- Files Modified
- Verification
- Risks
- Remaining Work
- References
- Next Action
