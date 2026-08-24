"""
Exceptions & Error Handling
============================

An exception is an event that occurs during program execution that disrupts
the normal flow of instructions. When Python encounters a problem it cannot
continue past (dividing by zero, accessing a missing key, opening a file
that does not exist, and so on) it "raises" an exception. If nothing handles
that exception, the program crashes and Python prints a traceback. Handling
exceptions lets a program detect these problems and respond gracefully
(retry, log, show a friendly message, clean up resources) instead of dying.
Mastering try/except is essential for writing robust, production-quality
Python code.

This file covers:
- What an exception is and what happens when one is not caught
- Basic try/except syntax
- Catching specific exception types
- Catching multiple exception types at once
- The exception object itself (the `as e` syntax)
- The `else` clause on a try statement
- The `finally` clause and exactly when it runs
- Catching a broad `except Exception`
- The exception hierarchy: BaseException -> Exception -> specific errors
- Common built-in exceptions: ValueError, TypeError, KeyError, IndexError,
  ZeroDivisionError, FileNotFoundError
"""

# ---------------------------------------------------------------------------
# 1. What is an exception?
# ---------------------------------------------------------------------------
# If we let an exception happen without catching it, Python stops execution
# of that code path and prints a traceback. We simulate that idea here by
# catching it ourselves so this demo file keeps running.
print("=== 1. What is an exception? ===")

try:
    result = 10 / 0  # ZeroDivisionError: dividing by zero is not allowed
except ZeroDivisionError:
    print("Caught an exception: you cannot divide by zero!")

# ---------------------------------------------------------------------------
# 2. Basic try/except
# ---------------------------------------------------------------------------
print("\n=== 2. Basic try/except ===")

try:
    number = int("not a number")  # this will raise ValueError
    print("This line never runs because the line above failed.")
except ValueError:
    print("Could not convert the text to an integer.")

# ---------------------------------------------------------------------------
# 3. Catching specific exception types
# ---------------------------------------------------------------------------
print("\n=== 3. Catching specific exception types ===")

data = {"name": "Alice"}
try:
    print(data["age"])  # "age" key does not exist -> KeyError
except KeyError:
    print("The key 'age' does not exist in the dictionary.")

numbers = [1, 2, 3]
try:
    print(numbers[10])  # index out of range -> IndexError
except IndexError:
    print("That index is out of range for the list.")

# ---------------------------------------------------------------------------
# 4. Catching multiple exceptions
# ---------------------------------------------------------------------------
print("\n=== 4. Catching multiple exceptions ===")


def divide_and_convert(value, divisor):
    """Convert value to int and divide it, showing multi-exception handling."""
    try:
        converted = int(value)
        return converted / divisor
    except (ValueError, ZeroDivisionError) as error:
        # A tuple of exception types lets one except block handle several
        # different kinds of errors.
        print(f"Operation failed: {error}")
        return None


divide_and_convert("abc", 2)   # triggers ValueError
divide_and_convert("10", 0)    # triggers ZeroDivisionError
print("Successful case:", divide_and_convert("20", 4))

# ---------------------------------------------------------------------------
# 5. The exception object (as e)
# ---------------------------------------------------------------------------
print("\n=== 5. The exception object (as e) ===")

try:
    price = float("twenty")
except ValueError as e:
    # "e" holds the actual exception instance; str(e) gives the message.
    print("Exception type:", type(e).__name__)
    print("Exception message:", e)

# ---------------------------------------------------------------------------
# 6. The else clause on try
# ---------------------------------------------------------------------------
print("\n=== 6. The else clause on try ===")

# The `else` block runs only if the try block did NOT raise any exception.
try:
    total = 100 / 5
except ZeroDivisionError:
    print("Division failed.")
else:
    print(f"Division succeeded, result is {total}. 'else' runs only on success.")

try:
    total = 100 / 0
except ZeroDivisionError:
    print("Division failed, so 'else' is skipped this time.")
else:
    print("This will not print because an exception occurred.")

