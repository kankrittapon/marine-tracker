# Marine Tracker RevA

Before starting any task:

1. Read `docs/ENGINEERING_INDEX.md`.
2. Read `docs/STATUS.md` for the only authoritative current project state.
3. Load only the documents required for the current task.
4. Follow `docs/ENGINEERING_RULEBOOK.md`.
5. If technical documents conflict, STOP and report the conflict.
6. Never make engineering assumptions.
7. Before modifying KiCad files, verify that the approved KiCad toolchain is connected and responsive.

---

## KiCad Policy

Only these tools may modify `*.kicad_sch` or `*.kicad_pcb`:

- KiCad GUI
- `kicad-cli` where the command is designed for that operation
- Approved KiCad MCP Server

Raw text, regex, Python, S-expression, `sed`, `awk`, Perl, or bulk textual editing of KiCad source files is forbidden.

If no approved KiCad tool is available, STOP and report the missing tool.

---

## MCP Tool Policy

Allowed when the current phase authorizes them:

- Read project and schematic state
- Save project
- Create snapshot or verified filesystem backup
- Run ERC and DRC
- Place or move schematic symbols
- Connect schematic nets
- Generate review PDFs

Forbidden until explicitly authorized by `docs/STATUS.md` and the applicable validation gate:

- Autorouting or Freerouting
- Bulk replacement or automatic repair
- PCB synchronization during schematic-only phases
- Gerber or production export

---

## Status Ownership

Do not define the current phase or current task in this file.

`docs/STATUS.md` is the single source of truth for live project state.
