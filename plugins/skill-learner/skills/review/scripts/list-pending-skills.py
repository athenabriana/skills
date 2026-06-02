#!/usr/bin/env python3
"""List pending skills in review/ with parsed frontmatter. Outputs JSON."""

import json
import os
import re
import sys
from pathlib import Path

REVIEW_DIR = Path.home() / ".claude" / "skills" / "review"
ACTIVE_DIR = Path.home() / ".claude" / "skills" / "active"
REJECTED_DIR = Path.home() / ".claude" / "skills" / "rejected"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from markdown."""
    match = re.match(r"^---\n(.+?)\n---\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith("  - "):
            key, _, val = line.partition(":")
            val = val.strip()
            # Handle inline lists
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            elif val.replace(".", "").replace("-", "").isdigit():
                try:
                    val = float(val) if "." in val else int(val)
                except ValueError:
                    pass
            meta[key.strip()] = val
        elif line.startswith("  - "):
            # Multi-line list item
            last_key = [k for k in meta][-1] if meta else None
            if last_key:
                if not isinstance(meta[last_key], list):
                    meta[last_key] = [] if not meta[last_key] else [meta[last_key]]
                meta[last_key].append(line.strip("- ").strip())

    return meta, match.group(2)


def extract_section(body: str, heading: str) -> str:
    """Extract content under a ## heading."""
    pattern = rf"## {re.escape(heading)}\n\n?(.*?)(?=\n## |\Z)"
    match = re.search(pattern, body, re.DOTALL)
    return match.group(1).strip() if match else ""


def main():
    if not REVIEW_DIR.is_dir():
        print("[]")
        return

    skills = []
    for path in sorted(REVIEW_DIR.glob("*.md")):
        text = path.read_text()
        meta, body = parse_frontmatter(text)

        skills.append({
            "file": path.name,
            "name": meta.get("name", path.stem),
            "description": meta.get("description", ""),
            "confidence": meta.get("confidence", 0),
            "occurrences": meta.get("occurrences", 0),
            "scope": meta.get("scope", "unknown"),
            "sources": meta.get("sources", []),
            "extracted": meta.get("extracted", ""),
            "procedure": extract_section(body, "Procedure"),
            "gotchas": extract_section(body, "Gotchas"),
            "when_to_use": extract_section(body, "When to Use"),
        })

    # Sort by confidence descending
    skills.sort(key=lambda s: s["confidence"], reverse=True)

    # Add counts summary
    active_count = len(list(ACTIVE_DIR.glob("*.md"))) if ACTIVE_DIR.is_dir() else 0
    rejected_count = len(list(REJECTED_DIR.glob("*.md"))) if REJECTED_DIR.is_dir() else 0

    output = {
        "pending": skills,
        "counts": {
            "pending": len(skills),
            "active": active_count,
            "rejected": rejected_count,
        }
    }

    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
