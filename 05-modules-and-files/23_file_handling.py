"""
File Handling
--------------
Reading and writing files is one of the most common tasks in real
programs - configuration files, logs, reports, and data all live on
disk. Python provides the built-in `open()` function for this, along
with several read/write modes, and the `with` statement to guarantee
files are closed properly even if an error occurs. This file also
introduces `pathlib.Path`, the modern, object-oriented way to work with
filesystem paths. Understanding these tools is essential before moving
on to structured formats like CSV and JSON.

This file covers:
- Opening files with `open()` and modes ('r', 'w', 'a', 'x', 'b')
- Reading: `read()`, `readline()`, `readlines()`, iterating a file object
- Writing to files
- The `with` statement / context manager and why it beats manual `close()`
- Checking existence with `os.path.exists`
- Working with paths via `pathlib.Path`
"""

import os
from pathlib import Path

# All demo files are created inside a "sample_files" folder next to this
# script, and removed again at the end so re-running this file is safe
# and nothing is left behind in the repository.
BASE_DIR = Path(__file__).parent
SAMPLE_DIR = BASE_DIR / "sample_files"
SAMPLE_DIR.mkdir(exist_ok=True)

text_file = SAMPLE_DIR / "notes.txt"
binary_file = SAMPLE_DIR / "data.bin"

# ---------------------------------------------------------------------------
# 1. Writing a file with open() and mode 'w'
# ---------------------------------------------------------------------------
# Mode 'w' creates the file if it does not exist, and OVERWRITES it if it
# does. We use the "with" statement (a context manager), which
# automatically closes the file for us when the block ends - even if an
# exception happens inside the block. This is preferred over manually
# calling file.close(), because a manual close() can be skipped entirely
# if an error is raised before that line runs.
print("-- Writing with mode 'w' --")
with open(text_file, "w") as f:
    f.write("Line one: hello file handling\n")
    f.write("Line two: Python makes this easy\n")
print("Wrote initial content to:", text_file)
print("Is file closed right after the 'with' block?", f.closed)

# ---------------------------------------------------------------------------
# 2. Appending with mode 'a'
# ---------------------------------------------------------------------------
# Mode 'a' opens the file for appending; new writes are added to the end
# without erasing existing content. The file is created if missing.
print("\n-- Appending with mode 'a' --")
with open(text_file, "a") as f:
    f.write("Line three: appended afterwards\n")
print("Appended a line to:", text_file)

# ---------------------------------------------------------------------------
# 3. Reading a whole file with read()
# ---------------------------------------------------------------------------
print("\n-- Reading with read() --")
with open(text_file, "r") as f:
    whole_content = f.read()
print("Entire file content:")
print(whole_content)

# ---------------------------------------------------------------------------
# 4. Reading one line at a time with readline()
# ---------------------------------------------------------------------------
print("-- Reading with readline() --")
with open(text_file, "r") as f:
    first_line = f.readline()
    second_line = f.readline()
print("First line:", repr(first_line))
print("Second line:", repr(second_line))

# ---------------------------------------------------------------------------
# 5. Reading all lines into a list with readlines()
# ---------------------------------------------------------------------------
print("\n-- Reading with readlines() --")
with open(text_file, "r") as f:
    all_lines = f.readlines()
print("All lines as a list:", all_lines)
print("Number of lines:", len(all_lines))

# ---------------------------------------------------------------------------
# 6. Iterating over a file object directly
# ---------------------------------------------------------------------------
# A file object is itself iterable, yielding one line at a time. This is
# the most memory-efficient way to process large files, since it does not
# load the whole file into memory at once like readlines() does.
print("\n-- Iterating over the file object --")
with open(text_file, "r") as f:
    for line_number, line in enumerate(f, start=1):
        print(f"  Line {line_number}: {line.strip()}")

# ---------------------------------------------------------------------------
# 7. Mode 'x' - exclusive creation (fails if the file already exists)
# ---------------------------------------------------------------------------
print("\n-- Mode 'x' (exclusive creation) --")
exclusive_file = SAMPLE_DIR / "only_once.txt"
if exclusive_file.exists():
    exclusive_file.unlink()  # make sure it does not exist yet, for a clean demo

