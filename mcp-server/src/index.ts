import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";

const root = path.resolve(process.env.PROJECT_DIR ?? "project");
const maxOutput = 200_000;

function insideRoot(candidate: string): string {
  const resolved = path.resolve(root, candidate);
  if (resolved !== root && !resolved.startsWith(root + path.sep)) {
    throw new Error("Path escapes PROJECT_DIR");
  }
  return resolved;
}

function allowedKiCadFile(file: string, extensions: string[]): string {
  const p = insideRoot(file);
  if (!extensions.some((ext) => p.endsWith(ext))) {
    throw new Error(`File extension is not allowed: ${file}`);
  }
  return p;
}

async function run(command: string, args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
  if (command !== "kicad-cli") throw new Error("Only kicad-cli is allowed");
  for (const arg of args) {
    const lower = arg.toLowerCase();
    if (lower.includes("python") || lower.includes(";") || lower.includes("&&") || lower.includes("|")) {
      throw new Error("Rejected unsafe argument");
    }
  }
  return await new Promise((resolve, reject) => {
    const child = spawn(command, args, { shell: false, cwd: root, env: { PATH: process.env.PATH ?? "" } });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => { if (stdout.length < maxOutput) stdout += d.toString(); });
    child.stderr.on("data", (d) => { if (stderr.length < maxOutput) stderr += d.toString(); });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code: code ?? -1, stdout, stderr }));
  });
}

const server = new McpServer({ name: "marine-tracker-guard", version: "0.1.0" });

server.tool("project_inventory", "List only approved project engineering files; read-only.", {}, async () => {
  const entries = await fs.readdir(root, { withFileTypes: true });
  const allowed = entries
    .filter((e) => e.isFile() && /\.(kicad_sch|kicad_pcb|kicad_pro|kicad_dru|kicad_mod|md|pdf|step|stp)$/i.test(e.name))
    .map((e) => e.name)
    .sort();
  return { content: [{ type: "text", text: JSON.stringify({ projectDir: root, files: allowed }, null, 2) }] };
});

server.tool("validate_schematic", "Run KiCad ERC. Never edits the schematic.", {
  schematic: z.string().describe("Path relative to PROJECT_DIR ending .kicad_sch"),
  report: z.string().default("reports/erc.json")
}, async ({ schematic, report }) => {
  const input = allowedKiCadFile(schematic, [".kicad_sch"]);
  const output = insideRoot(report);
  await fs.mkdir(path.dirname(output), { recursive: true });
  const result = await run("kicad-cli", ["sch", "erc", "--format", "json", "--output", output, input]);
  return { content: [{ type: "text", text: JSON.stringify({ ...result, report: output }, null, 2) }], isError: result.code !== 0 };
});

server.tool("validate_pcb", "Run KiCad DRC. Never edits the PCB.", {
  pcb: z.string().describe("Path relative to PROJECT_DIR ending .kicad_pcb"),
  report: z.string().default("reports/drc.json")
}, async ({ pcb, report }) => {
  const input = allowedKiCadFile(pcb, [".kicad_pcb"]);
  const output = insideRoot(report);
  await fs.mkdir(path.dirname(output), { recursive: true });
  const result = await run("kicad-cli", ["pcb", "drc", "--format", "json", "--output", output, input]);
  return { content: [{ type: "text", text: JSON.stringify({ ...result, report: output }, null, 2) }], isError: result.code !== 0 };
});

server.tool("render_pcb", "Export a read-only PCB SVG preview.", {
  pcb: z.string(),
  output: z.string().default("reports/pcb-preview.svg"),
  layers: z.string().default("F.Cu,F.Silkscreen,Edge.Cuts")
}, async ({ pcb, output, layers }) => {
  const input = allowedKiCadFile(pcb, [".kicad_pcb"]);
  const out = insideRoot(output);
  await fs.mkdir(path.dirname(out), { recursive: true });
  const result = await run("kicad-cli", ["pcb", "render", "--output", out, "--layers", layers, input]);
  return { content: [{ type: "text", text: JSON.stringify({ ...result, output: out }, null, 2) }], isError: result.code !== 0 };
});

server.tool("export_gerbers_candidate", "Export candidate Gerbers only after explicit environment opt-in. Does not claim production readiness.", {
  pcb: z.string(),
  outputDir: z.string().default("candidate-fabrication/gerbers")
}, async ({ pcb, outputDir }) => {
  if (process.env.ALLOW_FAB_EXPORT !== "YES") {
    throw new Error("Fabrication export locked. Set ALLOW_FAB_EXPORT=YES only after review approval.");
  }
  const input = allowedKiCadFile(pcb, [".kicad_pcb"]);
  const out = insideRoot(outputDir);
  await fs.mkdir(out, { recursive: true });
  const result = await run("kicad-cli", ["pcb", "gerbers", "--output", out + path.sep, input]);
  return { content: [{ type: "text", text: JSON.stringify({ ...result, status: "CANDIDATE_ONLY", outputDir: out }, null, 2) }], isError: result.code !== 0 };
});

server.tool("guardrail_check", "Check for forbidden generated scripts and direct KiCad text-rewrite artifacts.", {}, async () => {
  const findings: string[] = [];
  async function walk(dir: string): Promise<void> {
    for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
      if (["node_modules", ".git", "dist"].includes(entry.name)) continue;
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(p);
      else if (/\.(py|pyc|ipynb)$/i.test(entry.name)) findings.push(`Forbidden Python artifact: ${path.relative(root, p)}`);
      else if (/rewrite.*kicad|patch.*kicad/i.test(entry.name)) findings.push(`Suspicious KiCad rewrite artifact: ${path.relative(root, p)}`);
    }
  }
  await walk(root);
  return { content: [{ type: "text", text: JSON.stringify({ pass: findings.length === 0, findings }, null, 2) }], isError: findings.length > 0 };
});

await server.connect(new StdioServerTransport());
