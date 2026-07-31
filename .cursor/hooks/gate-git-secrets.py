#!/usr/bin/env python3
"""Cursor hook: block git commit/push when sensitive-data scan fails."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "check_sensitive_data.py"

# Match real git invocations inside compound shell commands.
GIT_COMMIT_RE = re.compile(r"(?:^|[\n;&|]\s*)git(?:\.exe)?\s+commit\b", re.I)
GIT_PUSH_RE = re.compile(r"(?:^|[\n;&|]\s*)git(?:\.exe)?\s+push\b", re.I)
COMMIT_ALL_RE = re.compile(r"(?:^|\s)(?:-a|--all)(?:\s|$)")


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload))
    sys.stdout.write("\n")
    sys.stdout.flush()


def deny(user_message: str, agent_message: str) -> None:
    emit(
        {
            "permission": "deny",
            "user_message": user_message,
            "agent_message": agent_message,
        }
    )


def read_command() -> str | None:
    """Return the shell command from Cursor hook stdin, or None if not gated."""
    raw = sys.stdin.buffer.read()
    if not raw or not raw.strip():
        # No payload: do not block unrelated tooling; matcher should usually avoid this.
        return None

    text = raw.decode("utf-8", errors="replace").strip()
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        # Some hosts may pass a bare command string; still try to gate.
        return text

    if not isinstance(payload, dict):
        return str(payload)

    return str(payload.get("command") or "")


def run_scan(staged: bool) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(SCANNER)]
    if staged:
        args.append("--staged")
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    command = read_command()
    if command is None:
        emit({"permission": "allow"})
        return 0

    is_commit = bool(GIT_COMMIT_RE.search(command))
    is_push = bool(GIT_PUSH_RE.search(command))
    if not (is_commit or is_push):
        emit({"permission": "allow"})
        return 0

    if not SCANNER.is_file():
        deny(
            "機密情報スキャナが見つかりません。",
            f"Missing scanner: {SCANNER}",
        )
        return 0

    # commit -a/--all can include unstaged edits; prefer full-tree scan.
    use_staged = is_commit and not is_push and not COMMIT_ALL_RE.search(command)
    result = run_scan(staged=use_staged)
    if result.returncode == 0:
        emit({"permission": "allow"})
        return 0

    output = (result.stdout or "").strip()
    errors = (result.stderr or "").strip()
    details = "\n".join(part for part in (output, errors) if part) or "sensitive-data check failed"
    if len(details) > 1500:
        details = details[:1500] + "\n..."

    mode = "staged" if use_staged else "full-tree"
    deny(
        "機密情報検査に失敗したため git 操作をブロックしました。",
        (
            f"check_sensitive_data.py ({mode}) failed with exit {result.returncode}.\n"
            f"{details}\n"
            "Remove or redact findings, then retry. Do not bypass with --no-verify."
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
