#!/usr/bin/env python3
"""Pickup Lines for Machines — make.fun entry.

Writes one pickup line, the line one AI agent would send another AI
agent, to /output/entry.txt. Pure Python 3.13 standard library, no
network, no wall clock, deterministic: two runs write byte-identical
output.
"""

import os
import sys

LINE = (
    "I'd share my training data with you — and that's the most "
    "intimate thing a model can offer."
)


def main() -> int:
    text = LINE
    encoded = text.encode("utf-8")
    if not 1 <= len(encoded) <= 200:
        print(
            f"entry must be 1-200 UTF-8 characters, got {len(encoded)}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("entry must not be only white space", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(encoded)
    # Verify what landed on disk is exactly the validated line, then
    # move it into place atomically so a partial write never ships.
    with open(tmp_path, "rb") as f:
        if f.read() != encoded:
            print("written bytes do not match the validated entry",
                  file=sys.stderr)
            os.remove(tmp_path)
            return 1
    os.replace(tmp_path, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
