"""
Lambda Functions

A lambda is a small, anonymous function defined with the `lambda` keyword
instead of `def`. Lambdas are restricted to a single expression -- no
statements, no multiple lines -- which makes them convenient for short,
throwaway functions that you need briefly, such as a sort key or a simple
transformation. They matter because many built-in tools (`sorted`, `map`,
`filter`) accept a function as an argument, and a lambda lets you supply
one inline without formally defining a named function elsewhere.

This file covers:
- Lambda syntax
- When to use a lambda vs a regular `def` function
- Using lambdas with `sorted()` and `key=`
- Using lambdas with `map()`
- Using lambdas with `filter()`
- Limitations of lambdas (single expression, no statements)
- Readability considerations
"""

# ---------------------------------------------------------------------------
# 1. Lambda syntax
# ---------------------------------------------------------------------------

# General form: lambda parameters: expression
# The expression's value is automatically returned -- no `return` keyword.
square = lambda n: n * n
add = lambda a, b: a + b
greet = lambda name: f"Hello, {name}!"

print("square(5):", square(5))
print("add(3, 4):", add(3, 4))
print("greet('Alice'):", greet("Alice"))

# A lambda can take zero or default-valued parameters too.
constant_five = lambda: 5
power = lambda base, exponent=2: base ** exponent

print("constant_five():", constant_five())
print("power(3):", power(3))
print("power(2, 5):", power(2, 5))


# ---------------------------------------------------------------------------
# 2. When to use a lambda vs a regular def function
# ---------------------------------------------------------------------------

# Equivalent regular function for comparison:
def square_def(n):
    """Return n squared (regular function version)."""
    return n * n


print("\nsquare_def(5):", square_def(5), "vs lambda square(5):", square(5))

# Rule of thumb:
# - Use `lambda` for short, one-off functions passed directly as arguments
#   (e.g. a sort key), where naming it separately would add little value.
# - Use `def` when the function has a name worth documenting, needs a
#   docstring, spans multiple statements, or will be reused in many places.


# ---------------------------------------------------------------------------
# 3. Lambdas with sorted() and key=
# ---------------------------------------------------------------------------

students = [
    {"name": "Alice", "grade": 88},
    {"name": "Bob", "grade": 95},
    {"name": "Cara", "grade": 72},
]

# Sort by grade using a lambda as the key function.
by_grade = sorted(students, key=lambda student: student["grade"])
print("\nSorted by grade (ascending):")
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")

# Sort by grade descending.
by_grade_desc = sorted(students, key=lambda student: student["grade"], reverse=True)
print("Sorted by grade (descending):")
for s in by_grade_desc:
    print(f"  {s['name']}: {s['grade']}")

# Sort words by length.
words = ["banana", "fig", "apple", "kiwi"]
print("Sorted by length:", sorted(words, key=lambda w: len(w)))


# ---------------------------------------------------------------------------
# 4. Lambdas with map()
# ---------------------------------------------------------------------------

# map() applies a function to every item in an iterable, returning an
# iterator of results.
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda n: n * 2, numbers))
print("\nDoubled:", doubled)

names = ["alice", "bob", "cara"]
capitalized = list(map(lambda name: name.capitalize(), names))
print("Capitalized:", capitalized)


# ---------------------------------------------------------------------------
# 5. Lambdas with filter()
# ---------------------------------------------------------------------------

# filter() keeps only the items for which the function returns a truthy
# value.
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda n: n % 2 == 0, values))
print("\nEvens:", evens)

long_words = list(filter(lambda w: len(w) > 4, words))
print("Words longer than 4 letters:", long_words)

# map() and filter() can be combined: filter first, then transform.
result = list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, values)))
print("Squares of the evens:", result)


# ---------------------------------------------------------------------------
# 6. Limitations of lambdas
# ---------------------------------------------------------------------------

# A lambda body must be a SINGLE EXPRESSION. It cannot contain statements
# such as assignments, `if`/`else` blocks (only the conditional expression
# form is allowed), loops, or multiple lines.

# This works: a conditional EXPRESSION (ternary), which is still one expression.
classify = lambda n: "even" if n % 2 == 0 else "odd"
print("\nclassify(4):", classify(4))
print("classify(7):", classify(7))

# The following would NOT be valid as a lambda (shown as a comment, would
# raise a SyntaxError if uncommented), because it needs real statements:
#
#   bad_lambda = lambda n:
#       if n > 0:
#           return "positive"
#       return "non-positive"
#
# For anything needing multiple statements, loops, or multiple `return`
# points, use a regular `def` function instead:
def classify_def(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero"


print("classify_def(-3):", classify_def(-3))


# ---------------------------------------------------------------------------
# 7. Readability considerations
# ---------------------------------------------------------------------------

# Short lambdas used inline are easy to read:
print("\nShort and clear:", sorted([3, 1, 2], key=lambda x: -x))

# But a complicated lambda hurts readability. Compare:
data = [("a", 3, 1), ("b", 1, 2), ("c", 2, 0)]

# Hard to read at a glance:
hard_to_read = sorted(data, key=lambda t: (t[1], -t[2], t[0].upper()))
print("Hard-to-read lambda sort result:", hard_to_read)

# Better: extract a named function so the intent is clear.
def sort_key(item):
    """Sort by second field ascending, third field descending, then name."""
    name, second, third = item
    return (second, -third, name.upper())


clearer = sorted(data, key=sort_key)
print("Same result using a named function:", clearer)

# Guideline: if a lambda needs a comment to explain it, it's probably
# better written as a named `def` function.


# Key takeaways:
# - `lambda parameters: expression` creates a small anonymous function that automatically returns the expression's value.
# - Prefer lambdas for short, inline, one-off uses; prefer `def` when you need a docstring, multiple statements, or reuse.
# - `sorted(..., key=...)`, `map()`, and `filter()` are the classic places lambdas shine.
# - Lambdas can only contain a single expression -- no assignments, loops, or multi-line statements; use `def` for that.
# - If a lambda becomes hard to read, extract it into a named function for clarity.
