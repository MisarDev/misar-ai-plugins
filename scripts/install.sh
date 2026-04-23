#!/usr/bin/env bash
# scripts/install.sh — Universal installer for misar-ai-plugins
# Works on: Claude Code, Codex, Cline, Cursor, Windsurf, Continue, Gemini CLI
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { printf "${GREEN}[✔]${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}[!]${NC} %s\n" "$*"; }
info() { printf "${CYAN}[→]${NC} %s\n" "$*"; }
fail() { printf "${RED}[✘]${NC} %s\n" "$*"; }

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     Misar.Dev Plugin Suite — Universal Setup    ║"
echo "║     Skills · Agents · MCPs · Hooks · Memory     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── 1. Detect platform ──────────────────────────────────────────────────────
PLATFORM="unknown"
HAS_CLAUDE=false; HAS_CODEX=false; HAS_GEMINI=false

command -v claude  &>/dev/null && HAS_CLAUDE=true  && PLATFORM="claude-code"
command -v codex   &>/dev/null && HAS_CODEX=true   && PLATFORM="${PLATFORM}+codex"
command -v gemini  &>/dev/null && HAS_GEMINI=true  && PLATFORM="${PLATFORM}+gemini"

info "Detected platform: ${PLATFORM:-none (manual MCP setup will run)}"
echo ""

# ── 2. Install MCP scripts ──────────────────────────────────────────────────
info "Installing MCP server scripts..."
MCP_DEST="${HOME}/.claude/scripts"
mkdir -p "$MCP_DEST"

for script in misarcoder-mcp.py guardian-mcp.py guardrails-mcp.py; do
  src="$REPO_DIR/mcp/$script"
  dst="$MCP_DEST/$script"
  if [[ -f "$src" ]]; then
    cp "$src" "$dst"
    chmod +x "$dst"
    log "  $script → $MCP_DEST"
  else
    warn "  $script not found in repo/mcp/ — skipping"
  fi
done
echo ""

# ── 3. Claude Code setup ─────────────────────────────────────────────────────
if $HAS_CLAUDE; then
  info "Setting up Claude Code plugin..."
  claude plugins marketplace add https://github.com/MisarDev/misar-ai-plugins.git 2>/dev/null || true
  claude plugins install misar-dev 2>/dev/null || claude plugins update misar-dev@misar-ai-plugins 2>/dev/null || true
  log "Claude Code: misar-dev plugin installed"
  echo ""
fi

# ── 4. Wire MCPs into settings.json (Claude Code) ───────────────────────────
if $HAS_CLAUDE; then
  info "Wiring MCPs into Claude Code settings..."
  SETTINGS="${HOME}/.claude/settings.json"

  # Ensure settings.json exists
  [[ -f "$SETTINGS" ]] || echo '{}' > "$SETTINGS"

  # Use python3 to merge MCP servers without clobbering existing settings
  python3 - "$SETTINGS" "$REPO_DIR/adapters/mcp.json" <<'PYEOF'
import json, sys, os

settings_path = sys.argv[1]
mcp_path = sys.argv[2]

with open(settings_path) as f:
    settings = json.load(f)

with open(mcp_path) as f:
    new_mcps = json.load(f).get("mcpServers", {})

# Expand ${HOME} in args
home = os.path.expanduser("~")
for name, cfg in new_mcps.items():
    cfg["args"] = [a.replace("${HOME}", home) for a in cfg.get("args", [])]

existing = settings.get("mcpServers", {})
existing.update(new_mcps)
settings["mcpServers"] = existing

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"  Merged {len(new_mcps)} MCP servers into {settings_path}")
PYEOF
  log "MCPs wired: misarcoder, guardrails, guardian"
  echo ""
fi

# ── 5. Codex (AGENTS.md) ────────────────────────────────────────────────────
if $HAS_CODEX || [[ -f "${HOME}/.codex/config.toml" ]] || [[ -d "${HOME}/.codex" ]]; then
  info "Setting up Codex (AGENTS.md)..."
  AGENTS_DIR="${HOME}/.codex"
  mkdir -p "$AGENTS_DIR"
  cp "$REPO_DIR/adapters/AGENTS.md" "$AGENTS_DIR/AGENTS.md"
  # Merge MCP config into codex settings
  if [[ -f "$REPO_DIR/adapters/mcp.json" ]]; then
    cp "$REPO_DIR/adapters/mcp.json" "$AGENTS_DIR/mcp.json"
  fi
  log "Codex: AGENTS.md + mcp.json installed"
  echo ""
