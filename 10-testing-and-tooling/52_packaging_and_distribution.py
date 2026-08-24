"""
Packaging & Distributing Python Projects

Packaging is the process of turning a folder of Python source files into an
installable, shareable artifact -- something other people (or your future
projects) can install with `pip install your-package` instead of copying
files by hand. The modern Python ecosystem has standardized on
`pyproject.toml` as the single configuration file that describes a
project's metadata, dependencies, and build instructions, replacing the
older setup.py-based approach. Understanding packaging matters even for
small projects because it forces you to think about project layout,
versioning, and dependency declaration in a way that makes your code
reusable and shareable. This file explains the pyproject.toml-based
workflow end to end -- layout, metadata, building, and publishing -- and
includes runnable code that generates and inspects an example
pyproject.toml.

This file covers:
- The modern pyproject.toml-based packaging approach
- Project layout conventions (the "src/" layout)
- Writing a minimal example pyproject.toml (generated and printed here)
- Building distributions with `python -m build` (explained, not executed)
- Publishing with `twine upload` (explained, not executed)
- Versioning basics (semantic versioning)
- __init__.py and __version__
"""


# ---------------------------------------------------------------------------
# 1. The modern pyproject.toml-based approach
# ---------------------------------------------------------------------------
# Historically, Python packages were configured with a setup.py script that
# executed arbitrary Python code to describe the package -- powerful, but
# error-prone and inconsistent between projects. PEP 517/518/621
# standardized a declarative alternative: a single "pyproject.toml" file at
# the project root, written in TOML, that:
#   - declares which build backend to use (e.g. setuptools, hatchling, flit)
#   - declares project metadata (name, version, description, dependencies)
#   - replaces setup.py, setup.cfg, and requirements.txt for most projects
#
# A build backend (setuptools, hatchling, poetry-core, flit-core, etc.)
# reads pyproject.toml and knows how to turn the source tree into an
# installable package. You choose a backend once, in the [build-system]
# table, and never call it directly -- tools like `build` and `pip` do.


# ---------------------------------------------------------------------------
# 2. Project layout conventions: the "src/" layout
# ---------------------------------------------------------------------------
# A recommended modern layout puts your actual package code inside a "src/"
# directory, separate from tests, docs, and config files:
#
#     my_project/
#       pyproject.toml
#       README.md
#       LICENSE
#       src/
#         my_package/
#           __init__.py
#           core.py
#           utils.py
#       tests/
#         test_core.py
#
# Why "src/" instead of putting my_package/ directly at the project root?
# - It prevents accidentally importing the package from the source
#   checkout instead of the installed version (a common source of "works
#   on my machine" bugs), because the src/ folder is not on sys.path by
#   default -- only the properly installed package is importable.
# - It forces you to test against the package as it will actually be
#   installed by users, catching packaging mistakes early.
#
# A simpler "flat" layout (package folder directly at the project root,
# without src/) is also common for small/simple projects and works fine;
# src/ is a convention adopted more as projects grow.


# ---------------------------------------------------------------------------
# 3. A minimal example pyproject.toml (generated and printed below)
# ---------------------------------------------------------------------------
# This is real, runnable code: we build the file's contents as a string
# and print it, without touching the actual filesystem, so the example is
# concrete but this script has no side effects outside itself.

EXAMPLE_PYPROJECT_TOML = """\
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "example-package"
version = "0.1.0"
description = "A minimal example package for the packaging tutorial."
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Ada Example", email = "ada@example.com"}
]
dependencies = [
    "requests>=2.28,<3.0",
]

[project.urls]
Homepage = "https://example.com/example-package"

[project.optional-dependencies]
dev = ["pytest", "black", "ruff", "mypy"]
"""


def print_example_pyproject():
    print("--- Example pyproject.toml ---")
    print(EXAMPLE_PYPROJECT_TOML)


# ---------------------------------------------------------------------------
# 4. Building distributions: python -m build
# ---------------------------------------------------------------------------
# Once pyproject.toml (and the src/ package) exist, you build two standard
# distribution artifacts using the `build` package (pip install build):
#
#     $ pip install build
#     $ python -m build
#
# This produces a "dist/" folder containing:
#   - a source distribution (sdist):   example_package-0.1.0.tar.gz
#       Contains your raw source files; pip can build a wheel from this
#       on the installing machine if needed.
#   - a built distribution (wheel):    example_package-0.1.0-py3-none-any.whl
#       A pre-built, ready-to-install format; pip prefers wheels because
#       they install faster and do not require running any build steps.
#
# `python -m build` is described here but not executed, since it requires
# installing the third-party "build" package.


