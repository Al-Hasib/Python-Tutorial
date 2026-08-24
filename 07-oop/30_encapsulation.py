"""
Encapsulation & Access Modifiers
==================================

Encapsulation means bundling data with the methods that operate on it,
and controlling how that data can be accessed or changed from outside the
class. Unlike languages such as Java or C++, Python does not have true
"private" attributes enforced by the interpreter -- instead it relies on
naming CONVENTIONS and a technique called "name mangling" to signal
intent. Understanding these conventions is essential for writing classes
that are safe to use and hard to misuse by accident.

This file covers:
- Public attributes (the default)
- `_protected` attributes (convention only)
- `__private` attributes (name mangling) and why Python has no true "private"
- Manual getter/setter methods
- A preview of @property as the more Pythonic alternative (deep dive next file)
"""

# ---------------------------------------------------------------------------
# 1. Public attributes -- the default
# ---------------------------------------------------------------------------
# By default, all attributes are public: accessible and modifiable from
# anywhere, with no restriction at all.

class Person:
    def __init__(self, name, age):
        self.name = name  # public
        self.age = age    # public


person = Person("Sara", 30)
print("Public access:", person.name, person.age)
person.age = 31  # nothing stops external code from changing this directly
print("After external change:", person.age)


# ---------------------------------------------------------------------------
# 2. _protected attributes -- convention only
# ---------------------------------------------------------------------------
# A single leading underscore signals "this is internal, please don't
# touch it directly from outside the class" -- but Python does not
# enforce this. It is purely a convention that other developers (and
# tools like linters) respect.

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary  # protected by convention: "internal use"

    def give_raise(self, amount):
        self._salary += amount
        print(f"{self.name} got a raise. New salary: {self._salary}")


emp = Employee("Tom", 50000)
emp.give_raise(2000)
print("\nAccessing _salary directly still works (not enforced):", emp._salary)


# ---------------------------------------------------------------------------
# 3. __private attributes -- name mangling
# ---------------------------------------------------------------------------
# A double leading underscore (with no trailing double underscore)
# triggers "name mangling": Python internally renames the attribute to
# _ClassName__attribute. This makes accidental external access much
# harder, but it is still NOT truly private -- it can be reached if you
# know the mangled name. This is why we say Python has "no true private".

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # name-mangled to _BankAccount__balance

    def get_balance(self):
        return self.__balance


account = BankAccount("Nadia", 1000)
print("\nBalance via method:", account.get_balance())

try:
    print(account.__balance)  # AttributeError: no such attribute directly
except AttributeError as exc:
    print("Direct access failed as expected:", exc)

# But it's still reachable via the mangled name -- proving it's not truly private.
print("Reached via mangled name:", account._BankAccount__balance)


# ---------------------------------------------------------------------------
# 4. Manual getter/setter methods
# ---------------------------------------------------------------------------
# A common pattern (borrowed from languages like Java) is to expose
# explicit get_x()/set_x() methods instead of touching the attribute
# directly. This lets us add validation logic when a value changes.

class Product:
    def __init__(self, name, price):
        self.name = name
        self.__price = None
        self.set_price(price)  # route through the setter so validation runs

    def get_price(self):
        return self.__price

    def set_price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value


product = Product("Laptop", 1200)
print("\nInitial price:", product.get_price())
product.set_price(999.99)
print("Updated price:", product.get_price())

try:
    product.set_price(-50)
except ValueError as exc:
    print("Validation caught bad price:", exc)


# ---------------------------------------------------------------------------
# 5. Preview: @property is the more Pythonic way
# ---------------------------------------------------------------------------
# Manual get_x()/set_x() methods work, but Python offers a cleaner
# approach: the @property decorator lets validated attribute access
# look exactly like plain attribute access (obj.price instead of
# obj.get_price()) while still running your validation code behind the
# scenes. We only preview the idea here -- the full deep dive on
# @property, @x.setter and @x.deleter is in the next file.

class ProductPreview:
    def __init__(self, name, price):
        self.name = name
        self._price = price

    @property
    def price(self):
        """Looks like a plain attribute, but it's really a method."""
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value


preview = ProductPreview("Headphones", 150)
print("\n@property access looks like plain attribute access:", preview.price)
preview.price = 199.99  # runs the setter's validation behind the scenes
print("Updated via property setter:", preview.price)

try:
    preview.price = -10
except ValueError as exc:
    print("Property setter validation caught bad price:", exc)


# Key takeaways:
# - Public attributes have no restriction; anyone can read/write them.
# - `_protected` is a naming CONVENTION meaning "internal use", not enforced by Python.
# - `__private` triggers name mangling (_ClassName__attr), making external access harder but not impossible.
# - Manual get_x()/set_x() methods let you validate data on read/write.
# - @property (covered next) achieves the same safety with cleaner, attribute-like syntax.
