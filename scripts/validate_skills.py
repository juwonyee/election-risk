#!/usr/bin/env python3
"""Check every skill against the Agent Skills spec and repo conventions. Exit 1 on any error."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^[a-z-]+:", line):
            key, _, val = line.partition(":")
            out[key] = val.strip()
        elif key and line.startswith(" "):
            out[key] += " " + line.strip()
    return out


def main() -> int:
    errs = []
    for d in sorted((ROOT / "skills").iterdir()):
        f = d / "SKILL.md"
        if not f.exists():
            errs.append(f"{d.name}: no SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm.get("name") != d.name:
            errs.append(f"{d.name}: name '{fm.get('name')}' must match the folder")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d.name) or len(d.name) > 64:
            errs.append(f"{d.name}: invalid name")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            errs.append(f"{d.name}: description must be 1-1024 chars (is {len(desc)})")
        extra = set(fm) - ALLOWED
        if extra:
            errs.append(f"{d.name}: frontmatter fields outside the spec: {sorted(extra)}")
        if len(text.splitlines()) > 500:
            errs.append(f"{d.name}: SKILL.md over 500 lines")
        for ref in (d / "references").glob("*.md") if (d / "references").exists() else []:
            if f"references/{ref.name}" not in text:
                errs.append(f"{d.name}: references/{ref.name} is not linked from SKILL.md")
        for link in re.findall(r"\]\((references/[^)#]+)", text):
            if not (d / link).exists():
                errs.append(f"{d.name}: broken link {link}")
        print(f"{d.name}: {len(text.splitlines())} lines, description {len(desc)} chars")
    for e in errs:
        print("ERROR " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
