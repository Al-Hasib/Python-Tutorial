"""
Sets in Python
================
A set is an unordered collection of unique, hashable elements. Sets
automatically eliminate duplicates and provide very fast membership testing
(average O(1)), which makes them ideal for deduplication and for expressing
mathematical set operations like union, intersection, and difference.
Python also provides `frozenset`, an immutable and therefore hashable
variant that can itself be used as a dict key or a member of another set.

This file covers:
    - Creating sets
    - The uniqueness property
    - Adding/removing elements
    - Set operations (union, intersection, difference, symmetric difference)
    - Set comprehensions
    - Frozensets
    - Common use cases (deduplication, membership testing)
"""

# ---------------------------------------------------------------------------
# 1. Creating sets
# ---------------------------------------------------------------------------
empty_set = set()  # NOTE: {} creates an empty dict, not an empty set
numbers = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3, 3, 3])  # duplicates collapse automatically
from_string = set("banana")          # set of unique characters

print("empty_set:", empty_set)
print("numbers:", numbers)
print("from_list:", from_list)
print("from_string:", from_string)

# ---------------------------------------------------------------------------
# 2. Uniqueness property
# ---------------------------------------------------------------------------
with_duplicates = {1, 1, 2, 2, 3, 3, 3}
print("duplicates removed automatically:", with_duplicates)

# ---------------------------------------------------------------------------
# 3. Adding and removing elements
# ---------------------------------------------------------------------------
colors = {"red", "green", "blue"}

colors.add("yellow")           # add a single element
print("after add:", colors)

colors.update(["purple", "orange"])  # add multiple elements
print("after update:", colors)

colors.remove("red")           # remove; raises KeyError if missing
print("after remove:", colors)

colors.discard("not-there")    # remove if present; no error if missing
print("after discard (no-op):", colors)

popped = colors.pop()          # remove and return an arbitrary element
print("popped element:", popped, "->", colors)

colors.clear()                 # remove all elements
print("after clear:", colors)

# ---------------------------------------------------------------------------
# 4. Set operations
# ---------------------------------------------------------------------------
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("union (a | b):", a | b)
print("union() method:", a.union(b))

print("intersection (a & b):", a & b)
print("intersection() method:", a.intersection(b))

print("difference (a - b):", a - b)      # items in a but not in b
print("difference (b - a):", b - a)      # items in b but not in a

print("symmetric difference (a ^ b):", a ^ b)  # items in either, not both

# Subset / superset checks
print("is {1, 2} subset of a:", {1, 2}.issubset(a))
print("is a superset of {1, 2}:", a.issuperset({1, 2}))
print("are a and b disjoint:", a.isdisjoint(b))

# ---------------------------------------------------------------------------
# 5. Set comprehensions
# ---------------------------------------------------------------------------
squares_set = {n * n for n in range(6)}
print("squares_set:", squares_set)

# with a filtering condition
even_squares_set = {n * n for n in range(10) if n % 2 == 0}
print("even_squares_set:", even_squares_set)

# deduplicate while transforming
words = ["Apple", "apple", "BANANA", "banana", "Cherry"]
lowercased_unique = {w.lower() for w in words}
print("lowercased_unique:", lowercased_unique)

# ---------------------------------------------------------------------------
# 6. Frozensets
# ---------------------------------------------------------------------------
frozen = frozenset([1, 2, 3])
print("frozen:", frozen)

try:
    frozen.add(4)  # frozensets are immutable
except AttributeError as exc:
    print("Cannot modify frozenset:", exc)

# Because frozensets are hashable, they can be used as dict keys or set
# members - a plain set cannot.
group_labels = {
    frozenset([1, 2]): "group A",
    frozenset([3, 4]): "group B",
}
print("lookup by frozenset key:", group_labels[frozenset([1, 2])])

try:
    bad = {set([1, 2]): "oops"}
except TypeError as exc:
    print("Cannot use a plain set as a key:", exc)

# ---------------------------------------------------------------------------
# 7. Common use cases
# ---------------------------------------------------------------------------
# Deduplication: removing repeated items while (usually) losing order.
raw_ids = [101, 102, 101, 103, 102, 104]
unique_ids = set(raw_ids)
print("raw_ids:", raw_ids)
print("unique_ids:", unique_ids)

# Membership testing: sets are much faster than lists for "is X in here?"
allowed_users = {"alice", "bob", "carol"}
candidate = "dave"
if candidate in allowed_users:
    print(f"{candidate} is allowed")
else:
    print(f"{candidate} is NOT allowed")

# Finding common items between two collections (e.g. shared tags).
post_a_tags = {"python", "tutorial", "beginner"}
post_b_tags = {"python", "advanced", "tips"}
shared_tags = post_a_tags & post_b_tags
print("shared_tags:", shared_tags)

# Key takeaways:
# - Sets store unique, hashable elements with no guaranteed order; use
#   set(), not {}, to create an empty set.
# - add()/update() insert elements; remove()/discard()/pop()/clear() take
#   them out (remove() raises if missing, discard() does not).
# - Union (|), intersection (&), difference (-), and symmetric difference
#   (^) implement standard set math directly.
# - frozenset is an immutable, hashable set usable as a dict key or set
#   member.
# - Sets excel at deduplication and fast O(1) average membership testing.
