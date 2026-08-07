# Prototype-Ready Acceptance Criteria

บอร์ดจะเป็น `PROTOTYPE_READY` ได้เมื่อครบทุกข้อ:

1. Schematic pin audit เสร็จและมี review record
2. ERC report ไม่มี unresolved electrical error
3. PCB ใช้ stackup โรงงานที่ยืนยันแล้ว
4. RF calculator/field-solver geometry บันทึกไว้ และ layout ตรง geometry
5. Power path ผ่านการคำนวณ voltage drop/temperature rise สำหรับ 2 A burst
6. DRC report ไม่มี unresolved error
7. Board outline และ placement ตรง battery/enclosure envelope
8. BOM ทุก fitted part มี exact MPN; DNP แยกชัด
9. Gerber/drill ผ่าน Gerber viewer independent check
10. CPL orientation ตรวจเทียบ pin-1 และ assembly drawing
11. Programming/recovery path เข้าถึงได้หลังประกอบ
12. Risks ที่ยังเหลือถูกบันทึก และผู้ใช้อนุมัติให้ผลิต prototype

`PRODUCTION_RELEASED` ต้องเพิ่มผลทดสอบจาก hardware prototype จริง จึงไม่สามารถประกาศจาก CAD เพียงอย่างเดียว
