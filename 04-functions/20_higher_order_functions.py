"""
Higher-Order Functions

In Python, functions are "first-class objects": they can be assigned to
variables, stored in data structures, passed as arguments to other
functions, and returned from other functions -- just like any other value.
A "higher-order function" is a function that takes one or more functions as
arguments, returns a function, or both. This pattern underlies powerful
tools like `map()`, `filter()`, and `functools.reduce()`, and lets you write
flexible, reusable code that separates "what to do" (the function) from
"how/when to do it" (the higher-order function).

This file covers:
- Functions as first-class objects (assigning to variables, passing as arguments, returning from functions)
- `map()`
- `filter()`
- `functools.reduce()`
- Writing your own higher-order function (e.g. apply a function n times)
- Closures recap
"""

from functools import reduce

# ---------------------------------------------------------------------------
# 1. Functions as first-class objects
# ---------------------------------------------------------------------------

# Assigning a function to a variable: the variable now refers to the same
# function object, and can be called through that name.
def shout(text):
    return text.upper() + "!"


yell = shout  # no parentheses -- we're referring to the function itself
print("Calling via original name:", shout("hello"))
print("Calling via new variable name:", yell("hello"))
print("Are they the same object?", shout is yell)


# Passing a function as an argument to another function.
def apply_function(func, value):
    """Call func with value and return the result."""
    return func(value)


print("\napply_function(shout, 'hi'):", apply_function(shout, "hi"))
print("apply_function(str.lower, 'HI'):", apply_function(str.lower, "HI"))


# Returning a function from another function.
def make_multiplier(factor):
    """Return a new function that multiplies its input by `factor`."""
    def multiplier(number):
        return number * factor
    return multiplier


double = make_multiplier(2)
triple = make_multiplier(3)
print("\ndouble(5):", double(5))
print("triple(5):", triple(5))


# ---------------------------------------------------------------------------
# 2. map()
# ---------------------------------------------------------------------------

# map(function, iterable) applies `function` to every element, returning
# an iterator of results.
numbers = [1, 2, 3, 4, 5]


def square(n):
    return n * n


squared = list(map(square, numbers))
print("\nSquared with map():", squared)

# map() can also take multiple iterables, passing one item from each to
# the function.
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print("Element-wise sums with map():", sums)


# ---------------------------------------------------------------------------
# 3. filter()
# ---------------------------------------------------------------------------

# filter(function, iterable) keeps only the elements for which `function`
# returns a truthy value.
def is_even(n):
    return n % 2 == 0


evens = list(filter(is_even, numbers))
print("\nEvens with filter():", evens)

words = ["sky", "apple", "ox", "banana", "it"]
long_words = list(filter(lambda w: len(w) > 2, words))
print("Words longer than 2 letters:", long_words)


# ---------------------------------------------------------------------------
# 4. functools.reduce()
# ---------------------------------------------------------------------------

# reduce(function, iterable, [initializer]) repeatedly applies a function
# of two arguments, cumulatively, to reduce an iterable to a single value.
total = reduce(lambda acc, n: acc + n, numbers)
print("\nSum via reduce():", total)

product = reduce(lambda acc, n: acc * n, numbers)
print("Product via reduce():", product)

# Using an initializer sets the starting value for the accumulator.
total_with_start = reduce(lambda acc, n: acc + n, numbers, 100)
print("Sum via reduce() starting at 100:", total_with_start)

# reduce() can build up more complex results too, e.g. finding the longest word.
longest = reduce(lambda a, b: a if len(a) >= len(b) else b, words)
print("Longest word via reduce():", longest)


# ---------------------------------------------------------------------------
# 5. Writing your own higher-order function: apply a function n times
# ---------------------------------------------------------------------------

def apply_n_times(func, value, n):
    """Apply func to value, repeatedly, n times, and return the final result."""
    result = value
    for _ in range(n):
        result = func(result)
    return result


increment = lambda x: x + 1
print("\napply_n_times(increment, 0, 5):", apply_n_times(increment, 0, 5))
print("apply_n_times(double, 1, 4):", apply_n_times(double, 1, 4))  # 1*2*2*2*2 = 16


def shout_twice_example():
    return apply_n_times(shout, "go", 1)


print("apply_n_times(shout, 'go', 1):", shout_twice_example())


# ---------------------------------------------------------------------------
# 6. Closures recap
# ---------------------------------------------------------------------------

# A closure is a function that "remembers" variables from the enclosing
# scope in which it was created, even after that outer function has
# finished running. `make_multiplier()` above is a closure: `multiplier`
# remembers `factor` from `make_multiplier`'s scope.
def make_power_function(exponent):
    """Return a function that raises its input to `exponent`."""
    def power(base):
        return base ** exponent  # `exponent` is captured from the enclosing scope
    return power


square_fn = make_power_function(2)
cube_fn = make_power_function(3)

print("\nsquare_fn(4):", square_fn(4))
print("cube_fn(4):", cube_fn(4))

# Each call to make_power_function() creates a brand-new, independent
# closure -- square_fn and cube_fn do not interfere with each other even
# though they came from the "same" function definition.
print("square_fn and cube_fn are different objects:", square_fn is not cube_fn)


# Key takeaways:
# - Functions in Python are first-class objects: they can be assigned to variables, passed around, and returned from other functions.
# - `map()` transforms every item of an iterable; `filter()` keeps only items matching a condition; both take a function as an argument.
# - `functools.reduce()` cumulatively combines all items of an iterable into a single result using a two-argument function.
# - You can write your own higher-order functions, such as one that applies a given function repeatedly (n times) to a value.
# - A closure is a function that captures variables from its enclosing scope, letting factory-style functions like make_multiplier() produce independent, stateful-feeling functions.
