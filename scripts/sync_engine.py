#!/usr/bin/env python3
"""Copy engine/ into each skill's scripts/, so every skill works when installed on its own.

  python3 scripts/sync_engine.py           copy
  python3 scripts/sync_engine.py --check   exit 1 if the copy differs (for CI)
"""
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "engine"
SKILLS = ["election-risk", "prediction-markets", "profit-structure", "candidate-positions"]


def files(base: Path):
    return sorted(p.relative_to(base) for p in base.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")


def main() -> int:
    check = "--check" in sys.argv
    src = files(ENGINE)
    bad = []
    for s in SKILLS:
        dst = ROOT / "skills" / s / "scripts"
        if check:
            if files(dst) != src or any(not filecmp.cmp(ENGINE / f, dst / f, shallow=False) for f in src):
                bad.append(s)
            continue
        # Overwrite in place and remove stale files (deleting the folder fails on Windows/OneDrive locks).
        for stale in set(files(dst)) - set(src) if dst.exists() else ():
            (dst / stale).unlink()
        for f in src:
            (dst / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ENGINE / f, dst / f)
        print(f"synced {len(src)} files -> skills/{s}/scripts/")
    if bad:
        print("out of sync: " + ", ".join(bad) + " (run python3 scripts/sync_engine.py)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
