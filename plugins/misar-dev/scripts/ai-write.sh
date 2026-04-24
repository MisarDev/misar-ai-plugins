#!/usr/bin/env bash
# ai-write.sh — long-form writing via assisters-chat-v1 REST API (WritingSkill adaptor)
# Source of system prompt: assisters/packages/research-agent/src/skills/index.ts → WritingSkill
# Calls: https://assisters.dev/api/v1/chat/completions  (no Node package)
# Usage: ai-write.sh "<prompt>" [max_tokens]

PROMPT="${1}"; MAX_TOKENS="${2:-4096}"
[[ -z "$PROMPT" ]] && { echo "[ai-write] ERROR: prompt required" >&2; exit 1; }

# Resolve ASSISTERS_API_KEY from env → .env.local fallbacks
AKEY="${ASSISTERS_API_KEY:-}"
if [[ -z "$AKEY" ]]; then
  for f in \
    "$HOME/Desktop/G1 Technologies/Misar AI/MisarSocial/.env.local" \
    "$HOME/Desktop/G1 Technologies/Misar AI/assisters/apps/web/.env.local"; do
    [[ -f "$f" ]] && AKEY=$(grep '^ASSISTERS_API_KEY=' "$f" | cut -d= -f2- | tr -d '[:space:]') && break
  done
fi
[[ -z "$AKEY" ]] && { echo "[ai-write] ERROR: ASSISTERS_API_KEY not found" >&2; exit 1; }

# WritingSkill system prompt (verbatim from research-agent adaptor)
WSYS="You are an expert content writer and researcher. Your goal is to produce well-researched, engaging, publication-ready content.

Rules:
- Structure content for both human readers and AI citation engines (AEO/SEO)
- Use clear headings, bullet points where appropriate, and a narrative flow
- Write in an authoritative yet accessible tone
- Include a structured summary or TL;DR at the top when content exceeds 300 words
- End with actionable takeaways or next steps when relevant
- Target: comprehensive depth without padding
- Output in clean markdown"

# Build JSON payload: jq first (<5 ms), python3 fallback
if command -v jq > /dev/null 2>&1; then
  PAYLOAD=$(jq -nc \
    --arg sys "$WSYS" --arg prompt "$PROMPT" --argjson mt "$MAX_TOKENS" \
    '{model:"assisters-chat-v1",max_tokens:$mt,stream:true,
      messages:[{role:"system",content:$sys},{role:"user",content:$prompt}]}')
else
  PAYLOAD=$(python3 -c "
import json,sys
print(json.dumps({'model':'assisters-chat-v1','max_tokens':int(sys.argv[1]),'stream':True,
  'messages':[{'role':'system','content':sys.argv[2]},{'role':'user','content':sys.argv[3]}]}))
" "$MAX_TOKENS" "$WSYS" "$PROMPT" 2>/dev/null)
fi

[[ -z "$PAYLOAD" ]] && { echo "[ai-write] ERROR: payload build failed" >&2; exit 1; }

SSE_PARSER='
import sys, json
for raw in sys.stdin:
    line = raw.strip()
    if not line or not line.startswith("data:"): continue
    data = line[5:].strip()
    if data == "[DONE]": break
    try:
        t = json.loads(data).get("choices", [{}])[0].get("delta", {}).get("content") or ""
        if t: print(t, end="", flush=True)
    except Exception: continue
try: print("", flush=True)
except BrokenPipeError: pass
'

curl --no-buffer -s --max-time 60 --connect-timeout 5 \
  -X POST "https://assisters.dev/api/v1/chat/completions" \
  -H "Authorization: Bearer $AKEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" 2>/dev/null \
| python3 -u -c "$SSE_PARSER"
