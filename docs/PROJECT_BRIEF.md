# Project Brief — NK Marine Tracker Rev A

## เป้าหมาย

ออกแบบ GPS/LTE asset tracker ขนาดอยู่กลางฝ่ามือ สำหรับใช้งานชายฝั่งและสภาพแวดล้อมทางทะเล ผลิตต้นแบบล็อตแรกขั้นต่ำ 10 PCB โดยเน้นความเสถียร การกินไฟต่ำ การซ่อมและโปรแกรมในโรงงานได้ และไม่ใช้ MCU ภายนอกอย่าง ESP32/ESP8266

## สถาปัตยกรรมที่ล็อกแล้ว

- Cellular/OpenCPU: SIMCom A7670 family รุ่นที่เหมาะกับย่านไทย/เอเชียและมี OpenCPU/Open-SDK
- GNSS: โมดูลแยกผ่าน UART; แบบปัจจุบันใช้ LC29H footprint แต่สามารถประเมิน L76K/รุ่น low-power ก่อน Freeze BOM
- SIM: Nano-SIM; เผื่อทางเลือก eSIM footprint ได้แต่ไม่บังคับใน Rev A
- Battery: Li-ion/LiPo 1S แบบชาร์จได้
- Charging: USB-C เท่านั้นใน Rev A
- Solar: ตัดออกทั้งหมดใน Rev A
- PCB: 4-layer, palm-size เป้าหมายประมาณ 60 × 45 mm และห้ามเกิน 65 × 50 mm โดยไม่มีเหตุผลที่ได้รับอนุมัติ
- RF: LTE และ GNSS ต้องเป็น 50-ohm geometry อ้างอิง stackup โรงงานจริง
- Environment: กล่องสีอ่อน IP67/IP68, conformal coating, ป้องกันไอเกลือและ condensation

## ต้นแบบอ้างอิง

ST909/ST909B-4G-V1.0 ใช้เป็น reference ด้าน floorplan เท่านั้น: A7670SA, Quectel L76K, GNSS patch ด้านหลัง, test pads, SOS button และ RF connectors. ห้ามคัดลอก schematic, matching values หรือ power circuit จากภาพถ่ายโดยไม่มีหลักฐานจาก datasheet/measurement

## หลักการออกแบบ

1. Datasheet และ hardware design guide ของผู้ผลิตเป็น source of truth
2. ห้ามเดาขา, ค่า R/L/C, RF matching, stackup หรือ current capability
3. ทุกการเปลี่ยนต้อง traceable ใน CHANGELOG และ decision log
4. ห้ามเรียกไฟล์ว่า production-ready จน ERC/DRC ผ่าน, RF stackup ยืนยัน, BOM/CPL/Gerber ตรวจแล้ว
