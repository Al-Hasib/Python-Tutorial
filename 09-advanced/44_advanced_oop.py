"""
Advanced OOP: Multiple Inheritance, MRO, __slots__, Metaclasses, Mixins

Python's object model goes well beyond single inheritance. Classes can inherit
from multiple parents, and Python needs a deterministic algorithm to decide
which parent's method wins when several define the same name. Beyond that,
Python offers tools to control how instances are stored in memory (__slots__)
and even how classes themselves are created (metaclasses). Understanding these
tools helps you design flexible, memory-efficient, and predictable class
hierarchies instead of fighting surprising attribute lookups.

This file covers:
- Multiple inheritance and the Method Resolution Order (MRO)
- ClassName.__mro__ and cooperative super() calls
- __slots__: what it is, memory benefits, and tradeoffs
- A light introduction to metaclasses (type, custom metaclass)
- The mixin pattern for composing reusable behavior
"""

# ---------------------------------------------------------------------------
# 1. Multiple inheritance and the Method Resolution Order (MRO)
# ---------------------------------------------------------------------------
# When a class inherits from multiple parents, Python must decide the order
# in which it searches for attributes/methods. This order is the MRO, computed
# using the C3 linearization algorithm.

class A:
    def greet(self):
        return "Hello from A"


class B(A):
    def greet(self):
        return "Hello from B"


class C(A):
    def greet(self):
        return "Hello from C"


class D(B, C):
    # D does not define greet(), so Python walks the MRO to find it.
    pass


d = D()
print("D().greet():", d.greet())  # Uses B's greet because B comes before C in MRO
print("D.__mro__:")
for cls in D.__mro__:
    print("   ", cls.__name__)

# ---------------------------------------------------------------------------
# 2. Cooperative super() calls
# ---------------------------------------------------------------------------
# super() does not simply mean "my parent class". It means "the next class in
# the MRO". This lets every class in a chain cooperate and each get a turn,
# even in diamond-shaped hierarchies.

class Base:
    def __init__(self):
        print("Base.__init__")
        self.value = 0


class Left(Base):
    def __init__(self):
        print("Left.__init__ (before super)")
        super().__init__()
        print("Left.__init__ (after super)")
        self.value += 1


class Right(Base):
    def __init__(self):
        print("Right.__init__ (before super)")
        super().__init__()
        print("Right.__init__ (after super)")
        self.value += 10


class Diamond(Left, Right):
    def __init__(self):
        print("Diamond.__init__ (before super)")
        super().__init__()
        print("Diamond.__init__ (after super)")
        self.value += 100


print("\nCreating Diamond() -- watch the cooperative call order:")
obj = Diamond()
print("Diamond.__mro__:", [c.__name__ for c in Diamond.__mro__])
print("Final value:", obj.value)  # Every __init__ runs exactly once, cooperatively

# ---------------------------------------------------------------------------
# 3. __slots__: memory benefit and tradeoffs
# ---------------------------------------------------------------------------
# By default, instances store their attributes in a per-instance __dict__.
# __slots__ tells Python to allocate fixed, named storage slots instead,
# skipping the dict entirely. This saves memory when you create many
# instances, but it also disables some flexibility.

class PointWithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PointWithSlots:
    __slots__ = ("x", "y")  # only these attributes are allowed

    def __init__(self, x, y):
        self.x = x
        self.y = y


p1 = PointWithDict(1, 2)
p2 = PointWithSlots(1, 2)
print("\nPointWithDict has __dict__:", hasattr(p1, "__dict__"))
print("PointWithSlots has __dict__:", hasattr(p2, "__dict__"))

try:
    p2.z = 99  # not declared in __slots__
except AttributeError as e:
    print("Expected error adding new attribute to slotted instance:", e)

# Tradeoffs of __slots__:
# - Saves memory (no per-instance dict), useful for millions of small objects
# - Faster attribute access in some cases
# - Cannot add arbitrary new attributes at runtime
# - Cannot use multiple inheritance from more than one class that defines
#   non-empty __slots__
# - Some features like __weakref__ need to be explicitly added to __slots__

# ---------------------------------------------------------------------------
# 4. A light intro to metaclasses
# ---------------------------------------------------------------------------
# Classes themselves are objects, and their "type" is a metaclass. By default,
# the metaclass of every class is `type`. You can supply a custom metaclass to
# hook into class creation itself (not instance creation).

print("\ntype(PointWithDict):", type(PointWithDict))  # <class 'type'>


class LoggingMeta(type):
    """A metaclass that prints a message whenever a class using it is created."""

    def __new__(mcs, name, bases, namespace):
        print(f"LoggingMeta: creating class '{name}'")
        return super().__new__(mcs, name, bases, namespace)


class Widget(metaclass=LoggingMeta):
    def render(self):
        return "<widget>"


print("type(Widget):", type(Widget))
print("Widget().render():", Widget().render())

# Metaclasses are rarely needed in everyday code, but frameworks (like ORMs)
# use them to auto-register classes, validate class definitions, or inject
# behavior at class-creation time.

# ---------------------------------------------------------------------------
# 5. The mixin pattern
# ---------------------------------------------------------------------------
# A mixin is a small class designed to be combined with others via multiple
# inheritance. It provides one focused piece of behavior and is not meant to
# be instantiated on its own.

class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)


class ComparableByNameMixin:
    def __eq__(self, other):
        return getattr(self, "name", None) == getattr(other, "name", None)


class Person(JSONSerializableMixin, ComparableByNameMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age


alice = Person("Alice", 30)
alice2 = Person("Alice", 99)
print("\nalice.to_json():", alice.to_json())
print("alice == alice2 (compared by name only):", alice == alice2)

# Key takeaways:
# - Multiple inheritance is resolved deterministically via the MRO (C3 linearization);
#   inspect it with ClassName.__mro__.
# - super() means "next in the MRO", not "my parent" -- this makes cooperative
#   multiple inheritance work correctly when every class calls super().
# - __slots__ trades flexibility (no arbitrary new attributes, dict-free instances)
#   for lower memory usage and slightly faster attribute access.
# - Metaclasses (subclasses of type) let you customize class creation itself;
#   they are powerful but rarely needed outside of frameworks.
# - Mixins are small, focused, non-instantiated classes combined via multiple
#   inheritance to compose reusable behavior cleanly.
