# Marine Tracker RevA

# SYSTEM_REQUIREMENTS.md

Version: RevA
Status: Architecture Draft

---

# Purpose

This document defines the system-level engineering requirements.

Every engineering decision shall satisfy these requirements.

If a design violates a requirement,
the requirement takes precedence.

---

# SR-001
## Deployment

The tracker shall operate unattended in marine environments.

No user interaction shall be required.

---

# SR-002
## Power Source

Battery

Single-cell Li-ion

No solar charging in RevA.

---

# SR-003
## Operating Lifetime

Minimum

30 days

Target

60 days

Stretch Goal

90 days

---

# SR-004
## Sleep Current

Target

<200 µA

Stretch Goal

<100 µA

---

# SR-005
## GNSS

External GNSS module.

Independent power control.

---

# SR-006
## LTE

SIMCom A7670 OpenCPU.

No external ESP32.

No Raspberry Pi.

No external MCU.

---

# SR-007
## Firmware

Runs entirely on OpenCPU.

No secondary processor.

---

# SR-008
## Recovery

Automatic recovery.

No manual intervention.

---

# SR-009
## Waterproof

Designed for

IP67 enclosure.

---

# SR-010
## PCB Size

Target

60 x 45 mm

Maximum

65 x 50 mm

---

# SR-011
## Manufacturing

Prototype

10 boards

Production

100 boards

---

# SR-012
## Components

Prefer

LCSC

JLCPCB

Avoid obsolete components.

---

# SR-013
## Documentation

Every circuit

shall reference

Datasheet

ADR

Requirement

Verification

---

# Definition of Success

Project is complete only if

✓ Requirements satisfied

✓ ADR frozen

✓ ERC = 0

✓ DRC = 0

✓ Prototype validated