"""
Type Conversion & Type Checking

Type conversion (also called type casting) is the process of changing a
value from one data type to another -- either automatically by Python
(implicit conversion) or manually by the programmer (explicit conversion).
Because Python is dynamically typed, understanding when and how values
convert between types is essential for avoiding bugs, especially around
user input (which always arrives as a string) and boolean "truthiness"
(which every object has, even if it isn't literally True or False). This
file also covers the difference between type() and isinstance() for
checking a value's type.

This file covers:
- Implicit vs explicit type conversion
- Explicit conversion functions: int(), float(), str(), bool(), list(), etc.
- Common conversion pitfalls (e.g. int("3.5") raising an error)
- Truthiness of values (what counts as True or False)
- type() vs isinstance()
"""

# ---------------------------------------------------------------------------
# 1. Implicit type conversion
# ---------------------------------------------------------------------------
# Python automatically converts types in certain situations, most commonly
# when mixing int and float in arithmetic -- the int is promoted to float
# so no precision is lost.
whole = 5
decimal = 2.5
total = whole + decimal  # int is implicitly converted to float
print("5 + 2.5 =", total, "| type:", type(total))

# bool is actually a subtype of int, so True/False behave like 1/0 in math.
print("True + True =", True + True, "| type:", type(True + True))
print("True + 1 =", True + 1)

# ---------------------------------------------------------------------------
# 2. Explicit type conversion
# ---------------------------------------------------------------------------
# You explicitly convert a value by calling the target type as a function.
print("int('42'):     ", int("42"), type(int("42")))
print("int(3.9):      ", int(3.9))          # truncates toward zero, does NOT round
print("float('3.14'): ", float("3.14"))
print("float(7):      ", float(7))
print("str(100):      ", str(100), type(str(100)))
print("str(3.14):     ", str(3.14))
print("bool(1):       ", bool(1))
print("bool(0):       ", bool(0))
print("list('abc'):   ", list("abc"))       # splits a string into a list of characters
print("list((1, 2, 3)):", list((1, 2, 3)))  # converts a tuple into a list
print("tuple([1, 2, 3]):", tuple([1, 2, 3]))
print("set([1, 2, 2, 3]):", set([1, 2, 2, 3]))  # removes duplicates

# ---------------------------------------------------------------------------
# 3. Conversion pitfalls
# ---------------------------------------------------------------------------
# int() can convert a string of digits, but NOT a string that looks like a
# float -- that raises a ValueError. You must go through float() first.
try:
    int("3.5")
except ValueError as e:
    print("int('3.5') failed as expected:", e)

# The correct two-step approach:
value = int(float("3.5"))
print("int(float('3.5')) works:", value)

# Similarly, int() cannot parse a non-numeric string.
try:
    int("hello")
except ValueError as e:
    print("int('hello') failed as expected:", e)

# float() is fine with a plain integer-looking string...
print("float('10'):", float("10"))
# ...but int() cannot directly parse a string with a decimal point.
try:
    int("10.0")
except ValueError as e:
    print("int('10.0') failed as expected:", e)

# Converting None directly to int/float is not allowed either.
try:
    int(None)
except TypeError as e:
    print("int(None) failed as expected:", e)

# ---------------------------------------------------------------------------
# 4. Truthiness of values
# ---------------------------------------------------------------------------
# Every object in Python has an inherent "truthiness" when used in a
# boolean context (like an if statement), even if it's not literally
# True/False. Empty/zero-like values are considered "falsy"; everything
# else is "truthy".
falsy_values = [0, 0.0, "", [], {}, (), set(), None, False]
for v in falsy_values:
    print(f"bool({v!r}) =", bool(v))

truthy_values = [1, -1, 3.14, "hello", [0], {"a": 1}, (0,), True, "False"]
for v in truthy_values:
    print(f"bool({v!r}) =", bool(v))

# Note the last one: the STRING "False" is truthy, because it is a
# non-empty string -- only the actual boolean False (and falsy values
# above) are falsy.

# ---------------------------------------------------------------------------
# 5. type() vs isinstance()
# ---------------------------------------------------------------------------
# type(x) returns the exact type of x. isinstance(x, T) checks whether x
# is an instance of T OR any subclass of T -- generally the preferred way
# to check types, especially with inheritance.


class Animal:
    pass


class Dog(Animal):
    pass


my_dog = Dog()

print("type(my_dog) == Dog:       ", type(my_dog) == Dog)
print("type(my_dog) == Animal:    ", type(my_dog) == Animal)   # False! not an exact match
print("isinstance(my_dog, Dog):   ", isinstance(my_dog, Dog))
print("isinstance(my_dog, Animal):", isinstance(my_dog, Animal))  # True: Dog is a subclass

# isinstance() also accepts a tuple of types to check against several at once.
print("isinstance(5, (int, float)):  ", isinstance(5, (int, float)))
print("isinstance(5.0, (int, float)):", isinstance(5.0, (int, float)))
print("isinstance(True, int):        ", isinstance(True, int))  # bool is a subclass of int

# Key takeaways:
# - Implicit conversion happens automatically (e.g. int + float -> float);
#   explicit conversion uses functions like int(), float(), str(), bool().
# - int() cannot parse a decimal-looking string directly (int("3.5") fails
#   with ValueError) -- convert through float() first if needed.
# - Every value has a truthiness: 0, 0.0, "", [], {}, (), set(), and None
#   are falsy; almost everything else is truthy.
# - Prefer isinstance() over type() == for type checks, since isinstance()
#   correctly accounts for subclasses (inheritance).
# - Always validate/convert user input carefully, since input() returns a
#   string that may not represent the numeric type you expect.
