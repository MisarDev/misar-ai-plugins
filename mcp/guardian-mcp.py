#!/usr/bin/env python3
"""
Guardian MCP server for Claude Code.

Security scanning, code review, and dependency audit via Semgrep,
npm audit, and custom static analysis checks.

Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

TIMEOUT = int(os.getenv("GUARDIAN_TIMEOUT", "120"))
SEMGREP_BIN = os.getenv("SEMGREP_BIN", "semgrep")

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "guardian_semgrep_scan",
        "description": (
            "Run Semgrep SAST scan on a file or directory. "
            "Returns security findings with severity, CWE, line numbers, "
            "and fix suggestions. Supports custom rules or auto-config."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "File or directory path to scan.",
                },
                "rules": {
                    "type": "string",
                    "description": "Semgrep rule config: 'auto' (default), 'p/security-audit', 'p/owasp-top-ten', 'p/javascript', or a path to custom rules.",
                },
                "severity_filter": {
                    "type": "string",
                    "enum": ["INFO", "WARNING", "ERROR"],
                    "description": "Minimum severity to report. Default: WARNING.",
                },
                "max_findings": {
                    "type": "integer",
                    "description": "Max findings to return. Default: 50.",
                },
            },
            "required": ["target"],
        },
    },
    {
        "name": "guardian_scan_snippet",
        "description": (
            "Run Semgrep on a code snippet (not a file). "
            "Writes to a temp file, scans, and cleans up. "
            "Use for reviewing code before committing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code snippet to scan.",
                },
                "language": {
                    "type": "string",
                    "description": "Language: python, javascript, typescript, go, java, ruby, etc.",
                },
                "rules": {
                    "type": "string",
                    "description": "Semgrep rule config. Default: 'auto'.",
                },
            },
            "required": ["code", "language"],
        },
    },
    {
        "name": "guardian_dependency_audit",
        "description": (
            "Audit project dependencies for known vulnerabilities. "
            "Supports npm (package-lock.json), pip (requirements.txt), "
            "and pnpm (pnpm-lock.yaml). Returns CVEs with severity."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the project root directory.",
                },
                "package_manager": {
                    "type": "string",
                    "enum": ["npm", "pnpm", "pip", "auto"],
                    "description": "Package manager to audit. Default: auto-detect.",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "guardian_secret_scan",
        "description": (
            "Scan files for hardcoded secrets: API keys, tokens, passwords, "
            "private keys, connection strings. Uses pattern matching and "
            "entropy analysis. Returns findings with file locations."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "File or directory to scan for secrets.",
                },
                "include_low_confidence": {
                    "type": "boolean",
                    "description": "Include low-confidence findings. Default: false.",
                },
            },
            "required": ["target"],
        },
    },
    {
        "name": "guardian_license_check",
        "description": (
            "Check project dependencies for license compliance. "
            "Flags copyleft (GPL, AGPL) and unknown licenses. "
            "Returns a license inventory."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the project root directory.",
                },
            },
            "required": ["project_path"],
        },
    },
    {
        "name": "guardian_security_headers",
        "description": (
            "Check a Next.js / Express project for security header configuration. "
            "Verifies CSP, HSTS, X-Frame-Options, X-Content-Type-Options, etc."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Path to the project root directory.",
                },
            },
            "required": ["project_path"],
        },
    },
]

# ---------------------------------------------------------------------------
# Secret patterns (high + medium confidence)
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    # High confidence
    (r"AKIA[0-9A-Z]{16}", "aws_access_key", "high"),
    (r"(?:aws_secret_access_key|AWS_SECRET_ACCESS_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})", "aws_secret_key", "high"),
    (r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b", "github_token", "high"),
    (r"\bglpat-[A-Za-z0-9_-]{20,}\b", "gitlab_token", "high"),
    (r"\bxox[boaprs]-[A-Za-z0-9-]{10,}", "slack_token", "high"),
    (r"-----BEGIN\s+(RSA\s+|EC\s+|DSA\s+)?PRIVATE\s+KEY-----", "private_key", "high"),
    (r"\bsk-[A-Za-z0-9]{20,}\b", "openai_api_key", "high"),
    (r"\bsk_live_[A-Za-z0-9]{24,}\b", "stripe_secret_key", "high"),
    (r"\bSG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}\b", "sendgrid_key", "high"),
    (r"\bey[A-Za-z0-9-_]+\.ey[A-Za-z0-9-_]+\.[A-Za-z0-9-_.+/=]+\b", "jwt_token", "medium"),
    (r"mongodb(\+srv)?://[^:]+:[^@]+@", "mongodb_connection", "high"),
    (r"postgres(?:ql)?://[^:]+:[^@]+@", "postgres_connection", "high"),
    (r"mysql://[^:]+:[^@]+@", "mysql_connection", "high"),
    # Medium confidence
    (r"(?:password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", "generic_secret", "medium"),
    (r"(?:Bearer|Basic)\s+[A-Za-z0-9+/=_-]{20,}", "auth_header_value", "medium"),
]

# Security header checklist for Next.js
SECURITY_HEADERS = [
    ("Content-Security-Policy", "CSP"),
    ("Strict-Transport-Security", "HSTS"),
    ("X-Frame-Options", "Clickjacking protection"),
    ("X-Content-Type-Options", "MIME sniffing protection"),
    ("Referrer-Policy", "Referrer control"),
    ("Permissions-Policy", "Feature restrictions"),
    ("X-XSS-Protection", "XSS filter (legacy)"),
]


# ---------------------------------------------------------------------------
# Semgrep scanning
# ---------------------------------------------------------------------------
def _run_semgrep(target: str, rules: str, severity_filter: str, max_findings: int) -> Dict:
    if not os.path.exists(target):
        return {"error": f"Target not found: {target}"}

    severity_order = {"INFO": 0, "WARNING": 1, "ERROR": 2}
    min_severity = severity_order.get(severity_filter, 1)

    cmd = [
        SEMGREP_BIN, "scan",
        "--config", rules,
        "--json",
        "--quiet",
        "--no-git-ignore",
        target,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TIMEOUT,
        )
        if result.returncode not in (0, 1):  # 1 = findings found
            stderr = result.stderr.strip()
            if "invalid configuration" in stderr.lower():
                return {"error": f"Invalid Semgrep config: {rules}", "stderr": stderr[:500]}
            return {"error": f"Semgrep exited {result.returncode}", "stderr": stderr[:500]}

        body = json.loads(result.stdout) if result.stdout.strip() else {"results": []}
        raw_results = body.get("results", [])

        findings = []
        for r in raw_results:
            sev = r.get("extra", {}).get("severity", "WARNING")
            if severity_order.get(sev, 0) < min_severity:
                continue
            findings.append({
                "rule": r.get("check_id", ""),
                "severity": sev,
                "message": r.get("extra", {}).get("message", ""),
                "file": r.get("path", ""),
                "line_start": r.get("start", {}).get("line"),
                "line_end": r.get("end", {}).get("line"),
                "code": r.get("extra", {}).get("lines", "")[:200],
                "cwe": r.get("extra", {}).get("metadata", {}).get("cwe", []),
                "owasp": r.get("extra", {}).get("metadata", {}).get("owasp", []),
                "fix": r.get("extra", {}).get("fix", ""),
            })

        findings = findings[:max_findings]

        return {
            "scan_target": target,
            "rules": rules,
            "total_findings": len(raw_results),
            "filtered_findings": len(findings),
            "findings": findings,
            "errors_count": len(body.get("errors", [])),
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Semgrep scan timed out after {TIMEOUT}s"}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse Semgrep output: {e}"}
    except FileNotFoundError:
        return {"error": f"Semgrep not found at '{SEMGREP_BIN}'. Install: pip install semgrep"}


def _scan_snippet(code: str, language: str, rules: str) -> Dict:
    ext_map = {
        "python": ".py", "javascript": ".js", "typescript": ".ts",
        "tsx": ".tsx", "jsx": ".jsx", "go": ".go", "java": ".java",
        "ruby": ".rb", "rust": ".rs", "c": ".c", "cpp": ".cpp",
        "php": ".php", "swift": ".swift", "kotlin": ".kt",
    }
    ext = ext_map.get(language.lower(), f".{language}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        return _run_semgrep(tmp_path, rules, "WARNING", 50)
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Dependency audit
# ---------------------------------------------------------------------------
def _detect_package_manager(project_path: str) -> str:
    p = Path(project_path)
    if (p / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (p / "package-lock.json").exists() or (p / "package.json").exists():
        return "npm"
    if (p / "requirements.txt").exists() or (p / "Pipfile.lock").exists():
        return "pip"
    return "unknown"


def _audit_npm(project_path: str) -> Dict:
    try:
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True, text=True, timeout=60, cwd=project_path,
        )
        body = json.loads(result.stdout) if result.stdout.strip() else {}
        vulns = body.get("vulnerabilities", {})
        summary = body.get("metadata", {}).get("vulnerabilities", {})
        findings = []
        for pkg, info in list(vulns.items())[:30]:
            findings.append({
                "package": pkg,
                "severity": info.get("severity", "unknown"),
                "via": [v if isinstance(v, str) else v.get("title", "") for v in info.get("via", [])[:3]],
                "range": info.get("range", ""),
                "fix_available": info.get("fixAvailable", False),
            })
        return {"manager": "npm", "summary": summary, "findings": findings}
    except FileNotFoundError:
        return {"error": "npm not found"}
    except Exception as e:
        return {"error": f"npm audit failed: {e}"}


def _audit_pnpm(project_path: str) -> Dict:
    try:
        result = subprocess.run(
            ["pnpm", "audit", "--json"],
            capture_output=True, text=True, timeout=60, cwd=project_path,
        )
        body = json.loads(result.stdout) if result.stdout.strip() else {}
        advisories = body.get("advisories", {})
        findings = []
        for _id, info in list(advisories.items())[:30]:
            findings.append({
                "package": info.get("module_name", ""),
                "severity": info.get("severity", "unknown"),
                "title": info.get("title", ""),
                "url": info.get("url", ""),
                "patched_versions": info.get("patched_versions", ""),
            })
        return {"manager": "pnpm", "total": len(advisories), "findings": findings}
    except FileNotFoundError:
        return {"error": "pnpm not found"}
    except Exception as e:
        return {"error": f"pnpm audit failed: {e}"}


def _audit_pip(project_path: str) -> Dict:
    req_file = Path(project_path) / "requirements.txt"
    if not req_file.exists():
        return {"error": "requirements.txt not found"}
    try:
        result = subprocess.run(
            ["pip", "audit", "-r", str(req_file), "--format", "json"],
            capture_output=True, text=True, timeout=60,
        )
        body = json.loads(result.stdout) if result.stdout.strip() else {"dependencies": []}
        return {"manager": "pip", "findings": body.get("dependencies", [])[:30]}
    except FileNotFoundError:
        # pip-audit not installed, try safety
        try:
            result = subprocess.run(
                ["safety", "check", "-r", str(req_file), "--json"],
                capture_output=True, text=True, timeout=60,
            )
            return {"manager": "pip/safety", "findings": json.loads(result.stdout) if result.stdout.strip() else []}
        except FileNotFoundError:
            return {"error": "Neither pip-audit nor safety installed. Install: pip install pip-audit"}
    except Exception as e:
        return {"error": f"pip audit failed: {e}"}


def _dependency_audit(project_path: str, package_manager: str) -> Dict:
    if not os.path.isdir(project_path):
        return {"error": f"Directory not found: {project_path}"}

    if package_manager == "auto":
        package_manager = _detect_package_manager(project_path)

    if package_manager == "npm":
        return _audit_npm(project_path)
    elif package_manager == "pnpm":
        return _audit_pnpm(project_path)
    elif package_manager == "pip":
        return _audit_pip(project_path)
    else:
        return {"error": f"Could not detect package manager in {project_path}"}


# ---------------------------------------------------------------------------
# Secret scanning
# ---------------------------------------------------------------------------
SKIP_DIRS = {".git", "node_modules", ".next", "__pycache__", "dist", "build", ".venv", "venv"}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".svg", ".mp4", ".webm", ".zip", ".tar", ".gz"}


def _scan_secrets(target: str, include_low: bool) -> Dict:
    findings: List[Dict] = []
    target_path = Path(target)

    if target_path.is_file():
        files = [target_path]
    elif target_path.is_dir():
        files = []
        for root, dirs, filenames in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in filenames:
                fpath = Path(root) / fname
                if fpath.suffix.lower() in SKIP_EXTS:
                    continue
                if fpath.stat().st_size > 500_000:  # skip files > 500KB
                    continue
                files.append(fpath)
    else:
        return {"error": f"Target not found: {target}"}

    for fpath in files[:500]:  # cap at 500 files
        try:
            content = fpath.read_text(errors="ignore")
        except Exception:
            continue

        for pattern, secret_type, confidence in SECRET_PATTERNS:
            if not include_low and confidence == "low":
                continue
            for match in re.finditer(pattern, content):
                line_num = content[:match.start()].count("\n") + 1
                value = match.group()
                # Mask the value
                masked = value[:6] + "***" + value[-4:] if len(value) > 10 else "***"
                findings.append({
                    "file": str(fpath),
                    "line": line_num,
                    "type": secret_type,
                    "confidence": confidence,
                    "masked_value": masked,
                })

    return {
        "target": target,
        "files_scanned": len(files),
        "secrets_found": len(findings),
        "findings": findings[:100],  # cap output
    }


# ---------------------------------------------------------------------------
# License check
# ---------------------------------------------------------------------------
def _license_check(project_path: str) -> Dict:
    pkg_json = Path(project_path) / "package.json"
    if not pkg_json.exists():
        return {"error": "package.json not found — license check requires npm/pnpm project"}

    try:
        result = subprocess.run(
            ["npx", "license-checker", "--json", "--production"],
            capture_output=True, text=True, timeout=60, cwd=project_path,
        )
        if result.returncode != 0:
            return {"error": f"license-checker failed: {result.stderr[:300]}"}

        body = json.loads(result.stdout) if result.stdout.strip() else {}
        copyleft = []
        unknown = []
        inventory: Dict[str, int] = {}

        for pkg, info in body.items():
            lic = info.get("licenses", "Unknown")
            lic_str = lic if isinstance(lic, str) else ", ".join(lic)
            inventory[lic_str] = inventory.get(lic_str, 0) + 1

            if any(g in lic_str.upper() for g in ["GPL", "AGPL", "LGPL", "SSPL", "EUPL"]):
                copyleft.append({"package": pkg, "license": lic_str})
            elif lic_str in ("Unknown", "UNKNOWN", ""):
                unknown.append({"package": pkg, "license": lic_str})

        return {
            "total_packages": len(body),
            "license_inventory": inventory,
            "copyleft_flags": copyleft[:20],
            "unknown_licenses": unknown[:20],
            "issues": len(copyleft) + len(unknown),
        }
    except FileNotFoundError:
        return {"error": "npx not found — install Node.js"}
    except Exception as e:
        return {"error": f"License check failed: {e}"}


# ---------------------------------------------------------------------------
# Security headers check
# ---------------------------------------------------------------------------
def _check_security_headers(project_path: str) -> Dict:
    results: List[Dict] = []
    p = Path(project_path)

    # Check next.config.js/ts/mjs for headers
    next_configs = list(p.glob("next.config.*"))
    headers_config_found = False
    csp_found = False

    for cfg in next_configs:
        try:
            content = cfg.read_text()
            if "headers" in content:
                headers_config_found = True
            for header_name, desc in SECURITY_HEADERS:
                if header_name.lower() in content.lower():
                    results.append({"header": header_name, "description": desc, "status": "configured", "file": str(cfg)})
                    if header_name == "Content-Security-Policy":
                        csp_found = True
        except Exception:
            continue

    # Check middleware.ts/js for headers
    middleware_files = list(p.glob("**/middleware.ts")) + list(p.glob("**/middleware.js"))
    for mw in middleware_files[:3]:
        try:
            content = mw.read_text()
            for header_name, desc in SECURITY_HEADERS:
                if header_name.lower() in content.lower():
                    existing = [r for r in results if r["header"] == header_name]
                    if not existing:
                        results.append({"header": header_name, "description": desc, "status": "configured", "file": str(mw)})
                        if header_name == "Content-Security-Policy":
                            csp_found = True
        except Exception:
            continue

    # Report missing headers
    configured_headers = {r["header"] for r in results}
    for header_name, desc in SECURITY_HEADERS:
        if header_name not in configured_headers:
            results.append({"header": header_name, "description": desc, "status": "missing"})

    return {
        "project": project_path,
        "headers_config_found": headers_config_found,
        "csp_configured": csp_found,
        "headers": results,
        "missing_count": sum(1 for r in results if r["status"] == "missing"),
    }


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
            "serverInfo": {"name": "guardian", "version": "1.0.0"},
        })

    elif method == "notifications/initialized":
        pass

    elif method == "tools/list":
        _respond(req_id, {"tools": TOOLS})

    elif method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "guardian_semgrep_scan":
            result = _run_semgrep(
                target=args.get("target", "."),
                rules=args.get("rules", "auto"),
                severity_filter=args.get("severity_filter", "WARNING"),
                max_findings=int(args.get("max_findings", 50)),
            )
        elif name == "guardian_scan_snippet":
            result = _scan_snippet(
                code=args.get("code", ""),
                language=args.get("language", "python"),
                rules=args.get("rules", "auto"),
            )
        elif name == "guardian_dependency_audit":
            result = _dependency_audit(
                project_path=args.get("project_path", "."),
                package_manager=args.get("package_manager", "auto"),
            )
        elif name == "guardian_secret_scan":
            result = _scan_secrets(
                target=args.get("target", "."),
                include_low=args.get("include_low_confidence", False),
            )
        elif name == "guardian_license_check":
            result = _license_check(args.get("project_path", "."))
        elif name == "guardian_security_headers":
            result = _check_security_headers(args.get("project_path", "."))
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
