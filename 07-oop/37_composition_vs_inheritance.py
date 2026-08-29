"""
Composition vs Inheritance
=============================

Inheritance models an "is-a" relationship (a Car IS A Vehicle), while
composition models a "has-a" relationship (a Car HAS AN Engine). Both are
valid ways to reuse code and build complex objects out of simpler ones,
but they have different trade-offs: inheritance creates a tight coupling
between parent and child classes, while composition builds objects by
combining smaller, independent, more flexible pieces. A well-known
design guideline -- "favor composition over inheritance" -- exists
because composition tends to produce more maintainable, less fragile
code, especially as requirements grow.

This file covers:
- "has-a" vs "is-a" relationships
- Building objects out of other objects (composition)
- Subclassing (inheritance) for comparison
- The same feature implemented both ways
- Guidance on when to prefer composition
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. "is-a" relationships -- inheritance
# ---------------------------------------------------------------------------
# Inheritance says "this new class IS A more specific version of that
# other class." It works well when subclasses are genuinely specialized
# forms of the parent and share its entire behavior/contract.

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} earns {self.salary}"


class Manager(Employee):  # Manager IS AN Employee
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def describe(self):
        base = super().describe()
        return f"{base} and manages a team of {self.team_size}"


manager = Manager("Dana", 90000, 5)
print("Inheritance example:", manager.describe())


# ---------------------------------------------------------------------------
# 2. "has-a" relationships -- composition
# ---------------------------------------------------------------------------
# Composition says "this class HAS A(n) other object that it delegates
# work to." Instead of inheriting behavior, we build our object out of
# other, smaller objects and call their methods.

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"Engine roars to life ({self.horsepower} HP)."


class Radio:
    def turn_on(self):
        return "Radio playing your favorite station."


class Car:
    def __init__(self, make, model, horsepower):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower)  # Car HAS AN Engine
        self.radio = Radio()              # Car HAS A Radio

    def start(self):
        return f"{self.make} {self.model}: {self.engine.start()} {self.radio.turn_on()}"


car = Car("Honda", "Civic", 158)
print("\nComposition example:", car.start())


# ---------------------------------------------------------------------------
# 3. The same feature, implemented both ways
# ---------------------------------------------------------------------------
# Imagine we want "loggable" behavior (something that can record events).
# Below is the same feature built with inheritance, then with composition,
# so we can compare them directly.

# --- Version A: Inheritance ---
class LoggerMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class OrderInheritance(LoggerMixin):  # OrderInheritance IS A LoggerMixin
    def __init__(self, order_id):
        self.order_id = order_id

    def ship(self):
        self.log(f"Order {self.order_id} shipped.")  # inherited method


order_a = OrderInheritance("A-100")
order_a.ship()

# --- Version B: Composition ---
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")


class OrderComposition:  # OrderComposition HAS A Logger
    def __init__(self, order_id, logger=None):
        self.order_id = order_id
        self.logger = logger or Logger()

    def ship(self):
        self.logger.log(f"Order {self.order_id} shipped.")  # delegated call


order_b = OrderComposition("B-200")
order_b.ship()

print("\nBoth versions produce the same observable log output,")
print("but arrive there through inheritance vs delegation.")


# ---------------------------------------------------------------------------
# 4. Why composition is often more flexible
# ---------------------------------------------------------------------------
# With composition, we can swap in a different implementation at runtime
# (e.g. a "silent" logger for tests) without touching the Order class or
# its class hierarchy at all. Inheritance can't do this as easily --
# swapping behavior usually means creating yet another subclass.

class SilentLogger:
    def log(self, message):
        pass  # does nothing -- useful for tests, or muting output


quiet_order = OrderComposition("C-300", logger=SilentLogger())
quiet_order.ship()  # no output at all, because we swapped the logger
print("\nSwapped in a SilentLogger for order C-300 -- no log output above.")


# ---------------------------------------------------------------------------
# 5. When to prefer composition over inheritance
# ---------------------------------------------------------------------------
# General guidance ("favor composition over inheritance"):
# - Prefer composition when you want to reuse behavior WITHOUT locking
#   into a rigid "is-a" hierarchy, or when a class would need to inherit
#   from multiple unrelated things ("has an Engine AND a Radio AND GPS...").
# - Prefer composition when the relationship might change at runtime
#   (e.g. swappable strategies, plugins, dependency injection).
# - Prefer inheritance when subclasses are genuinely specialized versions
#   of the parent, share its full contract, and the hierarchy is stable
#   (e.g. the Shape/Circle/Rectangle abstract-class example from an
#   earlier file, where "is-a Shape" is a natural and stable relationship).
# - Deep inheritance chains (many levels) are a common warning sign that
#   composition would have been simpler to understand and modify.

class GpsNavigator:
    def navigate(self, destination):
        return f"Navigating to {destination}..."


class SmartCar:
    """Demonstrates composing MULTIPLE independent components --
    something that would require awkward multiple inheritance otherwise."""

    def __init__(self, make, model, horsepower):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower)
        self.radio = Radio()
        self.gps = GpsNavigator()

    def start_trip(self, destination):
        print(self.engine.start())
        print(self.radio.turn_on())
        print(self.gps.navigate(destination))


print("\n--- SmartCar composed of Engine + Radio + GpsNavigator ---")
smart_car = SmartCar("Tesla", "Model 3", 283)
smart_car.start_trip("San Francisco")


# Key takeaways:
# - Inheritance models "is-a" (Manager IS AN Employee); composition models "has-a" (Car HAS AN Engine).
# - Composition builds objects by delegating to other objects rather than sharing a base class.
# - The same feature can be built either way; composition is usually easier to swap and reconfigure.
# - Combining many unrelated behaviors is simpler with composition than with deep/multiple inheritance.
# - General rule of thumb: favor composition over inheritance unless the "is-a" relationship is
#   genuinely stable and the subclass truly shares the parent's whole contract.
