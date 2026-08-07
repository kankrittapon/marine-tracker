# marine-tracker-guard MCP

MCP นี้เป็น allowlist wrapper สำหรับ `kicad-cli` เท่านั้น:

- project_inventory
- validate_schematic
- validate_pcb
- render_pcb
- export_gerbers_candidate (ล็อกด้วย `ALLOW_FAB_EXPORT=YES`)
- guardrail_check

ไม่มี arbitrary shell, ไม่มี Python และใช้ `spawn(..., shell:false)`. ทุก path ต้องอยู่ภายใน `PROJECT_DIR`.

ข้อจำกัด: MCP ป้องกันเฉพาะคำสั่งที่ผ่าน MCP. ต้องปิดหรือจำกัด built-in shell/Python ของ client แยกต่างหาก
