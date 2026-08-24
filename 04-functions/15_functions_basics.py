"""
Functions Basics

A function is a named, reusable block of code that performs a specific task.
Instead of copy-pasting the same logic everywhere, you define it once with
`def` and call it whenever you need it. Functions take inputs (parameters),
optionally do some work, and can hand back a result using `return`. They are
one of the most important tools for organizing code, avoiding repetition, and
making programs easier to read, test, and maintain.

This file covers:
- Defining functions with `def` and calling them
- Parameters vs arguments
- The `return` statement, including returning multiple values via tuples
- Implicit `None` return when there is no explicit `return`
- Docstrings and inspecting them with `help()` / `__doc__`
- Why functions matter: DRY (Don't Repeat Yourself) and reuse
"""

# ---------------------------------------------------------------------------
# 1. Defining and calling functions with `def`
# ---------------------------------------------------------------------------

# The `def` keyword starts a function definition, followed by a name,
# parentheses (optionally containing parameters), and a colon.
def greet():
    print("Hello there!")


# Calling a function executes its body.
greet()
greet()  # can be called as many times as needed


# ---------------------------------------------------------------------------
# 2. Parameters vs arguments
# ---------------------------------------------------------------------------

# A "parameter" is the name listed in the function definition.
# An "argument" is the actual value passed in when calling the function.
def greet_person(name):  # `name` is a parameter
    print(f"Hello, {name}!")


greet_person("Alice")  # "Alice" is the argument
greet_person("Bob")


def add(a, b):  # `a` and `b` are parameters
    print(f"{a} + {b} = {a + b}")


add(3, 4)  # 3 and 4 are arguments


# ---------------------------------------------------------------------------
# 3. The `return` statement
# ---------------------------------------------------------------------------

# `return` sends a value back to the caller and immediately exits the
# function. Without `return`, a function just performs actions (side
# effects like printing) and gives nothing back to use later.
def square(number):
    return number * number


result = square(5)
print("Square of 5:", result)

# You can use the returned value directly in expressions.
print("Square of 6 plus 1:", square(6) + 1)


# ---------------------------------------------------------------------------
# 4. Returning multiple values via tuples
# ---------------------------------------------------------------------------

# When you "return" several comma-separated values, Python packs them into
# a tuple behind the scenes. You can unpack them into separate variables.
def min_max(numbers):
    return min(numbers), max(numbers)


smallest, largest = min_max([4, 1, 9, 2, 7])
print("Smallest:", smallest, "| Largest:", largest)

# You can also keep the tuple as-is if you don't want to unpack right away.
pair = min_max([10, -3, 8])
print("Tuple result:", pair, "-> type:", type(pair))


# ---------------------------------------------------------------------------
# 5. Implicit `None` return
# ---------------------------------------------------------------------------

# If a function has no `return` statement, or uses a bare `return` with no
# value, it implicitly returns `None`.
def log_message(message):
    print(f"[LOG] {message}")
    # no return statement here


outcome = log_message("System started")
print("Return value of log_message:", outcome)


def do_nothing_special(flag):
    if flag:
        return  # bare return -> None
    print("Flag was False")


print("Result when flag=True:", do_nothing_special(True))
print("Result when flag=False:", do_nothing_special(False))


# ---------------------------------------------------------------------------
# 6. Docstrings and help() / __doc__
# ---------------------------------------------------------------------------

# A docstring is a string literal placed as the first statement in a
# function body. It documents what the function does and shows up in
# help() and the function's __doc__ attribute.
def celsius_to_fahrenheit(celsius):
    """Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        The equivalent temperature in degrees Fahrenheit.
    """
    return celsius * 9 / 5 + 32


print("\n25C in Fahrenheit:", celsius_to_fahrenheit(25))
print("\nDocstring via __doc__:")
print(celsius_to_fahrenheit.__doc__)

print("\nDocstring via help():")
help(celsius_to_fahrenheit)


# ---------------------------------------------------------------------------
# 7. Why functions matter: DRY and reuse
# ---------------------------------------------------------------------------

# Without a function, repeated logic gets copy-pasted, which makes bugs
# harder to fix (you'd need to fix every copy) and code harder to read.
print("\n--- Without a function (repeated logic) ---")
price1, qty1 = 10, 3
print("Total:", price1 * qty1)
price2, qty2 = 25, 2
print("Total:", price2 * qty2)


# With a function, the logic lives in one place (DRY: Don't Repeat
# Yourself), and every call site simply reuses it.
def calculate_total(price, quantity):
    """Return the total cost for a given price and quantity."""
    return price * quantity


print("\n--- With a function (DRY, reusable) ---")
print("Total:", calculate_total(10, 3))
print("Total:", calculate_total(25, 2))
print("Total:", calculate_total(7.5, 4))


# Key takeaways:
# - `def` defines a function; calling it by name (with parentheses) runs its body.
# - Parameters are the names in the definition; arguments are the values passed at call time.
# - `return` sends a value back to the caller; multiple return values become a tuple.
# - A function with no `return` (or a bare `return`) implicitly returns `None`.
# - Docstrings document functions and are viewable via `help()` or `__doc__`; functions promote DRY code and reuse.
