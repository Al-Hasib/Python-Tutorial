"""
Classes & Objects
==================

Object-Oriented Programming (OOP) lets us model real-world things as
"objects" that bundle together data (attributes) and behavior (methods).
A `class` is a blueprint for creating objects; an object (also called an
"instance") is a concrete thing built from that blueprint. Python creates
every object through the class's `__init__` method, which sets up the
object's starting state. Understanding classes vs instances, and how
`self` refers to "this particular object," is the foundation for
everything else in OOP.

This file covers:
- The `class` keyword and basic class definition
- The `__init__` constructor and `self`
- Instance attributes vs class attributes
- Instance methods
- Creating and using multiple instances
- The difference between a class and an instance
- `__repr__` / `__str__` intro for nicer printing
"""

# ---------------------------------------------------------------------------
# 1. Defining a class with the `class` keyword
# ---------------------------------------------------------------------------
# A class is just a template. By itself it does nothing until we create
# instances (objects) from it.

class Animal:
    pass


print("Animal class object:", Animal)
print("Type of Animal:", type(Animal))


# ---------------------------------------------------------------------------
# 2. The __init__ constructor and `self`
# ---------------------------------------------------------------------------
# __init__ runs automatically whenever a new object is created. `self`
# is the first parameter of every instance method and refers to the
# specific object being created/used. Python passes it automatically;
# we never pass it ourselves when calling the method.

class Dog:
    def __init__(self, name, breed, age):
        # These are INSTANCE attributes: each Dog object gets its own copy.
        self.name = name
        self.breed = breed
        self.age = age


rex = Dog("Rex", "German Shepherd", 3)
print("\nCreated a dog:", rex.name, rex.breed, rex.age)


# ---------------------------------------------------------------------------
# 3. Instance attributes vs class attributes
# ---------------------------------------------------------------------------
# Class attributes are defined directly on the class body and are shared
# by ALL instances (unless an instance overrides them locally). Instance
# attributes are set in __init__ (or later) via `self.x = ...` and belong
# to that one object only.

class Cat:
    species = "Felis catus"  # class attribute -- shared by every Cat

    def __init__(self, name, age):
        self.name = name      # instance attribute
        self.age = age        # instance attribute


cat1 = Cat("Whiskers", 2)
cat2 = Cat("Milo", 5)

print("\ncat1 species:", cat1.species)
print("cat2 species:", cat2.species)
print("Cat.species (via class itself):", Cat.species)

# Changing the class attribute affects all instances that haven't
# overridden it locally.
Cat.species = "Felis silvestris catus"
print("After change -> cat1.species:", cat1.species, "| cat2.species:", cat2.species)

# Assigning to self.species on ONE instance creates a new instance
# attribute that shadows the class attribute for that instance only.
cat1.species = "Just Cat"
print("After shadowing -> cat1.species:", cat1.species, "| cat2.species:", cat2.species)


# ---------------------------------------------------------------------------
# 4. Instance methods
# ---------------------------------------------------------------------------
# Instance methods operate on a specific object's data via `self`.

class BankAccount:
    interest_rate = 0.02  # class attribute: same rate for every account

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"{self.owner} tried to withdraw {amount}, but balance is only {self.balance}.")
        else:
            self.balance -= amount
            print(f"{self.owner} withdrew {amount}. New balance: {self.balance}")

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate
        print(f"Interest applied. New balance: {self.balance:.2f}")


print("\n--- BankAccount demo ---")
acc = BankAccount("Alice", 100)
acc.deposit(50)
acc.withdraw(30)
acc.apply_interest()


# ---------------------------------------------------------------------------
# 5. Creating and using multiple instances
# ---------------------------------------------------------------------------
# Each instance keeps its own independent state, even though they were
# built from the same class.

print("\n--- Multiple accounts ---")
alice_acc = BankAccount("Alice", 200)
bob_acc = BankAccount("Bob", 500)

alice_acc.deposit(20)
bob_acc.withdraw(100)

print("Alice's balance:", alice_acc.balance)
print("Bob's balance:", bob_acc.balance)


# ---------------------------------------------------------------------------
# 6. Class vs instance -- the key distinction
# ---------------------------------------------------------------------------
# The CLASS (e.g. BankAccount) is the blueprint/definition.
# An INSTANCE (e.g. alice_acc, bob_acc) is one concrete object built from it.
# `isinstance()` checks whether an object was built from a given class.

print("\nIs alice_acc a BankAccount?", isinstance(alice_acc, BankAccount))
print("Is BankAccount itself a BankAccount?", isinstance(BankAccount, BankAccount))
print("Type of alice_acc:", type(alice_acc))


# ---------------------------------------------------------------------------
# 7. __repr__ / __str__ intro -- printing objects nicely
# ---------------------------------------------------------------------------
# By default, printing an object gives an unhelpful string like
# "<__main__.BankAccount object at 0x...>". Defining __str__ (for
# friendly, human-readable output) and __repr__ (for an unambiguous,
# developer-facing representation) fixes that. A deep dive on dunder
# methods comes in a later file -- this is just enough to print nicely.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        # Used by print() and str()
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        # Used in the REPL, in lists/containers, and by repr()
        return f"Point(x={self.x!r}, y={self.y!r})"


p = Point(3, 4)
print("\nstr(p):", str(p))
print("print(p):", p)
print("repr(p):", repr(p))
print("List of points:", [p, Point(0, 0)])  # uses __repr__ for each item


# Key takeaways:
# - A class is a blueprint; an instance (object) is a concrete thing built from it.
# - __init__ sets up instance attributes; `self` always refers to the current object.
# - Class attributes are shared across instances; instance attributes belong to one object.
# - Instance methods use `self` to read/modify that specific object's data.
# - Define __str__ for friendly printing and __repr__ for an unambiguous developer view.
