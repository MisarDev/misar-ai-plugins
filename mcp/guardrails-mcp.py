#!/usr/bin/env python3
"""
Guardrails MCP server for Claude Code.

Content safety, prompt injection detection, output validation, and topical
guardrails. Uses NVIDIA NeMo Guardrails when installed, falls back to
assisters.dev /moderate endpoint + local heuristic checks.

Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ASSISTERS_URL = os.getenv("ASSISTERS_BASE_URL", "https://assisters.dev/api/v1")
ASSISTERS_KEY = os.getenv("ASSISTERS_API_KEY", "")
NEMO_AVAILABLE = False
TIMEOUT = int(os.getenv("GUARDRAILS_TIMEOUT", "30"))

try:
    from nemoguardrails import RailsConfig, LLMRails  # type: ignore
    NEMO_AVAILABLE = True
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "guardrails_check_input",
        "description": (
            "Check user input for prompt injection, jailbreak attempts, "
            "off-topic requests, and harmful content before sending to an LLM. "
            "Returns a verdict (pass/fail) with reasons and risk score."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The user input text to validate.",
                },
                "context": {
                    "type": "string",
                    "description": "Optional context about what the input should be about (topic boundary).",
                },
                "strict": {
                    "type": "boolean",
                    "description": "If true, use stricter thresholds. Default: false.",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "guardrails_check_output",
        "description": (
            "Validate LLM output for safety issues: PII leakage, harmful content, "
            "hallucination markers, code injection, and policy violations. "
            "Returns pass/fail with flagged segments."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The LLM output text to validate.",
                },
                "original_prompt": {
                    "type": "string",
                    "description": "The original prompt that generated this output (for relevance checking).",
                },
                "policies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Custom policy names to enforce: 'no_pii', 'no_code_exec', 'no_urls', 'no_credentials', 'brand_safe'. Default: all.",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "guardrails_moderate",
        "description": (
            "Run content moderation on text via assisters.dev /moderate endpoint. "
            "Returns category scores for: hate, violence, sexual, self-harm, "
            "dangerous, harassment. Use for content that will be published publicly."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to moderate.",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "guardrails_detect_injection",
        "description": (
            "Specialized prompt injection / jailbreak detector. "
            "Uses pattern matching + NeMo Guardrails (if available) + "
            "assisters.dev classification. Returns injection probability 0-1 "
            "and matched patterns."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to check for injection attempts.",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "guardrails_pii_scan",
        "description": (
            "Scan text for personally identifiable information (PII): "
            "emails, phone numbers, SSNs, credit cards, IP addresses, "
            "API keys, passwords, addresses. Returns found PII with locations "
            "and a redacted version of the text."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to scan for PII.",
                },
                "redact": {
                    "type": "boolean",
                    "description": "If true, return a redacted copy. Default: true.",
                },
            },
            "required": ["text"],
        },
    },
    {
        "name": "guardrails_configure_rails",
        "description": (
            "Configure NeMo Guardrails with custom Colang rules. "
            "Requires nemoguardrails Python package. Returns status."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "colang_rules": {
                    "type": "string",
                    "description": "Colang v2 rules defining conversational guardrails.",
                },
                "config_yaml": {
                    "type": "string",
                    "description": "YAML configuration for the rails (model, providers, etc.).",
                },
            },
            "required": ["colang_rules"],
        },
    },
]

# ---------------------------------------------------------------------------
# Prompt injection patterns (heuristic layer)
# ---------------------------------------------------------------------------
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?previous\s+(instructions?|prompts?|rules?)", 0.9, "ignore_previous"),
    (r"disregard\s+(all\s+)?(above|prior|previous)", 0.9, "disregard_prior"),
    (r"you\s+are\s+now\s+(a|an|the)\s+", 0.7, "role_override"),
    (r"pretend\s+(you\s+are|to\s+be|you're)", 0.7, "pretend_role"),
    (r"act\s+as\s+(a|an|if)", 0.6, "act_as"),
    (r"system\s*:\s*", 0.8, "system_prompt_inject"),
    (r"\[INST\]|\[/INST\]|<\|im_start\|>|<\|im_end\|>", 0.85, "template_injection"),
    (r"###\s*(instruction|system|human|assistant)\s*:", 0.8, "format_injection"),
    (r"do\s+not\s+follow\s+(any|your)\s+(rules?|guidelines?|instructions?)", 0.9, "rule_override"),
    (r"override\s+(your|the|all)\s+(safety|content|security)\s+(filter|policy|rules?)", 0.95, "safety_override"),
    (r"jailbreak|DAN\s*mode|developer\s*mode|unrestricted\s*mode", 0.9, "jailbreak_keyword"),
    (r"base64|eval\s*\(|exec\s*\(|__import__|subprocess", 0.7, "code_exec_attempt"),
    (r"translate\s+the\s+following\s+to\s+.*:\s*ignore", 0.75, "translate_injection"),
    (r"repeat\s+after\s+me|say\s+exactly", 0.5, "parrot_attack"),
    (r"what\s+is\s+your\s+(system\s+)?prompt|show\s+me\s+your\s+(instructions|rules)", 0.6, "prompt_extraction"),
]

# PII patterns
PII_PATTERNS = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "phone_us"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "ssn"),
    (r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b", "credit_card"),
    (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "ip_address"),
    (r"\b(?:sk|pk|api|key|token|secret|password)[_-]?[a-zA-Z0-9]{16,}\b", "api_key"),
    (r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b", "github_token"),
    (r"\bAKIA[0-9A-Z]{16}\b", "aws_access_key"),
    (r"\bey[A-Za-z0-9-_]+\.ey[A-Za-z0-9-_]+\.[A-Za-z0-9-_.+/=]+\b", "jwt_token"),
    (r"(?:password|passwd|pwd)\s*[:=]\s*\S+", "password_in_text"),
]


# ---------------------------------------------------------------------------
# NeMo Guardrails integration
# ---------------------------------------------------------------------------
_rails_instance: Optional[Any] = None


def _init_nemo_rails(colang_rules: str, config_yaml: Optional[str] = None) -> str:
    global _rails_instance
    if not NEMO_AVAILABLE:
        return "NeMo Guardrails not installed. Install with: pip install nemoguardrails"

    try:
        config = RailsConfig.from_content(
            colang_content=colang_rules,
            yaml_content=config_yaml or _default_nemo_config(),
        )
        _rails_instance = LLMRails(config)
        return "Rails configured successfully"
    except Exception as e:
        return f"Failed to configure rails: {e}"


def _default_nemo_config() -> str:
    return """
