# สถานะตรวจ/แก้ schematic — marine-tracker-v1

อัปเดตล่าสุด: 2026-08-04 (session ตรวจ ERC + แก้ label ชนกัน + ลงทะเบียน footprint library)

ไฟล์นี้เขียนไว้เป็น handoff — ถ้าเปิด session ใหม่มาทำต่อ อ่านไฟล์นี้ก่อนเพื่อไม่ต้องไล่ ERC ใหม่ทั้งหมด

## สถานะอ้างอิงปัจจุบัน (2026-08-05, อัปเดตล่าสุด: แก้ SIM_DET)

- ERC สด: **0 violations** (0 errors, 0 warnings)
- **SIM_DET แก้แล้ว**: symbol J5 เดิม (`Connector:SIM_Card` มาตรฐาน) ไม่มี pin รองรับ card-detect switch เลย ทั้งที่ footprint จริง (`nanoSIM_GCT_SIM8060-6-1-14-00`) มี pad ชื่อ `"SW"` สำหรับสวิตช์นี้อยู่แล้ว — สร้าง symbol ใหม่ `MarineTracker:SIM_Card_DET` (clone จาก `Connector:SIM_Card` เดิม + เพิ่ม pin เลข `"SW"` type passive) เพิ่มเข้า `MarineTracker.kicad_sym` และสลับ J5 มาใช้ symbol นี้แทน ต่อ `SIM_DET` label เชื่อม J5 pin `SW` เข้ากับ U1 pin34 (USIM1_DET) แล้ว ยืนยันด้วย netlist
  - **แก้ shield แล้ว**: เพิ่ม pin `SH` type passive ใน project/embedded symbol และต่อ GND ใน schematic; pad `SH` ทั้ง 3 จุดใน footprint ใช้หมายเลขเดียวกัน จึงรับ GND net พร้อมกันทั้งหมด
- SIMCom hardware guide ระบุ U1 pin34 `USIM1_DET` เป็น `I/O,PU` จึงมี pull-up ภายในและไม่ต้องเพิ่ม pull-up ภายนอกสำหรับสวิตช์ active-low นี้
- V1 ใช้ GNSS UART1 เท่านั้น: ถอน R14/R15 และ labels GNSS I²C; LC29H pins 18/19 คง NC
- เปิดใช้ offline storage: U6 เปลี่ยนจาก W25Q32JV 3V/DNP เป็น **W25Q32JWSSIM 1.8V**, ต่อ SPI กับ U1 pins 11–14, เพิ่ม R28/R29 10k pull-up ที่ WP/HOLD และ C29 100n decoupling
- snap U3/D1 และ labels ที่เกี่ยวข้องเข้ากริด 1.27 mm; ตรวจ netlist หลังแก้แล้ว connectivity เดิมครบ
- Footprint U1/U2 resolve แล้ว; pad U1 1–124 และ U2 1–24 ครบ ไม่ซ้ำ
- แก้ annotation error แล้ว: VBAT_ADC divider เปลี่ยนจาก R24/R25 ที่ซ้ำ เป็น **R26=680k / R27=470k**
- R24=100k คงเป็น CHG_STATUS pull-up; R25=100k คงเป็น GNSS_WAKE bias
- ถอน label `CELL_RESET_A` ที่เลิกใช้และใส่ no-connect ที่ U5 A3
- แก้ชนิดขาใน project symbol และ embedded symbol ให้ตรงหน้าที่: U1 VBAT_ADC=`input`, U1 GPIO4=`bidirectional`, U7 QOD=`passive`; ERC exceptions เดิมทั้ง 3 รายการจึงหายโดยไม่เปลี่ยน connectivity
- export netlist ผ่านโดยไม่มี annotation warning; duplicate ที่เหลือมีเฉพาะ D3 จำนวน 4 unit ซึ่งถูกต้องสำหรับ multi-unit symbol
- รายการค้างเชิงสถาปัตยกรรม: auto-start/cold-recovery และการยืนยัน watchdog เมื่อโมเด็มปิดสนิท (ไม่ปรากฏใน ERC)

> ส่วนอัปเดตเก่าด้านล่างเป็นประวัติการตรวจ อาจบรรยายสถานะก่อนแก้ หัวข้อนี้และ ERC ล่าสุดเป็นแหล่งอ้างอิงหลัก

---

## ⚠️ ข้อควรระวังก่อนอ่านต่อ

**ไฟล์ `marine-tracker-v1.kicad_sch` ถูกแก้แบบ concurrent** — ระหว่าง session นี้ ผู้ใช้เปิด KiCad GUI แก้ไฟล์เดียวกันไปพร้อมกัน (ยืนยันจากผู้ใช้เองแล้ว) เพิ่ม component ใหม่เข้ามาระหว่างทาง: **U7 (TPS22917DBV, GNSS load switch), U8 (TPL5010, watchdog timer), C26–C28, R21–R23, TP1–TP12** — ผมยังไม่ได้รีวิว component กลุ่มนี้เลยสักตัว ไม่รู้ว่าต่อสายครบหรือยัง

ทุกครั้งที่จะแก้ไฟล์นี้ด้วยสคริปต์ (ไม่ใช่ผ่าน KiCad GUI) ต้อง **อ่านไฟล์สดใหม่ก่อนเขียนทุกครั้ง** ห้าม cache เนื้อหาไว้ข้ามคำสั่ง เพราะมีความเสี่ยง lost-update ถ้า KiCad GUI เซฟทับพอดีจังหวะเดียวกัน

**เครื่องมือ MCP (KiCAD-MCP-Server) ใช้ไม่ได้กับสคีมานี้** — `open_project`/`load_schematic` ผ่าน local SWIG backend แครชทุกครั้ง ("SWIG proxy is dehydrated") ต้องใช้ `kicad-cli.exe sch erc` / `kicad-cli.exe sch export netlist --format kicadxml` แทน (เสถียรกว่ามาก อ่านอย่างเดียว ไม่แก้ไฟล์)

