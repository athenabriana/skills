#!/usr/bin/env python3
"""Move a skill between review/, active/, rejected/ folders."""

import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"
FOLDERS = {"review", "active", "rejected"}


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <action> <skill-name> [skill-name ...]")
        print("Actions: approve, reject, skip")
        sys.exit(1)

    action = sys.argv[1]
    names = sys.argv[2:]

    if action == "approve":
        src, dst = "review", "active"
    elif action == "reject":
        src, dst = "review", "rejected"
    elif action == "skip":
        print(f"Skipped: {', '.join(names)}")
        return
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)

    src_dir = SKILLS_DIR / src
    dst_dir = SKILLS_DIR / dst
    dst_dir.mkdir(parents=True, exist_ok=True)

    for name in names:
        filename = f"{name}.md" if not name.endswith(".md") else name
        src_path = src_dir / filename
        dst_path = dst_dir / filename

        if not src_path.exists():
            print(f"Not found: {src_path}")
            continue

        src_path.rename(dst_path)
        past = {"approve": "Approved", "reject": "Rejected"}[action]
        print(f"{past}: {name} -> {dst}")


if __name__ == "__main__":
    main()
