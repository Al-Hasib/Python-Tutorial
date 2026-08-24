"""
Function Arguments

Python offers many ways to pass arguments into functions: by position, by
keyword, with default values, and with flexible catch-alls like `*args` and
`**kwargs`. Understanding these options lets you design functions that are
both convenient to call and safe from misuse. This file also highlights a
classic pitfall (mutable default arguments) and the rules Python enforces
about argument ordering.

This file covers:
- Positional arguments
- Default argument values (and the mutable-default-argument pitfall)
- Keyword arguments
- `*args` and `**kwargs`
- Positional-only (`/`) and keyword-only (`*`) parameters
- Argument order rules
- Unpacking arguments when calling (`*list`, `**dict`)
"""

# ---------------------------------------------------------------------------
# 1. Positional arguments
# ---------------------------------------------------------------------------

# Arguments matched to parameters by their position/order in the call.
def describe_pet(animal, name):
    print(f"{name} is a {animal}.")


describe_pet("dog", "Rex")  # animal="dog", name="Rex"
describe_pet("Rex", "dog")  # order matters! meaning flips


# ---------------------------------------------------------------------------
# 2. Default argument values
# ---------------------------------------------------------------------------

# A default value is used when the caller omits that argument.
def describe_pet_default(animal, name="Buddy"):
    print(f"{name} is a {animal}.")


describe_pet_default("dog")           # uses default name "Buddy"
describe_pet_default("cat", "Whiskers")  # overrides the default


# --- The mutable default argument pitfall ---
# Default values are evaluated ONCE, when the function is defined, not each
# call. If the default is a mutable object (list, dict, set), every call
# that relies on the default SHARES the same object, causing surprising bugs.
def add_item_buggy(item, basket=[]):  # BUG: shared mutable default
    basket.append(item)
    return basket


print("\nMutable default pitfall:")
print(add_item_buggy("apple"))   # ['apple']
print(add_item_buggy("banana"))  # ['apple', 'banana'] -- unexpected!


# The fix: use `None` as the default and create a new object inside.
def add_item_fixed(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket


print("\nFixed version:")
print(add_item_fixed("apple"))
print(add_item_fixed("banana"))  # fresh list each time: ['banana']


# ---------------------------------------------------------------------------
# 3. Keyword arguments
# ---------------------------------------------------------------------------

# Arguments passed by explicitly naming the parameter, in any order.
def make_profile(name, age, city):
    print(f"{name}, {age}, from {city}")


make_profile(name="Alice", age=30, city="Paris")
make_profile(city="Tokyo", name="Kenji", age=25)  # order doesn't matter
make_profile("Sam", city="Cairo", age=40)  # mixing positional + keyword


# ---------------------------------------------------------------------------
# 4. *args -- variable positional arguments
# ---------------------------------------------------------------------------

# `*args` collects any extra positional arguments into a tuple.
def sum_all(*args):
    print("args received as tuple:", args)
    return sum(args)


print("\nsum_all(1, 2, 3) =", sum_all(1, 2, 3))
print("sum_all(5, 10, 15, 20) =", sum_all(5, 10, 15, 20))
print("sum_all() =", sum_all())  # works with zero extra args too


# ---------------------------------------------------------------------------
# 5. **kwargs -- variable keyword arguments
# ---------------------------------------------------------------------------

# `**kwargs` collects any extra keyword arguments into a dictionary.
def print_info(**kwargs):
    print("kwargs received as dict:", kwargs)
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


print()
print_info(name="Alice", age=30, job="Engineer")


# Combining regular params, *args, and **kwargs:
def full_example(required, *args, **kwargs):
    print(f"required={required}, args={args}, kwargs={kwargs}")


full_example("must-have", 1, 2, 3, extra="yes", debug=True)


# ---------------------------------------------------------------------------
# 6. Positional-only (/) and keyword-only (*) parameters
# ---------------------------------------------------------------------------

# Parameters before `/` must be passed positionally (cannot use keyword).
# Parameters after `*` must be passed by keyword (cannot use position).
def calculate(x, y, /, *, mode="add"):
    if mode == "add":
        return x + y
    elif mode == "subtract":
        return x - y
    return None


print("\ncalculate(3, 4):", calculate(3, 4))                 # OK: x, y positional
print("calculate(3, 4, mode='subtract'):", calculate(3, 4, mode="subtract"))
# calculate(x=3, y=4) would raise TypeError -- x, y are positional-only
# calculate(3, 4, "subtract") would raise TypeError -- mode is keyword-only


# ---------------------------------------------------------------------------
# 7. Argument order rules in a function definition
# ---------------------------------------------------------------------------

# The general order allowed by Python when defining a function is:
#   def f(positional_only, /, normal, *args, keyword_only, **kwargs):
# i.e. positional-only params, then normal params (with optional defaults),
# then *args, then keyword-only params, then **kwargs.
def full_signature(a, b, /, c, d=10, *args, e, f=20, **kwargs):
    print(f"a={a} b={b} c={c} d={d} args={args} e={e} f={f} kwargs={kwargs}")


full_signature(1, 2, 3, e=5)
full_signature(1, 2, 3, 4, 100, 200, e=5, f=6, extra="x")


# ---------------------------------------------------------------------------
# 8. Unpacking arguments when calling: *list and **dict
# ---------------------------------------------------------------------------

# A list/tuple can be "unpacked" into positional arguments with *.
numbers = [3, 4]
print("\ncalculate(*numbers):", calculate(*numbers))

coords = (1, 2, 3)


def show_point(x, y, z):
    print(f"Point({x}, {y}, {z})")


show_point(*coords)

# A dict can be "unpacked" into keyword arguments with **.
person = {"name": "Diana", "age": 28, "city": "Berlin"}
make_profile(**person)

# Combine both when calling:
args_list = ["dog", "Rex"]
describe_pet(*args_list)


# Key takeaways:
# - Positional arguments rely on order; keyword arguments rely on explicit names and can appear in any order.
# - Default values are evaluated once at definition time -- never use a mutable object as a default; use None + create inside instead.
# - `*args` gathers extra positional arguments into a tuple; `**kwargs` gathers extra keyword arguments into a dict.
# - `/` marks preceding parameters positional-only; `*` marks following parameters keyword-only, giving you control over the call API.
# - Use `*iterable` and `**mapping` at the call site to unpack existing collections into a function call.
