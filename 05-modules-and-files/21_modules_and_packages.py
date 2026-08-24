"""
Modules & Packages
-------------------
A module is simply a file containing Python code (functions, classes,
variables) that can be imported and reused in other files. Packages are
directories of modules that share a common namespace, marked (in the
classic model) by an `__init__.py` file. Understanding modules and
packages is fundamental because almost all real Python code is split
across multiple files, and knowing how `import` works, how Python finds
modules, and how to inspect them helps you organize and debug programs.

This file covers:
- What a module is and the different ways to import one
- `import module`, `from module import name`, `import module as alias`
- How you would structure your own module (explained via comments)
- The `__name__ == "__main__"` idiom, explained with an example
- Packages and the role of `__init__.py`
- The module search path (`sys.path`)
- Using `dir()` to inspect a module
"""

import sys
import math          # a module from the standard library
import os as operating_system   # import ... as alias
from math import sqrt, pi       # from module import name(s)

# ---------------------------------------------------------------------------
# 1. What is a module?
# ---------------------------------------------------------------------------
# Any .py file is a module. When you write "import math", Python looks for
# a file named math (built into the interpreter here) and makes its
# contents available under the name "math".
print("math module object:", math)
print("math.pi via module.attribute:", math.pi)

# ---------------------------------------------------------------------------
# 2. import module
# ---------------------------------------------------------------------------
# This brings in the whole module; you access its contents with dot notation.
print("\n-- import module --")
print("Square root of 16 using math.sqrt:", math.sqrt(16))
print("Value of math.e:", math.e)

# ---------------------------------------------------------------------------
# 3. from module import name
# ---------------------------------------------------------------------------
# This copies specific names into the current namespace, so you can use
# them directly without the module prefix. Useful for frequently used
# names, but can cause name clashes if overused.
print("\n-- from module import name --")
print("sqrt(25) (imported directly):", sqrt(25))
print("pi (imported directly):", pi)

# ---------------------------------------------------------------------------
# 4. import module as alias
# ---------------------------------------------------------------------------
# Giving a module a shorter or clearer local name. Common for long names
# or to avoid clashing with a name already in use (e.g. "os" here).
print("\n-- import module as alias --")
print("Current working directory via alias 'operating_system':",
      operating_system.getcwd())

# ---------------------------------------------------------------------------
# 5. Creating your own module (conceptual - explained via comments)
# ---------------------------------------------------------------------------
# Since this is a single file, we cannot literally split code into two
# files here. But this is how you would do it in a real project:
#
#   File: geometry_utils.py
#   -------------------------------------------------
#   def area_of_circle(radius):
#       return math.pi * radius ** 2
#
#   def area_of_square(side):
#       return side ** 2
#   -------------------------------------------------
#
#   File: main.py (in the same directory)
#   -------------------------------------------------
#   import geometry_utils
#
#   print(geometry_utils.area_of_circle(3))
#   -------------------------------------------------
#
# Below we simulate this idea with a local function, pretending it lives
# in its own "geometry_utils" module:


def area_of_circle(radius):
    """Pretend this function lives in its own module file."""
    return math.pi * radius ** 2


print("\n-- 'own module' simulation --")
print("area_of_circle(3):", round(area_of_circle(3), 2))

# ---------------------------------------------------------------------------
# 6. __name__ == "__main__" explained
# ---------------------------------------------------------------------------
# Every module has a built-in variable called __name__.
# - When a file is run directly (e.g. "python this_file.py"), Python sets
#   __name__ to "__main__" for that file.
# - When a file is imported by another module, __name__ is set to the
#   module's own name (e.g. "geometry_utils") instead.
#
# This lets a file provide reusable functions AND runnable "demo" code,
# without the demo code running automatically when the file is imported
# elsewhere. Example pattern (as it would appear in geometry_utils.py):
#
#   def area_of_circle(radius):
#       return math.pi * radius ** 2
#
#   if __name__ == "__main__":
#       # This block only runs when geometry_utils.py is executed directly,
#       # NOT when another file does "import geometry_utils".
#       print(area_of_circle(5))
#
print("\n-- __name__ demonstration --")
print("__name__ in this running script is:", __name__)
if __name__ == "__main__":
    print("This script is being run directly, not imported.")
else:
    print("This script has been imported as a module.")

# ---------------------------------------------------------------------------
# 7. Packages and __init__.py (explained in comments)
# ---------------------------------------------------------------------------
# A package is a directory containing multiple module files plus a special
# file named __init__.py. The __init__.py file (which can be empty) tells
# Python "treat this directory as an importable package". It can also run
# initialization code or define what gets exposed when the package is
# imported.
#
# Example package layout:
#
#   my_package/
#       __init__.py          <- makes this directory a package
#       shapes.py            <- a module inside the package
#       colors.py            <- another module inside the package
#
# From outside the package, you could then write:
#
#   import my_package.shapes
#   from my_package import colors
#   from my_package.shapes import area_of_circle
#
# In modern Python (3.3+), "namespace packages" can work without an
# __init__.py, but including one explicitly is still common practice
# because it makes the package's intent clear and allows you to control
# imports (e.g. defining __all__ inside __init__.py).
print("\n-- Packages --")
print("(See comments above for package/__init__.py structure explanation)")

# ---------------------------------------------------------------------------
# 8. The module search path (sys.path)
# ---------------------------------------------------------------------------
# When you "import something", Python searches directories listed in
# sys.path, in order, until it finds a matching module or package.
# sys.path typically includes: the script's directory, PYTHONPATH entries,
# and the standard library / site-packages locations.
print("\n-- sys.path (module search path) --")
print("Number of search path entries:", len(sys.path))
print("First 3 search path entries:")
for entry in sys.path[:3]:
    print("  ", entry if entry else "(current directory)")

# ---------------------------------------------------------------------------
# 9. The dir() function to inspect a module
# ---------------------------------------------------------------------------
# dir() lists the names (functions, classes, variables) defined inside a
# module. Very handy for exploring an unfamiliar module interactively.
print("\n-- dir() on the math module --")
math_names = dir(math)
print("Total names in math module:", len(math_names))
print("A few of them:", math_names[:10])

print("\n-- dir() on this module itself --")
this_module_names = [name for name in dir() if not name.startswith("__")]
print("User-defined names so far:", this_module_names)

# Key takeaways:
# - A module is just a .py file; import it with import, from-import, or
#   import-as to reuse its code elsewhere.
# - __name__ == "__main__" lets a file act as both a reusable module and a
#   standalone runnable script without the demo code firing on import.
# - Packages are directories of modules, traditionally marked by
#   __init__.py, allowing dotted imports like package.module.
# - sys.path controls where Python looks for modules; the current script's
#   directory is usually searched first.
# - dir() is a quick way to inspect what names a module (or the current
#   scope) actually defines.
