"""
Class Methods, Static Methods & Properties
=============================================

Not every method needs to operate on a specific instance via `self`.
`@classmethod` gives a method access to the class itself (via `cls`),
which is perfect for alternative constructors. `@staticmethod` is for
utility functions that logically belong inside the class but don't need
access to either the instance or the class. `@property` lets us expose
computed or validated values using plain attribute syntax, which is the
idiomatic Python way to implement getters/setters (as previewed in the
encapsulation file). Together these decorators make classes more
flexible and expressive.

This file covers:
- @classmethod, `cls`, and alternative constructors
- @staticmethod, and when to use it vs a plain function
- @property and property setters/deleters
- Computed / read-only attributes
"""

# ---------------------------------------------------------------------------
# 1. @classmethod, `cls`, and alternative constructors
# ---------------------------------------------------------------------------
# A classmethod receives the class itself (conventionally named `cls`)
# instead of an instance. A very common use is providing alternative
# constructors -- extra ways to build an object besides __init__.

class Pizza:
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings

    def __repr__(self):
        return f"Pizza(size={self.size!r}, toppings={self.toppings!r})"

    @classmethod
    def margherita(cls):
        # Alternative constructor: builds a specific, common configuration.
        return cls(size="medium", toppings=["tomato", "mozzarella", "basil"])

    @classmethod
    def from_string(cls, description):
        # Alternative constructor: parse a compact string like "large:cheese,olives"
        size, toppings_str = description.split(":")
        toppings = toppings_str.split(",")
        return cls(size, toppings)


standard = Pizza("large", ["pepperoni"])
special = Pizza.margherita()
parsed = Pizza.from_string("small:mushroom,onion")

print("Standard pizza:", standard)
print("Margherita (alt constructor):", special)
print("Parsed pizza (alt constructor):", parsed)


# ---------------------------------------------------------------------------
# 2. @staticmethod -- and when to use it vs a plain function
# ---------------------------------------------------------------------------
# A staticmethod receives neither `self` nor `cls`. It behaves like a
# plain function, but is placed inside the class because it's logically
# related to it (e.g. a helper/validator/utility for that class's domain).
# Use @staticmethod when the logic doesn't need instance or class state;
# otherwise, a module-level plain function works just as well -- the
# main benefit of @staticmethod is namespacing and discoverability
# (Pizza.is_valid_size(...) reads clearly as "related to Pizza").

class Pizza2(Pizza):
    VALID_SIZES = ("small", "medium", "large")

    @staticmethod
    def is_valid_size(size):
        return size in Pizza2.VALID_SIZES


print("\nis_valid_size('medium'):", Pizza2.is_valid_size("medium"))
print("is_valid_size('huge'):", Pizza2.is_valid_size("huge"))
# Static methods can be called on an instance too, but it's the same call:
instance_pizza = Pizza2("medium", ["cheese"])
print("Called via instance:", instance_pizza.is_valid_size("small"))


# ---------------------------------------------------------------------------
# 3. @property -- computed / validated attribute access
# ---------------------------------------------------------------------------
# @property turns a method into something accessed like a plain
# attribute (no parentheses). This is the idiomatic Python equivalent of
# manual get_x()/set_x() methods.

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        # A computed, read-only attribute: recalculated every access,
        # with no setter defined -- so it cannot be assigned directly.
        return 3.14159 * self.radius ** 2

    @property
    def diameter(self):
        return self.radius * 2


circle = Circle(5)
print("\nCircle radius:", circle.radius)
print("Circle area (computed property):", circle.area)
print("Circle diameter (computed property):", circle.diameter)

try:
    circle.area = 100  # no setter defined -> raises AttributeError
except AttributeError as exc:
    print("Cannot set read-only property 'area':", exc)


# ---------------------------------------------------------------------------
# 4. Property setters and deleters
# ---------------------------------------------------------------------------
# @x.setter lets us validate/transform a value when it's assigned via
# `obj.x = value`. @x.deleter lets us customize what happens on
# `del obj.x`.

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible.")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        print("Resetting temperature to 0 (absolute deletion of custom value).")
        self._celsius = 0

    @property
    def fahrenheit(self):
        # Another computed, read-only property derived from celsius.
        return self._celsius * 9 / 5 + 32


temp = Temperature(25)
print("\nInitial celsius:", temp.celsius)
print("Computed fahrenheit:", temp.fahrenheit)

temp.celsius = 30  # runs the setter's validation
print("After setting celsius=30, fahrenheit:", temp.fahrenheit)

try:
    temp.celsius = -300  # invalid: below absolute zero
except ValueError as exc:
    print("Setter validation caught invalid value:", exc)

del temp.celsius  # runs the deleter
print("After del temp.celsius:", temp.celsius)


# Key takeaways:
# - @classmethod receives `cls` and is ideal for alternative constructors.
# - @staticmethod receives neither self nor cls; use it for related utility logic.
# - @property exposes a method as if it were a plain attribute (no parentheses).
# - @x.setter and @x.deleter let you validate assignment and customize deletion.
# - A property with only a getter defined is effectively a computed, read-only attribute.