fi

# ── 6. Gemini CLI ────────────────────────────────────────────────────────────
if $HAS_GEMINI || [[ -d "${HOME}/.gemini" ]]; then
  info "Setting up Gemini CLI (GEMINI.md)..."
  GEMINI_DIR="${HOME}/.gemini"
  mkdir -p "$GEMINI_DIR"
  cp "$REPO_DIR/adapters/GEMINI.md" "$GEMINI_DIR/GEMINI.md"
  log "Gemini CLI: GEMINI.md installed"
  echo ""
fi

# ── 7. VS Code extensions (Cline, Continue) ──────────────────────────────────
VSCODE_SETTINGS="${HOME}/Library/Application Support/Code/User/settings.json"
if [[ -f "$VSCODE_SETTINGS" ]]; then
  info "VS Code settings.json found — checking for Cline/Continue MCP config..."
  warn "  Manual step: add MCP servers from adapters/mcp.json to your Cline/Continue extension settings"
  warn "  Or run: cat adapters/mcp.json"
  echo ""
fi

# ── 8. Project-level adapter files ──────────────────────────────────────────
# Offer to install project-level adapter files (cursorrules, windsurfrules, etc.)
# in the current working directory if it looks like a project
CWD_IS_PROJ=false
[[ -f "$(pwd)/package.json" ]] || [[ -f "$(pwd)/pyproject.toml" ]] || [[ -f "$(pwd)/.git/config" ]] && CWD_IS_PROJ=true

if $CWD_IS_PROJ; then
  info "Project detected at $(pwd)"
  echo "  Install project-level adapter files? (.cursorrules, .windsurfrules, AGENTS.md, GEMINI.md)"
  read -rp "  [y/N]: " INSTALL_PROJECT
  if [[ "${INSTALL_PROJECT:-n}" =~ ^[Yy]$ ]]; then
    cp "$REPO_DIR/adapters/.cursorrules"   "$(pwd)/.cursorrules"   2>/dev/null && log "  .cursorrules installed" || true
    cp "$REPO_DIR/adapters/.windsurfrules" "$(pwd)/.windsurfrules" 2>/dev/null && log "  .windsurfrules installed" || true
    cp "$REPO_DIR/adapters/AGENTS.md"      "$(pwd)/AGENTS.md"      2>/dev/null && log "  AGENTS.md installed" || true
    cp "$REPO_DIR/adapters/GEMINI.md"      "$(pwd)/GEMINI.md"      2>/dev/null && log "  GEMINI.md installed" || true
    echo ""
  fi
fi

# ── 9. Bootstrap memory (Claude Code) ───────────────────────────────────────
if $HAS_CLAUDE; then
  info "Bootstrapping memory index..."
  MEMORY_DIR="${HOME}/.claude/memory"
  mkdir -p "$MEMORY_DIR"
  if [[ ! -f "$MEMORY_DIR/MEMORY.md" ]]; then
    cp "$REPO_DIR/memory/MEMORY.md" "$MEMORY_DIR/MEMORY.md"
    log "Memory index bootstrapped at $MEMORY_DIR/MEMORY.md"
  else
    log "Memory index already exists — skipping"
  fi
  echo ""
fi

# ── 10. Summary ─────────────────────────────────────────────────────────────
echo "╔══════════════════════════════════════════════════╗"
echo "║                   Setup Complete                 ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  MCP scripts   → $MCP_DEST"
echo "  Adapters      → $REPO_DIR/adapters/"
echo ""
echo "  Restart Claude Code (or your agent), then:"
echo "    /misar-dev:security"
echo "    /misar-dev:full-suite"
echo "    /misar-dev:guidelines show"
echo ""
echo "  claude mcp list   # verify misarcoder, guardrails, guardian"
echo ""
