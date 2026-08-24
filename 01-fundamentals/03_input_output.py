"""
Basic Input & Output

Every useful program needs to communicate with the outside world: showing
results to a user (output) and accepting data from them (input). Python's
`print()` function is the primary way to display information, and it has
several options that control exactly how things are shown. The `input()`
function is the primary way to read text typed by a user, and it always
returns that text as a string, no matter what the user types. Formatting
that output nicely -- aligning columns, controlling decimal places, mixing
variables into text -- is done with %-formatting, `.format()`, or f-strings.

This file covers:
- print(): sep, end, and printing multiple arguments
- input() and why it always returns a string
- Old-style % string formatting
- The .format() method
- f-strings, including format specs like alignment and decimals
"""

# ---------------------------------------------------------------------------
# 1. print() basics: multiple arguments
# ---------------------------------------------------------------------------
# print() can take any number of arguments, separated by commas. By
# default, they are joined with a single space and followed by a newline.
print("Hello", "World", 2026)
print("a", "b", "c", "d")

# ---------------------------------------------------------------------------
# 2. print() with sep
# ---------------------------------------------------------------------------
# The `sep` keyword argument changes what is placed BETWEEN arguments
# (default is a single space " ").
print("2026", "08", "24", sep="-")
print("apple", "banana", "cherry", sep=", ")
print("no", "space", "between", sep="")

# ---------------------------------------------------------------------------
# 3. print() with end
# ---------------------------------------------------------------------------
# The `end` keyword argument changes what is placed AFTER all arguments
# (default is "\n", a newline). This lets you keep printing on the same line.
print("Loading", end="")
print(".", end="")
print(".", end="")
print(".", end="\n")  # finally move to a new line
print("Done!")

# ---------------------------------------------------------------------------
# 4. input() and its return type
# ---------------------------------------------------------------------------
# input(prompt) displays `prompt`, waits for the user to type something and
# press Enter, and returns EXACTLY what they typed -- always as a str, even
# if they type digits like "42". You must convert it yourself if you need
# a number (see 06_type_conversion.py for details on int()/float()).
#
# This script guards the call in a try/except because when it is run in a
# non-interactive environment (no keyboard attached, e.g. an automated
# test), there is no input to read and Python raises EOFError. In a normal
# terminal, this will actually prompt you and wait for input.
try:
    user_input = input("Type your name and press Enter: ")
    print("You typed:", user_input, "| type:", type(user_input))
except EOFError:
    user_input = "Alice"  # fallback so the rest of the script still runs
    print("(no interactive input available, using fallback value 'Alice')")

# Even if a user types a number, input() still returns a string.
try:
    age_text = input("Type your age and press Enter: ")
except EOFError:
    age_text = "30"
print("age_text:", repr(age_text), "| type:", type(age_text))
print("age_text + age_text (string concatenation, not addition):", age_text + age_text)

# ---------------------------------------------------------------------------
# 5. Old-style % string formatting
# ---------------------------------------------------------------------------
# Inherited from C-style printf formatting. %s = string, %d = integer,
# %f = float. Still seen in older codebases.
name = "Grace"
score = 97.456
print("Hello, %s! Your score is %.2f" % (name, score))
print("%d apples and %d oranges" % (5, 3))

# ---------------------------------------------------------------------------
# 6. The .format() method
# ---------------------------------------------------------------------------
# A more modern, flexible way to build strings using {} placeholders.
print("Hello, {}! Your score is {:.2f}".format(name, score))
print("{0} scored {1}, and {0} is proud of it.".format(name, score))  # positional reuse
print("{n} is {adj}".format(n="Python", adj="fun"))  # keyword placeholders

# ---------------------------------------------------------------------------
# 7. f-strings (formatted string literals)
# ---------------------------------------------------------------------------
# The most modern and readable way: prefix the string with f and embed
# expressions directly inside {}.
print(f"Hello, {name}! Your score is {score}")
print(f"2 + 2 = {2 + 2}")  # any expression can go inside {}

# f-strings with format specs: decimals, width, and alignment.
pi = 3.14159265
print(f"pi rounded to 2 decimals: {pi:.2f}")
print(f"pi rounded to 4 decimals: {pi:.4f}")

width = 10
print(f"[{'left':<{width}}]")   # left-align within width 10
print(f"[{'right':>{width}}]")  # right-align within width 10
print(f"[{'mid':^{width}}]")    # center within width 10

# Combine alignment and decimal precision -- handy for printing tables.
for item, cost in [("apple", 1.5), ("bread", 3.25), ("milk", 2.0)]:
    print(f"{item:<10}{cost:>6.2f}")

# Key takeaways:
# - print() joins its arguments with `sep` (default " ") and finishes with
#   `end` (default "\n"); both are customizable.
# - input() always returns a str, even for numeric-looking input --
#   convert it explicitly if you need a number.
# - Three string formatting styles exist: %-formatting (old), .format()
#   (flexible), and f-strings (modern, readable, and recommended).
# - Format specs like {value:.2f}, {value:<10}, {value:>10}, {value:^10}
#   control decimals, and left/right/center alignment.
