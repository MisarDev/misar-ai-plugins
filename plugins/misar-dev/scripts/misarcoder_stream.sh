#!/usr/bin/env bash
# misarcoder_stream.sh — stream MisarCoder MoE response directly into Claude's context
# Usage: misarcoder_stream.sh <task_type> "<system>" "<prompt>" [max_tokens]
# task_type: code | reason | general | qa
#
# Phase 2: uses WebSocket (/ws/chat/v2) when websocat is available — persistent TCP,
# no per-request HTTP overhead. Falls back to SSE (/v1/chat/completions) when websocat absent.

TASK_TYPE="${1:-code}"
SYSTEM="${2:-You are an expert software engineer. Be concise and precise.}"
PROMPT="${3}"
MAX_TOKENS="${4:-8192}"

if [[ -z "$PROMPT" ]]; then
  echo "[MisarCoder] ERROR: prompt required as \$3" >&2
  exit 1
fi

# ── API key: tmpfile cache (~5 ms) → keychain → config.env fallback ──
KEY_CACHE="/tmp/.misarcoder_key"
WARM_FLAG="/tmp/.misarcoder_warm"

if [[ -f "$KEY_CACHE" ]] && \
   [[ $(( $(date +%s) - $(stat -f%m "$KEY_CACHE" 2>/dev/null || echo 0) )) -lt 3600 ]]; then
  MISARCODER_KEY=$(cat "$KEY_CACHE" 2>/dev/null)
fi
if [[ -z "$MISARCODER_KEY" ]]; then
  RAW=$(security find-generic-password -a "$USER" -s com.misar.misarcoder-api-key -w 2>/dev/null)
  if [[ -z "$RAW" ]]; then
    CONFIG_ENV="/Users/researchfellow/Desktop/G1 Technologies/Misar AI/MisarAICloud/MisarCoder/.env/config.env"
    [[ -f "$CONFIG_ENV" ]] && RAW=$(grep '^API_KEY=' "$CONFIG_ENV" | cut -d= -f2- | tr -d '[:space:]')
  fi
  if [[ -n "$RAW" ]]; then
    printf '%s' "$RAW" > "$KEY_CACHE"  # printf avoids trailing newline that breaks /warmup auth
    chmod 600 "$KEY_CACHE"
    MISARCODER_KEY="$RAW"
  fi
fi
if [[ -z "$MISARCODER_KEY" ]]; then
  echo "[MisarCoder unavailable: API key not found]" >&2
  exit 1
fi

# ── Model selection: groq for all non-code tasks (faster, free) ──
case "$TASK_TYPE" in
  reason)   MODEL="groq/llama-3.3-70b-versatile" ;;
  qa)       MODEL="groq/llama-3.3-70b-versatile" ;;
  general)  MODEL="groq/llama-3.3-70b-versatile" ;;
  code)     MODEL="gemini-2.5-flash" ;;
  *)        MODEL="gemini-2.5-flash" ;;
esac

# ── Health check: skip when recently warmed (saves 30 ms + round-trip) ──
WARM_AGE=$(( $(date +%s) - $(cat "$WARM_FLAG" 2>/dev/null || echo 0) ))
if [[ "$WARM_AGE" -gt 300 ]]; then
  if ! curl -s --max-time 2 "http://localhost:8000/health" > /dev/null 2>&1; then
    echo "[MisarCoder unavailable: not running on localhost:8000]" >&2
    exit 1
  fi
  date +%s > "$WARM_FLAG"
fi

# ── Build JSON payload: jq (<5 ms) with python3 fallback ──
if command -v jq > /dev/null 2>&1; then
  PAYLOAD=$(jq -nc \
    --arg model "$MODEL" \
    --arg system "$SYSTEM" \
    --arg prompt "$PROMPT" \
    --argjson max_tokens "$MAX_TOKENS" \
    '{model:$model,max_tokens:$max_tokens,stream:true,
      messages:[{role:"system",content:$system},{role:"user",content:$prompt}]}')
else
  PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
    'model': sys.argv[1],
    'max_tokens': int(sys.argv[2]),
    'stream': True,
    'messages': [
        {'role': 'system', 'content': sys.argv[3]},
        {'role': 'user',   'content': sys.argv[4]},
    ]
}))
" "$MODEL" "$MAX_TOKENS" "$SYSTEM" "$PROMPT" 2>/dev/null)
fi

if [[ -z "$PAYLOAD" ]]; then
  echo "[MisarCoder unavailable: failed to build payload]" >&2
  exit 1
