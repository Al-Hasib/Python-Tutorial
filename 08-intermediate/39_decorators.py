"""
Decorators
==========

A decorator is a function that takes another function (or class) and
returns a modified or wrapped version of it, letting you add behavior
without changing the original function's source code. This works because
Python treats functions as first-class citizens: they can be stored in
variables, passed as arguments, and returned from other functions, just
like any other value. Decorators are used everywhere in real Python code
-- logging, timing, caching, access control, retries -- because they let
you separate "what a function does" from "what extra behavior wraps
around it". The `@decorator` syntax is just a convenient shorthand for
reassigning a function to its decorated version.

This file covers:
- Functions as first-class citizens (recap)
- Writing a simple decorator
- *args / **kwargs in decorators
- Preserving metadata with functools.wraps
- Decorators with arguments (decorator factories)
- Stacking multiple decorators
- Practical examples: timing, logging, retry
"""

import functools
import time
import random

# ---------------------------------------------------------------------------
# 1. Functions as first-class citizens (recap)
# ---------------------------------------------------------------------------
# Functions can be assigned to variables, passed as arguments, and returned
# from other functions -- this is what makes decorators possible.

def greet(name):
    return f"Hello, {name}!"


def call_twice(func, argument):
    return func(argument) + " " + func(argument)


say_hi = greet  # assign a function to another name
print(say_hi("Ada"))
print(call_twice(greet, "Grace"))  # pass a function as an argument


def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier  # return a function from a function


times3 = make_multiplier(3)
print("times3(7) =", times3(7))

# ---------------------------------------------------------------------------
# 2. Writing a simple decorator
# ---------------------------------------------------------------------------
# A decorator wraps a function in another function, returning the wrapper.

def shout(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper


@shout
def greeting():
    return "hello there"


print("\n@shout decorated greeting():", greeting())

# The @ syntax is exactly equivalent to this manual reassignment:
def greeting_plain():
    return "hello again"


greeting_plain = shout(greeting_plain)
print("Manually decorated:", greeting_plain())

# ---------------------------------------------------------------------------
# 3. *args / **kwargs in decorators
# ---------------------------------------------------------------------------
# Real functions take varied arguments, so decorators use *args/**kwargs to
# forward whatever was passed in, no matter the original signature.

def announce(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper


@announce
def add(a, b, label="sum"):
    return a + b


print("\nCalling decorated add(3, 4, label='total'):")
add(3, 4, label="total")

# ---------------------------------------------------------------------------
# 4. Preserving metadata with functools.wraps
# ---------------------------------------------------------------------------
# Without functools.wraps, the wrapper hides the original function's name
# and docstring, which breaks introspection, help(), and debugging tools.

def logged_no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def logged_with_wraps(func):
    @functools.wraps(func)  # copies __name__, __doc__, etc. from func
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@logged_no_wraps
def compute_a(x):
    """Compute something important (version A)."""
    return x * 2


@logged_with_wraps
def compute_b(x):
    """Compute something important (version B)."""
    return x * 2


print("\nWithout functools.wraps:")
print("  __name__ =", compute_a.__name__)
print("  __doc__  =", compute_a.__doc__)

print("With functools.wraps:")
print("  __name__ =", compute_b.__name__)
print("  __doc__  =", compute_b.__doc__)

# ---------------------------------------------------------------------------
# 5. Decorators with arguments (decorator factories)
# ---------------------------------------------------------------------------
# To give a decorator its own parameters, wrap it in one more layer: a
# factory function that takes the decorator's arguments and returns the
# actual decorator.

def repeat(times):
    """Decorator factory: repeat the decorated function's call `times` times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(times=3)
def roll_die():
    return random.randint(1, 6)


random.seed(42)  # deterministic output for the tutorial
print("\n@repeat(times=3) roll_die():", roll_die())

# ---------------------------------------------------------------------------
# 6. Stacking multiple decorators
# ---------------------------------------------------------------------------
# Decorators apply bottom-up: the one closest to the function runs first,
# and its result is passed into the next decorator up.

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper


def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"_{func(*args, **kwargs)}_"
    return wrapper


@bold
@italic
def render(text):
    return text


print("\nStacked @bold @italic render('hi'):", render("hi"))
# Order matters: swapping the stack order changes the output.

@italic
@bold
def render_swapped(text):
    return text


print("Swapped @italic @bold render_swapped('hi'):", render_swapped("hi"))

# ---------------------------------------------------------------------------
# 7. Practical example: timing a function
# ---------------------------------------------------------------------------
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timed] {func.__name__} took {elapsed:.6f} seconds")
        return result
    return wrapper


@timed
def sum_of_squares(n):
    return sum(i * i for i in range(n))


print("\nTiming example:")
print("sum_of_squares(1000) =", sum_of_squares(1000))

# ---------------------------------------------------------------------------
# 8. Practical example: simple logging decorator
# ---------------------------------------------------------------------------
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] calling {func.__name__}{args}")
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            print(f"[LOG] {func.__name__} raised {exc!r}")
            raise
        print(f"[LOG] {func.__name__} -> {result!r}")
        return result
    return wrapper


@log_calls
def divide(a, b):
    return a / b


print("\nLogging example:")
divide(10, 2)

# ---------------------------------------------------------------------------
# 9. Practical example: retry decorator
# ---------------------------------------------------------------------------
def retry(max_attempts=3):
    """Decorator factory that retries the wrapped function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as exc:
                    last_error = exc
                    print(f"[retry] attempt {attempt} failed: {exc}")
            raise last_error
        return wrapper
    return decorator


attempt_counter = {"count": 0}


@retry(max_attempts=3)
def flaky_operation():
    attempt_counter["count"] += 1
    if attempt_counter["count"] < 2:
        raise ValueError("temporary failure")
    return "success"


print("\nRetry example:")
print("flaky_operation() ->", flaky_operation())

# Key takeaways:
# - Decorators work because functions are first-class values: a decorator
#   simply takes a function and returns a (usually wrapped) function.
# - Use *args/**kwargs in the wrapper so the decorator works with any
#   function signature, and always apply functools.wraps to keep the
#   original name/docstring for debugging and introspection.
# - A "decorator factory" (a function returning a decorator) is how you give
#   a decorator its own configurable arguments, e.g. @retry(max_attempts=3).
# - Stacked decorators apply bottom-up, closest to the function first, and
#   the order can change the final behavior.
# - Common real-world uses include timing, logging, caching, access control,
#   and retry logic -- all without touching the original function's code.
