#!/usr/bin/env python3
"""诊断 PDF 文本结构"""
import re
from pathlib import Path

with open("d:/pyworkplace/github/learning-open-source/pdf_all.txt", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")

url_lines = [(i, l) for i, l in enumerate(lines) if "clawhub.ai" in l]

out = []
out.append(f"含URL的行: {len(url_lines)}\n")

for idx, (i, l) in enumerate(url_lines[:15]):
    out.append(f"--- 记录 {idx+1} (line {i}) ---")
    for j in range(max(0, i-6), min(len(lines), i+3)):
        prefix = ">>>" if j == i else "   "
        out.append(f"{prefix} [{j:4d}] {lines[j]}")
    out.append("")

with open("d:/pyworkplace/github/learning-open-source/scripts/debug_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("done")
