import json

p = "08-intermediate/37_context_managers.ipynb"
nb = json.load(open(p, encoding="utf-8"))

target_snippet = 'demo_path = os.path.join(tempfile.gettempdir(), "context_managers_demo.txt")'

new_source_lines = [
    "import os\n",
    "import tempfile\n",
    "\n",
    "# A notebook has no __file__ to open, so create a small demo file instead --\n",
    "# the with-statement behavior being demonstrated is identical either way.\n",
    'demo_path = os.path.join(tempfile.gettempdir(), "context_managers_demo.txt")\n',
    'with open(demo_path, "w", encoding="utf-8") as f:\n',
    '    f.write("Hello from a temporary demo file.\\nSecond line.\\n")\n',
    "\n",
    'with open(demo_path, "r", encoding="utf-8") as f:\n',
    "    first_line = f.readline().strip()\n",
    'print("First line of the demo file, read via \'with\':", first_line)\n',
    'print("File closed automatically after the block?", f.closed)\n',
    "\n",
    "# Without `with`, you would need manual try/finally:\n",
    'f2 = open(demo_path, "r", encoding="utf-8")\n',
    "try:\n",
    "    _ = f2.readline()\n",
    "finally:\n",
    "    f2.close()\n",
    'print("Manual try/finally also closes the file:", f2.closed)\n',
]

count = 0
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    if target_snippet in src:
        c["source"] = new_source_lines
        count += 1

print("cells patched:", count)
with open(p, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

nb2 = json.load(open(p, encoding="utf-8"))
for c in nb2["cells"]:
    if c["cell_type"] == "code" and target_snippet in "".join(c["source"]):
        print("".join(c["source"]))
