"""
Virtual Environments & Dependency Management

A virtual environment is an isolated, self-contained Python installation
(really just a directory) that has its own site-packages, separate from
your system-wide Python and from every other project on your machine.
Without isolation, every project you write would have to share one global
set of installed packages, which quickly leads to version conflicts: project
A needs requests==2.20 while project B needs requests==2.31, and installing
one breaks the other. Virtual environments solve this by giving each
project its own private set of dependencies, so you can install, upgrade,
or remove packages in one project without affecting any other. This file
explains the standard workflow with `venv` and `pip`, contrasts it with the
newer Poetry tool, and includes runnable code that inspects the interpreter
you are actually running in right now.

This file covers:
- What a virtual environment is and why isolation matters
- Creating one with `python -m venv venv`
- Activating it on Windows vs macOS/Linux
- Installing packages with `pip install`
- Freezing and restoring dependencies with `pip freeze` and `requirements.txt`
- A brief comparison with Poetry (pyproject.toml-based dependency management)
- Detecting programmatically whether you are inside a virtual environment
"""

import sys
import os


# ---------------------------------------------------------------------------
# 1. What a virtual environment is, and why isolation matters
# ---------------------------------------------------------------------------
# A virtual environment is a lightweight, disposable copy of the Python
# interpreter plus its own "site-packages" directory for installed
# libraries. It does NOT copy the whole standard library; instead it links
# back to the base Python install for that, but keeps installed third-party
# packages private to itself.
#
# Why this matters:
# - Different projects often need different (and incompatible) versions of
#   the same library.
# - Installing packages system-wide can require admin/root privileges and
#   risks breaking tools the operating system itself depends on.
# - A virtual environment can simply be deleted and recreated if it gets
#   into a broken state, with zero risk to anything else on the machine.
# - It makes your project's dependencies explicit and reproducible for
#   other developers (or your future self).


# ---------------------------------------------------------------------------
# 2. Creating a virtual environment: python -m venv venv
# ---------------------------------------------------------------------------
# From your project's root directory, run:
#
#     $ python -m venv venv
#
# This creates a "venv" folder containing:
#   venv/
#     Scripts/   (Windows)   or   bin/   (macOS/Linux)
#     Lib/ (or lib/)   -- where installed packages live
#     pyvenv.cfg       -- records which base Python built this env
#
# You can name the folder anything (".venv" is also a common convention),
# but "venv" or ".venv" are the most widely recognized names and are
# typically added to .gitignore since they should never be committed.


# ---------------------------------------------------------------------------
# 3. Activating the virtual environment
# ---------------------------------------------------------------------------
# Activation adjusts your shell's PATH so that "python" and "pip" resolve
# to the versions inside venv/ instead of the system ones. The command
# differs by platform and shell:
#
# Windows (Command Prompt):
#     > venv\Scripts\activate.bat
#
# Windows (PowerShell):
#     > venv\Scripts\Activate.ps1
#     (If this errors with a script-execution policy message, you may need:
#      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)
#
# macOS / Linux (bash/zsh):
#     $ source venv/bin/activate
#
# Once activated, your shell prompt is usually prefixed with "(venv)" and
# `python`/`pip` point inside the environment. To leave the environment:
#
#     $ deactivate     (same command on every platform)


# ---------------------------------------------------------------------------
# 4. Installing packages with pip
# ---------------------------------------------------------------------------
# With the environment activated, install packages with:
#
#     $ pip install requests
#     $ pip install requests==2.31.0        # pin an exact version
#     $ pip install "requests>=2.20,<3.0"   # constrain a version range
#     $ pip install --upgrade requests      # upgrade an existing package
#     $ pip uninstall requests              # remove a package
#     $ pip list                            # see what is installed
#     $ pip show requests                   # details about one package


