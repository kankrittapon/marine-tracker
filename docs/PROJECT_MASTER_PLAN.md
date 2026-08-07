# Marine Tracker RevA

# PROJECT_MASTER_PLAN.md

Version: RevA

Status: Master Project Plan

Priority: Highest

Owner: Project Architecture

---

# Purpose

This document defines the official engineering roadmap.

Every engineering task SHALL belong to one phase.

No work shall be performed outside the current approved phase.

Only one active phase is allowed.

---

# Project Objective

Design a palm-sized marine GPS tracker using:

- SIMCom A7670 OpenCPU
- External GNSS
- Single-cell Li-ion battery
- USB-C
- Nano SIM
- IP67 enclosure
- Low power operation
- Prototype run of 10 boards

The tracker must operate unattended in harsh marine environments.

---

# Status Ownership

Current project state is maintained only in `STATUS.md`.

This master plan defines the static roadmap, phase objectives, deliverables, and exit criteria.
It SHALL NOT contain the current phase, current batch, progress percentage, or active blockers.

---

# Phase Overview

| Phase | Name |
|---|---|
| P1 | Architecture Freeze |
| P2 | Electrical Design Review |
| P3 | Schematic Implementation and Freeze |
| P4 | PCB Placement |
| P5 | PCB Routing |
| P6 | RF Validation |
| P7 | Manufacturing Package |
| P8 | Prototype Build |
| P9 | Validation |
| P10 | Production Release |

---

# Engineering Philosophy

Think before implementing.

Verify before modifying.

Measure before optimizing.

Document before releasing.

Evidence over assumptions.

Correctness over speed.

Reliability over complexity.

Long-term maintainability over short-term convenience.