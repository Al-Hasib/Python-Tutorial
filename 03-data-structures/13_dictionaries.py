"""
Dictionaries in Python
========================
A dictionary is an unordered-by-value, key-based mapping type that stores
data as key-value pairs (Python 3.7+ dicts preserve insertion order as an
implementation detail turned language guarantee). Dictionaries provide fast
O(1) average-case lookups by key, which makes them ideal for representing
structured records, caches, counters, and configuration data. Keys must be
hashable (typically strings, numbers, or tuples), while values can be any
type, including other dictionaries.

This file covers:
    - Creating dictionaries
    - Key requirements (hashable)
    - Accessing, adding, updating, and deleting keys
    - .get() and .setdefault()
    - .keys() / .values() / .items()
    - Iterating over dictionaries
    - Dict comprehensions
    - Merging dicts (| operator and update())
    - Nested dictionaries
"""

# ---------------------------------------------------------------------------
# 1. Creating dictionaries
# ---------------------------------------------------------------------------
empty_dict = {}
person = {"name": "Alice", "age": 30, "city": "Paris"}
via_constructor = dict(name="Bob", age=25, city="Berlin")
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])

print("empty_dict:", empty_dict)
print("person:", person)
print("via_constructor:", via_constructor)
print("from_pairs:", from_pairs)

# ---------------------------------------------------------------------------
# 2. Key requirements (hashable)
# ---------------------------------------------------------------------------
# Valid keys: strings, numbers, tuples (of hashable items), frozensets, etc.
valid_keys = {1: "one", "two": 2, (3, 0): "three-zero"}
print("valid_keys:", valid_keys)

# Invalid: lists and dicts are mutable, so they are unhashable and cannot
# be used as keys.
try:
    bad = {[1, 2]: "oops"}
except TypeError as exc:
    print("Cannot use list as key:", exc)

# ---------------------------------------------------------------------------
# 3. Accessing, adding, updating, deleting keys
# ---------------------------------------------------------------------------
student = {"name": "Sara", "grade": "A"}

print("access existing key:", student["name"])

student["age"] = 21          # adding a new key
print("after adding age:", student)

student["grade"] = "A+"      # updating an existing key
print("after updating grade:", student)

del student["age"]           # deleting a key
print("after deleting age:", student)

removed_value = student.pop("grade")  # remove and return the value
print("popped grade:", removed_value, "->", student)

# Accessing a missing key with [] raises KeyError.
try:
    print(student["missing"])
except KeyError as exc:
    print("KeyError for missing key:", exc)

# ---------------------------------------------------------------------------
# 4. .get() and .setdefault()
# ---------------------------------------------------------------------------
# get() returns None (or a default) instead of raising KeyError.
print("get existing:", student.get("name"))
print("get missing with default:", student.get("grade", "N/A"))

# setdefault() returns the value if the key exists, otherwise inserts it
# with the given default and returns that default.
inventory = {"apples": 10}
inventory.setdefault("bananas", 0)
inventory.setdefault("apples", 999)  # existing key is left untouched
print("inventory after setdefault:", inventory)

# ---------------------------------------------------------------------------
# 5. .keys(), .values(), .items()
# ---------------------------------------------------------------------------
scores = {"math": 90, "science": 85, "art": 95}

print("keys:", list(scores.keys()))
print("values:", list(scores.values()))
print("items:", list(scores.items()))

# ---------------------------------------------------------------------------
# 6. Iterating over dictionaries
# ---------------------------------------------------------------------------
for subject in scores:              # iterates over keys by default
    print(f"iterating key: {subject}")

for subject, score in scores.items():  # iterate key-value pairs
    print(f"{subject}: {score}")

for score in scores.values():          # iterate values only
    print("score value:", score)

# ---------------------------------------------------------------------------
# 7. Dict comprehensions
# ---------------------------------------------------------------------------
squares_dict = {n: n * n for n in range(6)}
print("squares_dict:", squares_dict)

# with a filtering condition
even_squares_dict = {n: n * n for n in range(10) if n % 2 == 0}
print("even_squares_dict:", even_squares_dict)

# building a dict from two related lists
names = ["a", "b", "c"]
values = [1, 2, 3]
zipped_dict = {k: v for k, v in zip(names, values)}
print("zipped_dict:", zipped_dict)

# ---------------------------------------------------------------------------
# 8. Merging dicts
# ---------------------------------------------------------------------------
defaults = {"theme": "light", "font_size": 12}
overrides = {"font_size": 16, "language": "en"}

# The | operator (Python 3.9+) creates a new merged dict.
merged = defaults | overrides
print("merged with |:", merged)
print("defaults unchanged:", defaults)

# update() merges in place, overwriting existing keys.
settings = defaults.copy()
settings.update(overrides)
print("settings after update():", settings)

# ---------------------------------------------------------------------------
# 9. Nested dictionaries
# ---------------------------------------------------------------------------
company = {
    "name": "TechCorp",
    "address": {"city": "Lyon", "zip": "69000"},
    "employees": [
        {"name": "Alice", "role": "Engineer"},
        {"name": "Bob", "role": "Designer"},
    ],
}

print("company city:", company["address"]["city"])
print("first employee name:", company["employees"][0]["name"])

# Safely navigate nested structures with chained .get() calls.
missing_zip = company.get("address", {}).get("country", "Unknown")
print("missing nested key with default:", missing_zip)

for employee in company["employees"]:
    print(f"{employee['name']} works as {employee['role']}")

# Key takeaways:
# - Dicts map hashable keys to values with fast average O(1) lookups, and
#   preserve insertion order.
# - Use .get()/.setdefault() to avoid KeyError when a key may be missing.
# - .keys()/.values()/.items() give convenient views for iteration.
# - The | operator and .update() both merge dicts, but | returns a new
#   dict while update() modifies in place.
# - Dictionaries can be nested arbitrarily to model structured, JSON-like
#   data.
