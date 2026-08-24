"""
Performance Optimization & Profiling

Before optimizing anything, you need to measure it -- guessing where a
program is slow is notoriously unreliable. Python provides several tools for
this: `time.perf_counter` for quick manual timing, the `timeit` module for
precise micro-benchmarks of small code snippets, and `cProfile` for finding
which functions consume the most time in a larger program. Once you know
where the time actually goes, common techniques like avoiding repeated work
in loops, using built-in functions, and choosing the right data structure
usually give the biggest wins for the least amount of code churn.

This file covers:
- Measuring elapsed time with time.perf_counter
- Precise micro-benchmarks with the timeit module
- Profiling a function with cProfile and printing stats
- Common optimization techniques (loops, built-ins, comprehensions, data
  structure choice)
- A before/after optimization example with a timing comparison
"""

import time
import timeit
import cProfile
import pstats
import io

# ---------------------------------------------------------------------------
# 1. Measuring time with time.perf_counter
# ---------------------------------------------------------------------------
# perf_counter() gives a high-resolution monotonic clock, ideal for timing
# code -- always take a difference between two readings, never trust the
# raw value alone.

def slow_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total


start = time.perf_counter()
slow_sum(500_000)
elapsed = time.perf_counter() - start
print("time.perf_counter timing:")
print(f"  slow_sum(500_000) took {elapsed:.6f}s")

# ---------------------------------------------------------------------------
# 2. Precise micro-benchmarks with timeit
# ---------------------------------------------------------------------------
# timeit runs a snippet many times and reports total/average time, avoiding
# noise from a single measurement. It's best for small, isolated snippets.

loop_time = timeit.timeit(
    "sum(i for i in range(1000))",
    number=1000,
)
builtin_time = timeit.timeit(
    "sum(range(1000))",
    number=1000,
)

print("\ntimeit micro-benchmark (1000 repetitions each):")
print(f"  generator expression + sum(): {loop_time:.6f}s total")
print(f"  sum(range(1000)) directly:    {builtin_time:.6f}s total")
print("  -> the built-in range+sum path is typically faster (less per-item overhead).")

# ---------------------------------------------------------------------------
# 3. Profiling with cProfile
# ---------------------------------------------------------------------------
# cProfile measures how much time is spent in EACH function call across a
# whole run -- useful for finding hot spots in larger programs, not just one
# line of code.

def compute_squares(n):
    return [i * i for i in range(n)]


def compute_sum_of_squares(n):
    return sum(compute_squares(n))


def example_workload():
    total = 0
    for _ in range(50):
        total += compute_sum_of_squares(2000)
    return total


print("\ncProfile output for example_workload():")
profiler = cProfile.Profile()
profiler.enable()
example_workload()
profiler.disable()

stats_stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stats_stream).sort_stats("cumulative")
stats.print_stats(5)  # top 5 entries by cumulative time
print(stats_stream.getvalue())

# ---------------------------------------------------------------------------
# 4. Common optimization techniques
# ---------------------------------------------------------------------------
print("Common optimization techniques:")
print("  - Avoid recomputing the same value inside a loop; hoist it out.")
print("  - Prefer built-in functions (sum, min, max, sorted) -- they're implemented")
print("    in C and are usually faster than an equivalent manual Python loop.")
print("  - List/dict/set comprehensions are typically faster than an equivalent")
print("    for-loop with .append()/[]=, due to fewer bytecode operations.")
print("  - Choose the right data structure: use a set/dict for membership tests")
print("    (O(1) average) instead of a list (O(n) per check).")

# ---------------------------------------------------------------------------
# 5. Before/after example: avoiding repeated work + right data structure
# ---------------------------------------------------------------------------
# "Before": a naive membership-check loop using a list, and recomputing len()
# in a way that involves function-call overhead each iteration inside a loop.

data = list(range(20_000))
lookup_targets = list(range(0, 20_000, 137))  # values to check membership for


def before_version(data_list, targets):
    found = []
    for target in targets:
        # Membership check against a LIST is O(n) -- slow for many checks.
        if target in data_list:
            found.append(target)
    return found


def after_version(data_list, targets):
    data_set = set(data_list)  # build once: membership check becomes O(1) average
    found = [target for target in targets if target in data_set]  # comprehension
    return found


print("\nBefore/after optimization: list membership vs set membership")

start = time.perf_counter()
before_result = before_version(data, lookup_targets)
before_time = time.perf_counter() - start
print(f"  Before (list membership, loop + append): {before_time:.6f}s")

start = time.perf_counter()
after_result = after_version(data, lookup_targets)
after_time = time.perf_counter() - start
print(f"  After  (set membership, comprehension):  {after_time:.6f}s")

print("  Results match:", before_result == after_result)
if after_time > 0:
    print(f"  Speedup: ~{before_time / after_time:.1f}x faster after optimization")

# Key takeaways:
# - Always measure before optimizing: time.perf_counter for quick checks,
#   timeit for precise micro-benchmarks of small snippets.
# - cProfile (with pstats) shows where time is actually spent across function
#   calls in a larger program -- profile before guessing what to optimize.
# - Prefer built-in functions and comprehensions over manual loops where
#   possible; they are usually faster and more readable.
# - Choosing the right data structure (set/dict for membership tests instead
#   of a list) often gives the single biggest algorithmic speedup.
# - Avoid recomputing the same value repeatedly inside a loop -- compute it
#   once outside the loop when it does not change per iteration.
