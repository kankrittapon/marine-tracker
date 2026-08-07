# Marine Tracker RevA

# FMEA.md

---

| Failure | Cause | Detect | Recover | HW | FW | Severity |
|----------|-------|--------|----------|----|----|----------|
| LTE Lost | No Signal | Registration Timeout | Re-register | No | Yes | Medium |
| TCP Timeout | Network | Socket Timeout | Restart TCP | No | Yes | Medium |
| MQTT Hang | Broker | Heartbeat Timeout | Restart MQTT | No | Yes | Medium |
| GNSS Timeout | RF | No Fix | Restart GNSS | Optional | Yes | Low |
| SIM Removed | User | SIM Detect | Retry | No | Yes | Medium |
| Firmware Hang | Bug | Watchdog | Restart | Yes | Yes | High |
| Brownout | Battery | Supervisor | Restart | Yes | No | High |
| Flash Corruption | Power Loss | CRC | Restore Backup | No | Yes | High |
| Boot Loop | Firmware | Boot Counter | Safe Mode | No | Yes | High |
| USB Failure | ESD | Enumeration | Factory Recovery | No | No | Medium |

---

# Highest Priority Risks

1.
Brownout

2.
Firmware Lock

3.
Flash Corruption

4.
Boot Loop

These failures SHALL always have recovery paths.