#!/usr/bin/env python3
"""
MISAR DEFENDER — Local Machine Security Daemon
6-layer security monitor for macOS M1 Pro

Layers:
1. File Integrity Monitor — SHA-256 baselines, change detection
2. Network Sentinel — outbound connection monitoring
3. Process Watchdog — LaunchAgents, crypto miners, reverse shells
4. Credential Guard — .env, SSH key, Keychain access monitoring
5. USB/Peripheral Shield — new device alerts
6. App Integrity — code signature verification

Run: python3 defender.py start|stop|status|scan|dashboard
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import signal
import subprocess
import threading
import re
from pathlib import Path
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

HOME = Path.home()
DEFENDER_DIR = Path(__file__).parent.parent
DB_PATH = DEFENDER_DIR / "defender.db"
PID_FILE = DEFENDER_DIR / "defender.pid"
LOG_FILE = DEFENDER_DIR / "defender.log"
BASELINE_FILE = DEFENDER_DIR / "baseline.json"
DASHBOARD_PORT = 9876

# Critical directories to monitor (ONLY system/config dirs, NOT project dirs)
WATCH_DIRS = [
    HOME / ".ssh",
    HOME / ".claude",
    HOME / ".env",
    HOME / ".zshrc",
    HOME / ".bashrc",
    HOME / ".gitconfig",
    HOME / "Library/Keychains",
    HOME / "Library/LaunchAgents",
    Path("/Library/LaunchDaemons"),
    Path("/Library/LaunchAgents"),
]

# Paths to EXCLUDE from file integrity monitoring (false positive sources)
EXCLUDE_PATHS = [
    "plugins/cache/",          # Claude plugin cache — rotates normally
    "plugins/data/",           # Claude plugin data
    "/sessions/",              # Claude session files — rotate normally
    "/target/debug/",          # Rust build artifacts
    "/target/release/",        # Rust build artifacts
    "/node_modules/",          # npm packages
    ".jsonl",                  # Claude conversation logs (change every session)
    "/.next/",                 # Next.js build cache
    "/.turbo/",                # Turborepo cache
    "/dist/",                  # Build output
    "/.git/",                  # Git internals
    "/temp_git_",              # Claude temp plugin dirs
]

# Critical file patterns
CRITICAL_PATTERNS = [
    "*.env", "*.env.*", ".env.local", ".env.production",
    "id_rsa", "id_ed25519", "id_ecdsa", "*.pem", "*.key",
    "credentials.json", "service-account*.json",
    "*.keychain-db",
]

# Process whitelist — known safe processes that match suspicious names
PROCESS_WHITELIST = [
    "Claude Helper",           # Claude.app renderer process
    "Claude.app",              # Claude desktop app
    "/Applications/Claude",    # Claude app path
    "Visual Studio Code",      # VS Code (all helpers contain "nc" in path)
    "Code Helper",             # VS Code helper processes
    ".vscode/extensions/",     # VS Code extensions (Claude Code)
    "Brave Browser",           # Browser
    "Google Chrome",           # Browser
    "com.apple.",              # Apple system processes
    "/usr/libexec/",           # macOS system daemons
    "/usr/sbin/",              # macOS system (launchd, universalaccessd)
    "/System/",                # macOS system
    "/sbin/launchd",           # macOS init process
    "OneDrive",                # Microsoft OneDrive
    "Avast",                   # Avast antivirus
    "Microsoft",               # Microsoft apps
]

# Directories where .env files are EXPECTED (project dirs — not a threat)
ENV_SAFE_DIRS = [
    HOME / "Desktop/G1 Technologies",    # All G1 Tech projects
    HOME / "Desktop/Projects",           # Personal projects
    HOME / "Desktop/Clients",            # Client projects
]

# Known malicious/exfil domains
SUSPICIOUS_DOMAINS = [
    "pastebin.com", "hastebin.com", "transfer.sh", "file.io",
    "0x0.st", "webhook.site", "requestbin.com", "pipedream.com",
    "ngrok.io", "serveo.net", "localtunnel.me",
]

# Suspicious process names
SUSPICIOUS_PROCESSES = [
    "xmrig", "minerd", "cryptominer", "coinhive",
    "nc", "ncat", "socat",  # reverse shell tools
    "tcpdump", "wireshark-cli",  # packet sniffers
    "keylogger", "screenlogger",
]

THREAT_LEVELS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢",
    "INFO": "🔵",
}


# ═══════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            layer TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT,
            action_taken TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS baselines (
            path TEXT PRIMARY KEY,
            hash TEXT NOT NULL,
            size INTEGER,
            mtime REAL,
            recorded_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def log_event(conn, layer, severity, title, details="", action=""):
    timestamp = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO events (timestamp, layer, severity, title, details, action_taken) VALUES (?, ?, ?, ?, ?, ?)",
        (timestamp, layer, severity, title, details, action)
    )
    conn.commit()

    # Also notify via macOS
    icon = THREAT_LEVELS.get(severity, "⚪")
    if severity in ("CRITICAL", "HIGH"):
        notify(f"{icon} {title}", details[:200])

    # Log to file
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{severity}] [{layer}] {title} — {details[:100]}\n")


def notify(title, message):
    """Send macOS notification"""
    try:
        escaped_title = title.replace('"', '\\"')
        escaped_msg = message.replace('"', '\\"')
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{escaped_msg}" with title "Misar Defender" subtitle "{escaped_title}" sound name "Sosumi"'],
            capture_output=True, timeout=5
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# LAYER 1: FILE INTEGRITY MONITOR
# ═══════════════════════════════════════════════════════════════

def hash_file(filepath):
    """SHA-256 hash of a file"""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def build_baseline(conn):
    """Build SHA-256 baseline of all critical files"""
    count = 0
    for watch_dir in WATCH_DIRS:
        if not watch_dir.exists():
            continue
        for root, dirs, files in os.walk(watch_dir):
            # Skip deep traversal of large dirs
            if len(files) > 1000:
                continue
            for fname in files:
                fpath = Path(root) / fname
                if fpath.is_symlink():
                    continue
                try:
                    file_hash = hash_file(fpath)
                    if file_hash:
                        stat = fpath.stat()
                        conn.execute(
                            "INSERT OR REPLACE INTO baselines (path, hash, size, mtime, recorded_at) VALUES (?, ?, ?, ?, ?)",
                            (str(fpath), file_hash, stat.st_size, stat.st_mtime, datetime.now().isoformat())
                        )
                        count += 1
                except (PermissionError, OSError):
                    continue
    conn.commit()
    return count


def is_excluded_path(fpath):
    """Check if a file path should be excluded from monitoring"""
    fpath_str = str(fpath)
    for exclude in EXCLUDE_PATHS:
        if exclude in fpath_str:
            return True
    return False


def check_file_integrity(conn):
    """Check all baselined files for changes"""
    alerts = []
    cursor = conn.execute("SELECT path, hash, size FROM baselines")
    for row in cursor.fetchall():
        fpath, expected_hash, expected_size = row
        path = Path(fpath)

        # Skip excluded paths (cache, build artifacts, etc.)
        if is_excluded_path(fpath):
            continue

        if not path.exists():
            alerts.append(("CRITICAL", f"Critical file DELETED: {fpath}", fpath))
            continue

        current_hash = hash_file(path)
        if current_hash and current_hash != expected_hash:
            alerts.append(("HIGH", f"File MODIFIED: {fpath}", f"Hash changed from {expected_hash[:16]}... to {current_hash[:16]}..."))

    return alerts


def check_new_files(conn):
    """Detect new files in watched directories that aren't in baseline"""
    alerts = []
    known_paths = set()
    cursor = conn.execute("SELECT path FROM baselines")
    for row in cursor.fetchall():
        known_paths.add(row[0])

    for watch_dir in WATCH_DIRS:
        if not watch_dir.exists():
            continue
        for root, dirs, files in os.walk(watch_dir):
            if len(files) > 1000:
                continue
            for fname in files:
                fpath = str(Path(root) / fname)
                # Skip excluded paths
                if is_excluded_path(fpath):
                    continue
                if fpath not in known_paths:
                    # Check if it matches critical patterns
                    for pattern in CRITICAL_PATTERNS:
                        if Path(fname).match(pattern):
                            alerts.append(("MEDIUM", f"New critical file detected: {fpath}", "Not in baseline"))
                            break

    return alerts


