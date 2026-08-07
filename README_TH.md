# Marine Tracker — AI Agent Handoff Pack

แพ็กนี้ใช้ย้ายบริบทโครงการจากแชทไปยัง Codex, Claude Code หรือ Gemini CLI โดยไม่ต้องป้อนประวัติทั้งหมดซ้ำ

## เริ่มใช้งาน

1. แตก ZIP แล้ววางไฟล์ทั้งหมดไว้ที่ราก repository ของโครงการ KiCad
2. วางไฟล์ KiCad ล่าสุดในโฟลเดอร์ `project/` หรือเปลี่ยนค่า `PROJECT_DIR` ของ MCP
3. อ่าน `docs/PROJECT_BRIEF.md`, `docs/FEATURES.md` และ `docs/ACCEPTANCE_CRITERIA.md`
4. ติดตั้ง KiCad ที่มี `kicad-cli` และ Node.js 20+
5. ติดตั้ง MCP server:

```bash
cd mcp-server
npm install
npm run build
```

6. ตั้งค่า client ตาม `docs/CLIENT_SETUP_TH.md`

## ไฟล์คำสั่งสำหรับ Agent

- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- Gemini CLI: `GEMINI.md`
- กฎกลาง: `docs/PROJECT_RULES.md`

## ข้อจำกัดสำคัญ

MCP server นี้ไม่เปิด arbitrary shell และไม่เปิด Python tool ใด ๆ โดยตั้งใจ แต่กฎใน MCP เพียงอย่างเดียวไม่สามารถปิด shell/Python ที่มากับ AI client ได้ ต้องตั้ง permission ของ Codex/Claude/Gemini เพิ่มตามคู่มือ Client Setup
