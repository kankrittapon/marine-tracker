#!/usr/bin/env python3
"""Marine Tracker workstation migration installer.

Standard-library only. Safe, explicit, idempotent. Does not install
software, does not write secrets, and never overwrites an existing
project-local config file without a timestamped backup.

Modes (combine as needed; they run in the fixed order listed below):
    --check            read-only prerequisite report
    --bootstrap-tools  clone/verify external repos at the exact commit
                        pinned in manifest.json (never builds; never resets
                        a dirty worktree; never falls back to latest main)
    --build-konnect    explicit opt-in: build custom Konnect from source
    --build-kicad-mcp  explicit opt-in: npm install/build KiCAD-MCP-Server
    --configure        render .mcp.json / .agents/mcp_config.json from templates
    --configure-codex  print/write a Codex config snippet (never auto-applies
                        to ~/.codex/config.toml unless --yes is also given)
    --verify           filesystem-level verification of the rendered config

Run with --dry-run to preview --configure / --configure-codex / --build-*
actions without writing or executing anything.
"""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import string
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
MANIFEST_PATH = Path(__file__).resolve().parent / "manifest.json"

CLAUDE_MCP_JSON = PROJECT_ROOT / ".mcp.json"
GEMINI_MCP_JSON = PROJECT_ROOT / ".agents" / "mcp_config.json"

CUSTOM_KONNECT_EXE_REL = Path("target") / "release" / "konnect.exe"
CUSTOM_KONNECT_DEPRECATED_REL = Path("target") / "release" / "konnect-codex.exe"
KICAD_MCP_INDEX_REL = Path("dist") / "index.js"
STOCK_KONNECT_EXE_REL = Path("bin") / "konnect.exe"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(msg, flush=True)


