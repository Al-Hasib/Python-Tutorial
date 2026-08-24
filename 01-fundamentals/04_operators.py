"""
Operators

Operators are special symbols that perform operations on values (called
operands). Python groups operators into several families: arithmetic (for
math), comparison (for comparing values), logical (for combining boolean
expressions), assignment (for storing/updating values), bitwise (for
working with individual bits), identity (for checking if two names point
to the same object), and membership (for checking if a value exists inside
a collection). Knowing how these operators behave -- and in what order
they are evaluated -- is essential for writing correct expressions.

This file covers:
- Arithmetic operators: + - * / // % **
- Comparison operators
- Logical operators: and, or, not, and short-circuiting
- Assignment operators: = += -= etc.
- Bitwise operators: & | ^ ~ << >>
- Identity (is / is not) vs equality (==)
- Membership operators: in / not in
- Operator precedence
"""

# ---------------------------------------------------------------------------
# 1. Arithmetic operators
# ---------------------------------------------------------------------------
a, b = 17, 5
print("a + b  (addition):      ", a + b)
print("a - b  (subtraction):   ", a - b)
print("a * b  (multiplication):", a * b)
print("a / b  (true division): ", a / b)   # always returns a float
print("a // b (floor division):", a // b)  # discards the remainder
print("a % b  (modulo):        ", a % b)   # remainder of division
print("a ** b (exponentiation):", a ** b)  # a raised to the power of b

# ---------------------------------------------------------------------------
# 2. Comparison operators
# ---------------------------------------------------------------------------
# These always evaluate to a bool: True or False.
print("a == b:", a == b)  # equal to
print("a != b:", a != b)  # not equal to
print("a > b: ", a > b)   # greater than
print("a < b: ", a < b)   # less than
print("a >= b:", a >= 5)  # greater than or equal to
print("a <= b:", a <= 17) # less than or equal to

# ---------------------------------------------------------------------------
# 3. Logical operators and short-circuiting
# ---------------------------------------------------------------------------
# `and` / `or` / `not` combine or invert boolean expressions.
is_sunny = True
is_warm = False
print("is_sunny and is_warm:", is_sunny and is_warm)
print("is_sunny or is_warm: ", is_sunny or is_warm)
print("not is_sunny:        ", not is_sunny)


def noisy_true(label):
    print(f"  -> evaluating {label}")
    return True


def noisy_false(label):
    print(f"  -> evaluating {label}")
    return False


# Short-circuiting: `and` stops as soon as it finds a False value; `or`
# stops as soon as it finds a True value. The second call is never made.
print("Short-circuit with 'and' (second call skipped):")
result = noisy_false("first") and noisy_true("second")
print("result:", result)

print("Short-circuit with 'or' (second call skipped):")
result = noisy_true("first") or noisy_false("second")
print("result:", result)

# ---------------------------------------------------------------------------
# 4. Assignment operators
# ---------------------------------------------------------------------------
# `=` assigns a value. Compound assignment operators combine an operation
# with assignment, e.g. `x += 1` means `x = x + 1`.
x = 10
print("x =", x)
x += 5   # x = x + 5
print("x += 5 ->", x)
x -= 3   # x = x - 3
print("x -= 3 ->", x)
x *= 2   # x = x * 2
print("x *= 2 ->", x)
x //= 4  # x = x // 4
print("x //= 4 ->", x)
x **= 2  # x = x ** 2
print("x **= 2 ->", x)
x %= 5   # x = x % 5
print("x %= 5 ->", x)

# ---------------------------------------------------------------------------
# 5. Bitwise operators
# ---------------------------------------------------------------------------
# These operate on the binary representation of integers.
m, n = 12, 10  # 12 = 0b1100, 10 = 0b1010
print(f"m={m} ({bin(m)}), n={n} ({bin(n)})")
print("m & n  (AND):         ", m & n)   # bits set in both
print("m | n  (OR):          ", m | n)   # bits set in either
print("m ^ n  (XOR):         ", m ^ n)   # bits set in exactly one
print("~m     (NOT):         ", ~m)      # inverts all bits (~m == -m - 1)
print("m << 2 (left shift):  ", m << 2)  # shifts bits left (multiply by 4)
print("m >> 2 (right shift): ", m >> 2)  # shifts bits right (divide by 4)

# ---------------------------------------------------------------------------
# 6. Identity (is / is not) vs equality (==)
# ---------------------------------------------------------------------------
# `==` checks if two values are EQUAL. `is` checks if two names refer to
# the EXACT SAME object in memory. Two equal values are not always the
# identical object.
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

print("list1 == list2 (equal values):", list1 == list2)
print("list1 is list2 (same object): ", list1 is list2)
print("list1 is list3 (same object): ", list1 is list3)

# `is` is also the correct way to check for None, since there is only
# ever one None object.
value = None
print("value is None:    ", value is None)
print("value is not None:", value is not None)

# ---------------------------------------------------------------------------
# 7. Membership operators (in / not in)
# ---------------------------------------------------------------------------
# Check whether a value exists inside a sequence or collection.
fruits = ["apple", "banana", "cherry"]
print("'banana' in fruits:    ", "banana" in fruits)
print("'grape' in fruits:     ", "grape" in fruits)
print("'grape' not in fruits: ", "grape" not in fruits)
print("'a' in 'banana' (substring check):", "a" in "banana")

# ---------------------------------------------------------------------------
# 8. Operator precedence
# ---------------------------------------------------------------------------
# Python evaluates expressions using a fixed precedence order (similar to
# math's "PEMDAS"). From higher to lower priority (simplified):
#   ** -> unary +/- -> * / // % -> + - -> comparisons -> not -> and -> or
# Parentheses always override precedence and should be used to make
# intent clear.
print("2 + 3 * 4       =", 2 + 3 * 4)         # multiplication before addition -> 14
print("(2 + 3) * 4     =", (2 + 3) * 4)       # parentheses change the order -> 20
print("2 ** 3 ** 2     =", 2 ** 3 ** 2)       # ** is right-associative -> 2**(3**2) = 512
print("not True and False =", not True and False)  # `not` binds tighter than `and`
print("1 < 2 and 3 < 4 =", 1 < 2 and 3 < 4)   # comparisons happen before `and`

# Key takeaways:
# - Arithmetic operators include // (floor division) and ** (exponent);
#   / always returns a float in Python 3.
# - `and`/`or` short-circuit: they stop evaluating as soon as the result
#   is determined, skipping the remaining operand(s).
# - `==` compares values; `is` compares identity (same object in memory) --
#   use `is`/`is not` specifically for None checks.
# - `in`/`not in` test membership in strings, lists, and other collections.
# - Operator precedence follows a fixed order; use parentheses to make
#   the intended order explicit and avoid mistakes.
