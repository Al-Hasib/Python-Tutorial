"""
Code Style & Linting

Code style is the set of conventions that make Python code readable and
consistent across a team or project; PEP 8 is the official style guide for
the standard library and the de facto standard for the entire Python
ecosystem. Following a consistent style matters because code is read far
more often than it is written, and a shared style removes an entire class
of pointless debates (tabs vs spaces, camelCase vs snake_case) so reviews
can focus on logic instead of formatting. Tools exist to enforce style
automatically: formatters like `black` rewrite your code to a consistent
style, while linters like `flake8` and `ruff` scan for style violations,
unused imports, and common bugs without changing your files. This file
walks through PEP 8's core rules, shows real before/after code, and
explains where formatters, linters, and type checkers each fit in.

This file covers:
- PEP 8 essentials: naming, line length, whitespace, imports
- Docstring conventions
- `black`, the auto-formatter (explained, not executed)
- `flake8` and `ruff`, the linters (explained, not executed)
- Runnable BEFORE/AFTER examples of restyling messy code
- Type checking with `mypy` and how it complements style tools
"""


# ---------------------------------------------------------------------------
# 1. PEP 8 essentials: naming conventions
# ---------------------------------------------------------------------------
# - snake_case for functions, methods, and variables:   total_price, get_user()
# - PascalCase (CapWords) for classes:                  UserAccount, HttpClient
# - UPPER_SNAKE_CASE for module-level constants:         MAX_RETRIES, PI = 3.14159
# - Leading underscore for "internal use" names:         _cache, _helper()
# - Double leading underscore triggers name mangling in
#   classes (rarely needed):                             __private_attr
# - Avoid single-character names except in short loops
#   or well-known math contexts (i, j, x, y are fine in
#   a tight `for i in range(n)` loop, but not for a
#   variable that lives for 50 lines).

MAX_RETRIES = 3          # module-level constant: UPPER_SNAKE_CASE


class UserAccount:       # class: PascalCase
    def __init__(self, display_name):
        self.display_name = display_name   # attribute: snake_case

    def get_greeting(self):                 # method: snake_case
        return f"Hello, {self.display_name}!"


def calculate_total_price(unit_price, quantity):   # function: snake_case
    return unit_price * quantity


# ---------------------------------------------------------------------------
# 2. PEP 8 essentials: line length, whitespace, imports
# ---------------------------------------------------------------------------
# - Limit lines to 79 characters (PEP 8's classic rule); many modern teams
#   relax this to 88 (black's default) or 100, but pick one limit and use
#   it consistently across the project.
# - Use 4 spaces per indentation level; never mix tabs and spaces.
# - Exactly one blank line between methods inside a class, two blank lines
#   between top-level functions/classes (as seen between the sections in
#   this very file).
# - No trailing whitespace at the end of a line.
# - Space after commas, around binary operators, but NOT immediately
#   inside parentheses/brackets:
#       good:  func(a, b, c)      total = a + b
#       bad:   func(a,b,c)        total=a+b
# - Imports go at the top of the file, one per line, grouped in this
#   order with a blank line between groups:
#       1. standard library imports   (os, sys, json)
#       2. third-party imports         (requests, numpy)
#       3. local/project imports       (from mypackage import thing)
#
# Example import block (illustrative only -- not all of these exist here):
#     import os
#     import sys
#
#     import requests
#
#     from mypackage.utils import helper


# ---------------------------------------------------------------------------
# 3. Docstring conventions
# ---------------------------------------------------------------------------
# - Every public module, class, and function should have a docstring.
# - Use triple double-quotes """like this""" even for one-liners.
# - One-line docstrings: summary only, on one line, imperative mood
#   ("Return the sum", not "Returns the sum" or "This returns the sum").
# - Multi-line docstrings: a one-line summary, a blank line, then further
#   detail (parameters, return value, exceptions raised).

