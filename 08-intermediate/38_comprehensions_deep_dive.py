"""
Comprehensions Deep Dive
========================

Comprehensions are Python's compact syntax for building lists, dicts, sets,
and generators from an existing iterable in a single expression. They read
naturally as "for each item, optionally filter it, then transform it", and
they are usually faster and more readable than the equivalent manual loop.
This file goes beyond the basics: comparing the four comprehension forms
side by side, nesting them, choosing between a conditional expression and a
filtering condition, using the walrus operator inside a comprehension, and
knowing when a comprehension has become too clever and a plain loop would
be clearer.

This file covers:
- List / dict / set / generator comprehensions side by side
- Nested comprehensions
- Conditional expressions inside comprehensions (if/else vs filtering if)
- The walrus operator (:=) inside comprehensions
- Readability guidance: when to prefer a plain loop
- Performance notes
"""

import sys

# ---------------------------------------------------------------------------
# 1. List / dict / set / generator comprehensions side by side
# ---------------------------------------------------------------------------
numbers = [1, 2, 3, 4, 5, 6]

list_comp = [n * n for n in numbers]                  # [] -> list, eager
dict_comp = {n: n * n for n in numbers}                # {} with key:value -> dict
set_comp = {n % 3 for n in numbers}                     # {} with single expr -> set
gen_comp = (n * n for n in numbers)                     # () -> generator, lazy

print("List comprehension  :", list_comp)
print("Dict comprehension  :", dict_comp)
print("Set comprehension   :", set_comp, "(duplicates collapsed automatically)")
print("Generator expression:", gen_comp, "-> list(gen_comp) =", list(gen_comp))

# ---------------------------------------------------------------------------
# 2. Nested comprehensions
# ---------------------------------------------------------------------------
# A nested comprehension can flatten a 2D structure or build one, using
# multiple `for` clauses in the order you would write nested for-loops.

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

flattened = [value for row in matrix for value in row]
print("\nFlattened matrix:", flattened)

transposed = [[row[i] for row in matrix] for i in range(3)]
print("Transposed matrix:", transposed)

# Equivalent plain loop for the flattening, for comparison:
flattened_loop = []
for row in matrix:
    for value in row:
        flattened_loop.append(value)
print("Same result via plain nested loops:", flattened_loop)

# ---------------------------------------------------------------------------
# 3. Conditional expressions vs filtering conditions
# ---------------------------------------------------------------------------
# Two different things that both use the word "if" inside a comprehension:
#   - A trailing `if condition` FILTERS which items are included.
#   - A leading `... if condition else ...` is a conditional EXPRESSION that
#     transforms every item (nothing is dropped).

values = range(10)

filtered = [n for n in values if n % 2 == 0]
print("\nFiltering if (keep only even numbers):", filtered)

transformed = [n if n % 2 == 0 else -n for n in values]
print("Conditional expression (negate odd numbers):", transformed)

# The two forms can combine: filter first, then transform.
combined = [n * 10 if n % 2 == 0 else n for n in values if n > 2]
print("Filter (n > 2) + conditional expression:", combined)

# ---------------------------------------------------------------------------
# 4. The walrus operator (:=) inside comprehensions
# ---------------------------------------------------------------------------
# := lets you compute a value once inside the comprehension and reuse it,
# avoiding duplicate work (e.g. calling an expensive function twice).

def expensive_transform(n):
    """Pretend this does real work; we just square the number."""
    return n * n


# Without walrus: expensive_transform() would be called twice per item.
without_walrus = [
    expensive_transform(n) for n in numbers if expensive_transform(n) > 10
]
print("\nWithout walrus (calls the function twice per item):", without_walrus)

# With walrus: compute once, bind to a name, reuse it in the filter and body.
with_walrus = [result for n in numbers if (result := expensive_transform(n)) > 10]
print("With walrus (calls the function once per item):", with_walrus)

# Walrus can also capture a running value for inspection afterward.
totals = []
running_total = 0
accumulated = [running_total := running_total + n for n in numbers]
print("Running totals via walrus:", accumulated)

# ---------------------------------------------------------------------------
# 5. Readability guidance: when a comprehension is too complex
# ---------------------------------------------------------------------------
# Comprehensions shine when they stay short and read like a sentence.
# Once you need multiple conditions, multiple nested loops, or side effects,
# a plain loop is almost always clearer -- and easier to debug.

# Reasonably readable: one loop, one filter, one transform.
readable = [n * 2 for n in numbers if n % 2 == 0]
print("\nReadable comprehension:", readable)

# Too clever: deeply nested, multiple conditions, hard to scan at a glance.
# words = [w.upper() for row in matrix for w in row if w > 2 for _ in range(w) if w % 2]
# --> Written as a plain loop instead, this is much easier to follow:
result = []
for row in matrix:
    for value in row:
        if value > 2 and value % 2 == 0:
            result.append(value * 100)
print("Same logic as a plain loop (clearer than a triple-nested comprehension):")
print(" ", result)

print("\nGuideline: if a comprehension needs more than ~2 clauses (one 'for'")
print("plus one 'if'), or produces side effects, prefer a regular for-loop.")

# ---------------------------------------------------------------------------
# 6. Performance notes
# ---------------------------------------------------------------------------
# Comprehensions are typically faster than an equivalent for-loop with
# .append() calls, because the looping happens in optimized C code with less
# Python-level bytecode overhead per iteration.

import timeit

loop_time = timeit.timeit(
    "result = []\nfor n in range(1000):\n    result.append(n * n)",
    number=1000,
)
comp_time = timeit.timeit("[n * n for n in range(1000)]", number=1000)

print("\nPerformance comparison (1000 runs of squaring range(1000)):")
print(f"  for-loop with .append(): {loop_time:.4f} seconds")
print(f"  list comprehension:      {comp_time:.4f} seconds")
print("  (comprehensions are usually a bit faster, though correctness and")
print("   readability should still guide the choice, not speed alone)")

# Generator expressions also save memory versus building an intermediate
# list you only intend to iterate over once.
list_size = sys.getsizeof([n for n in range(10_000)])
gen_size = sys.getsizeof((n for n in range(10_000)))
print(f"\nMemory: list comprehension ~{list_size} bytes vs generator ~{gen_size} bytes")

# Key takeaways:
# - List, dict, set, and generator comprehensions share the same for/if
#   structure; only the brackets (and dict's key:value) differ.
# - Nested comprehensions mirror nested for-loops, written left-to-right in
#   the same order you would nest them manually.
# - A trailing `if` filters items out; a leading `... if ... else ...` is a
#   conditional expression that transforms every item without dropping any.
# - The walrus operator (:=) avoids recomputing an expensive expression
#   inside both the filter and the body of a comprehension.
# - Prefer a plain loop once a comprehension needs multiple conditions,
#   multiple nested loops, or side effects -- readability beats cleverness.
