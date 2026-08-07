# Marine Tracker Rev B — ST909-inspired floorplan

ไฟล์นี้เป็นการปรับปรุง Floorplan จาก `marine-tracker-v1.3.kicad_pcb` โดยใช้ภาพบอร์ด ST909B-4G-V1.0 เป็นข้อมูลอ้างอิงด้านการจัดวางเท่านั้น ไม่ได้คัดลอกวงจรหรือค่า RF matching ของ ST909

## สิ่งที่ปรับ

- คงขนาดบอร์ดเดิมประมาณ 65 × 50 มม.
- จัดกลุ่ม A7670G, Nano-SIM, GNSS, Power และ RF connector ให้แบ่งโซนชัดเจนขึ้น
- ย้าย TP1–TP19 ไปด้านหลังบอร์ด (`B.Cu`) และเรียงเป็น Pogo-jig grid เพื่อให้พื้นที่ด้านหน้าว่างขึ้น
- จัด LTE U.FL และ GNSS U.FL ไว้ริมบอร์ด ลดความยาวสาย RF
- เพิ่มกรอบ `GNSS PATCH KEEP-OUT 20 × 20 mm` บน User.Drawings สำหรับเสา Patch ที่ติดในฝาหรือเชื่อมผ่าน J4 coax
- เพิ่มคำเตือนห้ามวางแบตหรือโลหะใต้พื้นที่ GNSS patch
- คง USB, SIM, Battery connector และจุด Boot/PWRKEY/Debug สำหรับการผลิตล็อตทดลอง

## สถานะทางวิศวกรรม

ไฟล์นี้เป็น **Floorplan/placement revision** ไม่ใช่ Gerber พร้อมผลิต เนื่องจากยังต้อง:

1. Route เน็ตไฟเลี้ยงและสัญญาณทั้งหมดให้ครบ
2. วาง GND plane และ stitching vias
3. ยืนยัน stackup โรงงานเพื่อคำนวณ 50 Ω CPWG/Microstrip
4. รัน KiCad ERC/DRC จริง
5. ตรวจ BOM/footprint เทียบ datasheet ทีละรายการ
6. ตรวจเสา LTE/GNSS หลังใส่กล่องและแบตจริงด้วย VNA

## ข้อควรระวังก่อนสั่ง 10 แผ่น

อย่าส่งผลิตจากไฟล์นี้โดยตรงจนกว่าจะผ่าน DRC และตรวจ RF/power layout ครบ การออกแบบ RF จากภาพถ่ายไม่สามารถยืนยัน impedance หรือ matching component values ได้
