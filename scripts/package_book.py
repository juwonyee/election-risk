#!/usr/bin/env python3
"""Zip a built policy book for a GitHub release (the file `erisk book download` fetches).

  python3 scripts/package_book.py <path-to/_book> [out.zip]

The zip holds the contest files and SOURCE.json (who built it, when, fingerprint). Attach it to a release as
`policy-book.zip`. The book itself is never committed to the repository.
"""
import datetime as dt
import hashlib
import json
import sys
import zipfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = Path(sys.argv[1])
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "policy-book.zip")
    files = sorted(src.glob("*.md"))
    if not files:
        print(f"no .md files in {src}")
        return 1
    h = hashlib.sha256()
    for p in files:
        h.update(p.name.encode())
        h.update(p.read_bytes())
    meta = {"built_by": "election-risk maintainers", "built_on": dt.date.today().isoformat(),
            "contests": len(files), "fingerprint": h.hexdigest()[:12]}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.name)
        z.writestr("SOURCE.json", json.dumps(meta, indent=2))
    print(f"{out}: {len(files)} contests, fingerprint {meta['fingerprint']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
