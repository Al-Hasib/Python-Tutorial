"""
Iterators & Generators
=======================

An iterable is any object you can loop over, and an iterator is the object
that actually produces values one at a time when asked. Python's for-loops,
comprehensions, and many built-in functions all rely on the "iterator
protocol" behind the scenes. Generators are a shortcut for writing iterators
using ordinary function syntax with the `yield` keyword, and they are lazy:
values are produced only when requested, which can save a huge amount of
memory compared to building a full list up front. Understanding this
machinery helps you write memory-efficient, composable data pipelines.

This file covers:
- The iterator protocol (__iter__ / __next__)
- Building a custom iterator class
- iter() and next() built-ins
- Generator functions with yield
- Generator expressions
- Lazy evaluation and memory efficiency vs lists
- StopIteration
- Chaining generators
- A light touch on send() and early exit
"""

# ---------------------------------------------------------------------------
# 1. The iterator protocol
# ---------------------------------------------------------------------------
# An "iterable" implements __iter__, which returns an "iterator".
# An "iterator" implements __next__, which returns the next value, and raises
# StopIteration when there is nothing left.

numbers = [1, 2, 3]
print("Is a list iterable? ->", hasattr(numbers, "__iter__"))

iterator = iter(numbers)  # calls numbers.__iter__()
print("Type of iterator:", type(iterator))
print("next(iterator):", next(iterator))
print("next(iterator):", next(iterator))
print("next(iterator):", next(iterator))

# ---------------------------------------------------------------------------
# 2. Building a custom iterator class
# ---------------------------------------------------------------------------
class CountUp:
    """A custom iterator that counts up from `start` to `end` (inclusive)."""

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start

    def __iter__(self):
        # An iterator's __iter__ usually just returns itself.
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


print("\nCustom iterator CountUp(1, 5):")
for n in CountUp(1, 5):
    print(" ", n)

# Using it manually with next() shows the StopIteration explicitly.
manual = CountUp(1, 2)
print("manual next:", next(manual))
print("manual next:", next(manual))
try:
    next(manual)
except StopIteration:
    print("StopIteration raised when the iterator is exhausted")

# ---------------------------------------------------------------------------
# 3. iter() with a sentinel (bonus form of iter())
# ---------------------------------------------------------------------------
# iter(callable, sentinel) keeps calling `callable` until it returns sentinel.
counter = iter([10, 20, 30, "STOP", 40])
for value in iter(lambda: next(counter), "STOP"):
    print("iter-with-sentinel value:", value)

# ---------------------------------------------------------------------------
# 4. Generator functions with yield
# ---------------------------------------------------------------------------
# A function containing `yield` becomes a generator function. Calling it
# does not run the body -- it returns a generator object immediately.

def count_up(start, end):
    current = start
    while current <= end:
        yield current
        current += 1


gen = count_up(1, 3)
print("\nGenerator object:", gen)
print("Generator next():", next(gen))
print("Generator next():", next(gen))
print("Generator next():", next(gen))
try:
    next(gen)
except StopIteration:
    print("Generator exhausted -> StopIteration")

print("Looping over a fresh generator:")
for n in count_up(5, 8):
    print(" ", n)

# ---------------------------------------------------------------------------
# 5. Generator expressions
# ---------------------------------------------------------------------------
# Like a list comprehension, but with parentheses instead of brackets, and it
# produces values lazily instead of building the whole list immediately.
squares_list = [x * x for x in range(5)]        # eager, builds a full list
squares_gen = (x * x for x in range(5))         # lazy, builds a generator

print("\nList comprehension result:", squares_list)
print("Generator expression object:", squares_gen)
print("Generator expression values:", list(squares_gen))

# ---------------------------------------------------------------------------
# 6. Lazy evaluation and memory efficiency vs lists
# ---------------------------------------------------------------------------
import sys

big_list = [x for x in range(100_000)]
big_gen = (x for x in range(100_000))

print("\nMemory for a list of 100,000 ints: ~{} bytes".format(sys.getsizeof(big_list)))
print("Memory for a generator (any size):  ~{} bytes".format(sys.getsizeof(big_gen)))
print("The generator stays tiny because it computes values on demand,")
print("one at a time, instead of storing them all in memory at once.")

# ---------------------------------------------------------------------------
# 7. StopIteration in practice
# ---------------------------------------------------------------------------
# StopIteration is the normal signal that an iterator is done. for-loops
# catch it for you automatically; that's how `for x in gen:` knows to stop.

def first_n(iterable, n):
    """Take the first n items from any iterable using manual next() calls."""
    it = iter(iterable)
    result = []
    for _ in range(n):
        try:
            result.append(next(it))
        except StopIteration:
            break
    return result


print("\nfirst_n(count_up(1, 100), 4):", first_n(count_up(1, 100), 4))

# ---------------------------------------------------------------------------
# 8. Chaining generators
# ---------------------------------------------------------------------------
# Generators compose nicely: one generator can feed another, forming a lazy
# pipeline where nothing is computed until the final consumer asks for it.

def evens(iterable):
    for value in iterable:
        if value % 2 == 0:
            yield value


def doubled(iterable):
    for value in iterable:
        yield value * 2


pipeline = doubled(evens(count_up(1, 10)))
print("\nChained generator pipeline (evens then doubled):", list(pipeline))

# itertools.chain is the standard-library way to chain separate iterables.
import itertools

chained = itertools.chain(count_up(1, 2), count_up(10, 12))
print("itertools.chain result:", list(chained))

# ---------------------------------------------------------------------------
# 9. send() and early exit (light touch)
# ---------------------------------------------------------------------------
# Generators can also receive values via send(), turning yield into an
# expression. This is an advanced feature -- most code never needs it -- but
# it's useful to know it exists for coroutine-style generators.

def running_total():
    total = 0
    while True:
        value = yield total
        if value is None:
            continue
        total += value


acc = running_total()
next(acc)  # prime the generator up to the first yield
print("\nsend(5) ->", acc.send(5))
print("send(10) ->", acc.send(10))

# A generator can be closed early with .close(), which raises GeneratorExit
# inside it. This is how "for ... break" cleans up a generator early.
acc.close()
print("Generator closed early with .close()")

# Key takeaways:
# - Iterables provide __iter__; iterators provide __next__ and raise
#   StopIteration when exhausted -- that is the whole iterator protocol.
# - Any function using `yield` becomes a generator function: calling it
#   returns a lazy generator object instead of running the body immediately.
# - Generator expressions look like list comprehensions but use () and stay
#   lazy, which makes them far more memory-efficient for large sequences.
# - Generators compose naturally into pipelines, and itertools.chain is the
#   standard tool for chaining multiple iterables together.
# - send() and close() exist for advanced coroutine-like use cases, but plain
#   yield-based generators cover the vast majority of real-world needs.