---

## ✅ สิ่งที่แก้ไปแล้ว (ยืนยันด้วย ERC + netlist แล้ว)

### บั๊กการเดินสาย (ไม่ใช่แค่ ERC noise — ต่อผิดจริง)
| จุด | ปัญหาเดิม | แก้เป็น |
|---|---|---|
| L1 (GNSS bias-tee) ขาบน | label `GNSS_BIAS_LIMITED` ซ้อนทับ `USB_VBUS_FUSED` — bias เสาอากาศ GNSS ต่อตรงเข้า USB VBUS 5V ดิบ | ลบ `USB_VBUS_FUSED` ที่ซ้อนออก เหลือ `GNSS_BIAS_LIMITED` |
| L1 ขาล่าง | label `GNSS_RF_CONN` ซ้อนทับ `GND` — สาย RF ของ GNSS ต่อลงกราวด์ | ลบ `GND` ที่ซ้อนออก เหลือ `GNSS_RF_CONN` |
| U3 pin1 (TS) vs FB1 pin2 | label `CHG_TS` ซ้อนทับ `VBAT_MODEM` — thermistor sense ต่อรวมกับสาย VBAT กำลังสูง | ลบ `CHG_TS` ที่ซ้อนออก เหลือ `VBAT_MODEM` |
| U1 pin53 (GPIO4) | มี pin จริงชนกับ U3 pin7 (PGOOD) ตรงๆ ทางกายภาพ (ไฟล์นี้ไม่มี wire เลย ใช้พิกัดชนกันแทนสายทั้งไฟล์) + มี label `CELL_PPS_A` แอบมาเกาะจุดเดียวกัน ดึง U5 (level shifter) เข้ามาพัวพันด้วย | ลบ `CELL_PPS_A` ที่จุดนี้ออก (คง PGOOD↔GPIO4 ไว้ตามที่ตั้งใจ), เพิ่ม **R20 (10k pull-up ไป VDD_1V8)** ให้ PGOOD (open-collector ต้องมี pull-up) |
| A7670G pin100 (1PPS เฉพาะ) | ไม่ได้ต่ออะไรเลย ทั้งที่มี pin เฉพาะสำหรับรับ PPS | เพิ่ม label `GNSS_PPS_A` เชื่อมกับ U5 pin A4 (ซึ่ง level-shift มาจาก LC29H pin3 1PPS จริงผ่าน `GNSS_PPS_B`) — เปลี่ยนชื่อจาก `CELL_PPS_A` (เข้าใจผิดว่ามาจากโมเด็ม) เป็น `GNSS_PPS_A` |
| U1 GND 28 ขา (pin 2,17,18,29,39,45,46,54,58,59,62,63,64,65,69,70,71,72,73,75,76,78,79,80,81,85,86,88) | ไม่มี label ต่อเลย ลอยอยู่เฉยๆ (มีแค่ 10 ขาจาก ~38 ขาที่ถูกต่อ) | เติม `GND` label ให้ครบ — ตอนแรกคำนวณพิกัดผิด 3 ขา (2,17,18) เพราะ regex scan ไปเจอ pin เลขเดียวกันจากคอมโพเนนต์อื่นก่อน แก้พิกัดถูกแล้ว ยืนยันด้วย netlist ว่า GND รวมเป็น net เดียว 38 ขา |
| J5 (SIM) pin1 VCC, pin5 GND | ไม่ต่ออะไรเลย | pin1 → label `SIM_VDD` (net เดียวกับ U1 pin30 USIM1_VDD), pin5 → `GND` |

### Power symbol / PWR_FLAG (ของที่ ERC บ่นว่า "ไม่มี driver" เพราะไฟล์นี้ไม่มี power symbol เลยสักตัว)
เพิ่ม PWR_FLAG จริง 5 จุด: **GND, VBAT_MODEM, USB_VBUS_FUSED, USB_VBUS_MODEM, GNSS_VBACKUP**
(เคยใส่ตัวที่ 6 บน `CHG_STATUS` ไปด้วย แต่ถอนออกแล้ว — net นั้นเป็นสัญญาณสถานะ open-collector ไม่ใช่ power rail จริง ใส่ PWR_FLAG กลับไปสร้าง conflict ใหม่)

เพิ่ม `power` library เข้า project `sym-lib-table` ตรงๆ (เดิม global sym-lib-table เป็นแค่ nested "Table" ชี้ template ของ KiCad ซึ่ง `kicad-cli` ไม่ตามไปอ่าน)

### Footprint library
- สร้าง project-level `fp-lib-table` ลงทะเบียน library มาตรฐานที่ใช้จริงทั้งหมด (Capacitor_SMD, Connector_Card/Coaxial/JST/USB, Diode_SMD, Filter, Fuse, Inductor_SMD, MountingHole, Package_DFN_QFN/SO/TO_SOT_SMD, Resistor_SMD, MarineTracker)
- สร้างโฟลเดอร์ `MarineTracker.pretty` ไว้ (ว่างเปล่า รอ footprint จริงของ U1/U2)

