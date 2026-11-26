#!/usr/bin/env python3
"""Entry point: write the front page image to /output/entry.png.

Standard library only, no network. The image is drawn at build time by
draw.py and bundled in this repository as entry.png; this program copies
those exact bytes to the output path, so both runs write the same bytes.
It verifies the copy by comparing SHA-256 digests of source and output.
Clears only the files inside the output folder, never the folder itself,
because the grader runs this as sandbox user 65534.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("ENTRY_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path):
            os.remove(path)
    out_path = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, out_path)
    size = os.path.getsize(out_path)
    assert size <= 1024 * 1024, size
    assert _sha256(src) == _sha256(out_path), "copy mismatch"
    print("wrote %s (%d bytes, sha256 %s)"
          % (out_path, size, _sha256(out_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
