# ตั้งค่า Codex / Claude Code / Gemini CLI

สมมติคำว่า “gay” ในคำขอเดิมหมายถึง Gemini CLI

## Codex

Codex อ่าน `AGENTS.md` อัตโนมัติเมื่ออยู่ใน repository. ตั้ง sandbox เป็น workspace-write และ approval เป็น on-request. การปิด Python แบบเด็ดขาดต้องใช้ permission profile/OS policy เพิ่ม เพราะ AGENTS.md เป็นคำสั่ง ไม่ใช่ security boundary

ตัวอย่าง `.codex/config.toml`:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[mcp_servers.marine-tracker-guard]
command = "node"
args = ["mcp-server/dist/index.js"]
env = { PROJECT_DIR = "project" }
```

## Claude Code

Claude Code อ่าน `CLAUDE.md`. เพิ่ม MCP ด้วยคำสั่งหรือ settings ของ Claude Code แล้วตั้ง permission deny สำหรับ Bash patterns ที่เป็น Python และ deny การแก้ KiCad ผ่าน shell. ตัวอย่าง policy อยู่ใน `.claude/settings.example.json`

## Gemini CLI

Gemini CLI อ่าน `GEMINI.md`. เพิ่ม MCP ใน `.gemini/settings.json`; ตัวอย่างอยู่ใน `.gemini/settings.example.json`. ควรปิด/จำกัด shell tool ใน workspace นี้ เพราะ MCP ไม่สามารถปิด built-in shell ของ client ได้

## วิธีนำ “แชท” เข้าไป

ไม่ควรย้าย transcript ทั้งหมดเป็น context ทุกครั้ง เพราะยาวและมีคำตอบเก่าบางส่วนที่ยังไม่ผ่านการตรวจ. ใช้ `docs/PROJECT_BRIEF.md` + `STATUS.md` + `FEATURES.md` เป็น handoff ที่ควบคุมเวอร์ชันได้ และเก็บ transcript เดิมเป็น reference เท่านั้น
