# Feature Backlog

## P0 — ต้องเสร็จก่อนสั่ง 10 แผ่น

- [ ] ตรวจ pin-by-pin schematic ของ A7670, GNSS, charger, USB-C, SIM, flash, level shifting และ watchdog
- [ ] เลือก A7670 SKU ที่มี LTE bands เหมาะกับไทย/Asia และยืนยัน OpenCPU SDK
- [ ] Freeze GNSS: LC29H เทียบ L76K/low-power alternative
- [ ] Freeze battery connector, battery chemistry, capacity และ envelope
- [ ] Route power tree: BAT_CELL, VBAT_MODEM, VSYS และ rails ทั้งหมด
- [ ] Route USB 2.0, SIM, UART, SPI และ control signals
- [ ] ยืนยัน stackup โรงงานและคำนวณ LTE/GNSS 50-ohm CPWG/microstrip
- [ ] Ground zones, stitching vias, RF via fences และ thermal paths
- [ ] ERC 0 errors ที่เกี่ยวข้อง; documented waivers เท่านั้น
- [ ] DRC 0 errors; documented waivers เท่านั้น
- [ ] BOM พร้อม manufacturer part number และ alternates
- [ ] CPL/Pick-and-place, Gerber, drill, assembly drawing
- [ ] Independent pre-production review

## P1 — แนะนำสำหรับ Rev A

- [ ] Fuel gauge เช่น MAX17048-class
- [ ] Battery NTC / temperature measurement
- [ ] Low-power IMU เช่น LIS2DW12-class สำหรับ motion wake
- [ ] Reverse-current/reverse-polarity protection
- [ ] ESD/TVS ที่ USB, SIM, external connectors และ RF แบบ capacitance เหมาะสม
- [ ] Pogo programming/test fixture definition
- [ ] Current profiling modes: shipping, sleep, GNSS fix, network attach, TX burst

## P2 — หลังต้นแบบติด

- [ ] OpenCPU firmware base: GNSS parser, MQTT/HTTPS, offline queue, watchdog, OTA/FOTA
- [ ] Power-state machine และ adaptive reporting interval
- [ ] Enclosure STEP, gasket, membrane vent และ coating mask
- [ ] Environmental tests: heat soak, condensation, salt fog, vibration/drop
- [ ] Production test application และ pass/fail limits

## Explicitly out of scope Rev A

- Solar charger
- ESP32/ESP8266/external application MCU
- Satellite communication
- RTK unless user explicitly changes product requirement
