#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261120.

The artwork ships in this repository as entry.png (drawn by
make_image.py).  This program's whole job is to deliver those exact
bytes to the judge: it copies the file that sits beside it to
/output/entry.png, creating the folder first when needed.

The destination can be redirected with the ENTRY_OUTPUT environment
variable, which is how the local determinism checks exercise the same
code path without touching /output.  Only the standard library is
used, and nothing here reads the clock, the network or randomness, so
every run writes byte-identical output.
"""

import os
import shutil
from pathlib import Path

FALLBACK_DESTINATION = "/output/entry.png"


def source_picture() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def destination() -> Path:
    override = os.environ.get("ENTRY_OUTPUT", "").strip()
    return Path(override) if override else Path(FALLBACK_DESTINATION)


def deliver() -> Path:
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_picture(), target)
    return target


if __name__ == "__main__":
    written = deliver()
    print(f"entry image delivered to {written}")
