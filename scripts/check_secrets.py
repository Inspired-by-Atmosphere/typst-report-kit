#!/usr/bin/env python3
"""Self-contained secret / leak scanner (stdlib only, no dependencies).

Run from the repo root:
    python scripts/check_secrets.py .

Exit code 0 = no findings. Exit code 1 = findings (listed on stdout).

Checks
  1. Credential-shaped strings: API keys, tokens, passwords, private keys.
  2. Personal / internal identifiers: e-mail addresses, absolute host paths
     (Windows drive paths, MSYS-style home paths, Unix home paths), private
     IPv4 ranges, MAC addresses, internal-looking hostnames.
  3. High-entropy tokens (long random-looking strings) that may be secrets.

Lines that only *name* a variable (e.g. `API_KEY=`) are reported by check 1
as a warning-free match only when a value follows; bare assignments are
skipped because they carry no secret.
"""
import math
import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache"}
SKIP_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip", ".gz",
            ".exe", ".dll", ".woff", ".woff2", ".ttf", ".pyc", ".so", ".dylib"}
MAX_BYTES = 2_000_000

# --- 1. credentials ---------------------------------------------------------
CRED_PATTERNS = [
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
    ("assigned-password", re.compile(r"(?i)\b(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)\b\s*[:=]\s*['\"]?([^\s'\"]{6,})")),
    ("inline-credential-url", re.compile(r"(?i)\b[a-z][a-z0-9+.\-]*://[^\s:/@]+:[^\s/@]{4,}@")),
]

# --- 2. personal / internal identifiers -------------------------------------
PATH_PATTERNS = [
    ("windows-abs-path", re.compile(r"\b[A-Za-z]:[\\/](?:Users|Documents|Desktop|projects?|repo|src|work|data)\b")),
    ("msys-home-path", re.compile(r"/[cde]/Users/[A-Za-z0-9_.\-]+")),
    ("msys-drive-path", re.compile(r"/(?:[cde]|mnt/[a-z])/[A-Za-z0-9_.\-]{2,}/")),
    ("unix-home-path", re.compile(r"/(?:home|Users)/[A-Za-z0-9_.\-]+")),
]

IDENT_PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
    ("private-ip", re.compile(r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b")),
    ("mac-address", re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")),
    ("tencent-qq", re.compile(r"\b(?:qq|QQ)\s*[:=]?\s*\d{5,12}\b")),
    ("net-broadcast-url", re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?")),
]

# File extensions treated as text for path scanning
TEXT_EXT = {".md", ".txt", ".typ", ".py", ".toml", ".yaml", ".yml", ".json",
            ".cfg", ".ini", ".sh", ".bash", ".ps1", ".js", ".ts", ".html",
            ".css", ".rs", ".go", ".c", ".h", ".cpp", ".gitignore", ""}

# Allowlist: exact substrings that are legitimately not secrets.
ALLOW_LINE_SUBSTRINGS = [
    "noreply.github.com",       # GitHub noreply author e-mail in metadata
    "127.0.0.1",                # loopback (proxy example)
    "0.0.0.0",
    "255.255.255.255",
    "example.com",
    "your-name", "your-org", "your-server", "your-team",
]

ENTROPY_MIN_LEN = 24
ENTROPY_THRESHOLD = 4.2


def shannon_entropy(s):
    if not s:
        return 0.0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


TOKEN_RE = re.compile(r"[A-Za-z0-9+/=_\-]{%d,}" % ENTROPY_MIN_LEN)


def scan_line(line):
    """Return a list of (label, match-text) for one line."""
    hits = []
    lowered = line.lower()
    for label, rx in CRED_PATTERNS:
        m = rx.search(line)
        if m:
            val = m.group(1) if m.groups() else m.group(0)
            # bare `FOO_TOKEN=` with no value carries no secret
            if label == "assigned-password" and val in ("", '""', "''"):
                continue
            if any(s in line for s in ALLOW_LINE_SUBSTRINGS):
                if label == "email":
                    continue
            hits.append((label, m.group(0)))
    for label, rx in PATH_PATTERNS:
        if rx.search(line):
            hits.append((label, rx.search(line).group(0)))
    for label, rx in IDENT_PATTERNS:
        m = rx.search(line)
        if m and not any(s in line for s in ALLOW_LINE_SUBSTRINGS):
            hits.append((label, m.group(0)))
    for m in TOKEN_RE.finditer(line):
        tok = m.group(0)
        if 'http' in lowered or shannon_entropy(tok) < ENTROPY_THRESHOLD:
            continue
        if any(s in tok for s in ALLOW_LINE_SUBSTRINGS):
            continue
        hits.append(("high-entropy-string", tok[:40] + ("..." if len(tok) > 40 else "")))
    return hits


def iter_files(root):
    if os.path.isfile(root):
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    findings = []
    scanned = 0
    for path in iter_files(root):
        ext = os.path.splitext(path)[1].lower()
        base = os.path.basename(path)
        if ext in SKIP_EXT or base.endswith(".bak") or ".bak_" in base:
            continue
        if ext not in TEXT_EXT and base not in (".gitignore", ".gitattributes"):
            continue
        try:
            if os.path.getsize(path) > MAX_BYTES:
                continue
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
        except OSError:
            continue
        scanned += 1
        for i, line in enumerate(content.split("\n"), 1):
            if len(line) > 5000:
                line = line[:5000]
            for label, text in scan_line(line):
                findings.append((os.path.relpath(path, root), i, label, text))

    print(f"scanner: {os.path.abspath(root)}")
    print(f"files scanned: {scanned}")
    if not findings:
        print("findings: 0")
        print("RESULT: PASS (no secrets, credentials or internal identifiers)")
        return 0
    print(f"findings: {len(findings)}")
    for rel, line, label, text in findings:
        print(f"  {rel}:{line}: [{label}] {text}")
    print("RESULT: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
