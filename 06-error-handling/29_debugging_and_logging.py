"""
Debugging Techniques & Logging
=================================

Writing code that sometimes fails is unavoidable, so knowing how to find out
WHY it failed is just as important as handling the failure itself. Beginners
usually start by sprinkling `print()` statements everywhere, which works for
tiny scripts but quickly becomes messy and has to be deleted before shipping.
Python's `assert` statement, the `traceback` module, and real debuggers give
more structured ways to inspect what is happening. For anything beyond a
throwaway script, the `logging` module is the professional replacement for
print debugging: it can be turned on/off, filtered by severity, timestamped,
and routed to files or external systems without touching the code that
produces the messages.

This file covers:
- Using print() for quick debugging, and its limitations
- Using assert to check assumptions
- Reading and understanding a traceback
- The traceback module for capturing error details programmatically
- A conceptual intro to debuggers (pdb.set_trace() / breakpoint())
- The logging module: basicConfig, log levels, and logging to the console
- Why logging is preferred over print() in real projects
"""

import traceback
import logging

# ---------------------------------------------------------------------------
# 1. Using print() for quick debugging (and its limits)
# ---------------------------------------------------------------------------
print("=== 1. print() debugging ===")


def calculate_discounted_price(price, discount_percent):
    print(f"DEBUG: price={price}, discount_percent={discount_percent}")  # ad-hoc debug line
    discounted = price - (price * discount_percent / 100)
    print(f"DEBUG: discounted={discounted}")
    return discounted


calculate_discounted_price(200, 15)

print("Limits of print() debugging:")
print("  - Clutters output and must be manually removed before shipping")
print("  - No severity levels: cannot easily silence 'noisy' debug prints")
print("  - No timestamps, no filtering, no consistent formatting")
print("  - Cannot easily redirect output to a file or monitoring system")

# ---------------------------------------------------------------------------
# 2. Using assert
# ---------------------------------------------------------------------------
print("\n=== 2. Using assert ===")

# `assert condition, message` raises AssertionError if condition is False.
# Asserts are meant to catch programmer errors / broken assumptions during
# development; they should not be used for validating untrusted user input,
# because assertions can be stripped out when Python runs with `-O`.


def average(numbers):
    assert len(numbers) > 0, "numbers list must not be empty"
    return sum(numbers) / len(numbers)


print("average([1, 2, 3]) =", average([1, 2, 3]))

try:
    average([])
except AssertionError as e:
    print(f"AssertionError caught: {e}")

# ---------------------------------------------------------------------------
# 3. Reading tracebacks
# ---------------------------------------------------------------------------
print("\n=== 3. Reading tracebacks ===")

# A traceback shows the chain of function calls that led to an exception,
# most recent call last, ending with the exception type and message.
# Example of what an uncaught traceback looks like (shown as text here,
# since we catch it to keep this script running):
#
#   Traceback (most recent call last):
#     File "example.py", line 10, in <module>
#       result = divide(5, 0)
#     File "example.py", line 6, in divide
#       return a / b
#   ZeroDivisionError: division by zero
#
# Read it from the BOTTOM up: the last line tells you the exception type and
# message; the lines above show the call stack, i.e. which function called
# which, all the way back to where execution started.


def divide(a, b):
    return a / b


try:
    divide(5, 0)
except ZeroDivisionError:
    print("See the comment block above for how to read a real traceback.")
    print("The key: read bottom-up. Last line = error. Lines above = call stack.")

# ---------------------------------------------------------------------------
# 4. The traceback module
# ---------------------------------------------------------------------------
print("\n=== 4. The traceback module ===")

# The traceback module lets you capture/format traceback information
# programmatically, which is very useful for logging errors in detail.
try:
    divide(10, 0)
except ZeroDivisionError:
    print("traceback.format_exc() output:")
    formatted = traceback.format_exc()
    print(formatted)

    print("traceback.print_exc() writes directly to stderr:")
    traceback.print_exc()

# ---------------------------------------------------------------------------
# 5. Debuggers: pdb.set_trace() / breakpoint() (conceptual)
# ---------------------------------------------------------------------------
print("\n=== 5. Debuggers (conceptual intro) ===")

# A debugger lets you pause a running program at a specific line and inspect
# variables interactively, step line-by-line, and even change values on the
# fly. In real (non-automated) development you would add a line like:
#
#     import pdb; pdb.set_trace()
#
# or, in Python 3.7+, simply:
#
#     breakpoint()
#
# right before the suspicious code. When the program reaches that line, it
# drops you into an interactive prompt where you can type commands such as:
#   n (next line), s (step into a function), c (continue), p variable_name
#   (print a variable), l (list source code around current line), q (quit)
#
# We do NOT call breakpoint() in this file because it would pause execution
# and wait for keyboard input, which would hang this demo script.
print("breakpoint() / pdb.set_trace() would pause execution here in real use.")
print("Not invoked in this demo because it would halt the script waiting for input.")

# ---------------------------------------------------------------------------
# 6. The logging module: basicConfig and log levels
# ---------------------------------------------------------------------------
print("\n=== 6. The logging module ===")

# Configure logging to print to the console with a useful format.
# Levels in increasing order of severity:
#   DEBUG    - detailed diagnostic information, useful only during development
#   INFO     - confirmation that things are working as expected
#   WARNING  - something unexpected happened, but the program still works
#   ERROR    - a more serious problem; some functionality failed
#   CRITICAL - a very serious error; the program itself may be unable to continue
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("tutorial.error_handling")

logger.debug("This is a DEBUG message: detailed info for developers.")
logger.info("This is an INFO message: normal operation confirmation.")
logger.warning("This is a WARNING message: something looks off.")
logger.error("This is an ERROR message: an operation failed.")
logger.critical("This is a CRITICAL message: the whole system may be at risk.")

# ---------------------------------------------------------------------------
# 7. Logging exceptions with context
# ---------------------------------------------------------------------------
print("\n=== 7. Logging exceptions with context ===")

try:
    divide(1, 0)
except ZeroDivisionError:
    # logger.exception() automatically includes the traceback in the log
    # output, at ERROR level, which is extremely useful for debugging
    # problems that happen in production.
    logger.exception("Division failed while processing request")

# ---------------------------------------------------------------------------
# 8. Why logging is better than print() for real projects
# ---------------------------------------------------------------------------
print("\n=== 8. Why logging beats print() ===")
print("Reasons to prefer logging over print() in real projects:")
print("  - Severity levels let you filter messages (e.g. hide DEBUG in production)")
print("  - Built-in timestamps and source information (module, line, etc.)")
print("  - Output can be routed to console, files, or remote log servers")
print("    without changing a single logger.info(...) call in your code")
print("  - Different parts of an app can have their own logger with its own")
print("    level, so you can silence noisy modules independently")
print("  - logger.exception() captures full traceback automatically")

# Key takeaways:
# - print() is fine for quick, throwaway debugging but does not scale to
#   real projects: no levels, no filtering, no timestamps, must be removed.
# - assert checks internal assumptions during development and raises
#   AssertionError when a condition is False; it is not for validating
#   untrusted input since asserts can be disabled with `python -O`.
# - Read tracebacks from the bottom up: the last line is the error, the
#   lines above are the call stack that led to it.
# - The traceback module (format_exc, print_exc) lets you capture and log
#   full error details programmatically instead of just printing to screen.
# - The logging module (with basicConfig and levels DEBUG/INFO/WARNING/
#   ERROR/CRITICAL) is the professional replacement for print debugging in
#   any real application.
