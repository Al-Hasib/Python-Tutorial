"""
Nested Loops and Loop Patterns

A nested loop is a loop placed inside the body of another loop, letting a
program repeat an action for every combination of two (or more) sequences.
Nested loops are the natural tool for working with grids, matrices, tables,
and printed patterns, where an "outer" iteration (e.g. rows) contains an
"inner" iteration (e.g. columns). They are also common when comparing every
item in a collection against every other item, such as finding pairs. Because
nested loops multiply the amount of work performed, understanding their
performance and readability trade-offs -- and how to break out of them
cleanly -- is an important practical skill.

This file covers:
- Nested for loops
- Grids/matrices and simple patterns (e.g. a triangle of stars)
- Breaking out of nested loops (flag variable / function-return technique)
- Loop performance and readability considerations
- Finding pairs and building a multiplication table
"""

# ---------------------------------------------------------------------------
# 1. Nested for loops basics
# ---------------------------------------------------------------------------
# The inner loop runs completely for every single iteration of the outer loop.

for outer in range(3):
    for inner in range(2):
        print(f"outer={outer}, inner={inner}")

# This means the inner loop's total number of runs is outer_count * inner_count.
total_runs = 0
for outer in range(3):
    for inner in range(2):
        total_runs += 1
print(f"Total inner iterations: {total_runs}")

# ---------------------------------------------------------------------------
# 2. Grids, matrices, and coordinate iteration
# ---------------------------------------------------------------------------
# Nested loops naturally express 2D structures: rows and columns.

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

for row in matrix:
    for value in row:
        print(value, end=" ")
    print()  # newline after each row

# Using indices instead of direct values is useful when you need coordinates.
rows = len(matrix)
cols = len(matrix[0])
for r in range(rows):
    for c in range(cols):
        print(f"matrix[{r}][{c}] = {matrix[r][c]}")

# Building a grid of coordinates, e.g. all (x, y) pairs on a small board.
board_size = 3
coordinates = []
for x in range(board_size):
    for y in range(board_size):
        coordinates.append((x, y))
print(f"All coordinates: {coordinates}")

# ---------------------------------------------------------------------------
# 3. Simple patterns: triangle of stars
# ---------------------------------------------------------------------------
# The outer loop controls the row number; the inner loop controls how many
# characters get printed on that row.

height = 5
for row in range(1, height + 1):
    for _ in range(row):
        print("*", end="")
    print()  # move to next line after each row

print()  # blank line separator

# An inverted triangle reverses the row counting.
for row in range(height, 0, -1):
    print("*" * row)  # string multiplication is a shortcut for the inner loop

print()

# A simple number pyramid combining nested loops with string formatting.
for row in range(1, 5):
    spaces = " " * (4 - row)
    print(spaces + " ".join(str(n) for n in range(1, row + 1)))

# ---------------------------------------------------------------------------
# 4. Breaking out of nested loops
# ---------------------------------------------------------------------------
# A plain `break` only exits the innermost loop. To stop BOTH loops, use a
# flag variable, or put the loops in a function and `return` from it.

# Technique 1: a flag variable checked by the outer loop.
target_value = 5
found = False
for row in matrix:
    for value in row:
        if value == target_value:
            found = True
            break  # only exits the inner loop
    if found:
        break  # outer loop checks the flag and exits too
print(f"Flag technique: found {target_value}? {found}")


# Technique 2: wrap the nested loops in a function and use `return`, which
# exits both loops immediately and can hand back the result directly.
def find_value(grid, target):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == target:
                return (r, c)  # returning exits all nested loops at once
    return None


position = find_value(matrix, 8)
print(f"Function technique: 8 found at position {position}")

# ---------------------------------------------------------------------------
# 5. Performance and readability considerations
# ---------------------------------------------------------------------------
# Nested loops have multiplicative cost: two loops of size n each mean
# roughly n * n = n^2 operations. This is fine for small inputs but can
# become slow as sizes grow, so it's worth being aware of the loop depth.

small_n = 20
operation_count = 0
for i in range(small_n):
    for j in range(small_n):
        operation_count += 1
print(f"{small_n} x {small_n} nested loop performs {operation_count} operations")

# Readability tip: deeply nested loops (3+ levels) are hard to follow.
# Extracting the inner logic into a well-named function keeps each loop
# shallow and the intent clear, as shown with find_value() above.

# Readability tip: prefer list comprehensions for simple nested constructions
# when a plain loop would only be building a list.
flattened = [value for row in matrix for value in row]
print(f"Flattened matrix via comprehension: {flattened}")

# ---------------------------------------------------------------------------
# 6. Finding pairs
# ---------------------------------------------------------------------------
# A classic nested-loop use case: comparing every item against every other
# item to find pairs that satisfy some condition.

numbers = [2, 4, 7, 5, 3, 8]
pair_target_sum = 10
pairs_found = []

for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):  # start at i+1 to avoid duplicate/self pairs
        if numbers[i] + numbers[j] == pair_target_sum:
            pairs_found.append((numbers[i], numbers[j]))

print(f"Pairs that sum to {pair_target_sum}: {pairs_found}")

# ---------------------------------------------------------------------------
# 7. Building a multiplication table
# ---------------------------------------------------------------------------
# A multiplication table is a straightforward and common nested-loop example.

table_size = 5
for i in range(1, table_size + 1):
    for j in range(1, table_size + 1):
        product = i * j
        print(f"{product:4}", end="")
    print()  # newline after each row of the table

# Key takeaways:
# - Nested loops run the inner loop completely for every outer iteration,
#   which is ideal for grids, matrices, and multi-dimensional data.
# - Printed patterns (triangles, pyramids) come from tying inner-loop counts
#   to the outer loop's current row.
# - A plain break only exits the innermost loop; use a flag variable or
#   wrap the loops in a function and return to exit all levels at once.
# - Nested loops cost roughly n^2 (or worse) operations, so watch loop depth
#   and input size, and extract inner logic into functions for readability.
# - Comparing every pair of items (finding pairs) and building tables
#   (multiplication table) are classic, practical nested-loop patterns.
