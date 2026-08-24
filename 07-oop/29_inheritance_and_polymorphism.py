"""
Inheritance & Polymorphism
===========================

Inheritance lets a class (the "child" or "subclass") reuse and extend the
behavior of another class (the "parent" or "superclass"), avoiding
duplicated code when several classes share common structure. Polymorphism
means that different classes can implement the same method name in their
own way, so code that calls that method works uniformly across many
types without caring about their exact class. Together these features
let us write flexible, extensible code -- a hallmark of good OOP design.

This file covers:
- Single inheritance
- super().__init__()
- Overriding methods
- Polymorphism (same method name, different behavior per subclass)
- isinstance() and issubclass()
- Method resolution basics (MRO)
"""

# ---------------------------------------------------------------------------
# 1. Single inheritance
# ---------------------------------------------------------------------------
# A subclass inherits all attributes and methods from its parent class.

class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def describe(self):
        return f"{self.make} {self.model}"

    def move(self):
        return "The vehicle moves."


class Car(Vehicle):
    """Car inherits everything from Vehicle without redefining it."""
    pass


car = Car("Toyota", "Corolla")
print("Car description:", car.describe())  # inherited method
print("Car move:", car.move())              # inherited method


# ---------------------------------------------------------------------------
# 2. super().__init__() -- extending the parent's constructor
# ---------------------------------------------------------------------------
# `super()` gives access to the parent class so a subclass can reuse the
# parent's __init__ (or other methods) instead of duplicating logic.

class Motorcycle(Vehicle):
    def __init__(self, make, model, has_sidecar=False):
        super().__init__(make, model)  # let Vehicle set up make/model
        self.has_sidecar = has_sidecar  # then add Motorcycle-specific data

    def move(self):
        return "The motorcycle roars down the road."


moto = Motorcycle("Harley-Davidson", "Iron 883", has_sidecar=False)
print("\nMotorcycle description:", moto.describe())  # inherited, unchanged
print("Motorcycle move:", moto.move())                # overridden below


# ---------------------------------------------------------------------------
# 3. Overriding methods
# ---------------------------------------------------------------------------
# A subclass can redefine (override) a method from its parent to change
# its behavior. Car below overrides move() while still reusing describe().

class Truck(Vehicle):
    def __init__(self, make, model, payload_tons):
        super().__init__(make, model)
        self.payload_tons = payload_tons

    def move(self):  # override
        return f"The truck hauls {self.payload_tons} tons down the highway."


truck = Truck("Volvo", "FH16", 12)
print("\nTruck move (overridden):", truck.move())


class SportsCar(Car):
    def move(self):  # override again, one level deeper
        return "The sports car speeds away with a roar!"


sports_car = SportsCar("Ferrari", "488")
print("SportsCar move (overridden):", sports_car.move())


# ---------------------------------------------------------------------------
# 4. Polymorphism -- same method name, different behavior
# ---------------------------------------------------------------------------
# Because every subclass implements move() (directly or inherited), we can
# treat a list of different Vehicle subtypes uniformly and let each object
# decide how to respond. This is the essence of polymorphism.

print("\n--- Polymorphism demo ---")
vehicles = [car, moto, truck, sports_car]
for v in vehicles:
    print(f"{v.describe():<20} -> {v.move()}")


# ---------------------------------------------------------------------------
# 5. isinstance() and issubclass()
# ---------------------------------------------------------------------------
# isinstance(obj, Class)   -> is this specific object built from Class
#                              (or a subclass of it)?
# issubclass(A, B)         -> is class A a subclass of class B?

print("\nisinstance(truck, Vehicle):", isinstance(truck, Vehicle))
print("isinstance(truck, Car):", isinstance(truck, Car))          # False, Truck is not a Car
print("isinstance(sports_car, Car):", isinstance(sports_car, Car))  # True, Car is its parent
print("isinstance(sports_car, Vehicle):", isinstance(sports_car, Vehicle))  # True, grandparent

print("\nissubclass(Car, Vehicle):", issubclass(Car, Vehicle))
print("issubclass(SportsCar, Vehicle):", issubclass(SportsCar, Vehicle))
print("issubclass(Motorcycle, Car):", issubclass(Motorcycle, Car))
print("issubclass(Vehicle, Vehicle):", issubclass(Vehicle, Vehicle))  # a class is its own subclass


# ---------------------------------------------------------------------------
# 6. Method resolution basics (MRO)
# ---------------------------------------------------------------------------
# When a method is called, Python looks it up following the Method
# Resolution Order (MRO): the class itself first, then its parents, in a
# well-defined order. `ClassName.__mro__` (or mro()) shows that order.

print("\nSportsCar MRO:")
for cls in SportsCar.__mro__:
    print(" ->", cls.__name__)

# Calling sports_car.describe() searches SportsCar first (not found),
# then Car (not found), then Vehicle (found!) -- following the MRO.
print("\nsports_car.describe() resolves up the chain to Vehicle:", sports_car.describe())


# Key takeaways:
# - Inheritance (class Child(Parent)) lets subclasses reuse a parent's code.
# - super().__init__(...) calls the parent constructor so you extend, not replace, it.
# - Overriding a method in a subclass changes behavior while keeping the same name.
# - Polymorphism lets code call the same method on different types and get type-appropriate results.
# - isinstance()/issubclass() check object/class relationships; __mro__ shows lookup order.
