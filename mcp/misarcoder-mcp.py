#!/usr/bin/env python3
"""
MisarCoder stdio MCP server for Claude Code.

Exposes MisarCoder's free-model MoE engine as Claude Code tools.
Claude delegates heavy work (code gen, analysis, reasoning) here
instead of consuming its own Anthropic inference tokens.

Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport).
Safe: if MisarCoder is not running, tools return an error and
Claude Code continues working normally — nothing breaks.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from subprocess import run, PIPE
from typing import Any, Dict, Optional

MISARCODER_URL = os.getenv("MISARCODER_URL", "http://127.0.0.1:8000")
TIMEOUT = int(os.getenv("MISARCODER_MCP_TIMEOUT", "60"))

TOOLS = [
    {
        "name": "misarcoder_complete",
        "description": (
            "Send a prompt to MisarCoder's free-model MoE engine "
            "(Gemini Flash, Groq Llama, Mistral, DeepSeek, etc.). "
            "Use for: code generation, debugging, refactoring, analysis, "
            "documentation writing, reasoning tasks. "
            "Returns the completion text. Falls back gracefully if unavailable."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The full prompt to complete.",
                },
                "task_type": {
                    "type": "string",
                    "enum": ["code", "reasoning", "general"],
                    "description": "Hint for model routing. Default: code.",
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Max output tokens. Default: 4096.",
                },
                "system": {
                    "type": "string",
                    "description": "Optional system prompt.",
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "misarcoder_ask",
        "description": (
            "Ask MisarCoder a quick question using the general/fast model "
            "(Gemini Flash). Best for short factual lookups, simple Q&A, "
            "summarisation, or any task under ~500 tokens."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question to answer."},
                "max_tokens": {"type": "integer", "description": "Max output tokens. Default: 1024."},
            },
            "required": ["question"],
        },
    },
]


def _get_api_key() -> str:
    try:
        result = run(
            ["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", "com.misar.misarcoder-api-key", "-w"],
            capture_output=True, text=True, timeout=3,
        )
        key = result.stdout.strip()
        if key:
            return key
    except Exception:
        pass
    # Fallback: read from config.env
    config_path = os.path.expanduser(
        "~/Desktop/G1 Technologies/Misar AI/MisarAICloud/MisarCoder/.env/config.env"
    )
    try:
        with open(config_path) as f:
            for line in f:
                if line.startswith("API_KEY="):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


def _call_misarcoder(prompt: str, system: Optional[str], task_type: str, max_tokens: int) -> str:
    key = _get_api_key()
    if not key:
        return "[misarcoder] API key not found — check Keychain or config.env"

    # Map task_type hint to model preference (MoE router picks the actual model)
    model_hint = {
        "reasoning": "groq/llama-3.3-70b-versatile",
        "general": "gemini-2.5-flash",
        "code": "gemini-2.5-flash",
    }.get(task_type, "gemini-2.5-flash")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": model_hint,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        f"{MISARCODER_URL}/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read())
            return body["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        return f"[misarcoder] Unavailable: {e.reason}. Start MisarCoder with: bash ~/.claude/scripts/misarcoder-start.sh"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"[misarcoder] Unexpected response: {e}"
    except Exception as e:
        return f"[misarcoder] Error: {e}"


# ---------------------------------------------------------------------------
# JSON-RPC / MCP protocol
# ---------------------------------------------------------------------------

def _send(obj: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _respond(req_id: Any, result: Any) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _error(req_id: Any, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def _handle(msg: Dict[str, Any]) -> None:
    method = msg.get("method", "")
    req_id = msg.get("id")  # None for notifications

    if method == "initialize":
        _respond(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "misarcoder", "version": "1.0.0"},
        })

    elif method == "notifications/initialized":
        pass  # notification — no response

    elif method == "tools/list":
        _respond(req_id, {"tools": TOOLS})

    elif method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "misarcoder_complete":
            text = _call_misarcoder(
                prompt=args.get("prompt", ""),
                system=args.get("system"),
                task_type=args.get("task_type", "code"),
                max_tokens=int(args.get("max_tokens", 4096)),
            )
        elif name == "misarcoder_ask":
            text = _call_misarcoder(
                prompt=args.get("question", ""),
                system=None,
                task_type="general",
                max_tokens=int(args.get("max_tokens", 1024)),
            )
        else:
            _error(req_id, -32601, f"Unknown tool: {name}")
            return

        _respond(req_id, {"content": [{"type": "text", "text": text}]})

    elif method == "ping":
        _respond(req_id, {})

    elif req_id is not None:
        _error(req_id, -32601, f"Method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            _handle(msg)
        except Exception as e:
            req_id = msg.get("id")
            if req_id is not None:
                _error(req_id, -32603, f"Internal error: {e}")


if __name__ == "__main__":
    main()
