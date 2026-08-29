import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

DIVIDER_RE = re.compile(r"^# -{10,}\s*$")
TITLE_RE = re.compile(r"^#\s*(\d+)\.\s*(.+)$")
DECORATIVE_RE = re.compile(r"^[=\-]{5,}$")


def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": text.splitlines(keepends=True)}


def strip_comment(line):
    stripped = line.rstrip("\n")
    if stripped.strip() == "#":
        return ""
    return re.sub(r"^\s*#\s?", "", stripped)


def split_comment_then_code(block):
    comment_lines = []
    j = 0
    while j < len(block) and (block[j].strip() == "" or block[j].lstrip().startswith("#")):
        comment_lines.append(block[j])
        j += 1
    while comment_lines and comment_lines[-1].strip() == "":
        comment_lines.pop()
    code_lines = block[j:]
    while code_lines and code_lines[0].strip() == "":
        code_lines.pop(0)
    while code_lines and code_lines[-1].strip() == "":
        code_lines.pop()
    return comment_lines, code_lines


def convert(py_path: Path):
    lines = py_path.read_text(encoding="utf-8").splitlines(keepends=True)

    assert lines[0].strip() == '"""', f"{py_path} does not start with a docstring"
    close_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == '"""')
    doc_lines = [l.rstrip("\n") for l in lines[1:close_idx]]
    non_empty = [i for i, l in enumerate(doc_lines) if l.strip()]
    title_line = doc_lines[non_empty[0]]
    body = doc_lines[non_empty[0] + 1:]
    body = [l for l in body if not DECORATIVE_RE.match(l.strip())]
    intro_md = f"# {title_line}\n\n" + "\n".join(body)

    cells = [md_cell(intro_md)]

    rest = lines[close_idx + 1:]
    while rest and rest[0].strip() == "":
        rest = rest[1:]

    divider_idxs = [i for i, l in enumerate(rest) if DIVIDER_RE.match(l.rstrip("\n"))]

    section_starts = []
    i = 0
    while i < len(divider_idxs) - 1:
        d1, d2 = divider_idxs[i], divider_idxs[i + 1]
        if d2 == d1 + 2 and TITLE_RE.match(rest[d1 + 1].rstrip("\n")):
            section_starts.append(d1)
            i += 2
        else:
            i += 1

    tail_start = len(rest)
    for i in range(len(rest) - 1, -1, -1):
        if rest[i].strip() == "" or rest[i].lstrip().startswith("#"):
            continue
        tail_start = i + 1
        break
    while tail_start < len(rest) and rest[tail_start].strip() == "":
        tail_start += 1

    boundaries = section_starts + [tail_start]

    preamble_end = section_starts[0] if section_starts else tail_start
    preamble = rest[:preamble_end]
    pre_comment, pre_code = split_comment_then_code(preamble)
    if pre_code:
        explanation = "\n".join(strip_comment(l) for l in pre_comment).strip()
        md_text = "## Setup"
        if explanation:
            md_text += "\n\n" + explanation
        cells.append(md_cell(md_text))
        cells.append(code_cell("".join(pre_code).rstrip("\n") + "\n"))

    for idx, start in enumerate(section_starts):
        title = TITLE_RE.match(rest[start + 1].rstrip("\n")).group(0)
        title_text = re.sub(r"^#\s*", "", title)
        content_start = start + 3
        content_end = boundaries[idx + 1]
        block = rest[content_start:content_end]

        comment_lines, code_lines = split_comment_then_code(block)
        explanation = "\n".join(strip_comment(l) for l in comment_lines).strip()
        md_text = f"## {title_text}"
        if explanation:
            md_text += "\n\n" + explanation
        cells.append(md_cell(md_text))
        if code_lines:
            cells.append(code_cell("".join(code_lines).rstrip("\n") + "\n"))

    tail = rest[tail_start:]
    tail = [l for l in tail if l.lstrip().startswith("#")]
    if tail:
        tail_text = "\n".join(strip_comment(l) for l in tail).strip()
        cells.append(md_cell("## Key Takeaways\n\n" + tail_text))

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    out_path = py_path.with_suffix(".ipynb")
    out_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)}  ({len(cells)} cells)")


for rel in sys.argv[1:]:
    convert(ROOT / rel)
