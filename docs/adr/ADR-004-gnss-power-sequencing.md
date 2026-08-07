# ADR-004: GNSS Power Sequencing

## Context

`GNSS_3V3` is gated by U7 (TPS22917 load switch), enabled by A7670 GPIO2
(`GNSS_PWR_EN`), feeding U4 (TPS7A2033 LDO) IN+EN, which produces `GNSS_3V3` for U2
(Quectel LC29H). Per `CONNECTIONS.md`, `GNSS_BCKP` is derived from `GNSS_3V3` through
a 0R link (not independently re-confirmed against the live RevA netlist during the
Power Architecture Review). Quectel's hardware design guide imposes explicit
power-up sequencing and ripple requirements on this rail.

## Problem

Quectel `LC29H_Series_Hardware_Design_V1.2.pdf` §3.4 "Power-up Sequence" requires:

1. `V_BCKP` must be powered **simultaneously with `VCC` or before it** ("the backup
   unit should start up no later than the PMU").
2. `VCC` must rise in **< 50 ms** with **< 50 mV** ripple during rise.

If `GNSS_BCKP` and `GNSS_3V3` are genuinely tied via a 0R link (same electrical node),
requirement 1 is trivially satisfied. Requirement 2 (turn-on speed and ripple) has not
been computed against U7/U4's actual behavior. U7's CT = 1 nF gives a
datasheet-referenced ~ms-scale controlled turn-on (TI `tps22917.txt`: CT = 1000 pF →
4000 µs / 4 ms turn-on at 5 V, the closest documented reference point to our exact
value), which is under the 50 ms limit by a wide margin, but this has not been
formally verified against LC29H's specific limits, nor has the 0R backup-tie been
re-confirmed in the current RevA netlist (schematic has changed significantly since
`CONNECTIONS.md` was written).

## Alternatives

| Option | Description | Trade-off |
|---|---|---|
| A. Re-verify existing topology against Quectel's limits | No schematic change; confirm `GNSS_BCKP`/`GNSS_3V3` tie and turn-on timing/ripple in the current RevA netlist and against U7/U4 datasheet behavior. | Zero cost if the existing topology already passes; low-risk verification-only step. |
| B. Add explicit sequencing hardware | e.g. independent backup supply with its own controlled ramp, or a dedicated sequencer. | Only justified if Option A's check reveals a real violation; otherwise unnecessary cost/complexity/area. |

## Decision

**Option A — verify, do not redesign.** No schematic change is authorized under this
ADR. The existing U7→U4→GNSS_3V3 topology, and the `GNSS_BCKP` 0R tie to `GNSS_3V3`,
are provisionally accepted as compliant with Quectel's sequencing requirements based
on the datasheet reference points gathered during the Power Architecture Review, but
this ADR records an open verification action, not a closed one.

## Consequences

- **Positive:** No premature hardware addition; the topology as designed is plausible
  and low-risk based on available evidence.
- **Negative / open item:** The 0R `GNSS_BCKP` tie must be re-confirmed directly
  against `hardware/RevA/marine-tracker-RevA.kicad_sch`'s live netlist (not just the
  older `CONNECTIONS.md` description) before this can be closed as fully verified.
  U7/U4's turn-on ripple has not been computed against the 50 mV limit.
- **Follow-up action:** Perform the netlist re-check and ripple calculation before
  `PROTOTYPE_READY` status is claimed (`docs/ACCEPTANCE_CRITERIA.md` item 5, "Power
  path ผ่านการคำนวณ voltage drop/temperature rise").

## References

- Quectel `LC29H_Series_Hardware_Design_V1.2.pdf` §3.4 "Power-up Sequence."
- TI `tps22917.pdf` — CT-to-turn-on-time reference data (CT = 1000 pF → 4000 µs at 5 V).
- `CONNECTIONS.md` — GNSS_BCKP/GNSS_3V3 0R tie description (pre-dates recent schematic
  changes; needs re-confirmation).
- Engineering Change Proposal, ECP-5 (this conversation).

## Approval status

**APPROVED** as a verification-only action. No hardware change is authorized until
the open verification items above are closed.
