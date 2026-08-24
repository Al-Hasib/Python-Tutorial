"""
Functional Programming Patterns

Functional programming favors pure functions (no side effects, same input
always gives same output) and immutable data over mutating shared state. This
style makes code easier to reason about, test, and parallelize. Python is not
a purely functional language, but its standard library -- especially
`functools` and `itertools` -- gives you powerful tools to write concise,
declarative data-processing pipelines. Learning these tools helps you replace
verbose manual loops with clear, composable expressions.

This file covers:
- Pure functions and the immutability mindset (recap)
- functools.reduce, functools.partial, functools.lru_cache
- itertools: chain, count, cycle (with a limit), groupby, permutations,
  combinations, islice
- Combining these tools for practical data-processing examples
"""

from functools import reduce, partial, lru_cache
import itertools

# ---------------------------------------------------------------------------
# 1. Pure functions and immutability (recap)
# ---------------------------------------------------------------------------
# A pure function's output depends only on its inputs, and it has no
# observable side effects (no mutating external state, no I/O).

def impure_add_to_list(lst, item):
    lst.append(item)  # mutates the input -- a side effect!
    return lst


def pure_add_to_list(lst, item):
    return lst + [item]  # returns a new list, leaves the original untouched


original = [1, 2, 3]
new_list = pure_add_to_list(original, 4)
print("Pure function: original untouched:", original, "| new:", new_list)

original2 = [1, 2, 3]
impure_add_to_list(original2, 4)
print("Impure function: original mutated:", original2)

# Preferring pure functions and treating data as immutable makes programs
# easier to test (no hidden state) and safer to run concurrently.

# ---------------------------------------------------------------------------
# 2. functools.reduce
# ---------------------------------------------------------------------------
# reduce(function, iterable, initial) repeatedly applies function(acc, item)
# to fold an iterable down to a single value.

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers, 0)
product = reduce(lambda acc, x: acc * x, numbers, 1)
maximum = reduce(lambda acc, x: acc if acc > x else x, numbers)

print("\nfunctools.reduce:")
print("  sum via reduce:", total)
print("  product via reduce:", product)
print("  max via reduce:", maximum)

# ---------------------------------------------------------------------------
# 3. functools.partial
# ---------------------------------------------------------------------------
# partial() freezes some arguments of a function, producing a new callable
# with fewer parameters -- great for specializing generic functions.

def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print("\nfunctools.partial:")
print("  square(5) =", square(5))
print("  cube(2) =", cube(2))

is_positive = partial(lambda threshold, x: x > threshold, 0)
print("  is_positive(5):", is_positive(5), "| is_positive(-3):", is_positive(-3))

# ---------------------------------------------------------------------------
# 4. functools.lru_cache
# ---------------------------------------------------------------------------
# lru_cache memoizes a function's results, avoiding recomputation for
# previously seen arguments -- ideal for expensive, pure (deterministic)
# functions like recursive Fibonacci.

call_count = 0


@lru_cache(maxsize=None)
def fib(n):
    global call_count
    call_count += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


result = fib(20)
print("\nfunctools.lru_cache:")
print("  fib(20) =", result, "| underlying calls made:", call_count)
print("  fib.cache_info():", fib.cache_info())
# Calling fib(20) again reuses the cache -- no new underlying calls.
fib(20)
print("  after calling fib(20) again, calls made:", call_count)

# ---------------------------------------------------------------------------
# 5. itertools basics: chain, count, cycle, islice
# ---------------------------------------------------------------------------
# chain: flattens several iterables into one sequence, lazily.
chained = list(itertools.chain([1, 2], [3, 4], [5]))
print("\nitertools.chain([1,2],[3,4],[5]):", chained)

# count: an infinite counter -- must be limited (e.g. with islice) to be safe.
first_five_counts = list(itertools.islice(itertools.count(start=10, step=5), 5))
print("itertools.count(10, step=5) first 5 via islice:", first_five_counts)

# cycle: repeats a sequence forever -- always pair with islice or a break.
first_seven_cycled = list(itertools.islice(itertools.cycle(["A", "B", "C"]), 7))
print("itertools.cycle(['A','B','C']) first 7 via islice:", first_seven_cycled)

# ---------------------------------------------------------------------------
# 6. itertools: groupby, permutations, combinations
# ---------------------------------------------------------------------------
# groupby groups CONSECUTIVE items sharing a key -- input is usually sorted
# first if you want all equal items grouped together.
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
grouped = {
    key: list(group)
    for key, group in itertools.groupby(words, key=lambda w: w[0])
}
print("\nitertools.groupby by first letter:", grouped)

# permutations: all orderings of a given length.
perms = list(itertools.permutations(["a", "b", "c"], 2))
print("itertools.permutations(['a','b','c'], 2):", perms)

# combinations: all unordered selections of a given length (no repeats).
combos = list(itertools.combinations([1, 2, 3, 4], 2))
print("itertools.combinations([1,2,3,4], 2):", combos)

# ---------------------------------------------------------------------------
# 7. Combining these tools: practical data-processing examples
# ---------------------------------------------------------------------------
# Example: process sales records using map/filter + reduce, functional style.
sales = [
    {"product": "Widget", "amount": 25.0},
    {"product": "Gadget", "amount": 40.0},
    {"product": "Widget", "amount": 15.0},
    {"product": "Gizmo", "amount": 60.0},
]

# Total revenue from sales over $20, computed without an explicit for-loop body.
big_sales_total = reduce(
    lambda acc, sale: acc + sale["amount"],
    filter(lambda s: s["amount"] > 20, sales),
    0.0,
)
print("\nTotal revenue from sales over $20:", big_sales_total)

# Group sales by product name (sort first since groupby needs consecutive keys).
sorted_sales = sorted(sales, key=lambda s: s["product"])
by_product = {
    product: [s["amount"] for s in group]
    for product, group in itertools.groupby(sorted_sales, key=lambda s: s["product"])
}
print("Sales amounts grouped by product:", by_product)

# Combine chain + reduce: merge multiple batches of numbers and sum them all.
batch1, batch2, batch3 = [1, 2, 3], [4, 5], [6, 7, 8, 9]
grand_total = reduce(lambda acc, x: acc + x, itertools.chain(batch1, batch2, batch3), 0)
print("Grand total across chained batches:", grand_total)

# Key takeaways:
# - Pure functions (no side effects, deterministic output) and immutable data
#   make code easier to reason about, test, and safely share across contexts.
# - functools.reduce folds an iterable to one value; functools.partial freezes
#   arguments to specialize a function; functools.lru_cache memoizes pure calls.
# - itertools provides lazy, memory-efficient building blocks (chain, count,
#   cycle, groupby, permutations, combinations, islice) for iteration patterns.
# - Infinite iterators (count, cycle) must always be bounded, typically with
#   itertools.islice or a break condition.
# - These tools compose well together to express data pipelines declaratively,
#   often replacing multi-line manual loops with a single expression.
