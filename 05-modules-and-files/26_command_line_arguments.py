"""
Command-Line Arguments with argparse

Real Python programs are rarely run with zero configuration -- a script
that converts files, calls an API, or processes data usually needs to know
WHICH file, WHICH mode, or WHICH options to use, and that information
typically comes from the command line. `sys.argv` gives you the raw list
of arguments, but parsing it by hand (checking lengths, converting types,
writing your own --help text) gets tedious and error-prone fast. The
standard library's `argparse` module handles all of that for you: define
what arguments your program accepts, and it takes care of parsing,
type conversion, defaults, validation, and even an auto-generated --help
message.

This file covers:
- Why argparse beats parsing sys.argv by hand
- Positional arguments
- Optional arguments (--flag VALUE) and default values
- Type conversion and required options
- Boolean flags with action="store_true"
- Restricting values with choices, and writing helpful --help text
- Handling invalid input: argparse's built-in errors

To keep this file runnable non-interactively (like every other file in this
tutorial), each example calls `parser.parse_args([...])` with an explicit
list of arguments instead of reading the real command line -- exactly what
you'd pass on the command line, just written out in code so it's testable.
"""

import argparse
import sys

# ---------------------------------------------------------------------------
# 1. Why argparse beats parsing sys.argv by hand
# ---------------------------------------------------------------------------
# sys.argv is just a plain list of strings: sys.argv[0] is the script name,
# and everything after it is whatever the user typed. Handling optional
# flags, defaults, type conversion, and typos all by hand doesn't scale.
print("Example sys.argv for 'python resize.py photo.png --width 800':")
print("  ", ["resize.py", "photo.png", "--width", "800"])
print("argparse turns that list into a structured, validated object instead")
print("of raw strings you'd have to index and convert yourself.")

# ---------------------------------------------------------------------------
# 2. Positional arguments
# ---------------------------------------------------------------------------
# Positional arguments are required and matched by ORDER, not by name --
# similar to a function's required parameters.
parser = argparse.ArgumentParser(description="Resize an image file.")
parser.add_argument("filename", help="Path to the image file to resize")

args = parser.parse_args(["photo.png"])
print("\nPositional argument example:")
print("  args.filename:", args.filename)

# ---------------------------------------------------------------------------
# 3. Optional arguments (--flag VALUE) and default values
# ---------------------------------------------------------------------------
# Arguments starting with -- are optional and matched by NAME, so users can
# supply them in any order (or omit them and get the `default`).
parser = argparse.ArgumentParser(description="Resize an image file.")
parser.add_argument("filename", help="Path to the image file to resize")
parser.add_argument("--width", default=1024, type=int, help="Target width in pixels")
parser.add_argument("--height", default=768, type=int, help="Target height in pixels")

args = parser.parse_args(["photo.png", "--width", "800"])
print("\nOptional argument example (--width given, --height defaults):")
print("  filename:", args.filename, "| width:", args.width, "| height:", args.height)

# ---------------------------------------------------------------------------
# 4. Type conversion and required options
# ---------------------------------------------------------------------------
# `type=int` converts the raw string automatically (and argparse reports a
# clean error if conversion fails -- see section 7). `required=True` makes
# an otherwise-optional-looking --flag mandatory.
parser = argparse.ArgumentParser(description="Send a greeting N times.")
parser.add_argument("--name", required=True, help="Who to greet")
parser.add_argument("--times", type=int, default=1, help="How many times to greet")

args = parser.parse_args(["--name", "Ada", "--times", "3"])
print("\nType conversion example:")
print("  args.times is", args.times, "with type", type(args.times).__name__)
for _ in range(args.times):
    print(f"  Hello, {args.name}!")

# ---------------------------------------------------------------------------
# 5. Boolean flags with action="store_true"
# ---------------------------------------------------------------------------
# A flag with no value attached (like --verbose) uses action="store_true":
# its default is False, and simply INCLUDING the flag flips it to True.
parser = argparse.ArgumentParser(description="Copy a file.")
parser.add_argument("source")
parser.add_argument("destination")
parser.add_argument("--verbose", action="store_true", help="Print detailed progress")

args_quiet = parser.parse_args(["a.txt", "b.txt"])
args_loud = parser.parse_args(["a.txt", "b.txt", "--verbose"])
print("\nBoolean flag example:")
print("  without --verbose:", args_quiet.verbose)
print("  with --verbose:   ", args_loud.verbose)

# ---------------------------------------------------------------------------
# 6. Restricting values with choices, and --help text
# ---------------------------------------------------------------------------
# `choices` restricts an argument to a fixed set of valid values; argparse
# rejects anything else automatically (see section 7). `help=` text feeds
# into the auto-generated --help message.
parser = argparse.ArgumentParser(prog="loglevel-demo", description="Set a log level.")
parser.add_argument(
    "--level",
    choices=["debug", "info", "warning", "error"],
    default="info",
    help="Logging verbosity to use",
)

args = parser.parse_args(["--level", "warning"])
print("\nchoices example: args.level =", args.level)
print("\nAuto-generated --help text for this parser:")
parser.print_help()

# ---------------------------------------------------------------------------
# 7. Handling invalid input: argparse's built-in errors
# ---------------------------------------------------------------------------
# On invalid input (a bad choice, a missing required argument, a value that
# fails `type=`), argparse prints a usage message to stderr and calls
# sys.exit(2), which raises SystemExit. In a real CLI you'd let this
# propagate (it's the standard, expected behavior); here we catch it so the
# demo file itself keeps running.
try:
    parser.parse_args(["--level", "verbose"])  # not in choices=[...]
except SystemExit as e:
    print(f"\nInvalid --level was rejected by argparse (exit code {e.code}), as expected.")

parser2 = argparse.ArgumentParser(description="Send a greeting.")
parser2.add_argument("--name", required=True)
try:
    parser2.parse_args([])  # missing required --name
except SystemExit as e:
    print(f"Missing required --name was rejected by argparse (exit code {e.code}), as expected.")

# ---------------------------------------------------------------------------
# 8. What this looks like from a real terminal
# ---------------------------------------------------------------------------
# In a real script, you'd call parser.parse_args() with NO arguments, which
# reads directly from sys.argv[1:] -- everything the user typed after the
# script's name. That's the only line that changes between this demo file
# and production code.
print("\nIn a real script, you would write just:")
print("  args = parser.parse_args()   # reads sys.argv[1:] from the real terminal")
print("and run it like:")
print("  $ python loglevel_demo.py --level warning")

# Key takeaways:
# - argparse turns the raw sys.argv list into a validated, typed object,
#   handling parsing, defaults, and error messages for you.
# - Positional arguments are required and matched by order; optional
#   arguments (--flag) are matched by name and can have a `default`.
# - `type=` converts and validates values (e.g. type=int); `required=True`
#   makes an optional-looking flag mandatory; action="store_true" makes a
#   flag with no value a boolean switch.
# - `choices=[...]` restricts an argument to a fixed set of valid values,
#   and argparse auto-generates readable --help text from your definitions.
# - Invalid input makes argparse print a usage message and raise
#   SystemExit -- expected behavior for a real CLI, left uncaught in
#   production code so the program exits with a clear error.
