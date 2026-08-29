"""
Structural Pattern Matching: match / case

Introduced in Python 3.10 (PEP 634), the `match` statement compares a
subject value against a series of `case` patterns and runs the code under
the first one that matches -- similar in spirit to a `switch` statement in
other languages, but far more powerful. Patterns can match literal values,
capture variables, destructure sequences and mappings, check object
attributes, and combine with guard clauses -- all in one readable
construct. `match`/`case` doesn't replace `if`/`elif`, but it often reads
more clearly than a long chain of equality checks, especially when the
data being inspected has shape (a tuple, a list, a dict, an object) rather
than being a single flat value.

This file covers:
- Basic match/case on literal values, and the `_` wildcard/default
- Or-patterns with `|` to match several values in one case
- Guard clauses: `case PATTERN if CONDITION`
- Destructuring sequences (lists/tuples), including `*rest`
- Destructuring mappings (dicts) by key, including `**rest`
- Matching class instances by their attributes
- When to reach for match/case vs a plain if/elif chain
"""

# ---------------------------------------------------------------------------
# 1. Basic match/case on literal values, and the `_` wildcard
# ---------------------------------------------------------------------------
# `match` evaluates the subject once, then checks each `case` pattern in
# order, top to bottom, running the first one that matches. `case _:` is
# the catch-all: it matches anything and binds nothing, playing the same
# role an `else` would in an if/elif chain. Python does not enforce
# exhaustiveness, so it's good practice to always include a `_` case
# unless every possible value is truly covered above it.
def describe_status(code):
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown status code"


for status in (200, 201, 404, 500, 999):
    print(f"describe_status({status}) ->", describe_status(status))

# ---------------------------------------------------------------------------
# 2. Or-patterns: matching several values in one case
# ---------------------------------------------------------------------------
# `|` lets a single case match any one of several literal patterns.
def day_type(day):
    match day:
        case "Saturday" | "Sunday":
            return "Weekend"
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
            return "Weekday"
        case _:
            return "Not a valid day"


for day in ("Saturday", "Wednesday", "Someday"):
    print(f"day_type({day!r}) ->", day_type(day))

# ---------------------------------------------------------------------------
# 3. Guard clauses: case PATTERN if CONDITION
# ---------------------------------------------------------------------------
# A guard adds an extra boolean condition to a pattern; the case only
# matches if BOTH the pattern matches AND the guard evaluates to True.
# Here the pattern also captures `x` and `y` from the subject so the
# guard (and the result) can use them directly.
def classify_point(point):
    match point:
        case (0, 0):
            return "origin"
        case (x, y) if x == y:
            return f"on the diagonal at ({x}, {y})"
        case (x, 0):
            return f"on the x-axis at x={x}"
        case (0, y):
            return f"on the y-axis at y={y}"
        case (x, y):
            return f"a regular point at ({x}, {y})"


for point in ((0, 0), (3, 3), (5, 0), (0, -2), (1, 4)):
    print(f"classify_point({point}) ->", classify_point(point))

# ---------------------------------------------------------------------------
# 4. Destructuring sequences: lists, tuples, and *rest
# ---------------------------------------------------------------------------
# A case can match the SHAPE of a list/tuple and bind names to its
# elements in one step -- no manual indexing required. `*rest` captures
# "everything else" into a list, just like in ordinary unpacking.
def summarize_sequence(seq):
    match seq:
        case []:
            return "empty sequence"
        case [single]:
            return f"one item: {single!r}"
        case [first, second]:
            return f"exactly two items: {first!r} and {second!r}"
        case [first, *rest]:
            return f"starts with {first!r}, followed by {len(rest)} more item(s): {rest!r}"


for seq in ([], [42], [1, 2], [1, 2, 3, 4]):
    print(f"summarize_sequence({seq!r}) ->", summarize_sequence(seq))

# ---------------------------------------------------------------------------
# 5. Destructuring mappings: matching a dict by key
# ---------------------------------------------------------------------------
# A mapping pattern matches if the subject is a dict-like object that
# contains (at least) the given keys; unlisted keys are ignored, so this
# is a partial match by design. `**rest` (like in function calls) can
# capture any remaining key/value pairs.
def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at ({x}, {y})"
        case {"type": "keypress", "key": key}:
            return f"key pressed: {key!r}"
        case {"type": event_type, **rest}:
            return f"unhandled event type {event_type!r} with extra data {rest!r}"


events = [
    {"type": "click", "x": 10, "y": 20},
    {"type": "keypress", "key": "Enter"},
    {"type": "scroll", "delta": -5},
]
for event in events:
    print(f"handle_event({event!r}) ->", handle_event(event))

# ---------------------------------------------------------------------------
# 6. Matching class instances by their attributes
# ---------------------------------------------------------------------------
# A class pattern (`ClassName(attr=pattern, ...)`) matches if the subject
# is an instance of that class (isinstance check) AND its attributes match
# the given sub-patterns -- combining a type check and destructuring.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def describe_shape(shape):
    match shape:
        case Point(x=0, y=0):
            return "a Point at the origin"
        case Point(x=0, y=y):
            return f"a Point on the y-axis at y={y}"
        case Point(x=x, y=y):
            return f"a Point at ({x}, {y})"
        case _:
            return "not a Point"


for shape in (Point(0, 0), Point(0, 7), Point(3, 4), "not a point"):
    print("describe_shape(...) ->", describe_shape(shape))

# ---------------------------------------------------------------------------
# 7. When to use match/case vs a plain if/elif chain
# ---------------------------------------------------------------------------
print("Prefer match/case when:")
print("  - You're comparing one value against many possible literals or shapes.")
print("  - The data has structure (sequences, mappings, objects) you want to")
print("    destructure as part of the check, not just compare for equality.")
print("Prefer if/elif when:")
print("  - The conditions involve unrelated variables/expressions, not one")
print("    single subject being matched against different shapes.")
print("  - You're targeting Python < 3.10, where match/case isn't available.")

# Key takeaways:
# - match/case (Python 3.10+) checks a subject against ordered case patterns,
#   running the first one that matches, with `_` as the catch-all/default.
# - `|` combines several literal patterns into one case; `case X if COND:`
#   adds a guard so the pattern must ALSO satisfy an extra condition.
# - Sequence patterns ([a, b], [first, *rest]) and mapping patterns
#   ({"key": value, **rest}) destructure data by shape as part of matching.
# - Class patterns (ClassName(attr=value)) combine an isinstance check with
#   attribute destructuring in a single case.
# - Reach for match/case when checking one subject's shape/value against many
#   possibilities; a plain if/elif chain is still the right tool for
#   unrelated boolean conditions or when targeting Python < 3.10.