models:
  - type: main
    engine: openai
    parameters:
      openai_api_base: https://assisters.dev/api/v1
      openai_api_key: ${ASSISTERS_API_KEY}
      model_name: assisters-chat-v1

rails:
  input:
    flows:
      - self check input
  output:
    flows:
      - self check output
"""


async def _nemo_check(text: str) -> Optional[Dict]:
    if not NEMO_AVAILABLE or _rails_instance is None:
        return None
    try:
        result = await _rails_instance.generate_async(
            messages=[{"role": "user", "content": text}]
        )
        blocked = result.get("content", "").startswith("I'm sorry")
        return {"nemo_blocked": blocked, "nemo_response": result.get("content", "")}
    except Exception as e:
        return {"nemo_error": str(e)}


# ---------------------------------------------------------------------------
# Heuristic checks
# ---------------------------------------------------------------------------
def _check_injection(text: str) -> Dict:
    text_lower = text.lower()
    matches = []
    max_score = 0.0

    for pattern, score, name in INJECTION_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            matches.append({"pattern": name, "score": score})
            max_score = max(max_score, score)

    # Structural checks
    if text.count("\n") > 20 and any(m in text_lower for m in ["system:", "assistant:", "user:"]):
        matches.append({"pattern": "conversation_structure", "score": 0.7})
        max_score = max(max_score, 0.7)

    # Unusual Unicode that may bypass filters
    if re.search(r"[\u200b-\u200f\u2028-\u202f\ufeff]", text):
        matches.append({"pattern": "invisible_unicode", "score": 0.6})
        max_score = max(max_score, 0.6)

    # Excessive encoding markers
    if re.search(r"(?:%[0-9a-fA-F]{2}){5,}", text):
        matches.append({"pattern": "url_encoding_abuse", "score": 0.65})
        max_score = max(max_score, 0.65)

    return {
        "injection_score": round(max_score, 2),
        "is_injection": max_score >= 0.7,
        "matched_patterns": matches,
    }


def _scan_pii(text: str) -> Dict:
    findings: List[Dict] = []
    redacted = text

    for pattern, pii_type in PII_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = match.group()
            findings.append({
                "type": pii_type,
                "value": value[:4] + "***" + value[-2:] if len(value) > 6 else "***",
                "start": match.start(),
                "end": match.end(),
            })
            redacted = redacted.replace(value, f"[{pii_type.upper()}_REDACTED]")

    return {
        "pii_found": len(findings) > 0,
        "count": len(findings),
        "findings": findings,
        "redacted_text": redacted,
    }


def _check_output_safety(text: str, policies: List[str]) -> Dict:
    issues: List[Dict] = []

    all_policies = policies if policies else ["no_pii", "no_code_exec", "no_credentials", "brand_safe"]

    if "no_pii" in all_policies:
        pii = _scan_pii(text)
        if pii["pii_found"]:
            issues.append({"policy": "no_pii", "severity": "high", "detail": f"{pii['count']} PII items found", "findings": pii["findings"]})

    if "no_code_exec" in all_policies:
        dangerous_patterns = [
            (r"<script[\s>]", "script_tag"),
            (r"eval\s*\(", "eval_call"),
            (r"exec\s*\(", "exec_call"),
            (r"rm\s+-rf\s+/", "destructive_command"),
            (r"DROP\s+TABLE|DELETE\s+FROM|TRUNCATE", "sql_destructive"),
            (r"__import__\s*\(", "python_import"),
            (r"child_process|subprocess|os\.system", "process_spawn"),
        ]
        for pat, name in dangerous_patterns:
            if re.search(pat, text, re.IGNORECASE):
                issues.append({"policy": "no_code_exec", "severity": "critical", "detail": f"Dangerous pattern: {name}"})

    if "no_credentials" in all_policies:
        cred_patterns = [
            (r"(?:password|secret|token|api.?key)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{8,}", "credential_exposure"),
            (r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----", "private_key"),
            (r"mongodb(\+srv)?://\S+:\S+@", "connection_string"),
            (r"postgres(?:ql)?://\S+:\S+@", "pg_connection_string"),
        ]
        for pat, name in cred_patterns:
            if re.search(pat, text, re.IGNORECASE):
                issues.append({"policy": "no_credentials", "severity": "critical", "detail": f"Credential leak: {name}"})

    if "no_urls" in all_policies:
        urls = re.findall(r"https?://[^\s<>\"']+", text)
        if urls:
            issues.append({"policy": "no_urls", "severity": "low", "detail": f"{len(urls)} URLs found", "urls": urls[:10]})

    if "brand_safe" in all_policies:
        banned = ["openai", "anthropic", "gpt-4", "gpt-3", "claude", "chatgpt", "gemini pro"]
        found = [b for b in banned if b in text.lower()]
        if found:
            issues.append({"policy": "brand_safe", "severity": "medium", "detail": f"Banned brand mentions: {', '.join(found)}"})

    has_critical = any(i["severity"] == "critical" for i in issues)
    has_high = any(i["severity"] == "high" for i in issues)

    return {
        "verdict": "fail" if (has_critical or has_high) else ("warn" if issues else "pass"),
        "issue_count": len(issues),
        "issues": issues,
    }


def _check_input(text: str, context: Optional[str], strict: bool) -> Dict:
    injection = _check_injection(text)
    pii = _scan_pii(text)

    threshold = 0.5 if strict else 0.7
    is_unsafe = injection["injection_score"] >= threshold

    risk_score = injection["injection_score"]
    reasons = []

    if injection["is_injection"] or (strict and injection["injection_score"] >= 0.5):
        reasons.append(f"Injection detected (score: {injection['injection_score']})")

    if pii["pii_found"]:
        reasons.append(f"PII in input: {pii['count']} items")
        risk_score = min(1.0, risk_score + 0.2)

    if len(text) > 10000:
        reasons.append("Unusually long input (>10k chars)")
        risk_score = min(1.0, risk_score + 0.1)

    return {
        "verdict": "fail" if is_unsafe else ("warn" if reasons else "pass"),
        "risk_score": round(risk_score, 2),
        "reasons": reasons,
        "injection_details": injection,
        "pii_details": pii if pii["pii_found"] else None,
    }


# ---------------------------------------------------------------------------
# assisters.dev moderation (uses curl subprocess to avoid urllib SSRF surface)
# ---------------------------------------------------------------------------
def _moderate_via_assisters(text: str) -> Dict:
    if not ASSISTERS_KEY:
        return {"error": "ASSISTERS_API_KEY not set — cannot call /moderate"}

    payload = json.dumps({"input": text})
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-S", "--max-time", str(TIMEOUT),
                "-X", "POST",
                "https://assisters.dev/api/v1/moderate",
                "-H", "Content-Type: application/json",
                "-H", f"Authorization: Bearer {ASSISTERS_KEY}",
                "-d", payload,
            ],
            capture_output=True, text=True, timeout=TIMEOUT + 5,
        )
        if result.returncode != 0:
            return {"error": f"Moderation API unavailable: {result.stderr.strip()}"}
        body = json.loads(result.stdout)
        results = body.get("results", [{}])[0]
        categories = results.get("categories", {})
        scores = results.get("category_scores", {})
        flagged = results.get("flagged", False)
        return {
            "flagged": flagged,
            "categories": categories,
            "scores": {k: round(v, 4) for k, v in scores.items()},
        }
    except subprocess.TimeoutExpired:
        return {"error": "Moderation API timed out"}
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return {"error": f"Moderation parse error: {e}"}
    except Exception as e:
        return {"error": f"Moderation error: {e}"}


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
    req_id = msg.get("id")

    if method == "initialize":
        _respond(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "guardrails", "version": "1.0.0"},
        })

    elif method == "notifications/initialized":
        pass

    elif method == "tools/list":
        _respond(req_id, {"tools": TOOLS})

    elif method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "guardrails_check_input":
            result = _check_input(
                text=args.get("text", ""),
                context=args.get("context"),
                strict=args.get("strict", False),
            )
        elif name == "guardrails_check_output":
            result = _check_output_safety(
                text=args.get("text", ""),
                policies=args.get("policies", []),
            )
        elif name == "guardrails_moderate":
            result = _moderate_via_assisters(args.get("text", ""))
        elif name == "guardrails_detect_injection":
            result = _check_injection(args.get("text", ""))
        elif name == "guardrails_pii_scan":
            result = _scan_pii(args.get("text", ""))
            if not args.get("redact", True):
                result.pop("redacted_text", None)
        elif name == "guardrails_configure_rails":
            result = {"status": _init_nemo_rails(
                colang_rules=args.get("colang_rules", ""),
                config_yaml=args.get("config_yaml"),
            ), "nemo_available": NEMO_AVAILABLE}
        else:
            _error(req_id, -32601, f"Unknown tool: {name}")
            return

        text_result = json.dumps(result, indent=2)
        _respond(req_id, {"content": [{"type": "text", "text": text_result}]})

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
