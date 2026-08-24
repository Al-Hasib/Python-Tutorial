"""
Introduction to Python & Setup

Python is a high-level, interpreted, general-purpose programming language
known for its readable syntax and huge ecosystem of libraries. It is used
for web development, data science, automation, scripting, artificial
intelligence, and much more. Because Python code is interpreted rather
than compiled to a standalone binary, you need a Python interpreter
installed on your machine to run it. This file introduces what Python is,
how to run it in different ways, and how a script executes.

This file covers:
- What Python is and why it is popular
- Installing Python and checking the installed version
- Running code via the REPL, scripts, and IDEs
- The `python` vs `python3` command
- Inspecting version info with the `sys` and `platform` modules
- Writing and running a "Hello, World!" program
- How a .py file executes from top to bottom
- A brief introduction to `if __name__ == "__main__":`
"""

# ---------------------------------------------------------------------------
# 1. What is Python?
# ---------------------------------------------------------------------------
# Python is:
#   - High-level: you don't manage memory manually.
#   - Interpreted: code runs line by line via an interpreter (CPython is
#     the most common implementation).
#   - Dynamically typed: variable types are determined at runtime.
#   - Multi-paradigm: supports procedural, object-oriented, and functional
#     styles of programming.
print("Python is a high-level, interpreted, general-purpose language.")

# ---------------------------------------------------------------------------
# 2. Installing Python
# ---------------------------------------------------------------------------
# Python is installed from https://python.org (or via a package manager
# like apt, brew, or the Microsoft Store on Windows). Once installed, the
# interpreter is available from the command line. This script itself is
# proof that Python is installed and working, since it is being executed
# by a Python interpreter right now.
print("If you can see this message, Python is installed and working!")

# ---------------------------------------------------------------------------
# 3. Running Python: REPL vs Scripts vs IDEs
# ---------------------------------------------------------------------------
# There are three common ways to run Python code:
#   1. REPL (Read-Eval-Print Loop): type `python` in a terminal with no
#      arguments and you get an interactive prompt (>>>) where you can
#      type expressions and see results immediately. Great for quick tests.
#   2. Script: write code in a .py file and run it with `python file.py`.
#      This is how most real programs are executed (like this file).
#   3. IDEs/Editors: tools like VS Code, PyCharm, or Jupyter notebooks give
#      you an editor plus a way to run/debug scripts or cells, combining
#      the convenience of a REPL with the structure of a file.
print("This file is being run as a SCRIPT, not typed into the REPL.")

# ---------------------------------------------------------------------------
# 4. The `python` vs `python3` command
# ---------------------------------------------------------------------------
# On many systems, `python` refers to Python 2 (now unsupported/legacy) and
# `python3` refers to Python 3 (the modern, actively developed version).
# On Windows and in fresh installs, `python` usually already points to
# Python 3. Always check with `python --version` or `python3 --version`
# in your terminal to be sure which one you are using.
print("Use 'python --version' or 'python3 --version' in your terminal.")

# ---------------------------------------------------------------------------
# 5. Checking the version with sys and platform
# ---------------------------------------------------------------------------
import sys
import platform

print("sys.version:", sys.version)
print("sys.version_info:", sys.version_info)
print("Major version only:", sys.version_info.major)
print("platform.python_version():", platform.python_version())
print("platform.system():", platform.system())      # e.g. Windows, Linux, Darwin
print("platform.platform():", platform.platform())  # detailed platform string

# ---------------------------------------------------------------------------
# 6. Hello, World!
# ---------------------------------------------------------------------------
# The classic first program in any language: print a greeting to the screen.
print("Hello, World!")

# ---------------------------------------------------------------------------
# 7. How a .py file executes top to bottom
# ---------------------------------------------------------------------------
# Python reads and executes statements in order, from the top of the file
# to the bottom. There is no separate "main" function that is required to
# be called first (unlike languages such as C or Java). Watch the order of
# these prints -- they happen exactly in the order they appear in the file.
print("Step 1: this line runs first")
print("Step 2: this line runs second")
print("Step 3: this line runs third")

# ---------------------------------------------------------------------------
# 8. A brief look at __name__ == "__main__"
# ---------------------------------------------------------------------------
# Every Python module has a built-in variable called __name__. When a file
# is run directly (e.g. `python this_file.py`), Python sets __name__ to
# the string "__main__". When the same file is instead imported into
# another file, __name__ is set to the module's name instead. This lets
# you write code that only runs when the file is executed directly, not
# when it is imported elsewhere. We will use this pattern more in later
# files; for now, just see what __name__ equals when running this script.
print("__name__ is currently:", __name__)

if __name__ == "__main__":
    print("This file was run directly, so this line executes.")

# Key takeaways:
# - Python is a high-level, interpreted, dynamically typed language.
# - You can run Python via the REPL (interactive), as a script (.py file),
#   or inside an IDE/notebook.
# - `python3` (or `python` on many modern setups) starts the interpreter;
#   `sys` and `platform` let you inspect version and OS details in code.
# - A .py script executes its statements strictly from top to bottom.
# - `__name__ == "__main__"` tells you whether a file was run directly
#   rather than imported -- a pattern you'll see throughout this tutorial.
