"""
One-off converter: turns the numbered/commented .py tutorial files in this
repo into .ipynb notebooks, splitting each numbered section into a
markdown cell (explanation) + code cell (runnable example) pair.

Usage: python _py_to_ipynb.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

DIVIDER_RE = re.compile(r"^# -{10,}\s*$")
TITLE_RE = re.compile(r"^#\s*(\d+)\.\s*(.+)$")
DECORATIVE_RE = re.compile(r"^[=\-]{5,}$")


def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code_cell(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def strip_comment(line):
    stripped = line.rstrip("\n")
    if stripped.strip() == "#":
        return ""
    return re.sub(r"^\s*#\s?", "", stripped)


def split_comment_then_code(block):
    """Given a list of raw lines, split into (leading comment lines, code lines)."""
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


def dedent_lines(block, spaces=4):
    out = []
    for l in block:
        if l.startswith(" " * spaces):
            out.append(l[spaces:])
        elif l.strip() == "":
            out.append(l)
        else:
            out.append(l)  # already at col 0 (e.g. blank/short line)
    return out


def preprocess_45_multiprocessing(lines):
    """This file wraps ALL its numbered sections inside a top-level
    `if __name__ == "__main__":` guard, indented one level. Strip the guard
    and dedent so the normal column-0 section parser can see them."""
    guard_idx = next(i for i, l in enumerate(lines) if l.strip() == 'if __name__ == "__main__":')
    # find where the guarded block ends: first subsequent line that is
    # non-blank and NOT indented (that's the "# Key takeaways:" tail)
    end_idx = len(lines)
    for i in range(guard_idx + 1, len(lines)):
        if lines[i].strip() != "" and not lines[i].startswith(" "):
            end_idx = i
            break
    before = lines[:guard_idx]
    guarded = dedent_lines(lines[guard_idx + 1:end_idx])
    after = lines[end_idx:]
    return before + guarded + after


SPECIAL_PREPROCESS = {
    "45_multiprocessing.py": preprocess_45_multiprocessing,
}


def convert(py_path: Path, notebook_title: str):
    lines = py_path.read_text(encoding="utf-8").splitlines(keepends=True)

    # 1. Pull the module docstring.
    assert lines[0].strip() == '"""', f"{py_path} does not start with a docstring"
    close_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == '"""')
    doc_lines = [l.rstrip("\n") for l in lines[1:close_idx]]
    non_empty = [i for i, l in enumerate(doc_lines) if l.strip()]
    title_line = doc_lines[non_empty[0]]
    body = doc_lines[non_empty[0] + 1:]
    body = [l for l in body if not DECORATIVE_RE.match(l.strip())]
    intro_md = f"# {notebook_title}\n\n**{title_line}**\n\n" + "\n".join(body)

    cells = [md_cell(intro_md)]

    rest = lines[close_idx + 1:]
    while rest and rest[0].strip() == "":
        rest = rest[1:]

    special = SPECIAL_PREPROCESS.get(py_path.name)
    if special:
        rest = special(rest)
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

    # Detect the trailing "Key takeaways" comment block (walking back from EOF
    # over blank/comment-only lines).
    tail_start = len(rest)
    for i in range(len(rest) - 1, -1, -1):
        if rest[i].strip() == "" or rest[i].lstrip().startswith("#"):
            continue
        tail_start = i + 1
        break
    while tail_start < len(rest) and rest[tail_start].strip() == "":
        tail_start += 1

    boundaries = section_starts + [tail_start]

    # Preamble: any code before the first recognized section (imports, module-
    # level constants/helpers). Only relevant if there IS a first section
    # (otherwise there's nothing to be "before").
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
        content_end = boundaries[idx + 1] if idx + 1 < len(boundaries) else tail_start
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
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    out_path = py_path.with_suffix(".ipynb")
    out_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)}  ({len(cells)} cells)")


def title_from_filename(stem):
    # "07_conditional_statements" -> "Conditional Statements"
    name = re.sub(r"^\d+_", "", stem)
    return name.replace("_", " ").title()


def main():
    only = sys.argv[1:]  # optional list of relative paths to restrict to
    targets = sorted(ROOT.glob("*/*.py"))
    for py_path in targets:
        if py_path.name == "run_all.py" or py_path.name.startswith("_"):
            continue
        rel = str(py_path.relative_to(ROOT)).replace("\\", "/")
        if only and rel not in only and py_path.name not in only:
            continue
        # Use the first non-empty docstring line as the notebook title.
        text = py_path.read_text(encoding="utf-8").splitlines()
        title = None
        if text and text[0].strip() == '"""':
            for l in text[1:]:
                if l.strip():
                    title = l.strip()
                    break
        if not title:
            title = title_from_filename(py_path.stem)
        convert(py_path, title)


if __name__ == "__main__":
    main()
