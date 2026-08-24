"""
Scope & Namespaces

Scope determines where in your code a variable name can be seen and used.
Python looks up names using the LEGB rule: Local, Enclosing, Global, then
Built-in. Understanding scope is essential for avoiding accidental name
clashes, knowing when a function can read or modify a variable, and writing
predictable code. The `global` and `nonlocal` keywords let you explicitly
opt in to modifying variables outside a function's local scope, but doing so
carelessly -- especially with global mutable state -- can make programs hard
to reason about and debug.

This file covers:
- Local vs global scope
- The LEGB rule (Local, Enclosing, Global, Built-in)
- The `global` keyword
- The `nonlocal` keyword with nested functions/closures
- Why global mutable state is risky
"""

# ---------------------------------------------------------------------------
# 1. Local vs global scope
# ---------------------------------------------------------------------------

# A variable created inside a function is "local" -- it only exists while
# the function runs and is not visible outside it.
def local_example():
    local_var = "I only exist inside this function"
    print(local_var)


local_example()
try:
    print(local_var)  # NameError: local_var doesn't exist out here
except NameError as e:
    print("Error accessing local_var outside function:", e)


# A variable created at the top level of a module is "global" -- it is
# visible everywhere in the module, including inside functions (for reading).
global_var = "I am visible everywhere in this module"


def read_global():
    print("Reading global_var inside a function:", global_var)


read_global()


# ---------------------------------------------------------------------------
# 2. The LEGB rule
# ---------------------------------------------------------------------------

# When Python looks up a name, it searches in this order:
#   L - Local:      names inside the current function
#   E - Enclosing:  names in any enclosing (outer) function
#   G - Global:      names at the top level of the module
#   B - Built-in:    names Python provides automatically (e.g. len, print)
x = "global x"


def outer():
    x = "enclosing x"

    def inner():
        x = "local x"
        print("Inside inner(), LEGB finds:", x)  # Local

    inner()
    print("Inside outer(), LEGB finds:", x)  # Enclosing (inner's x is gone)


outer()
print("At module level, LEGB finds:", x)  # Global

# Built-in example: `len` is not defined anywhere in this file, yet it works
# because Python falls back to the Built-in scope.
print("Built-in `len` on a string:", len("hello"))


# ---------------------------------------------------------------------------
# 3. The `global` keyword
# ---------------------------------------------------------------------------

# By default, assigning to a name inside a function creates a NEW local
# variable, even if a global variable of the same name exists. The `global`
# keyword tells Python: "use the global variable, don't make a local one."
counter = 0


def increment_without_global():
    counter = 100  # this creates a LOCAL variable, does not touch the global
    print("Inside function, local counter is:", counter)


increment_without_global()
print("Global counter is still:", counter)  # unchanged


def increment_with_global():
    global counter
    counter += 1  # this modifies the actual global variable


increment_with_global()
increment_with_global()
increment_with_global()
print("Global counter after global increments:", counter)


# ---------------------------------------------------------------------------
# 4. The `nonlocal` keyword with nested functions/closures
# ---------------------------------------------------------------------------

# `nonlocal` is like `global`, but for the nearest ENCLOSING function scope
# (not the module-level global scope). It's used with closures: a nested
# function that "remembers" variables from its enclosing function.
def make_counter():
    count = 0  # enclosing variable, captured by the closure

    def increment():
        nonlocal count  # without this, `count += 1` would raise an error
        count += 1
        return count

    return increment


counter_a = make_counter()
counter_b = make_counter()  # a completely separate closure with its own count

print("\nClosure counter_a:", counter_a())  # 1
print("Closure counter_a:", counter_a())  # 2
print("Closure counter_a:", counter_a())  # 3
print("Closure counter_b (independent):", counter_b())  # 1


# ---------------------------------------------------------------------------
# 5. Why global mutable state is risky
# ---------------------------------------------------------------------------

# Global mutable state (lists, dicts, or variables reassigned via `global`)
# can be changed by any function at any time. This makes it hard to trace
# where a bug came from, hard to test functions in isolation, and prone to
# unexpected interactions between unrelated parts of the code.
shared_list = []


def risky_append(item):
    shared_list.append(item)  # mutates shared global state as a side effect


def risky_clear():
    shared_list.clear()  # another function silently wiping shared state


risky_append("task1")
risky_append("task2")
print("\nshared_list after appends:", shared_list)
risky_clear()
print("shared_list after an unrelated function cleared it:", shared_list)

# A safer alternative: pass state explicitly and return new values instead
# of relying on hidden global mutation.
def append_safely(items, item):
    """Return a NEW list with item added, without mutating the input."""
    return items + [item]


safe_list = []
safe_list = append_safely(safe_list, "task1")
safe_list = append_safely(safe_list, "task2")
print("safe_list built without global mutation:", safe_list)


# Key takeaways:
# - Local variables live only inside the function that creates them; global variables live at module level and are readable everywhere.
# - Python resolves names using LEGB: Local, then Enclosing, then Global, then Built-in.
# - Assigning to a name inside a function creates a local variable by default; `global` opts in to modifying the module-level variable instead.
# - `nonlocal` lets a nested function modify a variable in its enclosing (non-global) function -- the basis of closures.
# - Global mutable state can be changed from anywhere, making bugs hard to trace; prefer passing values explicitly and returning new results.