fi

# ── Phase 2: WebSocket path (websocat) — lower per-request overhead ──
# WS format: {"type":"conversation.start","messages":[...],"model":"...","max_tokens":N}
# Events: task_classification|swe_phase|rag_context → skip
#         content_block_delta → {"delta":{"type":"text_delta","text":"..."}}
#         message_stop → end
#         error → report + exit 1
if command -v websocat > /dev/null 2>&1; then
  # Build WS-format payload (conversation.start, not stream:true)
  if command -v jq > /dev/null 2>&1; then
    WS_PAYLOAD=$(jq -nc \
      --arg model "$MODEL" \
      --arg system "$SYSTEM" \
      --arg prompt "$PROMPT" \
      --argjson max_tokens "$MAX_TOKENS" \
      '{"type":"conversation.start","model":$model,"max_tokens":$max_tokens,
        "messages":[{"role":"system","content":$system},{"role":"user","content":$prompt}]}')
  else
    WS_PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
    'type': 'conversation.start',
    'model': sys.argv[1],
    'max_tokens': int(sys.argv[2]),
    'messages': [
        {'role': 'system', 'content': sys.argv[3]},
        {'role': 'user',   'content': sys.argv[4]},
    ]
}))
" "$MODEL" "$MAX_TOKENS" "$SYSTEM" "$PROMPT" 2>/dev/null)
  fi

  WS_PARSER='
import sys, json
for raw in sys.stdin:
    line = raw.strip()
    if not line: continue
    try:
        ev = json.loads(line)
        t = ev.get("type", "")
        if t == "content_block_delta":
            text = ev.get("delta", {}).get("text", "")
            if text:
                print(text, end="", flush=True)
        elif t == "message_stop":
            break
        elif t == "error":
            msg = ev.get("error", {}).get("message", str(ev.get("error", ev)))
            print(f"\n[MisarCoder WS error: {msg}]", file=sys.stderr, flush=True)
            sys.exit(1)
        # skip: task_classification, swe_phase, rag_context, fault_localization,
        #        trace_id, message_start, content_block_start, content_block_stop
    except Exception:
        continue
try:
    print("", flush=True)
except BrokenPipeError:
    pass
'

  # Auth: WS endpoint requires Authorization header (query param rejected — nginx logs it)
  # FIFO feeder runs in background so it's NOT part of the foreground pipeline.
  # Foreground pipeline: websocat | python3 — completes as soon as python3 exits (message_stop).
  # python3 exits → SIGPIPE → websocat exits → pipeline done → kill feeder + close FIFO.
  # macOS-compatible (no GNU timeout, no --no-close which causes OS error 22 on ARM64).
  _ws_tmpfifo=$(mktemp -u /tmp/.wsFIFO_XXXXXX)
  mkfifo "$_ws_tmpfifo"
  (echo "$WS_PAYLOAD"; sleep 8) > "$_ws_tmpfifo" &
  _ws_feeder=$!

  websocat --text \
      -H="Authorization: Bearer ${MISARCODER_KEY}" \
      "ws://localhost:8000/ws/chat/v2" \
      2>/dev/null < "$_ws_tmpfifo" \
  | python3 -u -c "$WS_PARSER"

  WS_EXIT=$?
  kill -- "$_ws_feeder" 2>/dev/null
  rm -f "$_ws_tmpfifo"
  exit $WS_EXIT
fi

# ── Phase 1 fallback: HTTP SSE (/v1/chat/completions) ──
SSE_PARSER='
import sys, json
exit_code = 0
for raw_line in sys.stdin:
    line = raw_line.strip()
    if not line or not line.startswith("data:"):
        continue
    data = line[5:].strip()
    if data == "[DONE]":
        break
    try:
        obj = json.loads(data)
        if "error" in obj:
            msg = obj["error"].get("message", str(obj["error"]))
            print(f"\n[MisarCoder error: {msg}]", file=sys.stderr, flush=True)
            exit_code = 1
            break
        text = obj.get("choices", [{}])[0].get("delta", {}).get("content") or ""
        if text:
            print(text, end="", flush=True)
    except Exception:
        continue
try:
    print("", flush=True)
except BrokenPipeError:
    pass
sys.exit(exit_code)
'

curl --no-buffer -s \
  --max-time 8 \
  --connect-timeout 3 \
  -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer $MISARCODER_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  2>/dev/null \
| python3 -u -c "$SSE_PARSER"
