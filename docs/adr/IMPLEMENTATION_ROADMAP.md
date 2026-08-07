# ADR Implementation Roadmap

Order in which the approved ADRs should be implemented, based on their actual
dependencies (not just numeric order). No schematic, PCB, or KiCad file has been
modified as part of producing this roadmap.

## Track 1 — No dependencies, actionable immediately

These require no further research and do not touch the schematic.

1. **ADR-001 (Protected Battery Pack)** — Add "battery pack must include integrated
   PCM" as a hard BOM acceptance constraint. Pure sourcing/documentation action.
2. **ADR-002 (VBAT Always-On Architecture)** — No action required; decision is to
   keep the existing topology. Already satisfied by recording this ADR.
3. **ADR-004 (GNSS Power Sequencing)** — Verification-only: re-confirm the
   `GNSS_BCKP`/`GNSS_3V3` 0R tie directly in the live `hardware/RevA/marine-tracker-RevA.kicad_sch`
   netlist (not the older `CONNECTIONS.md` description), and compute U7/U4 turn-on
   ripple against Quectel's <50 mV/<50 ms limits. Read-only netlist inspection, no
   schematic edit required to close this item — only an edit if the check fails.

These three can proceed in any order, in parallel, and don't block or get blocked by
anything else in this list.

## Track 2 — Critical path (blocking everything reset/power-on related)

4. **ADR-007 research (Watchdog Strategy, currently Pending)** — Must be resolved
   next. Requires: (a) verifying A7670 OpenCPU's autonomous recovery capabilities
   (software watchdog, AT-independent recovery paths), and (b) determining which
   SIMCom-documented recovery mechanism(s) need a hardware RESET pulse vs. can be
   handled by firmware alone. This is the single item every other reset/power-on
   ADR is waiting on. **Nothing in Track 3 can be finalized until this resolves.**

## Track 3 — Gated on ADR-007 resolving

5. **ADR-005 (Coordinated Reset Architecture)** — Once ADR-007 lands on a decision
   (hardware fix, firmware fix, or both), design the coordinated RESET/PWRKEY
   timeline this ADR requires, explicitly checking for the "simultaneous
   RESET+PWRKEY assertion" violation SIMCom's datasheet forbids.
6. **ADR-003 (Automatic PWRKEY) — component sizing** — The architecture (RC one-shot)
   is already approved, but final R/C/transistor values can only be locked in once
   ADR-005's coordinated timeline is known, since ADR-003's assertion window must be
   verified against ADR-007's resolved RESET behavior.
7. **ADR-006 (Power-On Timeline) — final version** — Produce the single, complete
   power-on sequence diagram spanning `VSYS` rise, PWRKEY assertion, A7670 boot
   milestones, `VDD_1V8`/watchdog POR window, GNSS enable/turn-on, and RESET
   assertion windows, using the now-finalized values from steps 5–6. This becomes
   the acceptance artifact for the whole reset/power-on rework.

## Track 4 — Implementation (KiCad, after Track 3 is complete)

8. Implement ADR-003 + ADR-005 (+ ADR-007's resolved fix, if hardware) together in
   the KiCad GUI as one coordinated schematic change — not as separate edits — per
   ADR-005's explicit decision to treat these as one system rather than independent
   point fixes.
9. Re-run ERC; confirm 0 errors and that no previously-fixed issue has regressed.
10. Close out ADR-004's verification (if not already done in Track 1) against the
    post-change netlist.

## Summary dependency chain

```
ADR-001 ──────────────────────────────────────► (done, BOM note)
ADR-002 ──────────────────────────────────────► (done, no-op)
ADR-004 ──────────────────────────────────────► (verification, independent)

ADR-007 (research) ──► ADR-005 (design) ──► ADR-003 (sizing) ──► ADR-006 (final) ──► KiCad implementation ──► ERC re-verify
```

## What this roadmap does NOT authorize

No step above authorizes opening KiCad or editing `.kicad_sch`/`.kicad_pcb` files.
Track 4 (implementation) requires a separate, explicit approval once Tracks 2–3 are
complete — consistent with the standing instruction to stop and wait for approval
before implementation begins.
