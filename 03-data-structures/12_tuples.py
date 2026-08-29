"""
Tuples in Python
=================
A tuple is an ordered, immutable sequence. Once created, its contents cannot
be changed, which makes tuples useful for representing fixed collections of
values (like coordinates or database records) and for using as dictionary
keys or set members. Tuples support the same indexing/slicing operations as
lists, plus powerful packing/unpacking syntax that makes multi-value returns
and assignments concise. `collections.namedtuple` extends tuples with named
fields for extra readability.

This file covers:
    - Creating tuples (with/without parens, single-element tuple gotcha)
    - Immutability
    - Indexing and slicing
    - Packing & unpacking (including extended unpacking with *)
    - Tuple methods (count, index)
    - When/why to use tuples vs lists
    - Named tuples (collections.namedtuple)
"""

from collections import namedtuple

# ---------------------------------------------------------------------------
# 1. Creating tuples
# ---------------------------------------------------------------------------
with_parens = (1, 2, 3)
without_parens = 1, 2, 3  # parentheses are optional for tuple creation
print("with_parens:", with_parens)
print("without_parens:", without_parens)

empty_tuple = ()
print("empty_tuple:", empty_tuple, type(empty_tuple))

# Single-element tuple gotcha: a trailing comma is REQUIRED.
not_a_tuple = (5)       # this is just the int 5 in parentheses
single_tuple = (5,)     # this IS a one-item tuple
print("not_a_tuple:", not_a_tuple, type(not_a_tuple))
print("single_tuple:", single_tuple, type(single_tuple))

# tuple() can build a tuple from any iterable
from_list = tuple([1, 2, 3])
print("from_list:", from_list)

# ---------------------------------------------------------------------------
# 2. Immutability
# ---------------------------------------------------------------------------
point = (10, 20)
try:
    point[0] = 99  # raises TypeError - tuples cannot be modified
except TypeError as exc:
    print("Cannot modify tuple:", exc)

# Note: if a tuple contains a mutable object, that object can still change.
container = ([1, 2], "fixed")
container[0].append(3)  # the list inside the tuple is still mutable
print("tuple with mutable element:", container)

# ---------------------------------------------------------------------------
# 3. Indexing and slicing
# ---------------------------------------------------------------------------
colors = ("red", "green", "blue", "yellow", "purple")
print("first color:", colors[0])
print("last color:", colors[-1])
print("slice [1:3]:", colors[1:3])
print("every other color:", colors[::2])
print("reversed:", colors[::-1])

# ---------------------------------------------------------------------------
# 4. Packing and unpacking
# ---------------------------------------------------------------------------
# Packing: multiple values combined into a single tuple.
packed = 1, 2, 3
print("packed:", packed)

# Unpacking: tuple values assigned to separate variables.
a, b, c = packed
print("unpacked:", a, b, c)

# Common use: returning multiple values from a function.
def min_max(values):
    return min(values), max(values)

lowest, highest = min_max([4, 8, 1, 9, 3])
print("lowest:", lowest, "highest:", highest)

# Swapping variables using tuple packing/unpacking.
x, y = 1, 2
x, y = y, x
print("after swap: x =", x, "y =", y)

# Extended unpacking with * gathers remaining items into a list.
first, *middle, last = [1, 2, 3, 4, 5]
print("first:", first, "middle:", middle, "last:", last)

head, *rest = (10, 20, 30, 40)
print("head:", head, "rest:", rest)

*init, tail = (10, 20, 30, 40)
print("init:", init, "tail:", tail)

# ---------------------------------------------------------------------------
# 5. Tuple methods
# ---------------------------------------------------------------------------
numbers = (1, 2, 2, 3, 2, 4)
print("count of 2:", numbers.count(2))
print("index of first 3:", numbers.index(3))

# ---------------------------------------------------------------------------
# 6. When/why to use tuples vs lists
# ---------------------------------------------------------------------------
# Use a tuple when:
#   - The collection represents a fixed, unchanging record (e.g. a point,
#     an RGB color, a row from a database).
#   - You want to prevent accidental modification.
#   - You need a hashable value to use as a dict key or set member.
#   - Slightly better performance/memory for fixed-size data.
# Use a list when:
#   - The collection needs to grow, shrink, or be reordered.
#   - You plan to use list-specific mutating methods.

# Tuples are hashable (if their contents are), so they can be dict keys.
locations = {
    (0, 0): "origin",
    (1, 0): "east",
    (0, 1): "north",
}
print("lookup (0, 0):", locations[(0, 0)])

# A list, being unhashable, cannot be used as a dict key or set element.
try:
    bad_key = {[1, 2]: "oops"}
except TypeError as exc:
    print("Cannot use list as dict key:", exc)

# ---------------------------------------------------------------------------
# 7. Named tuples
# ---------------------------------------------------------------------------
Point = namedtuple("Point", ["x", "y"])
p1 = Point(3, 4)
print("named tuple:", p1)
print("access by name: x =", p1.x, "y =", p1.y)
print("access by index: p1[0] =", p1[0], "p1[1] =", p1[1])

# Named tuples still support all normal tuple operations.
px, py = p1
print("unpacked named tuple:", px, py)

# _replace() returns a new named tuple with updated fields (immutability
# preserved - the original is untouched).
p2 = p1._replace(x=10)
print("p1 (unchanged):", p1)
print("p2 (replaced):", p2)

print("as dict:", p1._asdict())

# Key takeaways:
# - Tuples are ordered and immutable; a single-element tuple needs a
#   trailing comma, e.g. (5,), or it is just a plain value.
# - Attempting to modify a tuple raises TypeError, but a mutable object
#   stored inside a tuple can still be changed in place.
# - Packing/unpacking (including extended unpacking with *) makes multiple
#   assignment and multi-value returns concise and readable.
# - Because tuples are hashable, they can be used as dictionary keys or set
#   members, unlike lists.
# - collections.namedtuple gives tuples readable, named field access while
#   keeping full tuple compatibility and immutability.
