#!/usr/bin/env python3
"""Reject internal process-status artifacts from tracked public text."""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRAGMENTS = [
    ("re", "view-protocol.md"),
    ("re", "view protocol"),
    ("re", "view gate"),
    ("re", "view sign-off"),
    ("re", "view status table"),
    ("re", "view", "er"),
    ("ref", "eree"),
    ("pe", "er re", "view"),
    ("pe", "er-re", "view"),
    ("human", " re", "view"),
    ("human", "-re", "view"),
    ("human", " validation"),
    ("human", " check"),
    ("human", " sign-off"),
    ("special", "ist re", "view"),
    ("special", "ist audit"),
    ("special", "ist check"),
    ("special", "ist sign-off"),
    ("special", "ist approval"),
    ("expert", " re", "view"),
    ("expert", " sign-off"),
    ("manual", " re", "view"),
    ("manual", " sign-off"),
    ("two", "-reader"),
    ("two", "-specialist"),
    ("pending", " re", "view"),
    ("not yet", " assigned"),
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
