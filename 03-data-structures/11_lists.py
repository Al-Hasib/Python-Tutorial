"""
Lists in Python
================
A list is Python's general-purpose, ordered, mutable collection type. Lists
can hold items of any type (even mixed types), grow and shrink at runtime,
and be indexed, sliced, and iterated like other sequences. Because lists are
mutable, understanding how copies behave (shallow vs deep) is essential to
avoid subtle bugs. Lists and list comprehensions are used constantly in
everyday Python code for filtering, transforming, and collecting data.

This file covers:
    - Creating lists
    - Indexing and slicing
    - Mutability
    - Common list methods (append, extend, insert, remove, pop, sort,
      reverse, index, count, clear, copy)
    - Nesting lists
    - List comprehensions (basic, with condition, nested)
    - Copying pitfalls (shallow copy vs copy.deepcopy)
"""

import copy

# ---------------------------------------------------------------------------
# 1. Creating lists
# ---------------------------------------------------------------------------
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True, None]
from_range = list(range(5))

print("empty_list:", empty_list)
print("numbers:", numbers)
print("mixed:", mixed)
print("from_range:", from_range)

# ---------------------------------------------------------------------------
# 2. Indexing and slicing
# ---------------------------------------------------------------------------
letters = ["a", "b", "c", "d", "e"]

print("first item:", letters[0])
print("last item:", letters[-1])
print("slice [1:3]:", letters[1:3])
print("slice [:3]:", letters[:3])
print("slice [2:]:", letters[2:])
print("slice with step [::2]:", letters[::2])
print("reversed via slice [::-1]:", letters[::-1])

# ---------------------------------------------------------------------------
# 3. Mutability
# ---------------------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"  # lists can be changed in place
print("after item assignment:", fruits)

fruits[0:2] = ["kiwi", "mango"]  # slice assignment
print("after slice assignment:", fruits)

# ---------------------------------------------------------------------------
# 4. Common list methods
# ---------------------------------------------------------------------------
nums = [3, 1, 4, 1, 5]

nums.append(9)          # add single item at the end
print("append:", nums)

nums.extend([2, 6])     # add all items from another iterable
print("extend:", nums)

nums.insert(0, 100)     # insert at a specific index
print("insert:", nums)

nums.remove(1)          # remove first occurrence of value
print("remove(1):", nums)

popped = nums.pop()     # remove and return last item
print("pop():", popped, "->", nums)

popped_index = nums.pop(0)  # remove and return item at index
print("pop(0):", popped_index, "->", nums)

print("index of 4:", nums.index(4))
print("count of 1:", nums.count(1))

nums.sort()              # sort in place, ascending
print("sort:", nums)

nums.sort(reverse=True)  # sort in place, descending
print("sort(reverse=True):", nums)

nums.reverse()           # reverse in place
print("reverse:", nums)

nums_copy = nums.copy()  # shallow copy
print("copy:", nums_copy)

nums.clear()             # remove all items
print("clear:", nums)

# ---------------------------------------------------------------------------
# 5. Nesting lists
# ---------------------------------------------------------------------------
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print("matrix:", matrix)
print("element at row 1, col 2:", matrix[1][2])

for row in matrix:
    print("row:", row)

# ---------------------------------------------------------------------------
# 6. List comprehensions
# ---------------------------------------------------------------------------
# Basic comprehension: transform each item
squares = [x * x for x in range(10)]
print("squares:", squares)

# Comprehension with a condition (filter)
even_squares = [x * x for x in range(10) if x % 2 == 0]
print("even_squares:", even_squares)

# Nested comprehension: flatten a matrix into a single list
flattened = [value for row in matrix for value in row]
print("flattened matrix:", flattened)

# Nested comprehension: build a fresh matrix (e.g. transpose-like structure)
grid = [[r * 3 + c for c in range(3)] for r in range(3)]
print("generated grid:", grid)

# ---------------------------------------------------------------------------
# 7. Copying pitfalls: shallow copy vs deep copy
# ---------------------------------------------------------------------------
original = [[1, 2], [3, 4]]

# A plain assignment does NOT copy - both names point to the same list.
alias = original
alias[0][0] = "changed"
print("original after aliasing:", original)  # affected too!

# Reset for the next demo
original = [[1, 2], [3, 4]]

# A shallow copy creates a new outer list, but inner lists are still shared.
shallow = original.copy()  # equivalent to list(original) or original[:]
shallow[0][0] = "shallow-changed"
print("original after shallow copy mutation:", original)  # inner list changed!
print("shallow copy:", shallow)

# A deep copy duplicates everything, including nested objects.
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = "deep-changed"
print("original after deepcopy mutation:", original)  # unaffected
print("deep copy:", deep)

# Key takeaways:
# - Lists are ordered, mutable sequences that can hold mixed types.
# - Indexing/slicing works like other sequences; slice assignment can
#   replace multiple elements at once.
# - Methods like append, extend, insert, remove, pop, sort, reverse mutate
#   the list in place, while index/count only inspect it.
# - list.copy() (or slicing) makes a shallow copy - nested mutable objects
#   are still shared; use copy.deepcopy() to fully duplicate nested data.
# - List comprehensions are a concise, readable way to build lists, with
#   optional filtering conditions and support for nested loops.