### Footprint ที่อ้างชื่อผิด (ไม่ใช่แค่ library ไม่ถูกลงทะเบียน — ชื่อ footprint ที่ระบุไว้ไม่มีอยู่จริง)
| Ref | เดิม | แก้เป็น | หมายเหตุ |
|---|---|---|---|
| D2, D4, D5 | `Package_TO_SOT_SMD:SOD-882` (ไม่มีในไลบรารีนี้) | `Diode_SMD:D_SOD-882` | ตรงกับที่ symbol library เองแนะนำอยู่แล้ว |
| D3 | `Package_DFN_QFN:DFN-10-1EP_2.5x1mm...` (ไม่มีจริง) | `Package_TO_SOT_SMD:SOT-886` | เช็ค datasheet Nexperia จริงแล้ว — PESD5V0L4UF ใช้ package SOT886/XSON6 (6 พิน) ไม่ใช่ DFN-10 |
| U3 (BQ24074RGT) | `...VQFN-16...EP2.6x2.6mm` (ไม่มีจริง) | `Texas_RVA_VQFN-16-1EP_3.5x3.5mm_P0.5mm_EP2.14x2.14mm` | ตรงกับ exposed-pad จริงตาม TI datasheet package RGT |
| FL1 | `Filter:Filter_SAW_1.4x1.1mm` (ไม่มีจริง) | `Filter:Filter_1411-5_1.4x1.1mm` | ขนาดเดียวกันตรงกับ B39162B2651P810 |
| J5 (SIM) | `Connector_Card:SIM_Card_Wurth_693072010801` (เลขพาร์ทนี้จริงๆ เป็น **microSD** ไม่ใช่ SIM) | `Connector_Card:nanoSIM_GCT_SIM8060-6-1-14-00` | เลือกตัวมี card-detect switch (มี label `SIM_DET` รออยู่แล้ว) — เป็นแบบ **hinged พับเปิด** (ไม่ใช่ push-type ตามที่บอกผิดไปตอนแรก) |

**ผล ERC**: 242 → 36 violations (ตัวเลขกลาง ๆ ที่เคยรายงานไป เช่น 237/167 ไม่แม่นเท่าตัวสุดท้าย — พบว่า footprint ที่อ้างชื่อผิดทำให้ `kicad-cli sch erc` รันแบบไม่สมบูรณ์/ไม่ครบ พอ footprint ทุกตัวหาเจอ ERC เพิ่งรันผ่านแบบเต็มรอบจริงครั้งแรก ตัวเลข 36 นี้น่าเชื่อถือกว่าตัวเลขก่อนหน้าทั้งหมด)

---

## 🟡 ยังค้างอยู่ — ต้องตัดสินใจ/ลงมือทำต่อ

### 1. Footprint จริงของ U1 (A7670G) และ U2 (LC29H) — ใหญ่สุด สำคัญสุด
เจอ datasheet ทางการแล้ว ยังไม่ได้วาด:
- **U1 A7670G**: SIMCom hardware design guide หน้า 24 (Figure 4) — 124 พิน (80 LCC วงนอก + 44 LGA วงใน) ผสม 4 pitch (1.00/1.40/3.80/0.90mm) **ซับซ้อนมาก เสี่ยงพิมพ์พิกัดผิดสูง ไม่ควรทำแบบ hand-edit raw text**
  - PDF ต้นฉบับ **มีอยู่แล้วในโปรเจกต์**: `references/A7670X_HW.pdf` (ไม่ต้องหาใหม่ — ตอนแรกไปค้นเว็บหาซ้ำโดยไม่รู้ว่ามีอยู่แล้ว)
  - รูป crop หน้า footprint ไว้แล้วที่ `references/a7670_footprint_p24.png`
- **U2 LC29H**: Quectel `LC29H_Series_Hardware_Design` V1.3 หน้า 47-48 (Figure 19) + หน้า 26 (pin assignment) — 24 พิน castellated 2 คอลัมน์ ง่ายกว่ามาก แต่ยังไม่ได้ทำ
  - ยังไม่มี PDF ต้นฉบับเก็บไว้ในโปรเจกต์ (ดาวน์โหลดจากเว็บตอนตรวจ ไม่ได้ save ไว้ถาวร) — รูป crop ไว้ที่ `references/lc29h_footprint_p48.png` และ `references/lc29h_pinassign_p26.png`
- **แนะนำ**: วาดใน KiCad Footprint Editor เอง (มี pad-array tool + วาง datasheet image อ้างอิงเทียบสดได้) ปลอดภัยกว่าให้ AI พิมพ์ราบ .kicad_mod มือเปล่า

### 2. D3 (PESD5V0L4UF) ต่อสายไม่ครบ — ไม่ใช่แค่ footprint
ตอนแรกคิดว่าแค่ unit B/C/D ไม่ได้วาง (ERC `missing_unit`) แต่เช็คละเอียดพบว่า **แม้แต่ unit A ที่วางไว้แล้วก็ pin1(K1)/pin2(A) ไม่ได้ต่อสายเลย** — แปลว่า ESD protection diode ตัวนี้ยังไม่ทำงานอะไรทั้งสิ้นตอนนี้ ต้องต่อสายจริงและตัดสินใจว่าจะใช้กี่ channel จาก 4 channel ที่มี

### 3. SIM interface ต่อไม่ครบ (J5 ↔ U1)
`RST`, `CLK`, `I/O`(=DATA), `VPP` ของ J5 ไม่ได้ต่อกับ A7670G เลย (VCC/GND แก้ให้แล้วในรอบนี้) — label ฝั่ง `SIM_RST`/`SIM_CLK`/`SIM_DATA` มีอยู่แต่เป็น isolated (แตะแค่ pin เดียว ไม่ถึง J5) ต้องเช็คว่า:
- pin name J5 ("I/O") ตรงกับ signal อะไรของ U1 (คาดว่าคือ SIM_DATA)
- VPP ไม่จำเป็นสำหรับ SIM สมัยใหม่ น่าจะปล่อย NC ได้ (ใส่ no-connect flag ให้ ERC เงียบ)

### 4. CHG_STATUS net ยังลอย (U3 pin9 ~CHG ↔ U1 pin51 VBAT_ADC)
เดิมเข้าใจผิดว่าเป็น power rail เลยใส่ PWR_FLAG (ถอนออกแล้ว) จริงๆ คือสัญญาณสถานะการชาร์จจาก BQ24074 ที่ควรไปเข้า ADC/GPIO ของโมเด็ม แต่ตอนนี้เช็คแล้วยังไม่ได้ต่อกันจริง (net นี้ isolated) ต้องต่อให้ครบ