with open(exclusive_file, "x") as f:
    f.write("Created for the first time.\n")
print("Created exclusive file successfully.")

try:
    with open(exclusive_file, "x") as f:
        f.write("This will never be written.\n")
except FileExistsError as error:
    print("Trying to create it again raised FileExistsError:", error)

# ---------------------------------------------------------------------------
# 8. Binary mode ('b') for non-text data
# ---------------------------------------------------------------------------
# Adding "b" to a mode (e.g. "wb", "rb") reads/writes raw bytes instead of
# decoded text. Use this for images, audio, or any non-text data.
print("\n-- Binary mode 'wb' / 'rb' --")
with open(binary_file, "wb") as f:
    f.write(bytes([72, 101, 108, 108, 111]))  # bytes for "Hello"

with open(binary_file, "rb") as f:
    raw_bytes = f.read()
print("Raw bytes read back:", raw_bytes)
print("Decoded as text:", raw_bytes.decode("utf-8"))

# ---------------------------------------------------------------------------
# 9. Why "with" beats manual close()
# ---------------------------------------------------------------------------
# Manual style (avoid this):
#   f = open(text_file, "r")
#   content = f.read()
#   f.close()          # <- if read() raised an exception, this line is
#                          skipped and the file stays open/locked.
#
# "with" style (preferred):
#   with open(text_file, "r") as f:
#       content = f.read()
#   # file is guaranteed to be closed here, even on error.
print("\n-- with vs manual close() --")
print("'with' guarantees the file is closed even if an error occurs inside.")

# ---------------------------------------------------------------------------
# 10. Checking existence with os.path.exists
# ---------------------------------------------------------------------------
print("\n-- os.path.exists --")
print("Does notes.txt exist?", os.path.exists(text_file))
missing_file = SAMPLE_DIR / "does_not_exist.txt"
print("Does does_not_exist.txt exist?", os.path.exists(missing_file))

# ---------------------------------------------------------------------------
# 11. Working with paths via pathlib.Path
# ---------------------------------------------------------------------------
# pathlib.Path offers an object-oriented, cross-platform way to build and
# inspect paths, often clearer than string-based os.path operations.
print("\n-- pathlib.Path --")
print("Path object:", text_file)
print("File name:", text_file.name)
print("File suffix/extension:", text_file.suffix)
print("Parent directory:", text_file.parent)
print("Does it exist? (Path.exists())", text_file.exists())
print("Is it a file? (Path.is_file())", text_file.is_file())
print("Read via Path.read_text():", text_file.read_text()[:20], "...")

# Building a new path with the / operator, pathlib's signature feature.
new_path = SAMPLE_DIR / "subfolder" / "deep.txt"
print("Path built with '/' operator:", new_path)

# ---------------------------------------------------------------------------
# 12. Cleanup - remove everything this script created
# ---------------------------------------------------------------------------
print("\n-- Cleanup --")
for created_file in (text_file, binary_file, exclusive_file):
    if created_file.exists():
        created_file.unlink()
        print("Removed:", created_file.name)

if SAMPLE_DIR.exists() and not any(SAMPLE_DIR.iterdir()):
    SAMPLE_DIR.rmdir()
    print("Removed empty directory:", SAMPLE_DIR)

# Key takeaways:
# - open() takes a mode string: 'r' read, 'w' write (overwrite), 'a'
#   append, 'x' exclusive create, plus 'b' for binary variants of each.
# - read() loads the whole file, readline() loads one line, readlines()
#   loads all lines into a list; iterating the file object directly is
#   the most memory-efficient option for large files.
# - Always prefer "with open(...) as f:" over manual open()/close(),
#   because it guarantees the file closes even if an exception occurs.
# - os.path.exists() and pathlib.Path.exists() both check whether a path
#   exists; pathlib also offers a clean, object-oriented API (.name,
#   .suffix, .parent, the / operator) for building and inspecting paths.
