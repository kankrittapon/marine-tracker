# Marine Tracker — Workstation Migration Package

Portable, text-only package for restoring the Marine Tracker AI/MCP tooling
environment on a new Windows PC. See `WORKSTATION_MIGRATION.md` for the full
architecture and contract; this file is a quick-start only.

## Quick start on a new PC

1. Install base prerequisites: Git, Python 3, Node.js/npm, Rust/Cargo, KiCad,
   Claude Code. See `dependencies.json` for the versions this package was
   tested against.
2. Clone/copy the Marine Tracker repository to any location on the new PC —
   no fixed username, drive, or folder is required.
3. Obtain the external tool repos/plugins (not included in this package —
   see `dependencies.json` / `manifest.json`):
   - `konnect-codex` (custom upgraded Konnect, used by Claude and recommended
     for Codex)
   - `KiCAD-MCP-Server` (generic KiCad MCP, used by Claude)
   - the stock Konnect KiCad plugin (used by Gemini only)
4. Run the setup script from the repository root:
   ```
   python workstation/setup_workstation.py --check
   python workstation/setup_workstation.py --configure ^
     --konnect-custom-root <path-to-konnect-codex> ^
     --konnect-stock-root  <path-to-stock-konnect-plugin> ^
     --kicad-mcp-root      <path-to-KiCAD-MCP-Server>
   python workstation/setup_workstation.py --verify
   ```
5. Launch KiCad and open the RevB project:
   `hardware/RevB/marine-tracker-RevB.kicad_pro`.
6. Launch Claude Code from the Marine Tracker project root (not a parent
   directory).
7. Approve the project MCP servers (`konnect`, `kicad`) if Claude prompts for
   trust.
8. Run the verification steps in `WORKSTATION_MIGRATION.md` section F
   (confirm `konnect` and `kicad` are connected and the required Konnect
   tools are visible).
9. Only after verification passes, resume PCB work. Do not perform routing
   as part of workstation setup itself.

## What's in this folder

- `README.md` — this file.
- `WORKSTATION_MIGRATION.md` — full migration contract (architecture, what's
  in Git, what must never be copied, path rebinding, verification gate).
- `manifest.json` — recorded project/environment/external-tool identity.
- `dependencies.json` — categorized dependency list.
- `checksums.sha256` — recorded SHA256 identity of config and runtime
  artifacts (identity only — binaries themselves are not copied).
- `setup_workstation.py` — standard-library-only installer/checker.
- `templates/` — placeholder-based MCP config templates rendered by the
  installer.