### 5. Label อื่นที่ isolated (แตะ pin เดียว รอปลายทาง)
`GNSS_I2C_SDA`, `GNSS_I2C_SCL`, `GNSS_WAKE_B`, `PWRKEY` (U1 pin1) — เช็คว่าตั้งใจปล่อยว่าง (ฟีเจอร์ไม่ใช้) หรือลืมต่อ

### 6. รายละเอียดเล็กๆ จาก ERC ล่าสุด (36 violations, ดูไฟล์ `erc_handoff.json` ใน scratchpad ถ้าต้องการรายละเอียดเต็ม)
- `endpoint_off_grid` x2: D1 pin1, U3 pin1 — pin ไม่ตรง grid เป๊ะ (cosmetic)
- `no_connect_connected`: U5 pin5 (A4) มี no-connect flag ค้างอยู่ทั้งที่ต่อ GNSS_PPS_A แล้ว — ต้องลบ flag นั้นออก
- `pin_to_pin` (1, ยอมรับได้แล้ว): PGOOD/GPIO4 — มี pull-up (R20) แล้ว ERC ยังเตือนเพราะ type-check แบบ static ไม่รู้ว่า GPIO ถูก config เป็น input

---

---

## 🔄 อัปเดต (รอบ 2) — รีวิว component ใหม่ที่ผู้ใช้เพิ่มระหว่างทาง (U7, U8, TP1-13, R21-23)

ทั้งหมดเป็นงานที่ผู้ใช้ทำเอง (live-editing ใน KiCad GUI คู่ขนานกับ session นี้จริง ตามที่ยืนยันแล้ว):
- **U7 (TPS22917DBV) load switch + U8 (TPL5010) watchdog**: ออกแบบดี — VSYS → U7 → gate ทั้ง IN/EN ของ U4(LDO) → GNSS_3V3 → U2, ปิดได้ผ่าน GPIO2 (`GNSS_PWR_EN`); U8 `~RST` ต่อ `MODEM_RESET_N` (ร่วม pull-up R22 + TP10) ต่อ U1 RESET ถูกต้อง; R21+R23 (124k+107k ขนาน) ตั้งค่า `WDT_DELAY`
- **U7 pin5 (QOD) ต่อตรงกับ pin6 (VOUT)** — ตอนแรกเข้าใจผิดว่าเป็นบั๊ก ไปเช็ค datasheet TPS22917 จริงแล้วพบว่า **นี่คือวิธีต่อที่ถูกต้องตามคู่มือ TI เป๊ะ** (ต่อ QOD ตรงเข้า VOUT = fastest discharge time ตามที่ datasheet แนะนำ) — ERC เตือนเพราะ pin type ในไลบรารีเป็น "open collector" แต่ไม่ใช่บั๊กจริง **ไม่ต้องแก้**

### บั๊กที่เจอและแก้แล้วจากการย้าย U3
ตอนย้าย U3 (BQ24074) จากตำแหน่งเดิม (44.45, 44.45) ไปที่ใหม่ (210, 30) มี label `VBAT_MODEM` ตัวหนึ่งที่เดิมอยู่ตรงขา U1 pin57 (VBAT) ถูกลากติดไปด้วยโดยไม่ตั้งใจ ไปตกลงตรงขา TS (pin1) ของ U3 ที่ตำแหน่งใหม่แทน ผลคือ:
- U3 TS ไปชนกับ VBAT_MODEM (เหมือนบั๊กเดิมที่เคยแก้รอบแรก)
- U1 pin57 (VBAT เส้นที่ 3 จาก 3 เส้น) หลุดจากเน็ต ไม่มี label เหลืออยู่เลย
- U1 pin53 (GPIO4) หลุดจาก CHG_PGOOD ไปด้วย (ไม่แน่ใจว่าเกี่ยวกับการย้าย U3 โดยตรงหรือเปล่า)

**แก้แล้ว**: เปลี่ยน label ที่หลงไปอยู่ผิดที่ (222.7, 32.54) จาก `VBAT_MODEM` เป็น `CHG_TS`, เพิ่ม `VBAT_MODEM` ใหม่ที่ตำแหน่งเดิมของ U1 pin57 (57.15, 46.99), เพิ่ม `CHG_PGOOD` ใหม่ที่ตำแหน่ง U1 pin53 (57.15, 52.07) — ยืนยันด้วย netlist แล้วว่า 3 เน็ตนี้ถูกต้องครบ:
- `CHG_PGOOD` = R20 + U1(GPIO4) + U3(PGOOD)
- `CHG_TS` = J2(NTC) + R9 + U3(TS)
- `VBAT_MODEM` = bulk caps + FB1 + TP5 + U1 VBAT ครบ 3 ขา (55,56,57)

**ผล ERC**: 36 → 34 violations

**ข้อสังเกตสำคัญ**: บั๊กนี้เป็นแพทเทิร์นเดียวกับที่เจอซ้ำๆ ทั้งไฟล์ — สคีมานี้ไม่มี wire เลยสักเส้น ต่อกันด้วยพิกัดตรงกันเป๊ะเท่านั้น ฉะนั้น **การย้าย component ใดๆ ใน KiCad GUI ต้องเช็คให้แน่ใจว่า label ที่เกี่ยวข้องถูก select/ย้ายไปด้วยครบทุกตัว** ไม่งั้นจะเกิดบั๊กแบบนี้ซ้ำได้เรื่อยๆ ทุกครั้งที่ย้ายอะไรสักตัว

---

---

## 🔄 อัปเดต (รอบ 3) — วาง D3 unit B/C/D + ต่อ ESD ครบ 4 เส้น + เสร็จงาน SIM interface ไปในตัว

