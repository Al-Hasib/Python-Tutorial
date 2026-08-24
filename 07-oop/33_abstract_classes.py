"""
Abstract Classes & Interfaces
================================

An abstract class defines a common blueprint that subclasses MUST follow,
without providing (or fully providing) an implementation itself. Python's
built-in `abc` module lets us mark a class as abstract (`ABC`) and mark
specific methods as required (`@abstractmethod`). This is useful for
designing "interface-like" contracts: e.g. "every Shape must know how to
compute its own area," while letting each concrete shape implement that
however makes sense for it. Abstract classes catch a whole class of bugs
early -- Python refuses to let you instantiate a class that hasn't
fulfilled its contract.

This file covers:
- The abc module and the ABC base class
- @abstractmethod
- Why you cannot instantiate a class with unimplemented abstract methods
- Designing a simple interface-like base class with multiple concrete subclasses
"""

from abc import ABC, abstractmethod
import math


# ---------------------------------------------------------------------------
# 1. The abc module, ABC, and @abstractmethod
# ---------------------------------------------------------------------------
# Inheriting from ABC and decorating a method with @abstractmethod marks
# that method as required: every concrete (non-abstract) subclass MUST
# override it. The abstract class itself can still provide shared,
# non-abstract methods and data that subclasses inherit for free.

class Shape(ABC):
    """Abstract base class describing the 'contract' every shape follows."""

    def describe(self):
        # A regular (non-abstract) method: shared logic, inherited as-is.
        return f"I am a {type(self).__name__} with area {self.area():.2f}"

    @abstractmethod
    def area(self):
        """Every concrete Shape subclass MUST implement this."""
        raise NotImplementedError

    @abstractmethod
    def perimeter(self):
        """Every concrete Shape subclass MUST implement this too."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# 2. Why you cannot instantiate a class with unimplemented abstract methods
# ---------------------------------------------------------------------------
# Trying to create a Shape() directly fails, because Shape leaves area()
# and perimeter() unimplemented. This is Python actively enforcing the
# "contract" -- it's not just a convention here.

try:
    shape = Shape()
except TypeError as exc:
    print("Cannot instantiate Shape directly:", exc)


# ---------------------------------------------------------------------------
# 3. Designing concrete subclasses that fulfill the contract
# ---------------------------------------------------------------------------
# Each concrete subclass provides its own area() and perimeter(),
# tailored to its own geometry, while inheriting describe() for free.

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Equilateral triangle, for simplicity."""

    def __init__(self, side):
        self.side = side

    def area(self):
        return (math.sqrt(3) / 4) * self.side ** 2

    def perimeter(self):
        return 3 * self.side


circle = Circle(radius=4)
rectangle = Rectangle(width=5, height=3)
triangle = Triangle(side=6)

print("\n--- Concrete shapes fulfilling the Shape contract ---")
for shape in (circle, rectangle, triangle):
    print(shape.describe(), f"| perimeter={shape.perimeter():.2f}")


# ---------------------------------------------------------------------------
# 4. What happens if a subclass forgets to implement an abstract method
# ---------------------------------------------------------------------------
# If a subclass leaves any abstract method unimplemented, Python still
# considers it abstract, and instantiating it fails just like the base
# class did.

class BrokenShape(Shape):
    def area(self):
        return 0
    # perimeter() is missing -- still abstract!


try:
    broken = BrokenShape()
except TypeError as exc:
    print("\nCannot instantiate BrokenShape (missing perimeter):", exc)


# ---------------------------------------------------------------------------
# 5. Using the abstract base as a uniform interface (polymorphism payoff)
# ---------------------------------------------------------------------------
# Code that works with Shape objects doesn't need to know which concrete
# subclass it's dealing with -- it just relies on the guaranteed contract.

def total_area(shapes):
    return sum(shape.area() for shape in shapes)


shapes = [circle, rectangle, triangle]
print("\nTotal area of all shapes:", round(total_area(shapes), 2))

print("\nisinstance(circle, Shape):", isinstance(circle, Shape))
print("issubclass(Rectangle, Shape):", issubclass(Rectangle, Shape))


# Key takeaways:
# - Inherit from abc.ABC and use @abstractmethod to define a required contract.
# - Python refuses to instantiate any class (abstract or not) that leaves an
#   abstract method unimplemented -- this is enforced, not just a convention.
# - Abstract base classes can still provide shared, concrete helper methods.
# - Concrete subclasses implement the abstract methods in whatever way fits their data.
# - Code written against the abstract interface works uniformly across all subclasses.
