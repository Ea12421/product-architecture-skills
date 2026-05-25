#!/usr/bin/env python3
"""validate_and_sync.py

Wrapper that runs `sync_references.py` first, then `quick_validate.py` on the
given skill path. This is the recommended pre-commit workflow.

Run from the repository root with module syntax (because quick_validate.py
inside this repo's scripts/ uses package-style imports if extended later):

    python3 -m scripts.validate_and_sync product-architecture-build/skills/product-architecture-build
    python3 -m scripts.validate_and_sync product-architecture-teardown/skills/product-architecture-teardown
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_references.py"
QUICK_VALIDATE = REPO_ROOT / "scripts" / "quick_validate.py"


def main() -> int:
    if not SYNC_SCRIPT.exists():
        print(f"❌ {SYNC_SCRIPT} not found.", file=sys.stderr)
        return 1
    if not QUICK_VALIDATE.exists():
        print(f"❌ {QUICK_VALIDATE} not found.", file=sys.stderr)
        return 1

    # 1. Sync first.
    print("🔄 Syncing references from _shared/ ...")
    result = subprocess.run([sys.executable, str(SYNC_SCRIPT)])
    if result.returncode != 0:
        print("❌ Sync failed. Aborting before validation.", file=sys.stderr)
        return result.returncode

    # 2. Validate the skill path passed in argv.
    if len(sys.argv) < 2:
        print(
            "\n⚠️ No skill path given. Sync done; skipping validation.\n"
            "   Usage: python3 -m scripts.validate_and_sync <path/to/skill>",
            file=sys.stderr,
        )
        return 0

    skill_path = sys.argv[1]
    print(f"\n🔍 Validating skill at: {skill_path}")
    result = subprocess.run([sys.executable, str(QUICK_VALIDATE), skill_path])
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
