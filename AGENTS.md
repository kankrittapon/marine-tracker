# Marine Tracker

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

---

## Analysis Tool Discipline

Do not create scripts for tasks that can be completed directly with Konnect, repository search, file reading, or existing approved CLI tools.

Preferred order:

1. Konnect / KiCad IPC for KiCad state and geometry.
2. Repository search / direct file reading for documentation.
3. Existing approved CLI tools.
4. Python only when an actual numerical computation is required.

Python must NOT be used merely to:

- search KiCad files
- count components
- locate references
- inspect nets
- extract information already available through Konnect
- wrap or proxy MCP operations

Do not create multiple scratch scripts to investigate one engineering task.

If Python is genuinely necessary:

- it must be read-only
- use one focused calculation only
- never modify KiCad source
- never invoke or proxy MCP write operations

Do not re-check facts already established in the current unchanged design state.

---

## Strict Python / MCP Rule

Python is NOT allowed to orchestrate KiCad work.

FORBIDDEN:

- Python scripts that call, wrap, proxy, automate, or batch Konnect/MCP commands
- Python scripts for querying KiCad state when Konnect can return the same information
- Python scripts for routing, placement, saving, verification, or MCP tool discovery
- Generating multiple scratch Python scripts for one KiCad task

The required KiCad workflow is:

`Agent -> Konnect MCP / KiCad IPC -> KiCad`

The following workflow is forbidden:

`Agent -> Python script -> Konnect MCP -> KiCad`

Python is permitted ONLY for a standalone numerical calculation when ALL conditions are true:

1. The calculation cannot reasonably be obtained from Konnect/KiCad.
2. The script does not call, wrap, proxy, or automate MCP/Konnect.
3. The script does not modify KiCad source files.
4. The script does not automate placement, routing, saving, verification, or tool discovery.
5. At most one focused numerical calculation is used for the task.

For normal KiCad tasks, direct Konnect MCP calls are mandatory even when Python would be more convenient.

If a required Konnect capability is unavailable or unclear, STOP and report the missing capability. Do NOT build a Python workaround.

---

## Part Identity Rule

Never infer a component model from an older revision, archived design, or outdated document.

Before making model-specific engineering claims:

1. Verify the actual part number in the active revision's schematic/BOM.
2. Treat the active revision as the source of truth for component identity.
3. If documentation refers to a different modem, GNSS module, IC, or component than the active revision, STOP and report the discrepancy instead of silently applying the older information.

Do not transfer electrical requirements, pin behavior, timing, voltage limits, or reference-design assumptions from a different component model without explicit verification.