# ---------------------------------------------------------------------------
# 5. Freezing and restoring dependencies
# ---------------------------------------------------------------------------
# Once your project's dependencies are installed, capture the exact
# versions so anyone else (or a deployment server) can reproduce your
# environment exactly:
#
#     $ pip freeze > requirements.txt
#
# This writes lines like:
#     requests==2.31.0
#     certifi==2024.2.2
#
# Another developer (or a CI pipeline, or "future you" on a new machine)
# then recreates the same set of dependencies with:
#
#     $ python -m venv venv
#     $ source venv/bin/activate      (or venv\Scripts\activate on Windows)
#     $ pip install -r requirements.txt
#
# requirements.txt should be committed to version control; the venv/
# folder itself should NOT be (it is large, platform-specific, and fully
# reproducible from requirements.txt).


# ---------------------------------------------------------------------------
# 6. A brief comparison with Poetry
# ---------------------------------------------------------------------------
# Poetry is a popular third-party tool that manages dependencies AND
# packaging together, using a single "pyproject.toml" file instead of
# requirements.txt. Rough comparison:
#
#   venv + pip                          Poetry
#   -----------------------------       -----------------------------
#   python -m venv venv                 poetry init  (creates pyproject.toml)
#   pip install requests                poetry add requests
#   pip freeze > requirements.txt       poetry.lock (generated automatically)
#   pip install -r requirements.txt     poetry install
#   source venv/bin/activate            poetry shell / poetry run <cmd>
#
# Key differences:
# - Poetry generates a "lock file" (poetry.lock) that pins the FULL
#   dependency tree (including transitive dependencies) with hashes, for
#   fully reproducible installs -- pip's requirements.txt can do this too,
#   but it is not automatic the way Poetry's lock file is.
# - Poetry combines dependency management with packaging metadata (project
#   name, version, authors) in one pyproject.toml file, whereas the
#   venv/pip workflow typically spreads this across requirements.txt and
#   a separate setup.py/pyproject.toml (see file 52 for packaging details).
# - venv + pip ships with Python and needs no extra install; Poetry must be
#   installed separately (e.g. via pipx) before you can use it.


# ---------------------------------------------------------------------------
# 7. Runnable check: are we inside a virtual environment right now?
# ---------------------------------------------------------------------------
# When a virtual environment is active, sys.prefix points inside the venv
# folder, while sys.base_prefix (or sys.real_prefix for the older
# "virtualenv" tool) points at the original, system-wide Python
# installation. If they differ, we are inside a virtual environment.

def in_virtual_env():
    """Return True if the running interpreter is inside a virtual env."""
    base_prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None)
    return base_prefix is not None and base_prefix != sys.prefix


def describe_environment():
    print("Python executable :", sys.executable)
    print("Python version    :", sys.version.split()[0])
    print("sys.prefix        :", sys.prefix)
    print("sys.base_prefix   :", getattr(sys, "base_prefix", "(not set)"))

    if in_virtual_env():
        print("Result            : Running INSIDE a virtual environment.")
    else:
        print("Result            : Running with the SYSTEM (base) Python.")

    # Another common signal: the VIRTUAL_ENV environment variable is set by
    # the activate script.
    venv_env_var = os.environ.get("VIRTUAL_ENV")
    if venv_env_var:
        print("VIRTUAL_ENV var   :", venv_env_var)
    else:
        print("VIRTUAL_ENV var   : not set")


if __name__ == "__main__":
    describe_environment()


# Key takeaways:
# - A virtual environment isolates a project's installed packages so
#   different projects can depend on different, even conflicting, versions.
# - Create one with `python -m venv venv`, activate it (activate.bat/
#   Activate.ps1 on Windows, `source bin/activate` on macOS/Linux), then use
#   `pip install` as usual.
# - `pip freeze > requirements.txt` captures exact installed versions;
#   `pip install -r requirements.txt` restores them elsewhere.
# - Poetry offers a more integrated, pyproject.toml-based alternative with
#   automatic lock files, at the cost of an extra tool to install.
# - Comparing sys.prefix to sys.base_prefix (or checking the VIRTUAL_ENV
#   environment variable) lets code detect programmatically whether it is
#   running inside a virtual environment.