def divide(a, b):
    """Return a divided by b.

    Args:
        a: The numerator.
        b: The denominator; must not be zero.

    Returns:
        The quotient a / b as a float.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    return a / b


# ---------------------------------------------------------------------------
# 4. black: the auto-formatter
# ---------------------------------------------------------------------------
# black is a third-party tool (pip install black) that reformats your code
# to a single, consistent, largely non-configurable style. The philosophy
# is "stop debating style; let the tool decide." It rewrites spacing,
# quote style, line breaks, and trailing commas automatically.
#
#     $ pip install black
#     $ black my_script.py          # reformat a file in place
#     $ black .                     # reformat an entire project
#     $ black --check .             # exit non-zero if files would change
#                                    # (useful in CI, does not modify files)
#
# black is NOT run here -- this file only describes it, since the exercise
# must not depend on packages that may not be installed.


# ---------------------------------------------------------------------------
# 5. flake8 and ruff: the linters
# ---------------------------------------------------------------------------
# A linter analyzes source code WITHOUT running or reformatting it, to spot
# style violations, unused variables/imports, undefined names, and other
# likely bugs.
#
# flake8 (pip install flake8) combines pyflakes (logical errors like
# unused imports) with pycodestyle (PEP 8 style checks):
#
#     $ pip install flake8
#     $ flake8 my_script.py
#     $ flake8 .                    # lint an entire project
#
# Typical flake8 output looks like:
#     my_script.py:12:1: F401 'os' imported but unused
#     my_script.py:20:80: E501 line too long (95 > 79 characters)
#
# ruff (pip install ruff) is a newer linter (and increasingly a formatter
# too) written in Rust. It re-implements the rules of flake8 and dozens of
# its plugins, running 10-100x faster, and has become the popular default
# for new projects:
#
#     $ pip install ruff
#     $ ruff check .                # lint
#     $ ruff format .                # ruff can also format, similar to black
#
# Neither flake8 nor ruff is executed in this file, for the same reason as
# black above.


# ---------------------------------------------------------------------------
# 6. BEFORE / AFTER: restyling a messy snippet
# ---------------------------------------------------------------------------
# Below is a deliberately poorly-styled snippet (kept as a string so it is
# never executed as real code -- it violates several PEP 8 rules on
# purpose), followed by a PEP-8-compliant rewrite that IS real, runnable
# code.

BEFORE_SNIPPET = '''
import os,sys
def CalcTotal(a,b ,c):
    x=a+b+c
    if(x>100):
        return   True
    else:
        return False
class userinfo:
    def __init__(self,Name,Age):
        self.Name=Name
        self.Age=Age
'''

print("--- BEFORE (poorly styled, shown as text, not executed) ---")
print(BEFORE_SNIPPET)

# Problems in BEFORE_SNIPPET:
# - "import os,sys" -- multiple imports on one line (should be one per line)
# - "CalcTotal" -- function name in PascalCase (should be snake_case)
# - "def CalcTotal(a,b ,c):" -- missing space after commas, stray space before one
# - "x=a+b+c" -- no spaces around operators
# - "if(x>100):" -- unnecessary parentheses, no spaces around >
# - "return   True" -- multiple spaces instead of one
# - "class userinfo:" -- class name in lowercase (should be PascalCase)
# - "self.Name=Name" -- attribute name capitalized (should be snake_case),
#   no spaces around =


def calc_total(a, b, c):
    """Return the sum of three numbers, flagged as large if over 100."""
    total = a + b + c
    if total > 100:
        return True
    else:
        return False


class UserInfo:
    """Simple container for a user's name and age."""

    def __init__(self, name, age):
        self.name = name
        self.age = age


print("\n--- AFTER (PEP 8 compliant, real runnable code) ---")
print("calc_total(10, 20, 30) ->", calc_total(10, 20, 30))
print("calc_total(50, 60, 70) ->", calc_total(50, 60, 70))
user = UserInfo("Ada", 30)
print(f"UserInfo -> name={user.name!r}, age={user.age}")


# ---------------------------------------------------------------------------
# 7. Type checking with mypy: a complementary tool
# ---------------------------------------------------------------------------
# Style tools (black, flake8, ruff) check FORMATTING and simple correctness
# issues, but they do not verify that your types are used consistently.
# mypy (pip install mypy) reads optional type hints (PEP 484) and reports
# type mismatches statically, before you ever run the code:
#
#     def add(a: int, b: int) -> int:
#         return a + b
#
#     add("2", "3")   # mypy would flag this as a type error, even though
#                      # Python itself would run it without complaint if
#                      # both were strings being concatenated instead
#
#     $ pip install mypy
#     $ mypy my_script.py
#
# In a modern workflow the three tool categories are complementary and
# often all run in CI:
#   - formatter  (black / ruff format) -> enforces consistent LAYOUT
#   - linter     (flake8 / ruff check) -> catches style + likely bugs
#   - type checker (mypy)              -> catches type inconsistencies


# Key takeaways:
# - PEP 8 defines naming (snake_case/PascalCase/UPPER_SNAKE_CASE), 79-char
#   lines, consistent whitespace, and a standard import ordering.
# - Docstrings should have a one-line summary (imperative mood), with
#   optional extended detail for parameters, return values, and exceptions.
# - `black` auto-formats code to a consistent style; `flake8` and `ruff`
#   lint code for style violations and likely bugs without changing files.
# - `mypy` adds a fourth, complementary layer: static type checking based
#   on type hints, catching a different class of bugs than style tools.
# - None of these tools were executed here -- only stdlib code runs in this
#   file, with the tools explained via comments and example commands.
