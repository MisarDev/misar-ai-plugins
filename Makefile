.PHONY: setup update uninstall help

help:
	@echo "misar-ai-plugins v7.8.0 — Universal AI Plugin Suite"
	@echo ""
	@echo "  make setup      Universal install (MCPs + plugin + adapters + memory)"
	@echo "  make update     Update to the latest version"
	@echo "  make uninstall  Remove the plugin"
	@echo ""
	@echo "  Supports: Claude Code, Codex, Gemini CLI, Cursor, Windsurf, Cline, Continue"

setup:
	@bash scripts/install.sh

update:
	claude plugins marketplace update misar-ai-plugins
	claude plugins update misar-dev@misar-ai-plugins

uninstall:
	claude plugins uninstall misar-dev
