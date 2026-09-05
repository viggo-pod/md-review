#!/usr/bin/env python3
"""Metadata probe: lines/words/est. tokens/heading outline/first-10-line preview/incomplete markers (Phase 0 review plan)."""

import re
import sys
from pathlib import Path

def read_text_safe(md_path):
    """Read a file, trying utf-8 first then common encodings; exit 2 on missing/binary."""
    p = Path(md_path)
    if not p.is_file():
        print(f"Error: file not found: {md_path}", file=sys.stderr)
        sys.exit(2)
    raw = p.read_bytes()
    if b"\x00" in raw:
        print(f"Error: binary file (contains NUL bytes): {md_path}", file=sys.stderr)
        sys.exit(2)
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    print(f"Error: cannot decode file: {md_path}", file=sys.stderr)
    sys.exit(2)

def probe(md_path):
    text = read_text_safe(md_path)
    lines = text.splitlines()
    tokens = len(text) // 4  # approx 4 chars = 1 token
    print("=== Document Metadata Probe ===")
    print(f"Document: {md_path}")
    print(f"Lines: {len(lines)} | Words: {len(text.split())} | Est. tokens: ~{tokens}")
    print()
    print("--- Heading outline (first 20) ---")
    # Fence-aware scan: lines inside ```/~~~ blocks are content, not headings
    heads = []
    in_fence = False
    fence_char, fence_len = "", 0
    for i, l in enumerate(lines):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", l)
        if m:
            marker, info = m.group(1), m.group(2).strip()
            if not in_fence:
                in_fence, fence_char, fence_len = True, marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len and not info:
                in_fence = False
            continue
        if not in_fence and re.match(r"^ {0,3}#{1,6}(\s|$)", l):
            heads.append((i + 1, l))
    for num, h in heads[:20]:
        print(f"  L{num}: {h}")
    if len(heads) > 20:
        print(f"  ... {len(heads)} headings total")
    print()
    print("--- First 10 lines ---")
    for l in lines[:10]:
        print("  " + l if l else "")
    print()
    todos = [l for l in lines if re.search(r"TODO|FIXME|TBD|WIP", l)]
    print(f"Incomplete markers (TODO/FIXME/TBD/WIP): {len(todos)}")
    for l in todos[:5]:
        print(f"  {l[:80]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 probe.py <markdown-file>")
        sys.exit(1)
    probe(sys.argv[1])
