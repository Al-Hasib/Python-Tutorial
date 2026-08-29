"""
Context Managers
================

The `with` statement is Python's way of guaranteeing that setup and cleanup
code runs around a block, even if that block raises an exception -- think
of opening/closing files, acquiring/releasing locks, or starting/stopping a
timer. Under the hood, `with` relies on the "context manager protocol":
an object with `__enter__` and `__exit__` methods. You can implement this
protocol yourself with a class, or more concisely with the `contextlib`
module's `@contextmanager` decorator and a generator function. Context
managers make resource-management code shorter, safer, and much harder to
get wrong than manual try/finally blocks scattered everywhere.

This file covers:
- The with statement recap
- What happens under the hood (__enter__ / __exit__)
- Writing a custom context manager class
- Writing one with contextlib.contextmanager and yield
- Handling exceptions inside __exit__
- Practical examples: timing a block, temporarily changing state,
  suppressing exceptions with contextlib.suppress
"""

import contextlib
import time

# ---------------------------------------------------------------------------
# 1. The with statement -- recap
# ---------------------------------------------------------------------------
# The classic example is file handling: `with` guarantees the file is closed
# even if an error happens while reading it.

with open(__file__, "r", encoding="utf-8") as f:
    first_line = f.readline().strip()
print("First line of this file, read via 'with':", first_line)
print("File closed automatically after the block?", f.closed)

# Without `with`, you would need manual try/finally:
f2 = open(__file__, "r", encoding="utf-8")
try:
    _ = f2.readline()
finally:
    f2.close()
print("Manual try/finally also closes the file:", f2.closed)

# ---------------------------------------------------------------------------
# 2. What happens under the hood: __enter__ / __exit__
# ---------------------------------------------------------------------------
# `with EXPR as VAR:` roughly translates to:
#   mgr = EXPR
#   VAR = mgr.__enter__()
#   try:
#       BODY
#   finally:
#       mgr.__exit__(exc_type, exc_value, traceback)

class Announcer:
    def __enter__(self):
        print("  __enter__ called")
        return self  # this becomes the value bound by 'as'

    def __exit__(self, exc_type, exc_value, traceback):
        print("  __exit__ called with", exc_type, exc_value)
        return False  # False/None means: don't suppress exceptions


print("\nManually tracing the protocol:")
with Announcer() as a:
    print("  inside the with-block, a =", a)

# ---------------------------------------------------------------------------
# 3. Writing a custom context manager class
# ---------------------------------------------------------------------------
class ManagedResource:
    """A toy 'resource' that reports when it is acquired and released."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Acquiring resource: {self.name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Releasing resource: {self.name}")
        return False  # let any exception propagate normally

    def use(self):
        print(f"Using resource: {self.name}")


print("\nCustom context manager class:")
with ManagedResource("database-connection") as resource:
    resource.use()

# ---------------------------------------------------------------------------
# 4. Writing one with contextlib.contextmanager and yield
# ---------------------------------------------------------------------------
# @contextmanager turns a generator function into a context manager: code
# before `yield` is __enter__, code after `yield` is __exit__.

@contextlib.contextmanager
def managed_resource(name):
    print(f"[contextmanager] Acquiring resource: {name}")
    try:
        yield name  # this value is bound by 'as'
    finally:
        print(f"[contextmanager] Releasing resource: {name}")


print("\nContext manager built with contextlib.contextmanager:")
with managed_resource("cache-connection") as name:
    print("  using resource:", name)

# ---------------------------------------------------------------------------
# 5. Handling exceptions inside __exit__
# ---------------------------------------------------------------------------
# __exit__ receives (exc_type, exc_value, traceback) when the block raises.
# Returning True from __exit__ suppresses the exception; returning
# False/None lets it propagate.

class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ValueError:
            print(f"  Suppressing a ValueError: {exc_value}")
            return True  # swallow this specific exception
        return False  # let anything else propagate


print("\nSuppressing exceptions inside __exit__:")
with SuppressValueError():
    print("  about to raise ValueError")
    raise ValueError("something went wrong")
print("  execution continues after the with-block (exception was suppressed)")

# The @contextmanager version handles exceptions with try/except around yield.
@contextlib.contextmanager
def suppress_value_error():
    try:
        yield
    except ValueError as exc:
        print(f"  [contextmanager] Suppressing a ValueError: {exc}")


with suppress_value_error():
    raise ValueError("another problem")
print("  continued after the contextmanager-based suppressor too")

# ---------------------------------------------------------------------------
# 6. Practical example: timing a block
# ---------------------------------------------------------------------------
@contextlib.contextmanager
def timer(label):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[timer] {label} took {elapsed:.6f} seconds")


print("\nTiming a block of code:")
with timer("summing squares"):
    total = sum(i * i for i in range(10_000))
print("  total =", total)

# ---------------------------------------------------------------------------
# 7. Practical example: temporarily changing state
# ---------------------------------------------------------------------------
settings = {"debug": False}


@contextlib.contextmanager
def temporary_setting(key, value):
    """Temporarily set settings[key] = value, restoring it afterward."""
    original = settings.get(key)
    settings[key] = value
    try:
        yield
    finally:
        settings[key] = original


print("\nTemporarily changing state:")
print("  before:", settings)
with temporary_setting("debug", True):
    print("  inside with-block:", settings)
print("  after:", settings)

# ---------------------------------------------------------------------------
# 8. Practical example: contextlib.suppress
# ---------------------------------------------------------------------------
# contextlib.suppress(*exceptions) is a ready-made context manager that
# silently ignores the given exception types -- a tidy alternative to a
# bare try/except/pass.

print("\nUsing contextlib.suppress:")
data = {"a": 1}
with contextlib.suppress(KeyError):
    print("  value:", data["missing-key"])
print("  code continues normally even though the key was missing")

with contextlib.suppress(FileNotFoundError):
    open("this_file_does_not_exist.txt", "r")
print("  FileNotFoundError was suppressed too")

# Key takeaways:
# - `with` guarantees cleanup code runs via __exit__, even when the block
#   raises an exception -- it is a safer alternative to manual try/finally.
# - A class-based context manager implements __enter__ (setup, returns the
#   'as' value) and __exit__ (cleanup, receives exception info if any).
# - contextlib.contextmanager lets you write a context manager as a
#   generator function: code before yield is __enter__, code after (or in a
#   finally) is __exit__.
# - Returning True from __exit__ suppresses the exception; returning
#   False/None (or nothing) lets it propagate normally.
# - contextlib.suppress(...) is a quick built-in way to ignore specific
#   exception types without writing a custom context manager.
