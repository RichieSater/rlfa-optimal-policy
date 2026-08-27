#!/usr/bin/env python3
"""Reject internal process-status artifacts from tracked public text."""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRAGMENTS = [
    ("review", "-", "protocol"),
    ("review", " protocol"),
    ("human", "-", "review", "-", "packet"),
    ("human", " review"),
    ("finite", "-", "group", "-", "specialist"),
    ("finite", "-", "group", " specialist"),
    ("lean", "/", "formalization", " specialist"),
    ("formalization", " specialist"),
    ("specialist", " review"),
    ("specialist", " audit"),
    ("specialist", " sign", "-", "off"),
    ("external", " referee"),
    ("referee", " candidate"),
    ("peer", "-", "review", " release"),
    ("human", " gate"),
    ("reviewer", " gate"),
    ("needs", " human", " validation"),
]


def fail(message: str) -> None:
    raise SystemExit("PUBLIC-CORPUS|FAIL|" + message)


tracked = subprocess.run(
    ["git", "-C", str(ROOT), "ls-files", "-z"],
    check=True,
    stdout=subprocess.PIPE,
).stdout.split(b"\0")
for encoded in tracked:
    if not encoded:
        continue
    path = ROOT / encoded.decode()
    if path.suffix.lower() == ".pdf":
        continue
    try:
        text = path.read_text().lower()
    except (OSError, UnicodeDecodeError):
        continue
    for fragments in FRAGMENTS:
        if "".join(fragments) in text:
            fail(str(path.relative_to(ROOT)))

print("PUBLIC-CORPUS|PASS")