D3 (PESD5V0L4UF, quad ESD array, common-anode SOT-886) วางแค่ unit A (K1) ก่อนหน้านี้ ตอนนี้วางครบทั้ง 4 unit แล้วและต่อสายครบ:
- ขา anode ร่วม (pin2 + pin5 ที่ unit A) → `GND` (ผู้ใช้ต่อไว้เองแล้วก่อนที่ผมจะเช็ค)
- K1 (unit A) → `SIM_RST` → J5 pin2 (RST) + U1 pin33 (USIM1_RST)
- K2 (unit B, วางใหม่) → `SIM_CLK` → J5 pin3 (CLK) + U1 pin32 (USIM1_CLK)
- K3 (unit C, วางใหม่) → `SIM_VPP` (net ใหม่ เฉพาะ D3↔J5 เท่านั้น ไม่ต่อ U1 เพราะ VPP ไม่จำเป็นสำหรับ SIM สมัยใหม่ แต่ยังป้องกัน ESD ที่ contact ไว้)
- K4 (unit D, วางใหม่) → `SIM_DATA` → J5 pin7 (I/O) + U1 pin31 (USIM1_DATA)

ผลพลอยได้: การเดินสายนี้ทำให้ **SIM interface (J5↔U1) ที่เคยค้างอยู่ในข้อ 3 เสร็จไปด้วยในตัว** (RST/CLK/DATA ครบ, เหลือแค่ VPP ที่ตั้งใจปล่อยไม่ต่อ U1 และ SIM_DET ที่ symbol J5 ไม่มี pin รองรับเลย — ดูหัวข้อ "ยังค้างอยู่" ด้านล่าง)

**ผล ERC**: 34 → 13 violations — เหลือแต่รายการที่รู้อยู่แล้วว่าไม่ใช่บั๊ก (pin_to_pin x2 ยอมรับได้ทั้งคู่, footprint MarineTracker x2 รอวาด, endpoint_off_grid x2 cosmetic) และรายการที่ยังไม่ได้แตะ (GNSS_I2C_SDA/SCL, SIM_DET, GNSS_WAKE_B, CHG_STATUS)

**หมายเหตุระหว่างทาง**: ตอนเช็ค D3 pin2/5 เจอว่า netlist snapshot เก่าที่ cache ไว้บอกว่ายังไม่ต่อ GND แต่พอ export netlist ใหม่สดๆ พบว่าผู้ใช้ต่อไว้แล้วจริง — ยืนยันอีกครั้งว่าไฟล์นี้เปลี่ยนแปลงสดตลอดเวลา **ต้อง export netlist ใหม่ทุกครั้งก่อนเชื่อข้อมูล ห้ามใช้ snapshot เก่าข้ามคำสั่ง**

---

---

## 🔄 อัปเดต (รอบ 4) — GNSS_WAKE_B, CHG_STATUS, และ**ความผิดพลาดสำคัญที่แก้แล้ว**เรื่อง VDD_1V8/GNSS_2V8_IO

### ✅ แก้แล้ว ถูกต้อง
- **GNSS_WAKE_B** (U2 WAKEUP): เพิ่ม R25 (100k) pull-up ไป `GNSS_3V3` — tie แบบ static ตามที่ตกลง (always wake, คุมเปิด/ปิดทั้งชิพผ่าน U7/GNSS_PWR_EN แทน)
- **CHG_STATUS** (U3 ~CHG): ต่อเข้า **GPIO3 ของ U1** (เดิม GPIO3 ผูกกับ label `CELL_RESET_A` แต่ปลายทางจริง — U5 pin B3 — ไม่ได้ต่ออะไรเลย เป็น GPIO ที่ตายอยู่แล้วโดยพฤตินัย) เปลี่ยน label เป็น `CHG_STATUS` แทน + เพิ่ม R24 (100k) pull-up ไป `VDD_1V8` (open-collector ต้องมี pull-up) — **ผลข้างเคียง**: label `CELL_RESET_A` เดิมอีกจุด (ที่ U5 pin A3) เหลือเป็น isolated (โดดเดี่ยว) เพราะไม่มีอะไรใช้ level-shift channel นี้จริงอยู่แล้ว ถือว่ายอมรับได้ ไม่เสียฟีเจอร์ที่ใช้งานจริง

### ⚠️ ผมเข้าใจผิดและเกือบสร้างบั๊กร้ายแรง — แก้แล้ว
ตอนแรกวิเคราะห์ (ผิด) ว่า `VDD_1V8` และ `GNSS_2V8_IO` ไม่มี regulator จ่ายไฟเลย เลยเพิ่ม **U9 (TPS7A2018, 1.8V LDO จาก VSYS)** และ **U10 (TPS7A2028, 2.8V LDO จาก GNSS_SW_IN)** เข้าไปตามที่ตกลงกับคุณ — พอรัน ERC ใหม่ **เจอ `pin_to_pin: Power output ชนกับ Power output`** ทั้งสองจุดทันที เช็ค datasheet LC29H จริง (Table 6: Pin Description) แล้วพบว่า **`VDD_EXT` (pin7) เป็น Power Output ของโมดูลเอง ("Provides 2.8V for external circuit", 100mA) ไม่ใช่ input ที่ต้องป้อนไฟเข้า** — และ `MarineTracker:A7670G_LABE` symbol เองก็ประกาศ pin15 (`VDD_1V8`) เป็น `power_out` เหมือนกัน หมายความว่า **ทั้ง A7670G และ LC29H จ่ายไฟ 1.8V/2.8V ให้ตัวเองอยู่แล้ว ไม่ต้องมี regulator เพิ่ม** — ถอน U9/U10 และ label ที่เกี่ยวข้องออกทั้งหมดแล้ว

