import json
import glob
import re

pattern = re.compile(r"^# (.+)\n\n\*\*(.+)\*\*\n\n", re.MULTILINE)

fixed = 0
for f in sorted(glob.glob("*/*.ipynb")):
    nb = json.load(open(f, encoding="utf-8"))
    cell = nb["cells"][0]
    assert cell["cell_type"] == "markdown"
    src = "".join(cell["source"])
    m = pattern.match(src)
    if not m:
        print("NO MATCH:", f, repr(src[:120]))
        continue
    title, bold = m.group(1), m.group(2)
    if title != bold:
        print("TITLE MISMATCH (kept as-is):", f, title, "|", bold)
        continue
    new_src = f"# {title}\n\n" + src[m.end():]
    cell["source"] = new_src.splitlines(keepends=True)
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(nb, fh, indent=1, ensure_ascii=False)
    fixed += 1

print("fixed:", fixed)
