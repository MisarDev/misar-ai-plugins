#!/usr/bin/env node
/**
 * Plugin integrity validator — run locally or in CI.
 * Checks: JSON validity, required fields, command↔agent cross-refs, frontmatter.
 */

import { readFileSync, existsSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dir = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dir, "..");
const PLUGIN_DIR = join(ROOT, "plugins/misar-dev");

let errors = 0;
let warnings = 0;

function err(msg) { console.error(`  ✗ ERROR: ${msg}`); errors++; }
function warn(msg) { console.warn(`  ⚠ WARN:  ${msg}`); warnings++; }
function ok(msg)   { console.log(`  ✓ ${msg}`); }

function readJSON(path) {
  if (!existsSync(path)) { err(`Missing file: ${path}`); return null; }
  try { return JSON.parse(readFileSync(path, "utf8")); }
  catch (e) { err(`Invalid JSON in ${path}: ${e.message}`); return null; }
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const fm = {};
  for (const line of match[1].split("\n")) {
    const idx = line.indexOf(":");
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    const val = line.slice(idx + 1).trim().replace(/^["']|["']$/g, "");
    fm[key] = val;
  }
  return fm;
}

// Strips traversal sequences from each segment before joining under ROOT.
function safeJoin(...relativeParts) {
  const clean = relativeParts.map(p =>
    String(p).replace(/\.\.[/\\]/g, "").replace(/^\.[/\\]/g, "").replace(/^[/\\]+/, "")
  );
  return join(ROOT, ...clean);
}

function subDirs(dirPath) {
  if (!existsSync(dirPath)) return [];
  return readdirSync(dirPath, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
}

// ── 1. Marketplace manifest ───────────────────────────────────────────────────
console.log("\n[1/5] Marketplace manifest");
const mkt = readJSON(join(ROOT, ".claude-plugin/marketplace.json"));
if (mkt) {
  for (const f of ["name", "description", "plugins"]) {
    if (!mkt[f]) err(`marketplace.json missing field: ${f}`);
  }
  if (Array.isArray(mkt.plugins)) {
    for (const p of mkt.plugins) {
      const src = join(ROOT, p.source);
      if (!existsSync(src)) err(`Plugin source path not found: ${p.source}`);
      else ok(`Plugin source exists: ${p.source}`);
    }
  }
  ok("marketplace.json valid");
}

// ── 2. Plugin manifest ────────────────────────────────────────────────────────
console.log("\n[2/5] Plugin manifest");
const plugin = readJSON(join(PLUGIN_DIR, ".claude-plugin/plugin.json"));
if (plugin) {
  for (const f of ["name", "version", "description"]) {
    if (!plugin[f]) err(`plugin.json missing field: ${f}`);
  }
  ok(`Plugin: ${plugin.name} v${plugin.version}`);
}

// ── 3. Command files ──────────────────────────────────────────────────────────
console.log("\n[3/5] Commands");
const COMMANDS_DIR = join(PLUGIN_DIR, "commands");
const commandFiles = existsSync(COMMANDS_DIR)
  ? readdirSync(COMMANDS_DIR).filter(f => f.endsWith(".md"))
  : [];

const commandNames = new Set();
for (const file of commandFiles) {
  const path = join(COMMANDS_DIR, file);
  const content = readFileSync(path, "utf8");
  const fm = parseFrontmatter(content);
  if (!fm) { err(`${file}: missing frontmatter`); continue; }
  if (!fm.description) err(`${file}: frontmatter missing 'description'`);
  if (!fm["argument-hint"]) warn(`${file}: frontmatter missing 'argument-hint'`);
  commandNames.add(file.replace(".md", ""));
  ok(`${file}`);
}
console.log(`  → ${commandFiles.length} commands found`);

// ── 4. Agent directories ──────────────────────────────────────────────────────
console.log("\n[4/5] Agents");
const AGENTS_DIR = join(PLUGIN_DIR, "agents");
const agentDirs = subDirs(AGENTS_DIR);
const agentNames = new Set(agentDirs);

for (const agent of agentDirs) {
  const agentMd = join(AGENTS_DIR, agent, "agent.md");
  if (!existsSync(agentMd)) {
    err(`agents/${agent}/agent.md is missing`);
    continue;
  }
  const content = readFileSync(agentMd, "utf8");
  const fm = parseFrontmatter(content);
  if (!fm) { err(`agents/${agent}/agent.md: missing frontmatter`); continue; }
  if (!fm.name) err(`agents/${agent}/agent.md: frontmatter missing 'name'`);
  if (!fm.description) err(`agents/${agent}/agent.md: frontmatter missing 'description'`);
  ok(`agents/${agent}`);
}
console.log(`  → ${agentDirs.length} agent categories found`);

// Cross-reference: commands that reference agents
for (const file of commandFiles) {
  const content = readFileSync(join(COMMANDS_DIR, file), "utf8");
  const refs = [...content.matchAll(/\*\*([\w-]+-agents|[\w-]+)\*\*/g)]
    .map(m => m[1])
    .filter(n => n.endsWith("-agents") || n === "context-saver" || n === "task-fragmenter");
  for (const ref of refs) {
    if (!agentNames.has(ref)) {
      err(`${file} references agent '${ref}' which does not exist in agents/`);
    }
  }
}

// ── 5. Skill directories ──────────────────────────────────────────────────────
console.log("\n[5/5] Skills");
const SKILLS_DIR = join(PLUGIN_DIR, "skills");
const ROOT_SKILLS_DIR = join(ROOT, "skills");

const pluginSkills = subDirs(SKILLS_DIR);
const rootSkills = subDirs(ROOT_SKILLS_DIR);

for (const skill of pluginSkills) {
  const md = join(SKILLS_DIR, skill, "SKILL.md");
  if (!existsSync(md)) { err(`skills/${skill}/SKILL.md is missing`); continue; }
  ok(`skills/${skill}`);
}

// Every plugin skill must also exist at root (for npx skills compatibility)
for (const skill of pluginSkills) {
  if (!rootSkills.includes(skill)) {
    warn(`skills/${skill} exists in plugin but missing from root skills/ (npx skills compat)`);
  }
}
for (const skill of rootSkills) {
  if (!pluginSkills.includes(skill)) {
    warn(`root skills/${skill} exists but missing from plugins/misar-dev/skills/ (sync drift)`);
  }
}
console.log(`  → ${pluginSkills.length} plugin skills, ${rootSkills.length} root skills`);

// ── Summary ───────────────────────────────────────────────────────────────────
console.log(`\n${"─".repeat(52)}`);
if (errors === 0 && warnings === 0) {
  console.log("✅ All checks passed");
} else {
  if (errors > 0) console.error(`❌ ${errors} error(s), ${warnings} warning(s)`);
  else console.warn(`⚠  0 errors, ${warnings} warning(s)`);
}
process.exit(errors > 0 ? 1 : 0);
