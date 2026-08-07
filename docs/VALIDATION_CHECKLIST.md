# Marine Tracker RevA

# VALIDATION_CHECKLIST.md

Version: RevA

Status: Living Document

---

# Purpose

This document defines the mandatory engineering gates.

No engineering phase may proceed until the current gate is approved.

This checklist has higher priority than implementation.

If any gate fails,

STOP.

Do not continue.

---

# Project Status

| Phase | Status |
|---------|--------|
| Architecture | ☐ |
| Electrical Review | ☐ |
| Schematic | ☐ |
| PCB Placement | ☐ |
| PCB Routing | ☐ |
| RF Review | ☐ |
| Manufacturing | ☐ |
| Prototype | ☐ |
| Validation | ☐ |

---

# GATE 1

## Architecture Freeze

### Documents

☐ PROJECT_BRIEF.md

☐ SYSTEM_REQUIREMENTS.md

☐ DESIGN_SPECIFICATION.md

☐ REQUIREMENTS_TRACEABILITY_MATRIX.md

☐ FMEA.md

☐ TEST_PLAN.md

### ADR

☐ ADR-001 Approved

☐ ADR-002 Approved

☐ ADR-003 Approved

☐ ADR-004 Approved

☐ ADR-005 Approved

☐ ADR-006 Approved

☐ ADR-007 Approved

☐ ADR-008 Approved

☐ ADR-009 Approved

☐ ADR-010 Approved

### Requirements

☐ Every Requirement has ADR

☐ Every ADR has Requirement

☐ No unresolved architecture conflict

### Result

PASS

FAIL

Reviewer

____________

Date

____________

---

# GATE 2

## Electrical Design Review

### Power

☐ Power Tree verified

☐ Battery architecture verified

☐ Brownout strategy verified

☐ Recovery strategy verified

☐ Energy Budget reviewed

### Signals

☐ USB reviewed

☐ SIM reviewed

☐ GNSS reviewed

☐ LTE reviewed

☐ Flash reviewed

☐ Reset reviewed

☐ Boot reviewed

### Protection

☐ ESD reviewed

☐ TVS reviewed

☐ Reverse polarity reviewed

☐ Battery protection reviewed

### Result

PASS

FAIL

---

# GATE 3

## Schematic Freeze

### ERC

☐ ERC = 0

☐ No undocumented warnings

### Components

☐ Every IC reviewed

☐ Every pin reviewed

☐ Every capacitor reviewed

☐ Every pull-up/down reviewed

☐ Every power rail reviewed

☐ Every test point reviewed

### Documentation

☐ Datasheet linked

☐ ADR linked

☐ RTM linked

### Result

PASS

FAIL

---

# GATE 4

## PCB Placement Review

### Placement

☐ Mechanical fit

☐ Battery location

☐ GNSS placement

☐ LTE placement

☐ RF separation

☐ USB placement

☐ SIM placement

☐ Programming pads

### Thermal

☐ Heat sources reviewed

☐ Copper area reviewed

### Manufacturing

☐ Assembly clearance

☐ Courtyard clearance

☐ Mounting holes

### Result

PASS

FAIL

---

# GATE 5

## PCB Routing

### Routing

☐ VBAT

☐ VSYS

☐ USB

☐ SIM

☐ UART

☐ SPI

☐ GNSS

☐ RF

### Ground

☐ Ground Plane

☐ Via Stitching

☐ Return Paths

☐ Analog Separation

### DRC

☐ DRC = 0

### Result

PASS

FAIL

---

# GATE 6

## RF Validation

☐ LTE RF

☐ GNSS RF

☐ 50 Ω Review

☐ Keep-out verified

☐ Via Fence

☐ Matching Network

☐ Antenna Placement

### Result

PASS

FAIL

---

# GATE 7

## Manufacturing Review

### BOM

☐ Complete

☐ LCSC Available

☐ No obsolete parts

☐ Alternatives defined

### Production

☐ Gerber

☐ Drill

☐ STEP

☐ CPL

☐ BOM

☐ Assembly Drawing

☐ Fabrication Notes

### Programming

☐ UART

☐ USB

☐ BOOT

☐ Factory Jig

### Result

PASS

FAIL

---

# GATE 8

## Prototype Validation

### Electrical

☐ Power

☐ Sleep Current

☐ Boot Time

☐ Current Profile

### Functional

☐ LTE

☐ MQTT

☐ TCP

☐ GNSS

☐ SIM

☐ Recovery

### Environmental

☐ Temperature

☐ Humidity

☐ Salt Air

### Mechanical

☐ Enclosure Fit

☐ Connector Access

☐ Battery Fit

### Result

PASS

FAIL

---

# GATE 9

## Release Approval

### Engineering

☐ All Gates Passed

☐ RTM Complete

☐ ADR Frozen

☐ Documentation Complete

☐ Git Tag Created

### Prototype

☐ 10 Boards Built

☐ All Boards Boot

☐ Factory Programming Successful

☐ No Critical Failure

### Final Approval

Engineering Lead

____________________

Hardware Lead

____________________

Firmware Lead

____________________

Project Owner

____________________

Release Version

____________________

Release Date

____________________

---

# STOP CONDITIONS

Engineering MUST STOP immediately if:

☐ ERC > 0

☐ DRC > 0

☐ Requirement has no verification

☐ ADR conflict exists

☐ Datasheet contradiction exists

☐ Undefined power rail

☐ Undefined voltage domain

☐ RF impedance unknown

☐ Component unavailable

☐ Brownout recovery undefined

☐ Boot sequence undefined

☐ Recovery architecture undefined

---

# Definition of Done

Marine Tracker RevA is complete only if:

✅ Architecture Frozen

✅ Requirements Frozen

✅ ADR Frozen

✅ FMEA Complete

✅ RTM Complete

✅ ERC = 0

✅ DRC = 0

✅ RF Review Complete

✅ Manufacturing Package Complete

✅ Prototype Built

✅ Prototype Validated

✅ Documentation Complete

Only then may the project be released for manufacturing.