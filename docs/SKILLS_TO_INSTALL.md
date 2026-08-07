# Skills / Tools ที่ต้องติดตั้ง

## Required

1. KiCad 9/10 พร้อม `kicad-cli` — เปิด, ตรวจ ERC/DRC, render และ export fabrication
2. Node.js 20+ — รัน MCP guard server
3. Git — version control, diff, rollback และ release tags
4. Gerber viewer อิสระ เช่น KiCad Gerber Viewer หรือ gerbv — ตรวจไฟล์ผลิตซ้ำอีกชั้น

## Agent-side

- Custom skill ใน `skills/marine-tracker-hardware/SKILL.md`
- MCP server `marine-tracker-guard`
- Codex: ใช้ `AGENTS.md`; สามารถติดตั้ง skill ตาม Open Agent Skills mechanism
- Claude Code: ใช้ `CLAUDE.md`; คัดลอก skill ไป `.claude/skills/marine-tracker-hardware/`
- Gemini CLI: ใช้ `GEMINI.md`; ให้ MCP เป็น tool หลักและจำกัด shell

## Recommended engineering tools

- Saturn PCB Toolkit หรือ field solver จากผู้ผลิต PCB สำหรับ preliminary impedance
- เครื่อง VNA สำหรับตรวจ antenna/feed หลังประกอบ
- Electronic load/oscilloscope/current profiler สำหรับ LTE burst และ sleep current
- Temperature chamber หรืออย่างน้อย controlled heat soak
- Salt-fog/condensation test setup สำหรับ validation หลัง Rev A
