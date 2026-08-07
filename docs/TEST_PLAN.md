# Marine Tracker RevA

# TEST_PLAN.md

---

# Electrical Tests

## TC-001

Battery Voltage

PASS

3.4V - 4.2V

---

## TC-002

Current Consumption

Sleep

Target

<200 µA

---

## TC-003

Boot Time

Target

<30 sec

---

## TC-004

GNSS TTFF

Hot

<10 sec

Warm

<30 sec

Cold

<120 sec

---

# Recovery Tests

## TC-005

LTE Lost

Expected

Reconnect

---

## TC-006

MQTT Deadlock

Expected

Restart MQTT

---

## TC-007

Firmware Hang

Expected

Watchdog Recovery

---

## TC-008

Brownout

Expected

Automatic Restart

---

## TC-009

Power Loss During Flash Write

Expected

No Configuration Corruption

---

## RF Tests

## TC-010

LTE RSSI

Verify

---

## TC-011

GNSS Sensitivity

Verify

---

## Manufacturing Tests

## TC-012

USB Programming

PASS

---

## TC-013

UART Programming

PASS

---

## TC-014

Pogo Pins

PASS

---

## Environmental Tests

## TC-015

Temperature

-20°C

+60°C

---

## TC-016

Humidity

95%

---

## TC-017

Salt Air

Verify

---

## Acceptance

Prototype RevA is accepted only when

✓ All test cases pass

✓ No critical failures remain

✓ Recovery tests pass

✓ Power tests pass

✓ RF tests pass