# ---------------------------------------------------------------------------
# 5. Publishing with twine upload
# ---------------------------------------------------------------------------
# twine is the standard tool for uploading built distributions to PyPI (the
# Python Package Index) or a private package index:
#
#     $ pip install twine
#     $ twine upload dist/*
#
# You will be prompted for PyPI credentials (or an API token, which is the
# recommended approach over a password). It is good practice to first
# upload to TestPyPI to verify everything works before publishing for real:
#
#     $ twine upload --repository testpypi dist/*
#
# Once uploaded, anyone can install your package with:
#
#     $ pip install example-package
#
# twine is explained here only, and is not executed, for the same reason as
# `build` above -- this tutorial file must run with the standard library
# alone.


# ---------------------------------------------------------------------------
# 6. Versioning basics: semantic versioning
# ---------------------------------------------------------------------------
# Semantic Versioning (SemVer) uses a three-part version number:
#
#     MAJOR.MINOR.PATCH     e.g. 2.4.1
#
#   - MAJOR: incremented for incompatible/breaking API changes
#   - MINOR: incremented for new, backwards-compatible functionality
#   - PATCH: incremented for backwards-compatible bug fixes
#
# Examples:
#   1.0.0 -> 1.0.1   bug fix, no new features, fully compatible
#   1.0.1 -> 1.1.0   new feature added, old code still works
#   1.1.0 -> 2.0.0   breaking change; old code may need updating
#
# Versions before 1.0.0 (e.g. 0.x.y) are conventionally considered
# unstable/in-development, where even minor version bumps may break things.

def next_patch_version(version_string):
    """Given 'MAJOR.MINOR.PATCH', return the next patch version as a string."""
    major, minor, patch = (int(part) for part in version_string.split("."))
    return f"{major}.{minor}.{patch + 1}"


def next_minor_version(version_string):
    """Given 'MAJOR.MINOR.PATCH', return the next minor version (patch reset to 0)."""
    major, minor, _patch = (int(part) for part in version_string.split("."))
    return f"{major}.{minor + 1}.0"


# ---------------------------------------------------------------------------
# 7. __init__.py and __version__
# ---------------------------------------------------------------------------
# __init__.py marks a directory as a regular Python package (so
# `import my_package` works) and is a natural place to expose a package's
# public API and its version number:
#
#     # src/my_package/__init__.py
#     from .core import do_something
#
#     __version__ = "0.1.0"
#
# Exposing __version__ lets both humans and tools check a package's
# version at runtime, e.g.:
#
#     import my_package
#     print(my_package.__version__)
#
# Many projects keep the version in exactly one place (either
# pyproject.toml or __init__.py) and use a small tool or script to keep the
# other in sync, to avoid the two ever disagreeing.


if __name__ == "__main__":
    print_example_pyproject()

    print("--- Semantic versioning helpers ---")
    current_version = "1.4.2"
    print(f"current version       : {current_version}")
    print(f"next patch version    : {next_patch_version(current_version)}")
    print(f"next minor version    : {next_minor_version(current_version)}")

    print("\n--- Simulated package metadata (as __init__.py might expose) ---")
    simulated_package_version = "0.1.0"
    print(f"my_package.__version__ -> {simulated_package_version!r}")


# Key takeaways:
# - pyproject.toml is the modern, declarative way to describe a package's
#   build system, metadata, and dependencies, replacing setup.py for most
#   projects.
# - The "src/" layout separates package code from tests/config and forces
#   testing against the installed package rather than the source checkout.
# - `python -m build` produces a source distribution (sdist) and a wheel in
#   dist/; `twine upload dist/*` publishes them to PyPI.
# - Semantic versioning (MAJOR.MINOR.PATCH) communicates the nature of each
#   release: breaking changes, new features, or bug fixes respectively.
# - __init__.py marks a package and is a natural place to expose a public
#   API and a __version__ string for runtime introspection.
