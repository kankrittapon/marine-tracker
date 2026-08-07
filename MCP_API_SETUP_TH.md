# การเชื่อมต่อ KiCAD-MCP API

## โครงสร้างที่ใช้ในโปรเจกต์นี้

```text
Codex ──SSH/stdio──> ai-brain:/opt/kicad-mcp
                            │ authenticated Tailnet relay
                            ▼
Windows worker 100.120.111.57:8765 ──> KiCad Python 10 ──> ไฟล์โปรเจกต์
```

MCP ใช้ JSON-RPC ผ่าน stdio ไม่ใช่ REST API สาธารณะ ตัว `ai-brain` เป็น MCP
frontend ส่วนคำสั่งที่ต้องใช้ `pcbnew` และไฟล์ Windows จะส่งไป worker ผ่าน Tailscale

## ไฟล์ที่เกี่ยวข้อง

- MCP server บน Windows: `tools/KiCAD-MCP-Server`
- Worker: `infrastructure/kicad-worker/windows_worker.py`
- Remote shim: `infrastructure/kicad-worker/remote_client.py`
- Remote launcher: `infrastructure/kicad-worker/start_remote.sh`
- Token ฝั่ง Windows: `infrastructure/kicad-worker/worker.token` (ห้าม commit)
- Token ฝั่ง ai-brain: `/etc/kicad-mcp/worker.token` permission `0600`
- MCP server ฝั่ง ai-brain: `/opt/kicad-mcp`

## Codex config

ไฟล์ `%USERPROFILE%\.codex\config.toml`:

```toml
[mcp_servers.kicad]
command = 'C:\Windows\System32\OpenSSH\ssh.exe'
args = ['-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10',
        'root@100.68.88.63', '/usr/local/bin/kicad-mcp-remote']
startup_timeout_sec = 180
```

หลังแก้ config ต้องเปิด Codex ใหม่ จากนั้นทดสอบด้วยคำสั่ง:

```text
ใช้ KiCAD-MCP เรียก get_backend_state แล้วรายงาน backend และไฟล์ที่เปิดอยู่
```

## เริ่ม Windows worker

มี Scheduled Task ชื่อ `KiCAD-MCP-Tailnet-Worker` เริ่มตอน login หรือสั่งเอง:

```powershell
Start-Process -WindowStyle Hidden `
  'C:\Program Files\KiCad\10.0\bin\python.exe' `
  'C:\Users\zexqm\programing\track\infrastructure\kicad-worker\windows_worker.py'
```

ตรวจ listener:

```powershell
Get-NetTCPConnection -LocalAddress 100.120.111.57 -LocalPort 8765 -State Listen
```

ตรวจจาก ai-brain:

```bash
ssh root@100.68.88.63
test -x /usr/local/bin/kicad-mcp-remote
test -r /etc/kicad-mcp/worker.token
```

## Local fallback

หาก remote transport timeout ให้หยุด worker เพื่อป้องกันผู้เขียนไฟล์ซ้อน แล้วเรียก
backend บน Windows โดยตรง:

```powershell
'{"command":"get_backend_state","params":{}}' |
  & 'C:\Program Files\KiCad\10.0\bin\python.exe' `
    'C:\Users\zexqm\programing\track\tools\KiCAD-MCP-Server\python\kicad_interface.py'
```

ห้ามให้ remote worker และ local fallback เขียน `.kicad_sch`/`.kicad_pcb` เดียวกัน
พร้อมกัน ต้องสร้าง snapshot ก่อน batch และตรวจว่าไฟล์มีขนาดไม่เป็นศูนย์หลังคำสั่ง

## ความปลอดภัย

- listener bind เฉพาะ Tailscale IPv4 ไม่ bind `0.0.0.0`
- ห้ามนำพอร์ต 8765 ไปเปิดผ่าน Funnel หรือ port-forward
- token ต้อง permission จำกัดและอยู่ใน `.gitignore`
- rotate token เมื่อสงสัยว่ารั่ว แล้ว restart worker/MCP session
- จำกัด Tailnet ACL ให้เฉพาะ `ai-brain` เข้าถึง worker port
- ไม่ใช้ root SSH ใน production ระยะยาว ควรสร้าง user `kicad-mcp` ที่ไม่มี shell อื่น

## อาการขัดข้อง

| อาการ | ตรวจสอบ |
|---|---|
| `Command timeout after 30s` | worker, orphan Python, stream relay และ symbol warm-up |
| `Connection refused` | KiCad IPC เปิดหรือไม่; SWIG fallback ยังใช้แก้ไฟล์ได้ |
| ไฟล์เป็น 0 byte | หยุด writer ทุกตัวและกู้ snapshot ล่าสุด ห้ามส่ง batch ซ้ำทันที |
| MCP transport closed | เปิด Codex ใหม่หลังตรวจ ai-brain launcher และ worker |
| มี Python หลายตัวใช้ CPU สูง | ปิด orphan เหลือ worker กับ backend session เดียว |

