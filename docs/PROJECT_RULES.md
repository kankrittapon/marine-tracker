# Mandatory Engineering Rules

คำว่า MUST/ห้าม เป็นข้อบังคับ ไม่ใช่คำแนะนำ

## 1. Scope control

- MUST ทำงานเฉพาะ NK Marine Tracker Rev A
- MUST อ่าน Project Brief, Features, Acceptance Criteria และ Status ก่อนแก้ไฟล์
- MUST เสนอแผนและระบุไฟล์ที่จะเปลี่ยนก่อนการแก้ใหญ่
- MUST หยุดถามผู้ใช้เมื่อข้อมูลที่ขาดมีผลต่อ safety, RF, stackup, connector, battery หรือ manufacturing
- ห้ามเพิ่ม Solar, ESP32, ESP8266 หรือ external MCU โดยไม่ได้รับอนุมัติ

## 2. Source of truth

ลำดับความน่าเชื่อถือ:
1. Datasheet/hardware design guide ฉบับตรง part number
2. KiCad source ใน repository
3. Measurement/DRC/ERC report
4. ภาพถ่าย reference
5. ข้อสันนิษฐาน

ข้อสันนิษฐานต้องระบุ `ASSUMPTION:` และห้ามนำไปใช้สร้าง Gerber final

## 3. Editing policy

- MUST ใช้ KiCad GUI หรือ `kicad-cli` สำหรับ ERC, DRC, render และ fabrication exports
- ห้ามใช้ Python, regex หรือ text substitution เพื่อ rewrite `.kicad_sch`/`.kicad_pcb`
- ห้ามแก้ S-expression โดยตรงแบบ bulk
- การแก้ text file, Markdown, JSON, TOML, TypeScript ทำได้
- ก่อนแก้ KiCad ต้องสร้าง backup/commit
- หลังแก้ KiCad ต้องตรวจ parse, ERC/DRC และ diff

## 4. PCB rules

- 4-layer: L1 components/RF/power, L2 solid GND, L3 power/slow signals, L4 signals/GND
- ห้าม split ground ใต้ RF, USB, SIM clock หรือ modem
- VBAT_MODEM ต้องรองรับ burst 2 A พร้อม margin; ห้ามมี via เดี่ยวเป็น bottleneck
- Bulk/decoupling ของ modem ต้องอยู่ใกล้ VBAT pins ตาม hardware guide
- RF traces ต้องสั้น, ไม่มี sharp corner, มี continuous return path และ via fence ตาม geometry
- ห้ามล็อกความกว้าง RF จนมี stackup จากโรงงาน
- GNSS patch keepout ต้องไม่มี battery, shield, magnet หรือ copper ที่ขัดกับ antenna guide
- Test pads: USB D+/D-, VBUS, GND, UART TX/RX, BOOT, PWRKEY, RESET และ battery measurement ตามความจำเป็น

## 5. Marine rules

- ENIG หรือ finish ที่เหมาะกับ coating
- ไม่มี exposed copper ที่ขอบบอร์ดโดยไม่จำเป็น
- วาง connector ให้ไม่เป็นจุดรับน้ำ/คราบเกลือ
- ระบุ conformal-coating keepout สำหรับ SIM, RF connector, button, USB และ programming pads
- แบตต้องมี thermal consideration และห้ามวางใต้ GNSS patch

## 6. Deliverable truth labels

ใช้สถานะเท่านั้น:
- CONCEPT
- ENGINEERING_DRAFT
- REVIEW_REQUIRED
- PROTOTYPE_READY
- PRODUCTION_RELEASED

ห้ามใช้คำว่า “สมบูรณ์”, “พร้อมผลิต”, “DRC 0” หรือ “50 Ω แล้ว” หากไม่มี report รองรับ

## 7. Required output after each task

รายงาน:
- Changed files
- Engineering rationale
- Checks actually run
- Checks not run
- New assumptions/risks
- Next blocking decision
