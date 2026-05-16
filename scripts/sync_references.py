#!/usr/bin/env python3
"""sync_references.py

Sync shared reference files from `_shared/` to both skill's `references/` directories.

Run from the repository root:

    python3 scripts/sync_references.py
    # or
    python3 -m scripts.sync_references

The teardown skill has an additional `speculation-markers.md` that lives only
in its own `references/` folder and is NOT managed by this script.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Repository root = parent of the directory containing this script.
REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = REPO_ROOT / "_shared"

TARGETS = [
    REPO_ROOT / "product-architecture-build/skills/product-architecture-build/references",
    REPO_ROOT / "product-architecture-teardown/skills/product-architecture-teardown/references",
]

# Files that live in _shared/ and need to be copied to each skill's references/.
SHARED_FILES = [
    "visual-styles.md",
    "html-spec.md",
    "arrow-routing.md",
]

# Header injected at the top of synced files so users don't edit the copies by mistake.
AUTO_GEN_HEADER = (
    "<!-- AUTO-GENERATED from _shared/. Do not edit here — edit the source in _shared/ "
    "and run `python3 scripts/sync_references.py`. -->\n\n"
)


def main() -> int:
    if not SHARED_DIR.exists():
        print(f"❌ {SHARED_DIR} does not exist. Aborting.", file=sys.stderr)
        return 1

    missing_sources = [f for f in SHARED_FILES if not (SHARED_DIR / f).exists()]
    if missing_sources:
        print(
            f"❌ Missing source files in {SHARED_DIR}: {missing_sources}",
            file=sys.stderr,
        )
        return 1

    synced_count = 0
    for target_dir in TARGETS:
        target_dir.mkdir(parents=True, exist_ok=True)
        for filename in SHARED_FILES:
            src = SHARED_DIR / filename
            dst = target_dir / filename

            # Read source content and inject AUTO-GENERATED header.
            content = src.read_text(encoding="utf-8")
            if not content.startswith("<!-- AUTO-GENERATED"):
                content = AUTO_GEN_HEADER + content

            dst.write_text(content, encoding="utf-8")
            rel = dst.relative_to(REPO_ROOT)
            print(f"✅ {SHARED_DIR.name}/{filename} → {rel}")
            synced_count += 1

    print(
        f"\n{synced_count} files synced. "
        "Note: teardown's speculation-markers.md is NOT managed by this script."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
