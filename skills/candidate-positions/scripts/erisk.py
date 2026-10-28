#!/usr/bin/env python3
"""Entry point for the election-risk engine. Run `python3 erisk.py --help`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erisk_engine.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