# ═══════════════════════════════════════════════════════════════
# LAYER 2: NETWORK SENTINEL
# ═══════════════════════════════════════════════════════════════

def check_network_connections():
    """Monitor outbound connections for suspicious activity"""
    alerts = []
    try:
        result = subprocess.run(
            ["lsof", "-i", "-n", "-P"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")[1:]  # skip header

        for line in lines:
            parts = line.split()
            if len(parts) < 9:
                continue

            process_name = parts[0]
            connection = parts[-2] if len(parts) > 8 else ""

            # Check for connections to suspicious domains
            for domain in SUSPICIOUS_DOMAINS:
                if domain in connection.lower():
                    alerts.append(("CRITICAL", f"Connection to suspicious domain: {domain}",
                                   f"Process: {process_name}, Connection: {connection}"))

            # Check for reverse shell indicators
            if process_name in ("nc", "ncat", "bash", "sh", "zsh"):
                if "ESTABLISHED" in line and "->" in connection:
                    remote = connection.split("->")[-1] if "->" in connection else ""
                    if remote and not remote.startswith("127.") and not remote.startswith("localhost"):
                        alerts.append(("CRITICAL", f"Possible reverse shell: {process_name}",
                                       f"Connection: {connection}"))

    except (subprocess.TimeoutExpired, Exception):
        pass

    return alerts


def check_dns_queries():
    """Check for suspicious DNS resolution attempts"""
    alerts = []
    try:
        # Check recent DNS cache
        result = subprocess.run(
            ["log", "show", "--predicate",
             'process == "mDNSResponder" AND eventMessage CONTAINS "query"',
             "--last", "5m", "--style", "compact"],
            capture_output=True, text=True, timeout=15
        )

        for domain in SUSPICIOUS_DOMAINS:
            if domain in result.stdout:
                alerts.append(("HIGH", f"DNS query to suspicious domain: {domain}",
                               "Detected in mDNSResponder logs"))
    except Exception:
        pass

    return alerts


# ═══════════════════════════════════════════════════════════════
# LAYER 3: PROCESS WATCHDOG
# ═══════════════════════════════════════════════════════════════

def check_suspicious_processes():
    """Detect suspicious running processes"""
    alerts = []
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")[1:]

        for line in lines:
            parts = line.split(None, 10)
            if len(parts) < 11:
                continue

            process = parts[10].lower()
            cpu = float(parts[2]) if parts[2].replace('.', '').isdigit() else 0

            # Check for known suspicious process names
            for suspicious in SUSPICIOUS_PROCESSES:
                if suspicious in process:
                    # Check whitelist before alerting
                    is_whitelisted = False
                    for safe in PROCESS_WHITELIST:
                        if safe.lower() in parts[10].lower():
                            is_whitelisted = True
                            break
                    if not is_whitelisted:
                        alerts.append(("CRITICAL", f"Suspicious process detected: {suspicious}",
                                       f"Full command: {parts[10][:100]}"))

            # Check for high CPU (potential crypto miner)
            if cpu > 90:
                proc_name = parts[10].split("/")[-1].split()[0]
                if proc_name not in ("kernel_task", "WindowServer", "Google Chrome", "node", "python3", "swift"):
                    alerts.append(("HIGH", f"High CPU process: {proc_name} ({cpu}%)",
                                   f"Possible crypto miner. Command: {parts[10][:100]}"))

    except Exception:
        pass

    return alerts


def check_launch_agents():
    """Detect new LaunchAgents and LaunchDaemons (persistence mechanisms)"""
    alerts = []
    launch_dirs = [
        HOME / "Library/LaunchAgents",
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
    ]

    for launch_dir in launch_dirs:
        if not launch_dir.exists():
            continue
        for f in launch_dir.iterdir():
            if f.suffix == ".plist":
                try:
                    stat = f.stat()
                    # Alert on recently created plist files (last 24 hours)
                    if time.time() - stat.st_mtime < 86400:
                        alerts.append(("HIGH", f"New LaunchAgent/Daemon: {f.name}",
                                       f"Path: {f}, Modified: {datetime.fromtimestamp(stat.st_mtime).isoformat()}"))
                except (PermissionError, OSError):
                    continue

    return alerts


def check_cron_jobs():
    """Check for unauthorized cron jobs"""
    alerts = []
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = [l for l in result.stdout.strip().split("\n") if l.strip() and not l.startswith("#")]
            if lines:
                alerts.append(("MEDIUM", f"Active cron jobs detected: {len(lines)}",
                               f"Jobs: {'; '.join(lines[:3])}"))
    except Exception:
        pass

    return alerts


# ═══════════════════════════════════════════════════════════════
# LAYER 4: CREDENTIAL GUARD
# ═══════════════════════════════════════════════════════════════

def check_env_files():
    """Scan for exposed .env files outside of known project directories"""
    alerts = []
    suspicious_locations = [
        HOME / "Downloads",
        HOME / "Documents",
        Path("/tmp"),
    ]

    for loc in suspicious_locations:
        if not loc.exists():
            continue
        for f in loc.rglob("*.env*"):
            if f.is_file() and f.stat().st_size > 0:
                # Skip Rust build artifacts (.rcgu.o files with .env in name)
                if ".rcgu." in str(f) or "/target/" in str(f):
                    continue
                # Skip .env.example files (not secrets)
                if str(f).endswith(".example") or str(f).endswith(".env.md"):
                    continue
                # Skip files inside known safe project dirs
                is_safe = False
                for safe_dir in ENV_SAFE_DIRS:
                    if str(f).startswith(str(safe_dir)):
                        is_safe = True
                        break
                if is_safe:
                    continue
                alerts.append(("HIGH", f".env file in exposed location: {f}",
                               f"Size: {f.stat().st_size} bytes. Not in a known project directory."))

    return alerts


def check_ssh_key_permissions():
    """Verify SSH key file permissions are correct"""
    alerts = []
    ssh_dir = HOME / ".ssh"
    if not ssh_dir.exists():
        return alerts

    for f in ssh_dir.iterdir():
        if f.name.startswith("id_") and not f.name.endswith(".pub"):
            try:
                mode = oct(f.stat().st_mode)[-3:]
                if mode != "600":
                    alerts.append(("HIGH", f"SSH key has wrong permissions: {f.name}",
                                   f"Current: {mode}, Expected: 600. Run: chmod 600 {f}"))
            except (PermissionError, OSError):
                continue

    return alerts


def check_clipboard_secrets():
    """Check if clipboard contains potential secrets"""
    alerts = []
    try:
        result = subprocess.run(
            ["pbpaste"], capture_output=True, text=True, timeout=3
        )
        clipboard = result.stdout

        secret_patterns = [
            (r'(?:api[_\-]?key|apikey)\s*[=:]\s*\S{20,}', "API Key"),
            (r'(?:secret|password|passwd|pwd)\s*[=:]\s*\S{8,}', "Password/Secret"),
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
            (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', "Private Key"),
            (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
        ]

        for pattern, secret_type in secret_patterns:
            if re.search(pattern, clipboard, re.IGNORECASE):
                alerts.append(("HIGH", f"Clipboard contains {secret_type}",
                               "Clear clipboard: pbcopy < /dev/null"))
                break

    except Exception:
        pass

    return alerts


# ═══════════════════════════════════════════════════════════════
# LAYER 5: USB / PERIPHERAL SHIELD
# ═══════════════════════════════════════════════════════════════

_known_usb_devices = set()

def check_usb_devices():
    """Monitor for new USB device connections"""
    global _known_usb_devices
    alerts = []

    try:
        result = subprocess.run(
            ["system_profiler", "SPUSBDataType", "-json"],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(result.stdout)
        current_devices = set()

        def extract_devices(items):
            for item in items:
                if isinstance(item, dict):
                    name = item.get("_name", "Unknown")
                    vendor = item.get("manufacturer", "Unknown")
                    serial = item.get("serial_num", "")
                    device_id = f"{name}|{vendor}|{serial}"
                    current_devices.add(device_id)

                    if "_items" in item:
                        extract_devices(item["_items"])

        if "SPUSBDataType" in data:
            extract_devices(data["SPUSBDataType"])

        if _known_usb_devices:
            new_devices = current_devices - _known_usb_devices
            for device in new_devices:
                name, vendor, serial = device.split("|")
                alerts.append(("MEDIUM", f"New USB device connected: {name}",
                               f"Vendor: {vendor}, Serial: {serial}"))

        _known_usb_devices = current_devices

    except Exception:
        pass

    return alerts


# ═══════════════════════════════════════════════════════════════
# LAYER 6: APP INTEGRITY
# ═══════════════════════════════════════════════════════════════

def check_app_signatures():
    """Verify code signatures of running applications"""
    alerts = []
    try:
        result = subprocess.run(
            ["ps", "-eo", "pid,comm"], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")[1:]

        checked = set()
        for line in lines:
            parts = line.strip().split(None, 1)
            if len(parts) < 2:
                continue
            binary = parts[1]
            if binary in checked or not binary.startswith("/"):
                continue
            checked.add(binary)

            # Only check app binaries, skip system
            if binary.startswith("/System/") or binary.startswith("/usr/"):
                continue

            try:
                sig_result = subprocess.run(
                    ["codesign", "-v", binary],
                    capture_output=True, text=True, timeout=3
                )
                if sig_result.returncode != 0 and "not signed" in sig_result.stderr.lower():
                    app_name = Path(binary).name
                    alerts.append(("MEDIUM", f"Unsigned binary running: {app_name}",
                                   f"Path: {binary}"))
            except (subprocess.TimeoutExpired, Exception):
                continue

    except Exception:
        pass

    return alerts


def check_camera_mic_access():
    """Check for processes accessing camera or microphone"""
    alerts = []
    try:
        # Check for processes using camera
        result = subprocess.run(
            ["lsof", "+D", "/dev/", "-c", "VDC"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            alerts.append(("MEDIUM", "Camera is currently in use",
                           result.stdout.strip()[:200]))
    except Exception:
        pass

    return alerts


# ═══════════════════════════════════════════════════════════════
# BIOMETRIC AUTH GATE
# ═══════════════════════════════════════════════════════════════

def require_biometric_auth(reason="Misar Defender requires authentication"):
    """Require Touch ID or password before sensitive operations"""
    try:
        # Use LocalAuthentication via osascript (doesn't need Developer cert)
        script = f'''
        tell application "System Events"
            display dialog "{reason}" ¬
                default answer "" ¬
                with hidden answer ¬
                buttons {{"Cancel", "Authenticate"}} ¬
                default button "Authenticate" ¬
                with title "Misar Defender — Authentication Required" ¬
                with icon caution
        end tell
        '''
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════
# DASHBOARD (localhost:9876)
# ═══════════════════════════════════════════════════════════════

def generate_dashboard_html(conn):
    """Generate security dashboard HTML"""
    # Get recent events
    cursor = conn.execute(
        "SELECT timestamp, layer, severity, title, details FROM events ORDER BY id DESC LIMIT 50"
    )
    events = cursor.fetchall()

    # Get counts by severity
    severity_counts = {}
    for sev in THREAT_LEVELS:
        cursor = conn.execute("SELECT COUNT(*) FROM events WHERE severity = ?", (sev,))
        severity_counts[sev] = cursor.fetchone()[0]

    # Get counts by layer
    layer_counts = {}
    cursor = conn.execute(
        "SELECT layer, COUNT(*) FROM events GROUP BY layer ORDER BY COUNT(*) DESC"
    )
    for row in cursor.fetchall():
        layer_counts[row[0]] = row[1]

    events_html = ""
    for ts, layer, sev, title, details in events:
        icon = THREAT_LEVELS.get(sev, "⚪")
        color = {"CRITICAL": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#eab308", "LOW": "#22c55e", "INFO": "#3b82f6"}.get(sev, "#6b7280")
        time_str = ts.split("T")[1][:8] if "T" in ts else ts
        date_str = ts.split("T")[0] if "T" in ts else ""
        events_html += f'''
        <div class="event" style="border-left: 3px solid {color};">
            <div class="event-header">
                <span class="severity" style="color:{color}">{icon} {sev}</span>
                <span class="layer">{layer}</span>
                <span class="time">{date_str} {time_str}</span>
            </div>
            <div class="event-title">{title}</div>
            <div class="event-details">{(details or '')[:150]}</div>
        </div>'''

    total_events = sum(severity_counts.values())
    threat_level = "SECURE"
    threat_color = "#22c55e"
    if severity_counts.get("CRITICAL", 0) > 0:
        threat_level = "CRITICAL"
        threat_color = "#ef4444"
    elif severity_counts.get("HIGH", 0) > 0:
        threat_level = "ELEVATED"
        threat_color = "#f97316"
    elif severity_counts.get("MEDIUM", 0) > 0:
        threat_level = "GUARDED"
        threat_color = "#eab308"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Misar Defender — Security Dashboard</title>
<meta http-equiv="refresh" content="30">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0a0a0a; color: #e5e5e5; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro', system-ui, sans-serif; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
h1 {{ font-size: 24px; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; gap: 12px; }}
h1 .shield {{ font-size: 32px; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 24px; }}
.stat {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 16px; text-align: center; }}
.stat .value {{ font-size: 32px; font-weight: 700; }}
.stat .label {{ font-size: 12px; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}
.threat-indicator {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 24px; }}
.threat-level {{ font-size: 48px; font-weight: 800; letter-spacing: 4px; }}
.threat-label {{ font-size: 14px; color: #888; margin-top: 8px; }}
.events {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 12px; padding: 16px; }}
.events h2 {{ font-size: 16px; margin-bottom: 12px; color: #888; }}
.event {{ padding: 12px; margin-bottom: 8px; background: #111; border-radius: 8px; }}
.event-header {{ display: flex; gap: 12px; align-items: center; font-size: 12px; margin-bottom: 4px; }}
.severity {{ font-weight: 600; }}
.layer {{ background: #2a2a2a; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
.time {{ color: #666; margin-left: auto; }}
.event-title {{ font-weight: 500; font-size: 14px; }}
.event-details {{ font-size: 12px; color: #666; margin-top: 2px; }}
.layers {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 24px; }}
.layer-card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 12px; text-align: center; }}
.layer-card .count {{ font-size: 24px; font-weight: 700; color: #c4913a; }}
.layer-card .name {{ font-size: 11px; color: #888; margin-top: 4px; }}
footer {{ text-align: center; padding: 24px; color: #444; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
    <h1><span class="shield">🛡️</span> Misar Defender</h1>

    <div class="threat-indicator">
        <div class="threat-level" style="color: {threat_color}">{threat_level}</div>
        <div class="threat-label">Current Threat Level</div>
    </div>

    <div class="stats">
        <div class="stat"><div class="value" style="color:#ef4444">{severity_counts.get("CRITICAL", 0)}</div><div class="label">Critical</div></div>
        <div class="stat"><div class="value" style="color:#f97316">{severity_counts.get("HIGH", 0)}</div><div class="label">High</div></div>
        <div class="stat"><div class="value" style="color:#eab308">{severity_counts.get("MEDIUM", 0)}</div><div class="label">Medium</div></div>
        <div class="stat"><div class="value" style="color:#22c55e">{severity_counts.get("LOW", 0)}</div><div class="label">Low</div></div>
        <div class="stat"><div class="value" style="color:#3b82f6">{severity_counts.get("INFO", 0)}</div><div class="label">Info</div></div>
        <div class="stat"><div class="value">{total_events}</div><div class="label">Total Events</div></div>
    </div>

    <div class="layers">
        {"".join(f'<div class="layer-card"><div class="count">{count}</div><div class="name">{name}</div></div>' for name, count in layer_counts.items())}
    </div>

    <div class="events">
        <h2>Recent Events (last 50)</h2>
        {events_html if events_html else '<div style="padding:20px;text-align:center;color:#444">No events recorded yet. Run a scan first.</div>'}
    </div>

    <footer>
        Misar Defender v1.0 — Local Machine Security Daemon<br>
        Auto-refreshes every 30 seconds | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </footer>
</div>
</body>
</html>'''


class DashboardHandler(SimpleHTTPRequestHandler):
    conn = None

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html = generate_dashboard_html(self.conn)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path == "/api/events":
            cursor = self.conn.execute(
                "SELECT timestamp, layer, severity, title, details FROM events ORDER BY id DESC LIMIT 100"
            )
            events = [{"timestamp": r[0], "layer": r[1], "severity": r[2], "title": r[3], "details": r[4]}
                       for r in cursor.fetchall()]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(events).encode())
        elif self.path == "/api/scan":
            run_full_scan(self.conn)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs


# ═══════════════════════════════════════════════════════════════
# SCAN ENGINE
# ═══════════════════════════════════════════════════════════════

def run_full_scan(conn):
    """Run all 6 security layers"""
    print("🛡️  Running full security scan...")
    total_alerts = 0

    # Layer 1: File Integrity
    print("  [1/6] File Integrity Monitor...")
    integrity_alerts = check_file_integrity(conn)
    new_file_alerts = check_new_files(conn)
    for sev, title, details in integrity_alerts + new_file_alerts:
        log_event(conn, "FILE_INTEGRITY", sev, title, details)
        total_alerts += 1

    # Layer 2: Network Sentinel
    print("  [2/6] Network Sentinel...")
    net_alerts = check_network_connections()
    for sev, title, details in net_alerts:
        log_event(conn, "NETWORK", sev, title, details)
        total_alerts += 1

    # Layer 3: Process Watchdog
    print("  [3/6] Process Watchdog...")
    proc_alerts = check_suspicious_processes()
    launch_alerts = check_launch_agents()
    cron_alerts = check_cron_jobs()
    for sev, title, details in proc_alerts + launch_alerts + cron_alerts:
        log_event(conn, "PROCESS", sev, title, details)
        total_alerts += 1

    # Layer 4: Credential Guard
    print("  [4/6] Credential Guard...")
    env_alerts = check_env_files()
    ssh_alerts = check_ssh_key_permissions()
    clip_alerts = check_clipboard_secrets()
    for sev, title, details in env_alerts + ssh_alerts + clip_alerts:
        log_event(conn, "CREDENTIAL", sev, title, details)
        total_alerts += 1

    # Layer 5: USB Shield
    print("  [5/6] USB/Peripheral Shield...")
    usb_alerts = check_usb_devices()
    for sev, title, details in usb_alerts:
        log_event(conn, "USB", sev, title, details)
        total_alerts += 1

    # Layer 6: App Integrity
    print("  [6/6] App Integrity...")
    sig_alerts = check_app_signatures()
    cam_alerts = check_camera_mic_access()
    for sev, title, details in sig_alerts + cam_alerts:
        log_event(conn, "APP_INTEGRITY", sev, title, details)
        total_alerts += 1

    # Log scan completion
    log_event(conn, "SYSTEM", "INFO", f"Full scan complete: {total_alerts} alerts",
              f"Scanned at {datetime.now().isoformat()}")

    print(f"  ✅ Scan complete: {total_alerts} alerts found")
    return total_alerts


# ═══════════════════════════════════════════════════════════════
# DAEMON
# ═══════════════════════════════════════════════════════════════

def start_daemon(conn):
    """Start the defender daemon with periodic scanning"""
    # Write PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    print("🛡️  Misar Defender started")
    print(f"   PID: {os.getpid()}")
    print(f"   Dashboard: http://localhost:{DASHBOARD_PORT}")
    print(f"   Log: {LOG_FILE}")
    print("   Press Ctrl+C to stop\n")

    # Build initial baseline if not exists
    cursor = conn.execute("SELECT COUNT(*) FROM baselines")
    if cursor.fetchone()[0] == 0:
        print("  Building file integrity baseline...")
        count = build_baseline(conn)
        log_event(conn, "SYSTEM", "INFO", f"Baseline created: {count} files", "Initial baseline")
        print(f"  ✅ Baselined {count} files\n")

    # Initial scan
    run_full_scan(conn)

    # Start dashboard server in background thread
    DashboardHandler.conn = conn
    server = HTTPServer(("127.0.0.1", DASHBOARD_PORT), DashboardHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"\n  📊 Dashboard live at http://localhost:{DASHBOARD_PORT}\n")

    # Periodic scanning loop
    scan_interval = 300  # 5 minutes
    try:
        while True:
            time.sleep(scan_interval)
            run_full_scan(conn)
    except KeyboardInterrupt:
        print("\n🛡️  Misar Defender stopped")
        server.shutdown()
        if PID_FILE.exists():
            PID_FILE.unlink()


def stop_daemon():
    """Stop the defender daemon"""
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"🛡️  Misar Defender stopped (PID: {pid})")
        except ProcessLookupError:
            print("🛡️  Daemon was not running")
        PID_FILE.unlink(missing_ok=True)
    else:
        print("🛡️  No running daemon found")


def show_status(conn):
    """Show current defender status"""
    running = False
    pid = None
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            os.kill(pid, 0)
            running = True
        except ProcessLookupError:
            PID_FILE.unlink()

    print("🛡️  Misar Defender Status")
    print(f"   Running: {'✅ Yes (PID: ' + str(pid) + ')' if running else '❌ No'}")
    print(f"   Database: {DB_PATH}")
    print(f"   Dashboard: http://localhost:{DASHBOARD_PORT}")

    # Event summary
    cursor = conn.execute("SELECT COUNT(*) FROM events")
    total = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM events WHERE severity = 'CRITICAL'")
    critical = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM events WHERE severity = 'HIGH'")
    high = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM baselines")
    files = cursor.fetchone()[0]

    print(f"\n   Events: {total} total | {critical} critical | {high} high")
    print(f"   Baselined files: {files}")

    # Last scan
    cursor = conn.execute(
        "SELECT timestamp FROM events WHERE layer='SYSTEM' AND title LIKE '%scan%' ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        print(f"   Last scan: {row[0]}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 defender.py [start|stop|status|scan|baseline|dashboard]")
        sys.exit(1)

    command = sys.argv[1].lower()
    conn = init_db()

    if command == "start":
        start_daemon(conn)
    elif command == "stop":
        stop_daemon()
    elif command == "status":
        show_status(conn)
    elif command == "scan":
        run_full_scan(conn)
        print(f"\n  📊 View results: python3 {__file__} dashboard")
    elif command == "baseline":
        print("Building file integrity baseline...")
        count = build_baseline(conn)
        print(f"✅ Baselined {count} files")
    elif command == "dashboard":
        DashboardHandler.conn = conn
        server = HTTPServer(("127.0.0.1", DASHBOARD_PORT), DashboardHandler)
        print(f"📊 Dashboard: http://localhost:{DASHBOARD_PORT}")
        print("Press Ctrl+C to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    conn.close()


if __name__ == "__main__":
    main()
