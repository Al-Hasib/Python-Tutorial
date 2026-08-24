"""
Conditional Statements

Conditional statements let a program make decisions and execute different
code paths depending on whether certain expressions are true or false.
Python evaluates conditions using `if`, `elif`, and `else`, and it treats
many non-boolean values as "truthy" or "falsy" in a boolean context. Mastering
conditionals -- including how truthiness works, how to nest decisions, and how
to write compact expressions -- is fundamental to writing logic that reacts to
real-world data. This file walks through the full range of conditional tools
available in Python.

This file covers:
- Basic if / elif / else statements
- Truthy and falsy evaluation of values
- Nested conditionals
- Ternary (conditional) expressions
- Chained comparisons (e.g. 0 < x < 10)
- Combining conditions with `and` / `or`
"""

# ---------------------------------------------------------------------------
# 1. Basic if / elif / else
# ---------------------------------------------------------------------------
# The `if` statement runs a block only when its condition is True.
# `elif` checks additional conditions in order, and `else` is the fallback.

temperature = 28

if temperature > 30:
    print("It's hot outside.")
elif temperature > 20:
    print("It's warm outside.")
elif temperature > 10:
    print("It's cool outside.")
else:
    print("It's cold outside.")

# Only the first matching branch runs; the rest are skipped.
score = 75
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"
print(f"Score {score} maps to grade {grade}")

# ---------------------------------------------------------------------------
# 2. Truthy and falsy evaluation
# ---------------------------------------------------------------------------
# Every object in Python can be tested for truth value. Falsy values include:
# False, None, 0, 0.0, "" (empty string), [] , {}, set(), and other empty
# containers. Everything else is generally truthy.

falsy_values = [False, None, 0, 0.0, "", [], {}, set(), ()]
for value in falsy_values:
    print(f"{value!r:10} is truthy? {bool(value)}")

truthy_values = [True, 1, -1, 3.14, "hello", [0], {"key": "value"}, " "]
for value in truthy_values:
    print(f"{value!r:15} is truthy? {bool(value)}")

# This means you can use a value directly in an `if` instead of comparing
# it explicitly to an empty value.
name = ""
if name:
    print(f"Hello, {name}!")
else:
    print("No name was provided.")

items = [1, 2, 3]
if items:
    print(f"There are {len(items)} items in the list.")

# ---------------------------------------------------------------------------
# 3. Nested conditionals
# ---------------------------------------------------------------------------
# A conditional block can contain another conditional block. Use nesting
# when a decision only makes sense after another decision has been made.

age = 20
has_ticket = True

if age >= 18:
    print("Age requirement met.")
    if has_ticket:
        print("Entry allowed: adult with a valid ticket.")
    else:
        print("Entry denied: no ticket.")
else:
    print("Entry denied: must be 18 or older.")

# Nesting can go multiple levels deep, though deeply nested code can become
# hard to read -- flattening logic with elif or early returns often helps.
user_role = "editor"
is_active = True

if is_active:
    if user_role == "admin":
        print("Full access granted.")
    elif user_role == "editor":
        print("Edit access granted.")
    else:
        print("Read-only access granted.")
else:
    print("Account is disabled; no access.")

# ---------------------------------------------------------------------------
# 4. Ternary (conditional) expressions
# ---------------------------------------------------------------------------
# A ternary expression evaluates to one of two values based on a condition,
# all in a single line: `value_if_true if condition else value_if_false`.

number = 7
parity = "even" if number % 2 == 0 else "odd"
print(f"{number} is {parity}")

# Ternary expressions can be used anywhere a value is expected, such as
# inside function calls or when building lists.
values = [-3, 5, -1, 8, 0]
labels = ["non-negative" if v >= 0 else "negative" for v in values]
print(labels)

# They can be chained, though readability suffers if overused.
x = 0
sign = "positive" if x > 0 else "negative" if x < 0 else "zero"
print(f"The sign of {x} is {sign}")

# ---------------------------------------------------------------------------
# 5. Chained comparisons
# ---------------------------------------------------------------------------
# Python allows chaining comparison operators, which reads naturally and
# avoids repeating the variable being compared.

x = 5
print("0 < x < 10:", 0 < x < 10)          # equivalent to (0 < x) and (x < 10)
print("10 < x < 20:", 10 < x < 20)

age = 45
if 18 <= age < 65:
    print("Considered working age.")
else:
    print("Outside the working-age range.")

# Chained comparisons can mix operators too.
a, b, c = 1, 2, 3
print("a < b <= c:", a < b <= c)

# ---------------------------------------------------------------------------
# 6. Combining conditions with `and` / `or`
# ---------------------------------------------------------------------------
# `and` requires both sides to be true; `or` requires at least one side to
# be true. Python short-circuits: it stops evaluating as soon as the result
# is determined.

username = "admin"
password = "secret123"

if username == "admin" and password == "secret123":
    print("Login successful.")
else:
    print("Login failed.")

is_weekend = True
is_holiday = False
if is_weekend or is_holiday:
    print("No work today.")
else:
    print("It's a work day.")

# `not` inverts a boolean value and combines well with and/or.
is_logged_in = False
if not is_logged_in:
    print("Please log in to continue.")

# Combine multiple conditions with parentheses for clarity.
cart_total = 120
is_member = True
if (cart_total > 100 and is_member) or cart_total > 500:
    print("Free shipping applied.")
else:
    print("Standard shipping rate applies.")

# Key takeaways:
# - if / elif / else branches run in order; only the first true branch executes.
# - Falsy values (False, None, 0, "", empty containers) let you test objects
#   directly in conditions without explicit comparisons.
# - Nested conditionals model dependent decisions, but keep nesting shallow
#   for readability.
# - Ternary expressions (`a if cond else b`) provide a compact one-line if/else.
# - Chained comparisons (0 < x < 10) and and/or/not combine conditions cleanly
#   while Python short-circuits evaluation for efficiency.