**บทเรียน**: การวิเคราะห์ "net นี้ไม่มี driver" จาก netlist member list เฉยๆ ไม่พอ ต้องเช็ค **pin type** ของแต่ละสมาชิกด้วยว่ามีตัวไหนเป็น `power_out` อยู่แล้วหรือเปล่าก่อนสรุปว่าต้องเพิ่ม regulator ใหม่ — ERC (`pin_to_pin` check) จับบั๊กนี้ได้ทันทีที่เพิ่ม component ผิดเข้าไป ซึ่งเป็นเหตุผลที่ต้องรัน ERC ยืนยันทุกครั้งหลังแก้ ไม่ใช่แค่เชื่อการวิเคราะห์ netlist เฉยๆ

**เรื่อง "watchdog รอดตอนโมเด็มแฮงค์ไหม"**: เนื่องจาก VDD_1V8 มาจาก pin ของ U1 เองที่ประกาศเป็น `power_out` (regulator ภายในโมดูล ไม่ใช่ software) โดยทั่วไป rail นี้จะยังมีไฟตราบใดที่โมเด็มมี VBAT อยู่ แม้ firmware/AT-command-processor จะแฮงค์ก็ตาม (เป็น hardware-level ไม่ขึ้นกับ firmware state) — **แต่ผมไม่มี datasheet A7670G ส่วนนี้มายืนยัน 100%** ต่างจาก LC29H ที่เช็ค datasheet จริงแล้ว ถ้าต้องการความมั่นใจเต็มที่ควรเช็ค SIMCom hardware design guide (`references/A7670X_HW.pdf`) ส่วน power-sequencing เพิ่มเติม

**ผล ERC**: 13 → 11 violations (นับจากรอบที่เพิ่ม U9/U10 ผิดแล้วแก้กลับ)

---

---

## 🔄 อัปเดต (รอบ 5) — วาด footprint U1 (A7670G) และ U2 (LC29H) เสร็จแล้ว

### LC29H_24LCC — วาดเอง จากข้อมูล datasheet ที่ดึงมาเอง
คำนวณตำแหน่ง pad ทั้ง 24 จาก Figure 19 (หน้า 48) + ยืนยันลำดับ pin จาก pin assignment (หน้า 26): 2 คอลัมน์ ห่างกัน 12.2mm, แต่ละคอลัมน์แบ่งเป็นกลุ่มบน 7 pad + gap 3mm + กลุ่มล่าง 5 pad (pitch 1.1mm ทั้งคู่) เช็คสมมาตรได้ลงตัว (pin24 อยู่ -7.0mm, pin13 อยู่ +7.0mm จากจุดกึ่งกลาง) ไฟล์อยู่ที่ `MarineTracker.pretty/LC29H_24LCC.kicad_mod`

