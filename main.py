#!/usr/bin/env python3
"""news-image-20261117 round-2 entry.

Copies the pre-rendered poster (drawn by render.py in this repository
from ~40 verified news stories of Tuesday 17 November 2026) to
/output/entry.png. Standard library only; no network, no clock, fully
deterministic: both runs write identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
