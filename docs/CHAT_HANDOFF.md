# Conversation Handoff Summary

- ผู้ใช้ต้องการ tracker ทางทะเล ขนาดอยู่กลางฝ่ามือ
- ต้องการเขียน source บน cellular module/OpenCPU โดยไม่ใช้ ESP32/ESP8266
- SIM ใช้งานในเอเชีย/ไทย; ต้องพิจารณา B28 และ bands ของ exact SKU
- GNSS แยก; เดิมออกแบบ LC29H, มี reference ST909 ที่ใช้ L76K
- ตัด Solar ออกจาก Rev A
- แบตชาร์จได้ 1S และต้องอยู่ได้นาน
- ต้องรองรับความร้อน, ไอเกลือ, ความชื้น และกล่องกันน้ำ
- เป้าหมาย PCB 60 × 45 mm, สูงสุด 65 × 50 mm
- Reference board: ST909/ST909B-4G-V1.0, A7670SA + Quectel L76K, GNSS patch ด้านหลัง, SOS และ factory test pads
- CAD ปัจจุบันเป็น engineering draft/floorplan; ยังไม่พร้อมผลิต
- ขั้นต่อไป: schematic audit, exact SKU/GNSS/battery freeze, complete routing, stackup/RF, ERC/DRC, manufacturing pack