### A7670G_LABE_124 — **ไม่ได้วาดเอง** ใช้ของ community แทน (ปลอดภัยกว่ามาก)
ลองวาดเองจาก SIMCom Figure 4 (หน้า 24) ก่อน แต่พบว่า pad ชั้นใน (44 พิน LGA) กระจายไม่เป็น grid สม่ำเสมอ ต้อง cross-reference กับ pin assignment diagram (หน้า 14, Figure 2) ซึ่งเป็นคนละสไตล์ภาพ (logical vs mechanical) ความเสี่ยงจับคู่เลขพินผิดสูงเกินไปสำหรับพาร์ท 124 ขา จึงเปลี่ยนแผน:
- หา community KiCad library แทน เจอ [sivakov512/kicad-library](https://github.com/sivakov512/kicad-library) (MIT license) มีไฟล์ `SIMCom_A7672X_A7670X.kicad_mod` ตรงพาร์ทพอดี
- **ตรวจสอบก่อนเชื่อ**: เทียบตำแหน่ง pad หลายจุดจากไฟล์นี้กับข้อมูลจาก datasheet จริงที่ผมดึงมาเอง — พบว่าตรงกันหมด (body 24×24mm ตรงกับสเปค, PWRKEY=pin1 ที่มุมซ้ายบน, GPIO4=pin53 ตรงกับที่ใช้ในสคีมา, RF_ANT=pin60 อยู่กึ่งกลางขอบบนตามจุดเด่นในรูป, กลุ่ม LCD_SPI/USIM2/CAM_I2C ทั้งหมดอยู่ตำแหน่งที่สมเหตุสมผล) มั่นใจมากกว่าที่จะวาดเองแน่นอน
- คัดลอกมาเป็น `MarineTracker.pretty/A7670G_LABE_124.kicad_mod` (เปลี่ยนชื่อ footprint ให้ตรงกับที่ schematic อ้างอิงอยู่)

### ผล ERC สุดท้าย: **242 → 9 violations**
ที่เหลือทั้งหมดเป็นรายการที่รู้แล้วว่าไม่ใช่บั๊ก หรือรอการตัดสินใจที่ยังไม่ได้ตอบ:
- `pin_to_pin` x2 — PGOOD/GPIO4 (มี pull-up แล้ว), U7 QOD/VOUT (ตรง datasheet TI, ไม่ใช่บั๊ก)
- `isolated_pin_label` x4 — GNSS_I2C_SDA/SCL (ยังไม่รู้ปลายทาง), SIM_DET (symbol J5 ไม่มี pin รองรับ), CELL_RESET_A (channel ที่เหลือจากการย้าย GPIO3 ไป CHG_STATUS)
- `endpoint_off_grid` x2 — D1, U3 pin1 (cosmetic ล้วน ไม่กระทบไฟฟ้า)
- `power_pin_not_driven` x1 — U1 VBAT_ADC (ADC sense pin ที่ symbol ระบุ type ผิดเป็น power, ไม่ใช่บั๊กจริง)

**สิ่งที่ยังต้องทำก่อนสั่งผลิตจริง**: เปิด footprint ทั้งสองใน KiCad Footprint Editor เทียบกับรูป datasheet ด้วยตาอีกรอบ (โดยเฉพาะ A7670G ที่มาจาก community ไม่ใช่ผมวาดเอง) และรัน DRC เต็มรูปแบบหลัง PCB layout จริงเริ่มแล้ว

---

## 😟 สิ่งที่กังวล

1. **Concurrent edit กับ KiCad GUI ที่เปิดอยู่จริง** — ความเสี่ยงหลักตอนนี้ ถ้าจะแก้ไฟล์นี้ต่อด้วยสคริปต์ ต้องเช็คให้แน่ใจว่าไม่ได้แก้ทับ component ที่เพิ่งเพิ่มมา (U7/U8/TP1-12/R21-23/C26-28) ที่ยังไม่ได้ review เลย
2. **ผมพลาดเองระหว่างแก้ 2 ครั้งในรอบนี้** — (1) วาง R20 ไปทับ U1 pin46 (GND) โดยไม่ตั้งใจตอน snap grid, (2) คำนวณพิกัด GND label ผิด 3 จุดเพราะ regex กว้างเกินไป ทั้งสองจุดจับได้และแก้แล้วจาก ERC แต่เป็นเครื่องเตือนว่า **การแก้ไฟล์ .kicad_sch แบบ raw text/regex มีความเสี่ยงจริง** ควร cross-check ด้วย ERC/netlist ทุกครั้งหลังแก้ ไม่ควรเชื่อการคำนวณพิกัดมือเปล่าเฉยๆ
3. **ตัวเลข ERC ที่รายงานไปก่อนหน้านี้ในบทสนทนา (242, 237, 167) ไม่แม่นยำเท่าที่ควร** เพราะ footprint ที่อ้างชื่อผิดทำให้ `kicad-cli` รันไม่ครบรอบ — ตัวเลขที่เชื่อถือได้คือรอบล่าสุด (36) เท่านั้น ถ้าจะอ้างอิงสถานะ ให้รัน ERC ใหม่เสมอ อย่าเชื่อตัวเลขเก่าในบทสนทนา
4. **U7/U8 และ component ใหม่ที่ผู้ใช้เพิ่มยังไม่ผ่านการรีวิวเลย** — ไม่รู้ว่ามีปัญหาแบบเดียวกับที่เจอใน U1-U6 (label ชนกัน, pin ลอย) หรือไม่ เพราะยังไม่ได้ดู

---

## 🔴 ออดิทเชิงหน้าที่เพิ่มเติมจาก netlist (2026-08-04 22:xx)

รอบนี้ไม่ได้ดูแค่ข้อความ ERC แต่ export `audit-current.xml` แล้วไล่สมาชิกของแต่ละ net จริง ผล ERC สดคือ **36 violations**. พบประเด็นต่อไปนี้ซึ่งต้องแก้ก่อนเริ่ม layout/สั่งผลิต:

### P0 — ต่อผิดจริง/อาจทำให้เครื่องไม่ทำงาน

1. **U3 pin 1 (BQ24074 TS) ต่ออยู่กับ `VBAT_MODEM`**
   - net ปัจจุบัน: `VBAT_MODEM = U3.1(TS), U1.55, U1.56, FB1.2, C5, C6, C25, TP5`
   - ส่วนสาย thermistor จาก J2 pin 2 อยู่คนละ net ชื่อ `CHG_TS` ผ่าน R9 จึงไม่ได้ถึง TS ของ charger
   - ข้อความก่อนหน้าที่ว่า “ลบ CHG_TS เหลือ VBAT_MODEM” เป็นการแก้ผิด ต้องถอนข้อสรุปนั้น
   - ต้องแยก U3.1 ออกจาก VBAT_MODEM แล้วต่อเข้าวงจร thermistor/temperature qualification ตาม BQ24074 datasheet

2. **USB-C J1 pin B8 (SBU2) ถูกต่อรวมกับ USB D+ ของโมเด็ม**
   - net ปัจจุบัน: `USB_DP_MODEM = D1.6, J1.B8(SBU2), U1.27(USB_DP)`
   - SBU2 ไม่ใช่ D+ และต้องไม่อยู่ในเส้น USB 2.0 นี้ การต่อปัจจุบันเพิ่ม stub/ESD path ผิดและอาจทำให้ USB enumeration ล้มเหลว
   - ต้องถอด label/net ออกจาก J1.B8 และใส่ no-connect หากไม่ได้ใช้ alternate mode

3. **U1 pin 24 VBUS ไม่มีแหล่ง 5 V**
   - `USB_VBUS_MODEM` มีเพียง U1.24 และ C8; ไม่ได้เชื่อมกับ `USB_VBUS_FUSED`
   - ต้องตรวจ A7670 hardware guide ว่า VBUS เป็น USB detect input และกำหนดการป้อนจาก VBUS fused (รวม divider/series element ถ้าผู้ผลิตกำหนด) ก่อนใช้ USB

4. **U1 pin 57 VBAT ยังลอย แม้ pin 55/56 ต่อแล้ว**
   - ต้องต่อ VBAT ทุกขาที่ผู้ผลิตกำหนดเข้าราง `VBAT_MODEM`; ห้ามถือว่าต่อบางขาเพียงพอ

### P0 — สถาปัตยกรรมเปิดเครื่อง/watchdog ยังไม่สมบูรณ์

5. **PWRKEY ของ U1 ยังไม่ได้ต่อกับวงจรขับ**
   - net `PWRKEY` มีเพียง TP9 แต่ U1.1 อยู่บน net unconnected แยกต่างหาก
   - หลังต่อแบต โมเด็มอาจไม่เริ่มเอง และไม่มีวงจรดึง PWRKEY ตาม pulse width ที่ SIMCom กำหนด

6. **TPL5010 ใช้ `VDD_1V8` ซึ่งสร้างโดย A7670 เอง**
   - net ปัจจุบัน: U8.1 ต่อ U1.15 (VDD_1V8 output)
   - เมื่อโมเด็มปิดหรือไฟภายในล้ม watchdog ก็ไม่มีไฟ จึงไม่ใช่ always-on supervisor และไม่สามารถปลุกระบบจาก cold-off ได้
   - WAKE ของ TPL5010 ต่อ MK_IN_2 ไม่ได้สร้าง PWRKEY pulse โดยอัตโนมัติ
   - ต้องเลือกระหว่าง (ก) เพิ่ม always-on LDO + transistor/open-drain ขับ PWRKEY หรือ (ข) ใช้ timer/power-gate architecture ที่ตัด/ต่อไฟโมเด็มได้จริง แล้วจึงสรุป U8

### P1 — interface ยังไม่ครบ

7. **SIM socket ต่อเพียง VCC/GND**
   - J5 RST/CLK/I-O ยังเป็น unconnected ขณะที่ `SIM_RST`, `SIM_CLK`, `SIM_DATA` ไปถึง U1 ฝั่งเดียว
   - J5 VPP ควรใส่ no-connect เมื่อยืนยันจาก datasheet/footprint แล้ว
   - D3 ยังไม่ได้ป้องกันเส้น SIM ใดจริง: D3 K1 ลอย และ unit/channel ที่เหลือยังไม่วาง

8. **PGOOD ไม่ได้ถึง GPIO4 ตามข้อความ audit เดิม**
   - `CHG_PGOOD` มีเพียง U3.7 และ R20.1; U1.53 GPIO4 ยัง unconnected
   - R20 pull-up ไป VDD_1V8 มีอยู่ แต่ยังไม่มีปลายรับสถานะ

9. **`VBAT_ADC` และ `CHG_STATUS` เป็นคนละหน้าที่และทั้งคู่ยังลอย**
   - U1.51 VBAT_ADC อยู่ unconnected; U3.9 `~CHG` อยู่บน `CHG_STATUS` เพียงขาเดียว
   - ห้ามต่อสอง net นี้เข้าหากันโดยอัตโนมัติ: `~CHG` เป็นสถานะ open-drain ส่วน VBAT_ADC เป็นทางวัดแบต ต้องตรวจระดับแรงดันและวงจร divider จาก SIMCom guide

10. **U5 A4 มี no-connect flag ค้างทั้งที่ต่อ `GNSS_PPS_A`**
    - เป็น cleanup ที่ควรแก้ แต่ไม่ใช่ความเสี่ยงเท่ารายการ P0

### สิ่งที่ตรวจแล้วในกลุ่ม U7/U8

- U7 VIN=`VSYS`, VOUT=`GNSS_SW_IN`, ON=`GNSS_PWR_EN`, CT มี C26 และ output มี C27: topology หลักครบ
- U7 QOD ต่อ VOUT โดยตรงทำให้ ERC เตือน open-collector ↔ power-output; อนุญาตได้เฉพาะเมื่อยืนยัน configuration นี้จาก TPS22917 datasheet และบันทึก ERC exclusion
- U4 IN/EN รับ `GNSS_SW_IN` และ OUT เป็น `GNSS_3V3`: ใช้งาน power gating ได้
- U8 REXT ใช้ R21 124k ขนาน R23 107k, reset มี R22 pull-up และ DONE/WAKE มีปลายทาง แต่ปัญหา always-on/PWRKEY ในข้อ 5–6 ยังทำให้ watchdog architecture ไม่ผ่าน

### เกณฑ์ผ่านรอบถัดไป

ก่อนเรียกว่า schematic พร้อมทำ PCB ต้องอย่างน้อย:

1. แก้ P0 ทั้ง 6 ข้อและ export netlist ยืนยันสมาชิก net ใหม่
2. ต่อ SIM + ESD ครบและตรวจ symbol-to-footprint pad mapping
3. สร้าง/ตรวจ footprint U1 และ U2 เทียบ mechanical drawing แบบ pad-by-pad
4. ERC ต้องไม่มี error จริง เหลือเฉพาะ warning/exception ที่มีเหตุผลและบันทึกไว้
5. ทำ power-state table: battery-only, USB-only, charging, modem-on, GNSS-off, deep-sleep และ cold-restart

### สถานะหลังแก้ชุดยืนยันจาก datasheet (2026-08-04 22:5x)

- แก้ U3 TS: `U3.1 -> CHG_TS` และ VBAT_MODEM มีเฉพาะรางไฟโมเด็ม
- ต่อ U1 VBAT pin 55/56/57 ครบ
- ต่อ PGOOD ถึง U1 GPIO4 พร้อม R20 pull-up
- ถอน J1.B8/SBU2 ออกจาก `USB_DP_MODEM`; SBU2 คง no-connect
- ต่อ U1.24 VBUS และ C8 เข้า `USB_VBUS_FUSED`
- ต่อ J5 RST/CLK/I-O ถึง `SIM_RST/SIM_CLK/SIM_DATA`; J5 VPP ใส่ no-connect
- เพิ่ม VBAT_ADC divider ตาม SIMCom: R24=680k จาก VBAT_MODEM และ R25=470k ลง GND, จุดกึ่งกลางเข้า U1.51
- ต่อ U1 PWRKEY ถึง net/test point แล้ว แต่ยังเป็น manual test point เท่านั้น ยังไม่มีวงจร auto-start/cold-recovery
- ถอน PWR_FLAG ที่ลอยและ NC marker ค้างบน GNSS PPS
- ERC หลังชุดนี้เหลือ 15 รายการ
- D3 multi-unit ยังไม่แก้: backend วาง unit B/C/D ไม่สำเร็จ จึงถอน label ทดลองทั้งหมดแล้ว ตรวจ netlist ยืนยันว่า SIM_VDD/RST/CLK/DATA ไม่ลัดรวมกัน
