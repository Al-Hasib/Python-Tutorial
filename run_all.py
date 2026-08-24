"""
Smoke-test runner for the Python Tutorial curriculum.

Runs every topic file in the numbered phase folders (01-fundamentals ... 12-capstone)
as a subprocess, in order, and reports which ones succeeded or failed. Useful as a
quick regression check after editing any tutorial file.

Usage:
    python run_all.py
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 60


def find_topic_files():
    """Return every .py file inside numbered phase folders, in curriculum order."""
    phase_dirs = sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name[:2].isdigit() and "-" in d.name
    )
    files = []
    for phase_dir in phase_dirs:
        files.extend(sorted(phase_dir.glob("*.py")))
    return files


def run_file(path):
    """Run one file with the current interpreter; return (ok, elapsed_seconds, output_tail)."""
    start = time.perf_counter()
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(path.parent),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        elapsed = time.perf_counter() - start
        ok = result.returncode == 0
        tail = (result.stdout + result.stderr).strip().splitlines()[-8:]
        return ok, elapsed, tail
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        return False, elapsed, [f"TIMED OUT after {TIMEOUT_SECONDS}s"]


def main():
    files = find_topic_files()
    print(f"Discovered {len(files)} topic files.\n")

    passed = []
    failed = []

    for path in files:
        rel = path.relative_to(ROOT)
        ok, elapsed, tail = run_file(path)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {rel}  ({elapsed:.2f}s)")
        if ok:
            passed.append(rel)
        else:
            failed.append(rel)
            for line in tail:
                print(f"       {line}")

    print("\n" + "=" * 70)
    print(f"Summary: {len(passed)} passed, {len(failed)} failed, {len(files)} total")
    if failed:
        print("\nFailed files:")
        for rel in failed:
            print(f"  - {rel}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
