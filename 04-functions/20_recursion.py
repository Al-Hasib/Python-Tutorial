"""
Recursion

Recursion is a technique where a function calls itself to solve smaller
instances of the same problem, until it reaches a "base case" simple enough
to answer directly. Every recursive function needs a base case (to stop the
recursion) and a recursive case (that makes progress toward the base case).
Recursion can express certain problems -- especially ones with a naturally
nested or self-similar structure -- more elegantly than loops, but it comes
with tradeoffs: each call uses stack space, and without memoization, naive
recursive solutions can be very slow.

This file covers:
- Base case and recursive case
- Simple examples: factorial, Fibonacci, sum of a list
- Recursion vs iteration tradeoffs
- Stack depth, `RecursionError`, and `sys.setrecursionlimit`
- Memoization intro with `functools.lru_cache` to speed up recursive Fibonacci
"""

import sys
from functools import lru_cache

# ---------------------------------------------------------------------------
# 1. Base case and recursive case
# ---------------------------------------------------------------------------

# Every correct recursive function needs:
#   - a BASE CASE: a simple condition where the function returns a result
#     directly, without calling itself (this stops infinite recursion).
#   - a RECURSIVE CASE: where the function calls itself with a smaller or
#     simpler version of the problem, making progress toward the base case.
def count_down(n):
    if n <= 0:          # base case
        print("Done!")
        return
    print(n)
    count_down(n - 1)   # recursive case: smaller problem (n - 1)


print("count_down(3):")
count_down(3)


# ---------------------------------------------------------------------------
# 2. Example: factorial
# ---------------------------------------------------------------------------

# factorial(n) = n * (n-1) * (n-2) * ... * 1, with factorial(0) = 1
def factorial(n):
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:               # base case
        return 1
    return n * factorial(n - 1)  # recursive case


print("\nfactorial(5):", factorial(5))   # 5*4*3*2*1 = 120
print("factorial(0):", factorial(0))     # base case directly
print("factorial(7):", factorial(7))


# ---------------------------------------------------------------------------
# 3. Example: Fibonacci
# ---------------------------------------------------------------------------

# Fibonacci: fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)
def fib(n):
    if n < 2:                    # base cases: fib(0)=0, fib(1)=1
        return n
    return fib(n - 1) + fib(n - 2)  # recursive case


print("\nFirst 10 Fibonacci numbers:")
print([fib(i) for i in range(10)])


# ---------------------------------------------------------------------------
# 4. Example: sum of a list, recursively
# ---------------------------------------------------------------------------

def recursive_sum(numbers):
    if not numbers:              # base case: empty list sums to 0
        return 0
    return numbers[0] + recursive_sum(numbers[1:])  # recursive case


print("\nrecursive_sum([1, 2, 3, 4, 5]):", recursive_sum([1, 2, 3, 4, 5]))
print("recursive_sum([]):", recursive_sum([]))


# ---------------------------------------------------------------------------
# 5. Recursion vs iteration tradeoffs
# ---------------------------------------------------------------------------

# The same problems can usually be solved iteratively, often more
# efficiently in Python since loops avoid function-call overhead and
# stack growth.
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print("\nfactorial_iterative(5):", factorial_iterative(5))

# Tradeoffs:
# - Recursion can express self-similar problems (trees, divide-and-conquer)
#   more naturally and readably.
# - Iteration is usually faster and uses constant stack space (no risk of
#   deep call stacks), which matters for large inputs.
# - Recursive calls carry function-call overhead: each call adds a "stack
#   frame" that must be kept in memory until it returns.


# ---------------------------------------------------------------------------
# 6. Stack depth, RecursionError, and sys.setrecursionlimit
# ---------------------------------------------------------------------------

# Python limits how deeply functions can call each other (the "recursion
# limit"), as protection against runaway recursion crashing the interpreter.
print("\nCurrent recursion limit:", sys.getrecursionlimit())


def count_up_forever(n):
    return 1 + count_up_forever(n + 1)  # no base case -- always recurses!


try:
    count_up_forever(0)
except RecursionError as e:
    print("Caught RecursionError:", e)

# You CAN raise the limit with sys.setrecursionlimit(), but doing so just
# moves the ceiling higher -- it does not fix an unbounded recursion, and
# setting it too high risks crashing the real C stack instead of getting a
# clean Python exception.
sys.setrecursionlimit(3000)
print("New recursion limit:", sys.getrecursionlimit())
sys.setrecursionlimit(1000)  # restore a sane default for the rest of the demo
print("Restored recursion limit:", sys.getrecursionlimit())


# ---------------------------------------------------------------------------
# 7. Memoization with functools.lru_cache to speed up recursive Fibonacci
# ---------------------------------------------------------------------------

# The naive `fib(n)` above recomputes the same sub-problems many times
# (e.g. fib(5) calls fib(3) twice, fib(2) three times, etc.), making it
# exponentially slow for larger n. Memoization caches results of previous
# calls so each unique sub-problem is computed only once.
@lru_cache(maxsize=None)
def fib_memoized(n):
    if n < 2:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)


print("\nfib_memoized(30):", fib_memoized(30))  # instant, thanks to caching
print("Cache info:", fib_memoized.cache_info())

# Without memoization, fib(30) via the naive version is noticeably slower
# because of repeated recomputation (try increasing n in `fib()` above to
# see it slow down).
print("Naive fib(20) for comparison:", fib(20))


# Key takeaways:
# - Every recursive function needs a base case (stops recursion) and a recursive case (makes progress toward it).
# - Classic recursive examples: factorial, Fibonacci, and summing a list, each with a clear base/recursive case split.
# - Recursion can be more readable for self-similar problems, but iteration is often faster and uses less stack space.
# - Python enforces a recursion limit (see sys.getrecursionlimit/setrecursionlimit); missing base cases cause RecursionError.
# - functools.lru_cache adds memoization, turning exponential naive recursive Fibonacci into a fast, linear-time computation.
