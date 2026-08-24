"""
Variables & Data Types

A variable is a name that refers to a value stored in memory. Python is
dynamically typed, meaning you don't declare a variable's type up front --
the type is determined automatically from the value you assign, and a
variable can even be reassigned to a value of a different type later.
Understanding the built-in data types (numbers, strings, booleans, None)
and how variables bind to them is the foundation for everything else you
will write in Python. This file walks through naming rules, assignment
styles, the core built-in types, and the idea of mutability.

This file covers:
- Naming rules and conventions (snake_case)
- Dynamic typing
- Basic assignment and multiple assignment
- Core types: int, float, str, bool, None, complex
- Checking types with type()
- Mutability vs immutability overview
"""

# ---------------------------------------------------------------------------
# 1. Naming rules and conventions
# ---------------------------------------------------------------------------
# Rules (enforced by Python):
#   - Names can contain letters, digits, and underscores.
#   - Names cannot start with a digit.
#   - Names are case-sensitive (age and Age are different variables).
#   - Names cannot be a reserved keyword (e.g. `class`, `for`, `if`).
#
# Conventions (style, not enforced, but expected in idiomatic Python):
#   - Use snake_case for variable and function names: student_name, total_price.
#   - Use UPPER_CASE for constants: MAX_SPEED = 120.
#   - Use descriptive names rather than single letters (except for loop
#     counters or short-lived throwaway values).
student_name = "Alice"
total_price = 49.99
MAX_SPEED = 120  # convention for a "constant" (Python has no true constants)
print("student_name:", student_name)
print("total_price:", total_price)
print("MAX_SPEED:", MAX_SPEED)

# ---------------------------------------------------------------------------
# 2. Dynamic typing
# ---------------------------------------------------------------------------
# You don't write `int x = 5` like in some languages. You just assign a
# value, and Python figures out the type. The SAME variable name can be
# rebound to a completely different type later -- the variable itself has
# no fixed type, only the value it currently refers to does.
value = 10
print("value is", value, "-> type:", type(value))
value = "now I'm a string"
print("value is", value, "-> type:", type(value))
value = 3.14
print("value is", value, "-> type:", type(value))

# ---------------------------------------------------------------------------
# 3. Assignment and multiple assignment
# ---------------------------------------------------------------------------
# Basic assignment uses the = operator.
x = 5
print("x:", x)

# Multiple assignment: assign the same value to several names at once.
a = b = c = 0
print("a, b, c:", a, b, c)

# Multiple (tuple) assignment: assign several values in one line.
first_name, last_name, age = "John", "Doe", 30
print("first_name:", first_name, "| last_name:", last_name, "| age:", age)

# Swapping values without a temporary variable, using tuple unpacking.
p, q = 1, 2
p, q = q, p
print("after swap -> p:", p, "q:", q)

# ---------------------------------------------------------------------------
# 4. Core built-in data types
# ---------------------------------------------------------------------------
# int: whole numbers, positive or negative, of arbitrary size.
count = 42
print("int example:", count, type(count))

# float: numbers with a decimal point (or written in exponential form).
price = 19.99
scientific = 1.5e3  # 1.5 * 10^3 = 1500.0
print("float examples:", price, scientific, type(price))

# str: text, written with single, double, or triple quotes.
greeting = "Hello"
print("str example:", greeting, type(greeting))

# bool: True or False, often the result of comparisons.
is_active = True
is_admin = False
print("bool examples:", is_active, is_admin, type(is_active))

# None: represents "no value" or "nothing" -- Python's null equivalent.
result = None
print("None example:", result, type(result))

# complex: numbers with a real and imaginary part (rare in everyday code,
# but built into the language for scientific/engineering use).
z = 2 + 3j
print("complex example:", z, "real:", z.real, "imag:", z.imag, type(z))

# ---------------------------------------------------------------------------
# 5. Checking types with type()
# ---------------------------------------------------------------------------
# type() returns the exact type of a value/variable -- useful for
# debugging or verifying what kind of data you're working with.
print("type(count):", type(count))
print("type(greeting):", type(greeting))
print("type(is_active):", type(is_active))
print("Comparing types:", type(count) == int)

# ---------------------------------------------------------------------------
# 6. Mutability vs immutability (overview)
# ---------------------------------------------------------------------------
# Immutable types cannot be changed in place once created; any "change"
# actually creates a brand new object. int, float, str, bool, complex, and
# tuple are all immutable.
name = "Bob"
original_id = id(name)
name += "!"  # this creates a NEW string object, it doesn't modify "Bob"
print("name after += :", name, "| id changed:", id(name) != original_id)

# Mutable types CAN be changed in place -- the same object is modified.
# list, dict, and set are mutable (covered in depth in later files).
numbers = [1, 2, 3]
original_list_id = id(numbers)
numbers.append(4)  # modifies the SAME list object in place
print("numbers after append:", numbers, "| id changed:", id(numbers) != original_list_id)

# Key takeaways:
# - Variable names use snake_case; constants are written in UPPER_CASE by convention.
# - Python is dynamically typed: a variable's type comes from its current value.
# - Multiple assignment (a = b = c = 0) and tuple assignment (x, y = 1, 2) are both valid.
# - The core built-in types are int, float, str, bool, None, and complex.
# - type() reveals a value's type; immutable types (str, int, tuple) can't
#   be changed in place, while mutable types (list, dict, set) can.
