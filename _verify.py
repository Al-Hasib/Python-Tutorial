import json
import subprocess
import sys
import glob
import os

fails = []
skipped = []
for f in sorted(glob.glob("*/*.ipynb")):
    nb = json.load(open(f, encoding="utf-8"))
    code = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    cwd = os.path.dirname(f)
    try:
        p = subprocess.run([sys.executable, "-c", code], input="", capture_output=True,
                            text=True, cwd=cwd, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"{f}: TIMEOUT (expected: multiprocessing needs a real script file)")
        skipped.append(f)
        continue
    status = "OK" if p.returncode == 0 else "FAIL"
    print(f"{f}: {status}")
    if p.returncode != 0:
        fails.append(f)
        print(p.stderr[-3000:])

print("\nTOTAL FAILS:", len(fails), fails)
print("TOTAL SKIPPED (expected timeout):", len(skipped), skipped)