# ---------------------------------------------------------------------------
# 7. The finally clause and when it runs
# ---------------------------------------------------------------------------
print("\n=== 7. The finally clause ===")

# `finally` always runs, whether or not an exception occurred, and even if
# the exception was not caught. It is typically used for cleanup (closing
# files, releasing locks, disconnecting from a database).
try:
    print("Trying something risky...")
    value = 10 / 2
except ZeroDivisionError:
    print("This will not run, no error happened.")
finally:
    print("Finally block: this always runs (cleanup happens here).")

try:
    print("Trying something that will fail...")
    value = 10 / 0
except ZeroDivisionError:
    print("Caught the division error.")
finally:
    print("Finally block: still runs, error or not.")

# ---------------------------------------------------------------------------
# 8. Catching a bare `except Exception`
# ---------------------------------------------------------------------------
print("\n=== 8. Catching a broad except Exception ===")


def risky_operation(choice):
    if choice == 1:
        return 1 / 0
    elif choice == 2:
        return int("nope")
    elif choice == 3:
        return [1, 2][5]
    return "no error"


for choice in (1, 2, 3, 4):
    try:
        outcome = risky_operation(choice)
        print(f"choice={choice} succeeded with result: {outcome}")
    except Exception as e:
        # `except Exception` catches almost any error, regardless of type.
        # Useful as a safety net, but prefer specific exceptions when you
        # know what can go wrong, so you do not hide real bugs.
        print(f"choice={choice} failed with {type(e).__name__}: {e}")

# ---------------------------------------------------------------------------
# 9. The exception hierarchy
# ---------------------------------------------------------------------------
print("\n=== 9. Exception hierarchy ===")

# All exceptions inherit from BaseException.
# Almost all user-facing exceptions inherit from Exception (a subclass of
# BaseException). Things like SystemExit and KeyboardInterrupt inherit
# directly from BaseException, not Exception, so a plain `except Exception`
# will NOT catch a user pressing Ctrl+C or calling sys.exit().
print("ValueError is a subclass of Exception:", issubclass(ValueError, Exception))
print("Exception is a subclass of BaseException:", issubclass(Exception, BaseException))
print("KeyError is a subclass of LookupError:", issubclass(KeyError, LookupError))
print("IndexError is a subclass of LookupError:", issubclass(IndexError, LookupError))

# Catching a parent class also catches its children:
try:
    raise KeyError("missing")
except LookupError as e:
    # KeyError and IndexError both derive from LookupError.
    print(f"Caught via parent class LookupError: {type(e).__name__}")

# ---------------------------------------------------------------------------
# 10. Common built-in exceptions
# ---------------------------------------------------------------------------
print("\n=== 10. Common built-in exceptions ===")

examples = []

try:
    int("abc")
except ValueError as e:
    examples.append(("ValueError", e))

try:
    "2" + 2
except TypeError as e:
    examples.append(("TypeError", e))

try:
    {"a": 1}["b"]
except KeyError as e:
    examples.append(("KeyError", e))

try:
    [1, 2, 3][99]
except IndexError as e:
    examples.append(("IndexError", e))

try:
    1 / 0
except ZeroDivisionError as e:
    examples.append(("ZeroDivisionError", e))

try:
    open("this_file_does_not_exist.txt")
except FileNotFoundError as e:
    examples.append(("FileNotFoundError", e))

for name, err in examples:
    print(f"{name}: {err}")

# Key takeaways:
# - try/except catches exceptions so a program can recover instead of crashing.
# - Catch the most specific exception type you can (ValueError, KeyError, etc.)
#   rather than always using a broad `except Exception`.
# - `else` runs only when the try block succeeds; `finally` always runs, making
#   it ideal for cleanup code (closing files, releasing resources).
# - All exceptions descend from BaseException, and nearly all normal errors
#   descend from Exception; catching a parent class also catches its children.
# - Common built-ins to know: ValueError, TypeError, KeyError, IndexError,
#   ZeroDivisionError, and FileNotFoundError.
