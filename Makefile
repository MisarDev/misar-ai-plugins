.PHONY: setup update uninstall help

help:
	@echo "misar-ai-plugins — Claude Code plugin"
	@echo ""
	@echo "  make setup      Install and enable misar-dev plugin via Claude Code CLI"
	@echo "  make update     Update to the latest version"
	@echo "  make uninstall  Remove the plugin"

setup:
	@echo "Adding marketplace..."
	claude plugins marketplace add https://github.com/MisarDev/misar-ai-plugins.git || true
	@echo "Installing misar-dev plugin..."
	claude plugins install misar-dev
	@echo ""
	@echo "Done. Restart Claude Code, then run: /misar-dev:guidelines show"

update:
	claude plugins marketplace update misar-ai-plugins
	claude plugins update misar-dev

uninstall:
	claude plugins uninstall misar-dev
