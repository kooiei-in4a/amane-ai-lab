#!/usr/bin/env python3
"""Detect likely sensitive data in repository content."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {".git", ".venv", "venv", "__pycache__", "node_modules", ".work"}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".html",
    ".xml",
    ".css",
    ".js",
    ".yml",
    ".yaml",
    ".py",
    ".mdc",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".properties",
}

HIGH = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "api_key_assignment": re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|secret[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}"
    ),
    "bearer_token": re.compile(r"(?i)bearer\s+[a-z0-9\-_\.=]{20,}"),
    "connection_string": re.compile(r"(?i)(postgres|mysql|mongodb|redis)://[^\s]+"),
}

MEDIUM = {
    "email": re.compile(
        r"(?<![A-Z0-9._%+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![A-Z0-9._%+-])",
        re.I,
    ),
    "ipv4_private": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})\b"
    ),
    "windows_path": re.compile(r"[A-Za-z]:\\(?:[^\s/:*?\"<>|]+\\)*[^\s/:*?\"<>|]+"),
    "unix_home": re.compile(r"(?<![\w-])/(?:home|Users)/[A-Za-z0-9._-]+(?:/[^\s]*)?"),
    "internal_url": re.compile(r"(?i)\bhttps?://(?:intranet|internal|corp)[^\s]*"),
}

REDACTED_TOKEN_RE = re.compile(r"\[REDACTED_[A-Z0-9_]+\]")

DOC_POLICY_PREFIXES = (
    "agents/policies/",
    "agents/checklists/",
    "AGENTS.md",
    "SECURITY.md",
    "docs/",
    "scripts/check_sensitive_data.py",
    "tests/",
)

SAFE_EMAIL_DOMAINS = (
    "example.com",
    "example.org",
    "github.com",
    "users.noreply.github.com",
)


def is_text_file(path: Path) -> bool:
    lower_name = path.name.lower()
    if lower_name == "dockerfile" or lower_name == ".env" or lower_name.startswith(".env."):
        return True
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        "AGENTS.md",
        "CLAUDE.md",
        "LICENSE",
        "LICENSE-CONTENT",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        ".gitignore",
    }


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def is_policy_doc(rel: str) -> bool:
    return any(rel == p or rel.startswith(p) for p in DOC_POLICY_PREFIXES)


def scan_file(path: Path, rel: str) -> list[tuple[int, str, str]]:
    """Return findings without returning the matched secret value.

    Redaction placeholders are removed before matching. A placeholder therefore
    remains allowed by itself, but it cannot suppress a real secret elsewhere on
    the same line.
    """

    findings: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings

    for lineno, line in enumerate(text.splitlines(), start=1):
        scan_line = REDACTED_TOKEN_RE.sub("", line)
        for kind, pattern in HIGH.items():
            if pattern.search(scan_line):
                findings.append((lineno, kind, "[MATCH_REDACTED]"))
        if is_policy_doc(rel):
            continue
        for kind, pattern in MEDIUM.items():
            match = pattern.search(scan_line)
            if not match:
                continue
            if kind == "email":
                email = match.group(0).lower()
                domain = email.rsplit("@", 1)[1]
                if domain in SAFE_EMAIL_DOMAINS:
                    continue
            findings.append((lineno, kind, "[MATCH_REDACTED]"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repository for sensitive data candidates")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    root = Path(args.root).resolve()

    findings_total = 0
    scanned = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip(path.relative_to(root)):
            continue
        if not is_text_file(path):
            continue
        scanned += 1
        rel = str(path.relative_to(root)).replace("\\", "/")
        for lineno, kind, _ in scan_file(path, rel):
            findings_total += 1
            # Never echo the matched line: CI logs must not become a second leak.
            print(f"{rel}:{lineno}: {kind}")

    print(f"scanned_files={scanned} findings={findings_total}")
    return 1 if findings_total else 0


if __name__ == "__main__":
    raise SystemExit(main())