def run_version(cmd: list[str]) -> str | None:
    """Run a --version-style command and return its first output line, or
    None if the executable is not on PATH / fails to run."""
    exe = shutil.which(cmd[0])
    if exe is None:
        return None
    try:
        result = subprocess.run(
            [exe, *cmd[1:]],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (result.stdout or result.stderr or "").strip().splitlines()
    return output[0] if output else "(found, no version output)"


def backup_file(path: Path, dry_run: bool) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-{stamp}")
    if dry_run:
        log(f"  [dry-run] would back up {path} -> {backup_path}")
    else:
        shutil.copy2(path, backup_path)
        log(f"  backed up {path} -> {backup_path}")
    return backup_path


def prompt_for_path(label: str, existing: str | None) -> str:
    if existing:
        return existing
    value = input(f"Enter path for {label}: ").strip()
    return value


# ---------------------------------------------------------------------------
# --check
# ---------------------------------------------------------------------------

def cmd_check() -> None:
    log("=== Prerequisite check (read-only) ===")
    checks = [
        ("python", ["python", "--version"]),
        ("git", ["git", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("cargo", ["cargo", "--version"]),
        ("rustc", ["rustc", "--version"]),
        ("kicad-cli", ["kicad-cli", "--version"]),
        ("claude", ["claude", "--version"]),
        ("codex", ["codex", "--version"]),
        ("gemini", ["gemini", "--version"]),
    ]
    optional = {"codex", "gemini"}
    missing_required = []
    for name, cmd in checks:
        version = run_version(cmd)
        if version is None:
            status = "NOT FOUND"
            if name not in optional:
                missing_required.append(name)
        else:
            status = f"FOUND ({version})"
        log(f"  {name:10s} {status}")

    if missing_required:
        log(f"\nMissing required tools: {', '.join(missing_required)}")
    else:
        log("\nAll required tools found.")
    log("Note: Codex/Gemini are optional and not treated as fatal.")


# ---------------------------------------------------------------------------
# --bootstrap-tools
# ---------------------------------------------------------------------------

def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"manifest.json not found at {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _run_git(git_args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *git_args], cwd=cwd, capture_output=True, text=True, check=False)


def _bootstrap_one_repo(label: str, target: Path, publish_remote: str | None, commit_sha: str | None, dry_run: bool, yes: bool) -> None:
    log(f"\n--- {label} ---")
    if not publish_remote or not commit_sha:
        log(f"  [FAIL] manifest.json is missing publish_remote/commit_sha for {label}. Skipping.")
        return

    if target.exists():
        if not (target / ".git").exists():
            log(f"  [FAIL] {target} exists and is not a git repository. Refusing to touch an unrelated directory.")
            return

        current_remote = _run_git(["remote", "get-url", "origin"], target).stdout.strip()
        if current_remote != publish_remote:
            log(f"  [FAIL] {target} exists with origin='{current_remote}', expected '{publish_remote}'.")
            log("  Refusing to reuse a repo whose remote does not match the pinned publish remote.")
            return
        log(f"  Found existing repo at {target} with matching origin.")

        status = _run_git(["status", "--porcelain"], target).stdout
        if status.strip():
            log(f"  [FAIL] {target} has uncommitted changes.")
            log("  Never resetting a dirty worktree automatically. Commit/stash manually, then re-run.")
            return

        if dry_run:
            log(f"  [dry-run] would fetch origin and checkout {commit_sha}")
            return

        fetch = _run_git(["fetch", "origin"], target)
        if fetch.returncode != 0:
            log(f"  [FAIL] git fetch failed: {fetch.stderr.strip()}")
            return
        checkout = _run_git(["checkout", commit_sha], target)
        if checkout.returncode != 0:
            log(f"  [FAIL] could not check out exact commit {commit_sha}: {checkout.stderr.strip()}")
            log("  Not falling back to main/latest. Resolve manually.")
            return
        log(f"  Checked out exact commit {commit_sha}.")
    else:
        if dry_run:
            log(f"  [dry-run] would clone {publish_remote} -> {target} and checkout {commit_sha}")
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        clone = _run_git(["clone", publish_remote, str(target)], target.parent)
        if clone.returncode != 0:
            log(f"  [FAIL] git clone failed: {clone.stderr.strip()}")
            return
        checkout = _run_git(["checkout", commit_sha], target)
        if checkout.returncode != 0:
            log(f"  [FAIL] cloned but could not check out exact commit {commit_sha}: {checkout.stderr.strip()}")
            log("  Not falling back to main/latest. Resolve manually.")
            return
        log(f"  Cloned {publish_remote} -> {target} and checked out exact commit {commit_sha}.")

    head = _run_git(["rev-parse", "HEAD"], target).stdout.strip()
    if head != commit_sha:
        log(f"  [FAIL] resulting HEAD {head} does not match manifest commit {commit_sha}.")
    else:
        log(f"  [OK] HEAD matches manifest commit exactly: {head}")


def cmd_bootstrap_tools(args: argparse.Namespace) -> None:
    log("=== Bootstrap external tool repos at exact manifest commit ===")
    manifest = load_manifest()
    ext = manifest.get("external_tools", {})
    konnect = ext.get("custom_konnect", {})
    kicad_mcp = ext.get("kicad_mcp_server", {})

    dest_root_str = args.bootstrap_dest_root or input(
        "Enter destination parent directory for external tool repos: "
    ).strip()
    dest_root = Path(dest_root_str)

    konnect_root = Path(args.konnect_custom_root) if args.konnect_custom_root else dest_root / "konnect-codex"
    kicad_mcp_root = Path(args.kicad_mcp_root) if args.kicad_mcp_root else dest_root / "KiCAD-MCP-Server"

    _bootstrap_one_repo(
        "custom Konnect (konnect-codex)", konnect_root,
        konnect.get("publish_remote"), konnect.get("commit_sha"),
        args.dry_run, args.yes,
    )
    _bootstrap_one_repo(
        "KiCAD-MCP-Server", kicad_mcp_root,
        kicad_mcp.get("publish_remote"), kicad_mcp.get("commit_sha"),
        args.dry_run, args.yes,
    )

    log(
        "\nBootstrap step finished. No build was run here — use "
        "--build-konnect / --build-kicad-mcp explicitly, then pass these "
        "roots to --configure:"
    )
    log(f"  --konnect-custom-root {konnect_root}")
    log(f"  --kicad-mcp-root {kicad_mcp_root}")


# ---------------------------------------------------------------------------
# --configure
# ---------------------------------------------------------------------------

def render_template(template_path: Path, mapping: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    return string.Template(text).substitute(mapping)


def cmd_configure(args: argparse.Namespace) -> None:
    log("=== Configure project-local MCP files ===")

    konnect_custom_root = prompt_for_path(
        "custom Konnect root (contains target/release/konnect.exe)",
        args.konnect_custom_root,
    )
    konnect_stock_root = prompt_for_path(
        "stock Konnect plugin root (contains bin/konnect.exe)",
        args.konnect_stock_root,
    )
    kicad_mcp_root = prompt_for_path(
        "KiCAD-MCP-Server root (contains dist/index.js)",
        args.kicad_mcp_root,
    )

    konnect_custom_exe = Path(konnect_custom_root) / CUSTOM_KONNECT_EXE_REL
    konnect_deprecated_exe = Path(konnect_custom_root) / CUSTOM_KONNECT_DEPRECATED_REL
    konnect_settings_json = Path(konnect_stock_root) / "settings.json"
    kicad_mcp_index = Path(kicad_mcp_root) / KICAD_MCP_INDEX_REL
    konnect_stock_exe = Path(konnect_stock_root) / STOCK_KONNECT_EXE_REL

    problems = []
    if not konnect_custom_exe.exists():
        problems.append(f"custom Konnect exe not found: {konnect_custom_exe}")
    if konnect_deprecated_exe.exists() and not konnect_custom_exe.exists():
        problems.append(
            "only the deprecated konnect-codex.exe was found; konnect.exe "
            "is the canonical build and must be produced (see --build-konnect)"
        )
    if not konnect_settings_json.exists():
        problems.append(f"konnect settings.json not found: {konnect_settings_json}")
    if not kicad_mcp_index.exists():
        problems.append(f"KiCAD-MCP-Server dist/index.js not found: {kicad_mcp_index}")
    if not konnect_stock_exe.exists():
        problems.append(f"stock Konnect exe not found: {konnect_stock_exe}")

    if problems:
        log("Problems detected:")
        for p in problems:
            log(f"  - {p}")
        log("Aborting --configure. Fix paths or build missing artifacts first.")
        return

    log("\nPlanned .mcp.json (Claude):")
    log(f"  konnect -> {konnect_custom_exe}")
    log(f"  konnect --config -> {konnect_settings_json}")
    log(f"  kicad -> node {kicad_mcp_index}")
    log("\nPlanned .agents/mcp_config.json (Gemini, stock Konnect):")
    log(f"  konnect -> {konnect_stock_exe}")

    if not args.yes:
        answer = input("\nProceed and write these files? [y/N] ").strip().lower()
        if answer != "y":
            log("Aborted by user. No files written.")
            return

    claude_mapping = {
        "KONNECT_CUSTOM_EXE": str(konnect_custom_exe),
        "KONNECT_SETTINGS_JSON": str(konnect_settings_json),
        "KICAD_MCP_INDEX": str(kicad_mcp_index),
    }
    gemini_mapping = {"KONNECT_STOCK_EXE": str(konnect_stock_exe)}

    claude_rendered = render_template(TEMPLATES_DIR / "claude.mcp.template.json", claude_mapping)
    gemini_rendered = render_template(TEMPLATES_DIR / "gemini.mcp.template.json", gemini_mapping)

    # validate JSON before touching anything on disk
    json.loads(claude_rendered)
    json.loads(gemini_rendered)

    modified = []
    for target, rendered in ((CLAUDE_MCP_JSON, claude_rendered), (GEMINI_MCP_JSON, gemini_rendered)):
        backup_file(target, args.dry_run)
        if args.dry_run:
            log(f"  [dry-run] would write {target}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
            log(f"  wrote {target}")
        modified.append(str(target))

    log(f"\n.claude/settings.local.json was NOT modified (preserved as tracked).")
    log("Modified files:")
    for m in modified:
        log(f"  - {m}")


# ---------------------------------------------------------------------------
# --configure-codex
# ---------------------------------------------------------------------------

CODEX_SNIPPET_TEMPLATE = """\
# Codex Konnect configuration (recommended)
# Add/merge into your user-level Codex config (commonly ~/.codex/config.toml).
# Do NOT use the deprecated konnect-codex.exe binary.

[mcp_servers.konnect]
command = "${KONNECT_CUSTOM_EXE}"
args = ["--config", "${KONNECT_SETTINGS_JSON}"]
"""


def cmd_configure_codex(args: argparse.Namespace) -> None:
    log("=== Codex configuration snippet ===")
    konnect_custom_root = prompt_for_path(
        "custom Konnect root (contains target/release/konnect.exe)",
        args.konnect_custom_root,
    )
    konnect_stock_root = prompt_for_path(
        "stock Konnect plugin root (used only for its settings.json)",
        args.konnect_stock_root,
    )
    konnect_custom_exe = Path(konnect_custom_root) / CUSTOM_KONNECT_EXE_REL
    konnect_settings_json = Path(konnect_stock_root) / "settings.json"

    snippet = string.Template(CODEX_SNIPPET_TEMPLATE).substitute(
        {
            "KONNECT_CUSTOM_EXE": str(konnect_custom_exe),
            "KONNECT_SETTINGS_JSON": str(konnect_settings_json),
        }
    )
    log("\n" + snippet)

    codex_config = Path.home() / ".codex" / "config.toml"
    if not args.apply_codex:
        log(
            f"Not written automatically. To apply, re-run with --configure-codex "
            f"--apply-codex --yes (target: {codex_config})."
        )
        return

    if not args.yes:
        answer = input(
            f"\nThis will back up and append to {codex_config}. Proceed? [y/N] "
        ).strip().lower()
        if answer != "y":
            log("Aborted by user. No changes made.")
            return

    backup_file(codex_config, args.dry_run)
    if args.dry_run:
        log(f"  [dry-run] would append Konnect snippet to {codex_config}")
    else:
        codex_config.parent.mkdir(parents=True, exist_ok=True)
        with codex_config.open("a", encoding="utf-8") as f:
            f.write("\n" + snippet)
        log(f"  appended Konnect snippet to {codex_config}")
    log("auth.json and credentials were not touched.")


# ---------------------------------------------------------------------------
# --verify
# ---------------------------------------------------------------------------

def cmd_verify() -> None:
    log("=== Filesystem-level verification ===")
    ok = True

    for label, path in (("Claude .mcp.json", CLAUDE_MCP_JSON), ("Gemini .agents/mcp_config.json", GEMINI_MCP_JSON)):
        if not path.exists():
            log(f"  [FAIL] {label} missing: {path}")
            ok = False
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            log(f"  [FAIL] {label} is not valid JSON: {exc}")
            ok = False
            continue
        servers = data.get("mcpServers", {})
        if "konnect" not in servers:
            log(f"  [FAIL] {label} has no 'konnect' server entry")
            ok = False
            continue
        konnect_cmd = servers["konnect"].get("command")
        if konnect_cmd and not Path(konnect_cmd).exists():
            log(f"  [WARN] {label} konnect command does not exist on disk: {konnect_cmd}")
        else:
            log(f"  [OK] {label} konnect entry present and command resolvable")

    if CLAUDE_MCP_JSON.exists():
        data = json.loads(CLAUDE_MCP_JSON.read_text(encoding="utf-8"))
        kicad_args = data.get("mcpServers", {}).get("kicad", {}).get("args", [])
        if kicad_args and Path(kicad_args[-1]).exists():
            log(f"  [OK] Claude kicad server target exists: {kicad_args[-1]}")
        elif kicad_args:
            log(f"  [WARN] Claude kicad server target missing: {kicad_args[-1]}")
        else:
            log("  [FAIL] Claude .mcp.json has no 'kicad' server entry")
            ok = False

    log(
        "\nThis script only checks files on disk. It cannot confirm MCP tool\n"
        "visibility inside Claude/Codex/Gemini itself. Launch Claude from\n"
        "MARINE_TRACKER_ROOT and confirm live tool visibility per\n"
        "WORKSTATION_MIGRATION.md section F before resuming PCB work."
    )
    log("\nVERIFY RESULT: " + ("PASS (file-level)" if ok else "FAIL"))


# ---------------------------------------------------------------------------
# --build-konnect
# ---------------------------------------------------------------------------

def cmd_build_konnect(args: argparse.Namespace) -> None:
    log("=== Build custom Konnect (explicit opt-in) ===")
    root = prompt_for_path("custom Konnect root", args.konnect_custom_root)
    root_path = Path(root)
    if not root_path.exists():
        log(f"Aborting: {root_path} does not exist.")
        return

    steps = [
        ["cargo", "fmt", "--check"],
        ["cargo", "check", "-p", "konnect"],
        ["cargo", "test", "-p", "konnect-core"],
        ["cargo", "build", "--release", "-p", "konnect"],
    ]
    for step in steps:
        log(f"\n$ {' '.join(step)}  (cwd={root_path})")
        if args.dry_run:
            log("  [dry-run] skipped")
            continue
        result = subprocess.run(step, cwd=root_path, check=False)
        if result.returncode != 0:
            log(f"\nSTOP: '{' '.join(step)}' failed with exit code {result.returncode}.")
            log("Custom Konnect was NOT reconfigured for Claude/Codex.")
            return

    if args.dry_run:
        log("\n[dry-run] would verify target/release/konnect.exe was produced")
        return

    exe = root_path / CUSTOM_KONNECT_EXE_REL
    if exe.exists():
        log(f"\nBuild succeeded: {exe}")
    else:
        log(f"\nSTOP: build reported success but {exe} was not found.")


# ---------------------------------------------------------------------------
# --build-kicad-mcp
# ---------------------------------------------------------------------------

def cmd_build_kicad_mcp(args: argparse.Namespace) -> None:
    log("=== Build KiCAD-MCP-Server (explicit opt-in) ===")
    root = prompt_for_path("KiCAD-MCP-Server root", args.kicad_mcp_root)
    root_path = Path(root)
    if not root_path.exists():
        log(f"Aborting: {root_path} does not exist.")
        return

    if not (root_path / "package.json").exists():
        log(f"Aborting: {root_path} does not look like the KiCAD-MCP-Server repo (no package.json).")
        return

    for step in (["npm", "install"], ["npm", "run", "build"]):
        log(f"\n$ {' '.join(step)}  (cwd={root_path})")
        if args.dry_run:
            log("  [dry-run] skipped")
            continue
        result = subprocess.run(step, cwd=root_path, shell=(sys.platform == "win32"), check=False)
        if result.returncode != 0:
            log(f"\nSTOP: '{' '.join(step)}' failed with exit code {result.returncode}.")
            return

    if args.dry_run:
        return
    index = root_path / KICAD_MCP_INDEX_REL
    if index.exists():
        log(f"\nBuild succeeded: {index}")
    else:
        log(f"\nSTOP: build reported success but {index} was not found.")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true", help="read-only prerequisite report")
    p.add_argument("--bootstrap-tools", action="store_true", help="clone/verify external repos at the exact commit pinned in manifest.json")
    p.add_argument("--bootstrap-dest-root", default=None, help="parent directory to clone missing external repos into (bootstrap-tools)")
    p.add_argument("--configure", action="store_true", help="render project-local MCP config files")
    p.add_argument("--configure-codex", action="store_true", help="print/write a Codex config snippet")
    p.add_argument("--apply-codex", action="store_true", help="with --configure-codex, actually write to ~/.codex/config.toml (backed up first)")
    p.add_argument("--verify", action="store_true", help="filesystem-level verification of rendered config")
    p.add_argument("--build-konnect", action="store_true", help="explicitly build custom Konnect from source")
    p.add_argument("--build-kicad-mcp", action="store_true", help="explicitly npm install/build KiCAD-MCP-Server")
    p.add_argument("--dry-run", action="store_true", help="preview actions without writing or executing anything")
    p.add_argument("--yes", action="store_true", help="skip interactive confirmation prompts")

    p.add_argument("--konnect-custom-root", default=None, help="path to the custom Konnect (konnect-codex) repo root")
    p.add_argument("--konnect-stock-root", default=None, help="path to the stock Konnect KiCad plugin root")
    p.add_argument("--kicad-mcp-root", default=None, help="path to the KiCAD-MCP-Server repo root")
    p.add_argument("--kicad-root", default=None, help="path to the KiCad install root (reserved for future use)")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()

    ran_anything = False

    if args.check:
        cmd_check()
        ran_anything = True

    if args.bootstrap_tools:
        cmd_bootstrap_tools(args)
        ran_anything = True

    if args.build_konnect:
        cmd_build_konnect(args)
        ran_anything = True

    if args.build_kicad_mcp:
        cmd_build_kicad_mcp(args)
        ran_anything = True

    if args.configure:
        cmd_configure(args)
        ran_anything = True

    if args.configure_codex:
        cmd_configure_codex(args)
        ran_anything = True

    if args.verify:
        cmd_verify()
        ran_anything = True

    if not ran_anything:
        build_arg_parser().print_help()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
