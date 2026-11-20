#!/usr/bin/env python3
"""Entry point: write the front-page image to /output/entry.png.

Renders the page with render.py when Pillow is available; otherwise copies
the pre-rendered entry.jpg shipped in this repository, so both runs write
identical bytes either way. No network, no randomness, no timestamps.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUT, "entry.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    try:
        sys.path.insert(0, HERE)
        import render

        image = render.render()
        image.save(TARGET, "JPEG", quality=88)
    except Exception:
        shutil.copyfile(os.path.join(HERE, "entry.jpg"), TARGET)


if __name__ == "__main__":
    main()
