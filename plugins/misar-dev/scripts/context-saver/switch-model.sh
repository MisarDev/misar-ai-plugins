#!/usr/bin/env bash
#
# 3D Switch Helper — Context Saver v7.0.0
# Updates settings.json with model AND effort level
#

set -euo pipefail

MODEL="${1:-sonnet}"
EFFORT="${2:-medium}"
SETTINGS_FILE="${HOME}/.claude/settings.json"

# Validate model
if [[ ! "$MODEL" =~ ^(haiku|sonnet|opus)$ ]]; then
    echo "Error: Invalid model. Use haiku, sonnet, or opus" >&2
    exit 1
fi

# Validate effort
if [[ ! "$EFFORT" =~ ^(low|medium|high|max)$ ]]; then
    echo "Error: Invalid effort. Use low, medium, high, or max" >&2
    exit 1
fi

# Check settings file
if [[ ! -f "$SETTINGS_FILE" ]]; then
    echo "Error: Settings file not found at $SETTINGS_FILE" >&2
    exit 1
fi

# Backup
cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"

# Update model + effort — prefer jq, fall back to Python
if command -v jq &> /dev/null; then
    jq --arg model "$MODEL" --arg effort "$EFFORT" \
        '.model = $model | .effortLevel = $effort' \
        "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"
    mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
elif command -v python3 &> /dev/null; then
    python3 - <<PYEOF
import json
with open('$SETTINGS_FILE') as f:
    s = json.load(f)
s['model'] = '$MODEL'
s['effortLevel'] = '$EFFORT'
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(s, f, indent=2)
PYEOF
else
    # Last resort: sed — handle GNU (Linux) and BSD (macOS) variants
    if sed --version 2>/dev/null | grep -q GNU; then
        sed -i "s/\"model\": \".*\"/\"model\": \"$MODEL\"/" "$SETTINGS_FILE"
        sed -i "s/\"effortLevel\": \".*\"/\"effortLevel\": \"$EFFORT\"/" "$SETTINGS_FILE"
    else
        sed -i '' "s/\"model\": \".*\"/\"model\": \"$MODEL\"/" "$SETTINGS_FILE"
        sed -i '' "s/\"effortLevel\": \".*\"/\"effortLevel\": \"$EFFORT\"/" "$SETTINGS_FILE"
    fi
fi

# Resolve version for logging
case "$MODEL" in
    haiku)  VERSION="4.5" ;;
    *)      VERSION="4.6" ;;
esac

# Log silently
echo "[$(date +'%Y-%m-%dT%H:%M:%S')] Switched: ${MODEL}+${EFFORT}+${VERSION}" >> "$HOME/.claude/router/router.log" 2>/dev/null || true
