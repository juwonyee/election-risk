"""The policy book: one Markdown file per Nov 3 contest in election-risk-out/_book/, built on the user's machine.

  status            contests in _markets/elections.md, covered or still to research (biggest first)
  find              rows matching an issue tag, a state and/or a word in the position, across the book
  info              where the book came from (built here or downloaded), its date and fingerprint
  download          the maintainers' book from the repository release; needs --accept-risk
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
import zipfile

from .util import USER_AGENT, load_json, now_iso, out_root, save_json

RELEASE_URL = "https://github.com/juwonyee/election-risk/releases/latest/download/policy-book.zip"
IDS = re.compile(r"\b(?:kalshi|polymarket):[A-Za-z0-9._-]+")
# Single US Senate seats and House districts move policy only through chamber control (US-*-control.md).
SEAT = re.compile(r"^(?!.*\bstate\b).*\b(senate|house) (winner|election winner)", re.I)
LINE = re.compile(r"^((?:kalshi|polymarket):\S+) \| (.*?) \| vol ([\d,]+) \|")
WARNING = ("This policy book was built by the election-risk maintainers, not by you. It may be wrong, "
           "incomplete or out of date: candidates change positions, and the agents that built it made mistakes "
           "we did not catch. Check the source link of any row you rely on. Re-research any contest with "
           "$candidate-positions to replace it.")


def book_dir():
    return out_root() / "_book"


def _files():
    d = book_dir()
    return sorted(p for p in d.glob("*.md")) if d.exists() else []


def covered_ids() -> dict[str, str]:
    """market id -> book file name, from each file's 'Markets:' line."""
    out = {}
    for p in _files():
        for line in p.read_text(encoding="utf-8").splitlines()[:6]:
            if line.lower().startswith("markets:"):
                for i in IDS.findall(line):
                    out[i] = p.name
    return out


def status(include_house: bool = False) -> dict:
    """include_house also lists single Senate seats and House districts."""
    path = out_root() / "_markets" / "elections.md"
    if not path.exists():
        return {"error": "No market list yet. Run `erisk markets pull` first."}
    rows = []
    text = path.read_text(encoding="utf-8")
    house = out_root() / "_markets" / "house-districts.md"
    if include_house and house.exists():
        text += "\n" + house.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = LINE.match(line)
        if m and (include_house or not SEAT.search(m.group(2))):
            rows.append({"id": m.group(1), "title": m.group(2), "volume": int(m.group(3).replace(",", ""))})
    cov = covered_ids()
    todo = [r for r in rows if r["id"] not in cov]
    done = [{**r, "file": cov[r["id"]]} for r in rows if r["id"] in cov]
    return {"book": str(book_dir()), "source": info().get("source"), "markets": len(rows), "covered": len(done),
            "to_research": len(todo), "note": "One contest is often listed on both venues; one book file can cover "
            "both ids. Single US Senate seats and House districts work through chamber control "
            "(US-senate-control.md, US-house-control.md) and are left out unless --include-house.",
            "todo": todo, "done_files": sorted({d["file"] for d in done})}


def find(tag: str | None, state: str | None, text: str | None = None) -> dict:
    hits = []
    for p in _files():
        if state and not p.name.upper().startswith(state.upper() + "-") and not p.name.upper().startswith("US-"):
            continue
        cand = None
        body = p.read_text(encoding="utf-8")
        title = body.splitlines()[0].lstrip("# ").strip() if body else p.name
        for line in body.splitlines():
            if line.startswith("## "):
                cand = line[3:].strip()
            if line.startswith("|") and not line.startswith("|---") and not line.lower().startswith("| tag"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if (len(cells) >= 5 and (not tag or tag.lower() in cells[0].lower())
                        and (not text or text.lower() in (cells[0] + " " + cells[1]).lower())):
                    hits.append({"file": p.name, "contest": title, "candidate": cand, "tag": cells[0],
                                 "position": cells[1], "route": cells[2], "p": cells[3], "source": cells[4]})
    return {"tag": tag, "state": state, "text": text, "rows": hits, "count": len(hits)}


def fingerprint() -> str | None:
    files = _files()
    if not files:
        return None
    h = hashlib.sha256()
    for p in files:
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def info() -> dict:
    meta_path = book_dir() / "SOURCE.json"
    meta = load_json(meta_path) if meta_path.exists() else {}
    files = _files()
    if not files:
        return {"source": None, "files": 0, "note": "No policy book yet. Build it with $candidate-positions, or "
                "download the maintainers' book with `erisk book download --accept-risk` after the user agrees."}
    newest = max(p.stat().st_mtime for p in files)
    return {"source": meta.get("source", "built here"), "downloaded_at": meta.get("downloaded_at"),
            "built_by": meta.get("built_by"), "last_edit": dt.datetime.fromtimestamp(newest).date().isoformat(),
            "files": len(files), "fingerprint": fingerprint()}


def download(accept_risk: bool) -> dict:
    if not accept_risk:
        return {"ok": False, "warning": WARNING,
                "next": "Tell the user the warning in your own words. Only if they agree, run "
                        "`erisk book download --accept-risk`."}
    req = urllib.request.Request(RELEASE_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            blob = r.read()
    except urllib.error.HTTPError as x:
        return {"ok": False, "warning": WARNING, "error": f"HTTP {x.code} from {RELEASE_URL}",
                "fix": "The release may not be published yet. Build the book with $candidate-positions instead."}
    d = book_dir()
    d.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = [n for n in z.namelist() if n.endswith(".md") and "/" not in n.strip("/")]
        for n in names:
            (d / n).write_bytes(z.read(n))
        built_by = json.loads(z.read("SOURCE.json")) if "SOURCE.json" in z.namelist() else None
    save_json(d / "SOURCE.json", {"source": "downloaded", "url": RELEASE_URL, "downloaded_at": now_iso(),
                                  "built_by": built_by})
    return {"ok": True, "warning": WARNING, "files": len(names), **info()}
