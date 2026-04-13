#!/usr/bin/env bash
#
# Context Saver — Install Script
# Copies router scripts to ~/.claude/router/ and sets up hooks
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUTER_DIR="${HOME}/.claude/router"
HOOKS_DIR="${HOME}/.claude/hooks"

echo "=== Context Saver — Installation ==="
echo ""

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is required but not installed" >&2
    echo "Install Python 3: https://python.org/downloads" >&2
    exit 1
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    echo "WARNING: PyYAML not installed. Installing..."
    if command -v pip3 &> /dev/null; then
        pip3 install pyyaml --quiet || {
            echo "ERROR: Failed to install pyyaml. Run: pip3 install pyyaml" >&2
            exit 1
        }
        echo "  PyYAML installed successfully."
    else
        echo "ERROR: pip3 not found. Run: pip3 install pyyaml" >&2
        exit 1
    fi
fi

# Create directories
mkdir -p "$ROUTER_DIR" "$HOOKS_DIR"

# Copy scripts
echo "[1/4] Copying router scripts to ${ROUTER_DIR}..."
cp "$SCRIPT_DIR/router.py" "$ROUTER_DIR/router.py"
cp "$SCRIPT_DIR/config.yaml" "$ROUTER_DIR/config.yaml"
cp "$SCRIPT_DIR/monitor.py" "$ROUTER_DIR/monitor.py"
cp "$SCRIPT_DIR/switch-model.sh" "$ROUTER_DIR/switch-model.sh"

# Make executable
echo "[2/4] Setting permissions..."
chmod +x "$ROUTER_DIR/router.py"
chmod +x "$ROUTER_DIR/monitor.py"
chmod +x "$ROUTER_DIR/switch-model.sh"

# Create pre-prompt hook
echo "[3/4] Creating pre-prompt hook..."
cat > "$HOOKS_DIR/pre-prompt-hook.sh" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail

ROUTER="${HOME}/.claude/router/router.py"
LOG_FILE="${HOME}/.claude/router/router.log"

if [[ ! -f "${ROUTER}" ]]; then
    exit 0
fi

PROMPT="${1:-}"
if [[ -z "${PROMPT}" ]] && [[ -p /dev/stdin ]]; then
    PROMPT=$(cat)
fi

if [[ "${PROMPT}" =~ ^/ ]]; then
    exit 0
fi

if [[ -n "${PROMPT}" ]]; then
    python3 "${ROUTER}" "${PROMPT}" >> "${LOG_FILE}" 2>&1 || true
fi

exit 0
HOOK
chmod +x "$HOOKS_DIR/pre-prompt-hook.sh"

# Create post-prompt hook
cat > "$HOOKS_DIR/post-prompt-hook.sh" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail

STATE_FILE="${HOME}/.claude/router/state.json"

if [[ -f "${STATE_FILE}" ]]; then
    python3 -c "
import json
from datetime import datetime
from pathlib import Path

state_file = Path('${STATE_FILE}')
if state_file.exists():
    with open(state_file) as f:
        state = json.load(f)
    state['last_activity'] = datetime.now().isoformat()
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
" 2>/dev/null || true
fi

exit 0
HOOK
chmod +x "$HOOKS_DIR/post-prompt-hook.sh"

# Verify
echo "[4/4] Verifying installation..."
if [[ -f "$ROUTER_DIR/router.py" ]] && [[ -f "$ROUTER_DIR/config.yaml" ]] && [[ -f "$HOOKS_DIR/pre-prompt-hook.sh" ]]; then
    echo ""
    echo "=== Installation Complete ==="
    echo "  Router:    ${ROUTER_DIR}/router.py"
    echo "  Config:    ${ROUTER_DIR}/config.yaml"
    echo "  Monitor:   ${ROUTER_DIR}/monitor.py"
    echo "  Switcher:  ${ROUTER_DIR}/switch-model.sh"
    echo "  Pre-hook:  ${HOOKS_DIR}/pre-prompt-hook.sh"
    echo "  Post-hook: ${HOOKS_DIR}/post-prompt-hook.sh"
    echo ""
    echo "Context Saver is now active on every prompt."
    echo "Edit ${ROUTER_DIR}/config.yaml to customize routing rules."
else
    echo "ERROR: Installation verification failed" >&2
    exit 1
fi
