#!/usr/bin/env python3
"""Point this repository at the checked-in .githooks directory."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS_PATH = ".githooks"


def main() -> int:
    hooks_dir = ROOT / HOOKS_PATH
    pre_commit = hooks_dir / "pre-commit"
    if not pre_commit.is_file():
        print(f"missing {HOOKS_PATH}/pre-commit", file=sys.stderr)
        return 1

    # Keep shell hooks LF-only so Git for Windows / bash can run them.
    text = pre_commit.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    pre_commit.write_bytes(text)

    subprocess.run(
        ["git", "config", "core.hooksPath", HOOKS_PATH],
        cwd=ROOT,
        check=True,
    )
    print(f"Installed local Git hooks: core.hooksPath={HOOKS_PATH}")
    print("pre-commit runs: python scripts/check_sensitive_data.py --staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
