# Marine Tracker — Workstation Migration Contract

This document is the human-readable contract for restoring the Marine
Tracker AI/MCP tooling environment on a new Windows PC without depending on
the old machine's absolute paths. It is generated from the actual state of
the source machine on 2026-08-10 (see `manifest.json`). Machine-specific
facts are recorded honestly, including gaps (e.g. Gemini's runtime
resolution was never fully CLI-verified on the source machine either).

## A. Architecture

```
Claude
  -> project .mcp.json
       -> konnect server -> custom upgraded Konnect (konnect-codex build)
       -> kicad server   -> generic KiCAD-MCP-Server (node dist/index.js)

Gemini
  -> project .agents/mcp_config.json
       -> konnect server -> stock Konnect KiCad plugin

Codex
  -> user/global config (NOT project-local)
       -> konnect server -> custom upgraded Konnect (recommended; not the
                             deprecated konnect-codex.exe)
```

Rules that must not silently change:

- Gemini stays on the **stock** Konnect binary. Do not switch it to the
  custom `konnect-codex` build.
- Claude and the Codex recommendation use the **custom** `konnect.exe` from
  `konnect-codex`, never the deprecated `konnect-codex.exe` binary that may
  sit alongside it in `target/release/`.
- Codex configuration is user/global. This package documents a safe snippet;
  it does not silently overwrite `~/.codex/config.toml`.

There is also a separate, already project-local, already-committed MCP
server at `mcp-server/` ("marine-tracker-guard-mcp"), referenced by the
existing `.codex/config.example.toml` and `.gemini/settings.example.json`.
It is unrelated to the Konnect/KiCAD-MCP-Server toolchain above and is not
rewired by this package — it travels with the repo automatically because it
is project-local and has no external absolute-path dependency.

## B. What is inside the Git repo

- `.mcp.json` — Claude project MCP config (paths rendered by
  `setup_workstation.py --configure`, not hand-edited).
- `.claude/settings.local.json` — Claude project permissions (tracked,
  preserved as-is by the installer).
- `.agents/mcp_config.json` — Gemini project MCP config (rendered by the
  installer).
- `.codex/config.example.toml`, `.gemini/settings.example.json` — existing
  examples for the project-local guard MCP (`mcp-server/`).
- `mcp-server/` — the project-local guard MCP server source (TypeScript,
  builds with `npm install && npm run build`).
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` — agent instructions.
- `skills/` — project skills, including
  `skills/marine-tracker-hardware/SKILL.md`.
- `docs/`, `hardware/` — the actual engineering project. **Not modified by
  this package.**
- `workstation/` — this migration package.

## C. What must be installed/recreated externally (not in Git)

- `konnect-codex` — custom upgraded Konnect. Reproducible publish remote:
  `https://github.com/kankrittapon/konnect-codex.git` (branch `main`,
  upstream `https://github.com/mixelpixx/Konnect.git`). Build with
  `setup_workstation.py --build-konnect` (explicit opt-in) or manually:
  `cargo fmt --check && cargo check -p konnect && cargo test -p konnect-core
  && cargo build --release -p konnect`. Canonical output:
  `target/release/konnect.exe`.
- `KiCAD-MCP-Server` — generic KiCad MCP. Reproducible publish remote:
  `https://github.com/kankrittapon/KiCAD-MCP-Server.git` (branch `main`,
  upstream `https://github.com/mixelpixx/KiCAD-MCP-Server.git`). Build with
  `setup_workstation.py --build-kicad-mcp` (explicit opt-in) or manually:
  `npm install && npm run build`. Canonical output: `dist/index.js`.
- The stock Konnect KiCad plugin — obtain per its own distribution channel
  (this was a KiCad 3rd-party plugin directory on the source machine).
  Canonical binary: `bin/konnect.exe`, alongside a `settings.json`.
- KiCad itself, Node.js, Rust/Cargo, Git, Python, Claude Code — see
  `dependencies.json` for tested versions.

### C.1 Reproducible restore procedure (exact published baselines)

`manifest.json` pins both external repos to an exact, published commit SHA.
Always check out that exact commit — never assume `main`'s latest tip, since
`main` on the `publish` remotes may move ahead of what was actually
validated for this Marine Tracker baseline.

**A. Clone Marine Tracker** to any location on the new PC.

**B. Custom Konnect:**
```
git clone https://github.com/kankrittapon/konnect-codex.git
cd konnect-codex
git checkout 6e1c6765e03d6b433280822b717d5d6cd59d8642
cargo fmt --all -- --check
cargo check --workspace --locked
cargo test --workspace --locked --lib --tests
cargo build --release -p konnect
```
Expected runtime: `target/release/konnect.exe`. If a bit-for-bit identical
toolchain is used, this should reproduce SHA256
`23fac703f5fc4ea0de184a7bcbd92f86f3f54f0d613fd211333ac8a86d7af3c2`
(informational — not enforced; a different Rust toolchain version will
legitimately produce a different hash for the same source). This commit's
CI is green (all jobs, verified at job level against this exact SHA) —
it supersedes `03c4b34`, whose CI failed on three protocol integration
tests that still assumed the pre-Marine-Tracker starter kit; that was a
test-only fix, no runtime behavior changed.

