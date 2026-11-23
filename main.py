#!/usr/bin/env python3
"""news-image-20261123 entrypoint (Python 3.13, standard library only).

Copies the entry image beside this file to the grader's output directory.
The program runs twice and both runs must write the same bytes; copying a
fixed file guarantees that.

Usage:
    python3 main.py
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")


if __name__ == "__main__":
    main()
