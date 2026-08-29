"""
Raising Custom Exceptions
===========================

Sometimes the exceptions Python provides out of the box are not specific
enough to describe what went wrong in your own program's logic. Python lets
you deliberately trigger an exception with the `raise` keyword, and lets you
define brand new exception types by subclassing `Exception`. Custom
exceptions make error handling code more readable and let callers catch
exactly the failure they care about (for example `InsufficientFundsError`
instead of a generic `ValueError`). Knowing when to reach for a built-in
exception versus writing your own is a key part of designing clean,
maintainable APIs.

This file covers:
- The `raise` statement
- Raising built-in exceptions with a custom message
- Defining custom exception classes by subclassing `Exception`
- Adding custom attributes and messages to an exception
- Exception chaining with `raise ... from ...`
- Re-raising an exception (bare `raise` inside an except block)
- When to create a custom exception vs. reuse a built-in one
"""

# ---------------------------------------------------------------------------
# 1. The raise statement
# ---------------------------------------------------------------------------
# `raise` immediately triggers an exception. We wrap it in try/except here
# so the demo script keeps running to the end.
print("=== 1. The raise statement ===")

try:
    raise ValueError("something went wrong")
except ValueError as e:
    print(f"Caught a manually raised exception: {e}")

# ---------------------------------------------------------------------------
# 2. Raising built-in exceptions
# ---------------------------------------------------------------------------
print("\n=== 2. Raising built-in exceptions ===")


def set_age(age):
    """Validate age using a built-in exception, since this is a generic
    'bad value' situation with no special behavior of its own."""
    if not isinstance(age, int):
        raise TypeError(f"age must be an int, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"age cannot be negative, got {age}")
    return age


for candidate in (25, -5, "old"):
    try:
        print(f"set_age({candidate!r}) ->", set_age(candidate))
    except (TypeError, ValueError) as e:
        print(f"Rejected {candidate!r}: {type(e).__name__}: {e}")

# ---------------------------------------------------------------------------
# 3. Defining custom exception classes
# ---------------------------------------------------------------------------
print("\n=== 3. Defining custom exception classes ===")


class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available account balance."""
    pass


class InvalidAmountError(Exception):
    """Raised when a deposit or withdrawal amount is not valid (e.g. <= 0)."""
    pass


def withdraw(balance, amount):
    if amount <= 0:
        raise InvalidAmountError("withdrawal amount must be positive")
    if amount > balance:
        raise InsufficientFundsError("not enough funds to complete withdrawal")
    return balance - amount


for amount in (50, -10, 500):
    try:
        new_balance = withdraw(balance=100, amount=amount)
        print(f"Withdrew {amount}, new balance: {new_balance}")
    except InvalidAmountError as e:
        print(f"Invalid amount error: {e}")
    except InsufficientFundsError as e:
        print(f"Insufficient funds error: {e}")

# ---------------------------------------------------------------------------
# 4. Adding custom attributes and messages to an exception
# ---------------------------------------------------------------------------
print("\n=== 4. Custom attributes on exceptions ===")


class InsufficientFundsError(Exception):
    """Custom exception that carries extra data about the failed operation."""

    def __init__(self, balance, amount_requested):
        self.balance = balance
        self.amount_requested = amount_requested
        self.shortfall = amount_requested - balance
        message = (
            f"Cannot withdraw {amount_requested}: only {balance} available "
            f"(short by {self.shortfall})"
        )
        # Call the parent constructor so str(exception) works as expected.
        super().__init__(message)


def withdraw_v2(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


try:
    withdraw_v2(balance=100, amount=250)
except InsufficientFundsError as e:
    print("Message:", e)
    print("Custom attribute 'balance':", e.balance)
    print("Custom attribute 'amount_requested':", e.amount_requested)
    print("Custom attribute 'shortfall':", e.shortfall)

# ---------------------------------------------------------------------------
# 5. Exception chaining with raise ... from ...
# ---------------------------------------------------------------------------
print("\n=== 5. Exception chaining (raise ... from ...) ===")


class ConfigLoadError(Exception):
    """Raised when application configuration cannot be loaded."""
    pass


def load_config(raw_value):
    try:
        return int(raw_value)
    except ValueError as original_error:
        # `raise ... from original_error` preserves the original exception
        # as the "__cause__", so the traceback shows both errors and makes
        # debugging the real root cause much easier.
        raise ConfigLoadError(f"invalid config value: {raw_value!r}") from original_error


try:
    load_config("not_a_number")
except ConfigLoadError as e:
    print(f"Caught chained exception: {e}")
    print(f"Original cause: {type(e.__cause__).__name__}: {e.__cause__}")

# ---------------------------------------------------------------------------
# 6. Re-raising an exception
# ---------------------------------------------------------------------------
print("\n=== 6. Re-raising an exception ===")


def process_item(item):
    try:
        return 100 / item
    except ZeroDivisionError:
        print(f"Logging: failed to process item={item}, re-raising for caller.")
        # A bare `raise` inside an except block re-raises the SAME exception,
        # preserving its original traceback, after doing some local handling
        # (like logging) that the caller does not need to know about.
        raise


try:
    process_item(0)
except ZeroDivisionError:
    print("Outer handler received the re-raised ZeroDivisionError.")

# ---------------------------------------------------------------------------
# 7. When to create a custom exception vs use a built-in one
# ---------------------------------------------------------------------------
print("\n=== 7. Custom vs built-in exceptions ===")
print("Guideline: use a built-in exception when the problem is generic")
print("  (a bad type -> TypeError, a bad value -> ValueError, a missing key ->")
print("  KeyError). Create a custom exception when:")
print("  - The error represents a specific business rule (InsufficientFundsError)")
print("  - Callers need to catch YOUR error specifically, without accidentally")
print("    catching unrelated ValueErrors/TypeErrors from other code")
print("  - You want to attach extra structured data to the exception")
print("  - You want to group several related errors under one base class,")
print("    e.g. class AppError(Exception): pass, then subclass AppError.")


class AppError(Exception):
    """Base class for all custom errors raised by this application."""
    pass


class UserNotFoundError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass


for exc_class in (UserNotFoundError, PermissionDeniedError):
    try:
        raise exc_class("example failure")
    except AppError as e:
        # Catching the shared base class AppError catches every subclass.
        print(f"Caught {type(e).__name__} via base class AppError: {e}")

# Key takeaways:
# - `raise SomeException("message")` triggers an exception on demand.
# - Subclass `Exception` (usually with an `__init__` calling super().__init__())
#   to create custom exceptions that carry a clear name and extra attributes.
# - Use `raise NewError(...) from original_error` to chain exceptions and keep
#   the original root cause visible in the traceback.
# - A bare `raise` inside an except block re-raises the current exception
#   unchanged, useful after logging or partial cleanup.
# - Prefer built-in exceptions for generic problems; write custom exceptions
#   for domain-specific errors, extra data, or a shared base class for your app.
