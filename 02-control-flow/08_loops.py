"""
Loops

Loops let a program repeat a block of code multiple times, which is essential
for processing collections, repeating actions until a condition changes, or
running a task a fixed number of times. Python provides two loop constructs:
`for` loops, which iterate over a sequence of items, and `while` loops, which
repeat as long as a condition holds true. Understanding how to control loop
flow with `break`, `continue`, and the lesser-known loop `else` clause -- along
with helpers like `enumerate()` and `zip()` -- makes iteration code far more
expressive and less error-prone.

This file covers:
- for loops over sequences (lists, strings, tuples, dicts)
- range() with start, stop, and step
- while loops
- break and continue
- the else clause on for/while loops (and when it runs)
- infinite loop pitfalls
- enumerate() and zip() in loops
"""

# ---------------------------------------------------------------------------
# 1. for loops over sequences
# ---------------------------------------------------------------------------
# A for loop iterates over the elements of any iterable: lists, tuples,
# strings, dictionaries, sets, etc.

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# Iterating over a string yields each character.
for letter in "abc":
    print(f"Letter: {letter}")

# Iterating over a dictionary by default yields its keys.
prices = {"apple": 1.5, "banana": 0.5, "cherry": 3.0}
for name in prices:
    print(f"{name} costs {prices[name]}")

# Use .items() to get key-value pairs directly.
for name, price in prices.items():
    print(f"{name}: ${price:.2f}")

# ---------------------------------------------------------------------------
# 2. range() with start, stop, and step
# ---------------------------------------------------------------------------
# range() generates a sequence of numbers without storing them all in memory.
# range(stop) starts at 0. range(start, stop) and range(start, stop, step)
# give finer control. The stop value is never included.

for i in range(5):
    print(f"range(5): {i}")

for i in range(2, 8):
    print(f"range(2, 8): {i}")

for i in range(0, 10, 2):
    print(f"range(0, 10, 2): {i}")

# A negative step counts downward.
for i in range(10, 0, -2):
    print(f"range(10, 0, -2): {i}")

# ---------------------------------------------------------------------------
# 3. while loops
# ---------------------------------------------------------------------------
# A while loop repeats as long as its condition remains True. It is useful
# when the number of iterations is not known in advance.

count = 0
while count < 5:
    print(f"count is {count}")
    count += 1

# Example: keep halving a number until it drops below 1.
value = 50
while value >= 1:
    print(f"value: {value}")
    value /= 2

# ---------------------------------------------------------------------------
# 4. break and continue
# ---------------------------------------------------------------------------
# `break` exits the loop entirely. `continue` skips the rest of the current
# iteration and moves on to the next one.

for number in range(10):
    if number == 5:
        print("Reached 5, stopping loop.")
        break
    print(f"number: {number}")

for number in range(10):
    if number % 2 != 0:
        continue  # skip odd numbers
    print(f"even number: {number}")

# break and continue work the same way inside while loops.
n = 0
while True:
    n += 1
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print(f"odd n: {n}")

# ---------------------------------------------------------------------------
# 5. The else clause on for/while loops
# ---------------------------------------------------------------------------
# A loop's `else` block runs only if the loop completes WITHOUT hitting a
# `break`. It does not run if the loop is exited early via break.

for number in range(5):
    print(f"checking {number}")
else:
    print("Loop finished without break.")

for number in range(5):
    if number == 3:
        print("Breaking early at 3.")
        break
else:
    print("This will NOT print, because we broke out.")

# Practical use: searching for an item and reporting "not found" only if the
# whole loop completed without finding it.
target = 99
numbers = [4, 8, 15, 16, 23]
for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} was not found in the list.")

# The same else behavior applies to while loops.
attempts = 0
while attempts < 3:
    attempts += 1
    print(f"attempt {attempts}")
else:
    print("while loop completed normally (no break).")

# ---------------------------------------------------------------------------
# 6. Infinite loop pitfalls
# ---------------------------------------------------------------------------
# A while loop whose condition never becomes False will run forever. This
# usually happens when the loop variable is never updated, or is updated in
# a way that never satisfies the exit condition. Below are examples of the
# MISTAKE (commented out) and the FIX.

# MISTAKE (do not uncomment -- this never terminates):
# i = 0
# while i < 5:
#     print(i)
#     # forgot to increment i, so the condition is always True

# FIX: always ensure the loop variable moves toward the exit condition.
i = 0
while i < 5:
    print(f"safe loop i={i}")
    i += 1  # this line is essential

# A common safeguard is a maximum iteration count to prevent runaway loops
# when the exit condition depends on unpredictable external input.
max_iterations = 100
iterations = 0
condition_met = False
while not condition_met and iterations < max_iterations:
    iterations += 1
    if iterations == 7:  # simulate a condition being satisfied
        condition_met = True
print(f"Stopped after {iterations} iterations, condition_met={condition_met}")

# ---------------------------------------------------------------------------
# 7. enumerate() and zip() in loops
# ---------------------------------------------------------------------------
# enumerate() gives both the index and the value while looping, avoiding
# manual counters.

colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")

# enumerate() accepts a start value.
for index, color in enumerate(colors, start=1):
    print(f"Color #{index}: {color}")

# zip() lets you iterate over multiple sequences in parallel, stopping at
# the shortest one.
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 95]
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# zip() can combine more than two sequences.
ids = [101, 102, 103]
for id_, name, score in zip(ids, names, scores):
    print(f"ID {id_}: {name} -> {score}")

# Key takeaways:
# - for loops iterate directly over items; range() generates numeric
#   sequences with optional start/stop/step (step can be negative).
# - while loops repeat based on a condition and require the condition to
#   eventually become False to avoid infinite loops.
# - break exits a loop immediately; continue skips to the next iteration.
# - A loop's else clause runs only when the loop finishes without a break --
#   useful for "search and report not-found" patterns.
# - enumerate() pairs values with indices, and zip() iterates multiple
#   sequences together, both avoiding manual index bookkeeping.