**C. KiCAD-MCP-Server:**
```
git clone https://github.com/kankrittapon/KiCAD-MCP-Server.git
cd KiCAD-MCP-Server
git checkout 7659c12f6e23347ce18c59e398fb4ba4623867a9
npm install
npm run build
```
Expected runtime: `dist/index.js` (source-recorded SHA256
`7f8f2dfc0eee151c2d5a7f4dd9613f2f5b0da383a227ffe03b6ae630ed316df4`,
informational only, same caveat as above). This commit's CI is green
(22/22 jobs) — it supersedes `cce03a0`, whose CI failed only on a
Prettier formatting check (fixed format-only, no runtime change). The
portable board smoke test (`scripts/codex-mcp-board.mjs`) is available
from `cce03a0` onward — run it with
`node scripts/codex-mcp-board.mjs <board-path.kicad_pcb>` or set
`MARINE_TRACKER_BOARD`.

**D. Install the stock Konnect KiCad plugin separately** (Gemini only) —
this is not published/pinned by this package; obtain it through its own
distribution channel.

**E. Run `setup_workstation.py`** to bind these machine-specific paths into
Marine Tracker's project-local `.mcp.json` / `.agents/mcp_config.json` (see
section E below), or use `--bootstrap-tools` to perform steps B/C above
automatically at an exact-commit level (see `README.md` /
`setup_workstation.py --help`).

## D. What must NEVER be copied into Git

- `konnect.exe` / `konnect-codex.exe` / any Konnect binary.
- The `konnect-codex` or `KiCAD-MCP-Server` repositories themselves
  (`node_modules/`, build outputs, or their own `.git/` directories).
- KiCad plugin binaries.
- Credentials, API keys, auth tokens (Claude, Codex, Gemini, or otherwise).
- Machine caches (`__pycache__/`, npm/cargo caches, etc).

`checksums.sha256` records identity (SHA256) for exactly this reason: so the
package can assert "this is the binary that was verified" without shipping
the binary.

## E. How paths are rebound on a new PC

Nothing in this package hardcodes the old machine's username, drive, or
OneDrive path. The installer takes these as CLI arguments (or prompts
interactively if omitted):

- `MARINE_TRACKER_ROOT` — wherever the repo is cloned/copied.
- `KONNECT_CUSTOM_ROOT` — `--konnect-custom-root`
- `KONNECT_STOCK_ROOT` — `--konnect-stock-root`
- `KICAD_MCP_SERVER_ROOT` — `--kicad-mcp-root`
- `KICAD_INSTALL_ROOT` — `--kicad-root` (reserved)
- Optional: `CODEX_HOME`, `CLAUDE_HOME`, `GEMINI_HOME` — not required as OS
  environment variables; they are only ever used as internal setup-script
  values if/when needed.

`setup_workstation.py --configure` renders `.mcp.json` and
`.agents/mcp_config.json` from `templates/*.template.json` by substituting
`${KONNECT_CUSTOM_EXE}`, `${KONNECT_SETTINGS_JSON}`, `${KICAD_MCP_INDEX}`,
and `${KONNECT_STOCK_EXE}` with the paths supplied on the new machine. Any
existing file is backed up first as `<file>.bak-YYYYMMDD-HHMMSS`.
`.claude/settings.local.json` is left untouched unless a genuinely
machine-specific path inside it requires replacement.

## F. How to verify MCP tools after migration

1. Run `python workstation/setup_workstation.py --verify` — file-level only
   (JSON parses, referenced binaries exist on disk).
2. Launch Claude Code from `MARINE_TRACKER_ROOT` and approve the project MCP
   servers if prompted.
3. Inside Claude, confirm:
   - project `.mcp.json` active
   - `konnect` connected
   - `kicad` connected
   - Konnect tools visible: `get_routing_geometry`, `check_route_clearance`,
     `check_via_clearance`, `refill_zones`
   - generic KiCad tools visible
   - one harmless read-only KiCad MCP call succeeds (e.g. a backend-state or
     UI-status query)
4. If using Gemini, confirm its Konnect server points at the stock binary,
   not the custom build. This step was not fully CLI-verified on the source
   machine — treat it as pending until actually run on the new PC.
5. If using Codex, apply the snippet from
   `setup_workstation.py --configure-codex` (or write it manually) and
   confirm Codex reaches the custom Konnect build.

## G. How to validate before PCB work resumes

Do not resume routing until all of the following hold:

- Section F verification above passes for Claude (Konnect + kicad, all four
  required Konnect tools visible).
- The correct RevB project is open in KiCad
  (`hardware/RevB/marine-tracker-RevB.kicad_pro`) and the KiCad IPC backend
  is responsive.
- `docs/STATUS.md` has been read and reflects the expected state: as of the
  last recorded snapshot, `WDT_DELAY` and `WDT_RST_TRIG` are both **CLOSED —
  WRITE-PASS VERIFIED**. If the new PC's copy of `docs/STATUS.md` shows
  anything else, trust the file, not this document.
- No routing or board changes are performed as part of workstation setup
  itself — setup only restores tooling.

## Known gaps to carry forward (recorded honestly)

- Global Claude hooks on the old machine historically contained duplicate
  stale Konnect hooks. A new PC's `~/.claude/settings.json` should **not**
  reproduce that duplication — keep only the current custom-Konnect
  pre-PCB hook if one is still required. This package does not copy or
  modify global Claude hooks; the cleanup is a manual step on the new PC.
- Gemini CLI was not installed on the source machine at packaging time, so
  its Konnect wiring (`.agents/mcp_config.json` -> stock `bin/konnect.exe`)
  was verified by config inspection only, not by a live CLI session.
