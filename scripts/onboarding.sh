#!/usr/bin/env bash
# scripts/onboarding.sh — Install misar-dev plugin for Claude Code
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { printf "${GREEN}[✔] %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}[!] %s${NC}\n" "$*"; }

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║   Misar.Dev — Claude Code Plugin Setup   ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check for claude CLI
if ! command -v claude &>/dev/null; then
  warn "Claude Code CLI not found. Install it from https://claude.ai/claude-code"
  echo ""
  echo "Manual install options:"
  echo "  • Desktop App / VS Code: Settings → Plugins → Add Marketplace"
  echo "    URL: https://github.com/MisarDev/misar-ai-plugins.git"
  echo ""
  echo "  • claude.ai Web (Skills): Settings → Skills → Add Skill → Import from URL"
  echo "    https://raw.githubusercontent.com/MisarDev/misar-ai-plugins/main/skills/security/SKILL.md"
  exit 0
fi

# Choose setup method
echo "Select setup method:"
echo "  1) make setup   (recommended)"
echo "  2) pnpm setup   (alternative)"
echo "  3) Direct CLI   (no build tool needed)"
read -rp "Enter 1, 2, or 3 [3]: " CHOICE
CHOICE="${CHOICE:-3}"

case "$CHOICE" in
  1)
    if ! command -v make &>/dev/null; then
      warn "make not found — falling back to direct CLI"
      CHOICE=3
    else
      log "Running make setup..."
      make setup
    fi
    ;;
  2)
    if ! command -v pnpm &>/dev/null; then
      warn "pnpm not found — falling back to direct CLI"
      CHOICE=3
    else
      log "Running pnpm setup..."
      pnpm setup
    fi
    ;;
esac

if [[ "$CHOICE" == "3" ]]; then
  log "Adding marketplace..."
  claude plugins marketplace add https://github.com/MisarDev/misar-ai-plugins.git 2>/dev/null || true
  log "Installing misar-dev..."
  claude plugins install misar-dev
fi

echo ""
log "Plugin installed!"
echo ""
echo "═══════════════════════════════════════════════════"
echo " Next steps"
echo "═══════════════════════════════════════════════════"
echo ""
echo " Restart Claude Code, then try:"
echo "   /misar-dev:guidelines show"
echo "   /misar-dev:security"
echo "   /misar-dev:full-suite"
echo ""
echo " Auto-enable for your whole team — add to .claude/settings.json:"
echo '   { "enabledPlugins": { "misar-dev@misar-ai-plugins": true } }'
echo ""
echo " claude.ai Web (Skills) — import any skill via URL:"
echo "   https://raw.githubusercontent.com/MisarDev/misar-ai-plugins/main/skills/security/SKILL.md"
echo ""
echo " Cursor / Cline / Windsurf:"
echo "   npx skills add MisarDev/misar-ai-plugins"
echo ""
echo "═══════════════════════════════════════════════════"
