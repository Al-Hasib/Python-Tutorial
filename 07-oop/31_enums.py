"""
Enums: Named Constants Done Right
==================================

Many programs need a small, fixed set of related constant values -- the
days of the week, an order's status, a traffic light's color. A common
(but fragile) approach is plain strings or ints: status = "pending", or
status = 1. Typos ("pendign") and out-of-range numbers (status = 99) go
uncaught until runtime, and the valid options live only in comments, if
anywhere. The `enum` module fixes this: an Enum is a class whose members
are a fixed, named set of values, each of which is a genuine singleton
object -- comparable, iterable, and immediately recognizable by name
wherever it's used, with your editor and type checker able to verify you
spelled it right.

This file covers:
- Why raw strings/ints for constants are fragile
- Defining an Enum and accessing member .name / .value
- Iterating over an Enum and membership checks
- Comparing members (identity, equality, and why cross-Enum comparison fails)
- auto() for automatic values when the value itself doesn't matter
- IntEnum, for members that also need to behave like plain ints
- Adding methods to an Enum
"""

from enum import Enum, IntEnum, auto

# ---------------------------------------------------------------------------
# 1. Why raw strings/ints for constants are fragile
# ---------------------------------------------------------------------------
# Nothing stops a typo or an invalid value from slipping through here --
# Python happily accepts any string, valid or not.
order_status = "shiped"  # typo! but Python won't complain
print("Fragile string constant (typo not caught):", order_status)


def describe_status_stringly(status):
    if status == "pending":
        return "Order is pending"
    elif status == "shipped":
        return "Order has shipped"
    return "Unknown status"  # the typo silently falls through to here


print("describe_status_stringly('shiped'):", describe_status_stringly(order_status))

# ---------------------------------------------------------------------------
# 2. Defining an Enum and accessing .name / .value
# ---------------------------------------------------------------------------
# An Enum is a class; each member is written as NAME = value. Members are
# accessed as OrderStatus.PENDING, never constructed like OrderStatus(),
# and each one is a unique, singleton object.
class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


current = OrderStatus.SHIPPED
print("\ncurrent:       ", current)
print("current.name:  ", current.name)
print("current.value: ", current.value)
print("type(current): ", type(current))

# Looking a member up by its underlying value:
looked_up = OrderStatus("pending")
print("OrderStatus('pending'):", looked_up, "| is PENDING:", looked_up is OrderStatus.PENDING)

# ---------------------------------------------------------------------------
# 3. Iterating over an Enum and membership checks
# ---------------------------------------------------------------------------
# Enum classes are iterable, in definition order -- handy for populating a
# dropdown, validating input, or just documenting every valid option.
print("\nAll OrderStatus members:")
for status in OrderStatus:
    print(f"  {status.name} = {status.value!r}")

print("OrderStatus.PENDING in OrderStatus:", OrderStatus.PENDING in OrderStatus)

# ---------------------------------------------------------------------------
# 4. Comparing members: identity, equality, and no cross-Enum comparisons
# ---------------------------------------------------------------------------
# Each member is a true singleton: there is only ever ONE OrderStatus.PENDING
# object, so `is` and `==` agree, and match/case (see 10_match_case_statements.py)
# works naturally with enum members as patterns.
a = OrderStatus.PENDING
b = OrderStatus.PENDING
print("\na is b (same singleton object):", a is b)
print("a == b:                        ", a == b)


class ShippingStatus(Enum):
    PENDING = "pending"  # deliberately the same value as OrderStatus.PENDING


print(
    "OrderStatus.PENDING == ShippingStatus.PENDING (different Enums):",
    OrderStatus.PENDING == ShippingStatus.PENDING,
)  # False! members from different Enum classes are never equal, even with
   # the same underlying value -- this is exactly the mix-up plain strings
   # would let slip through silently.

# ---------------------------------------------------------------------------
# 5. auto() for automatic values
# ---------------------------------------------------------------------------
# When the underlying value doesn't matter -- you only care about the
# distinct names -- auto() assigns increasing integers (1, 2, 3, ...) for
# you, so you never have to keep the numbers in sync by hand.
class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


print("\nDirection members with auto() values:")
for direction in Direction:
    print(f"  {direction.name} = {direction.value}")

# ---------------------------------------------------------------------------
# 6. IntEnum: members that also behave like plain ints
# ---------------------------------------------------------------------------
# A plain Enum member is NOT an int (OrderStatus.PENDING == 1 is False even
# if its value happens to be 1). IntEnum members ARE ints -- they compare
# and do arithmetic with plain integers -- useful when you need enum-style
# names but must still interoperate with code expecting real int values
# (e.g. HTTP status codes, exit codes).
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


print("\nPriority.HIGH == 3:", Priority.HIGH == 3)
print("Priority.HIGH > Priority.LOW:", Priority.HIGH > Priority.LOW)
print("sorted list of priorities:", sorted([Priority.HIGH, Priority.LOW, Priority.MEDIUM]))

# ---------------------------------------------------------------------------
# 7. Adding methods to an Enum
# ---------------------------------------------------------------------------
# An Enum is a real class, so it can define ordinary methods and properties
# alongside its members -- a great place for small pieces of behavior that
# are naturally "one per member".
class TrafficLight(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

    def next_light(self):
        order = [TrafficLight.RED, TrafficLight.GREEN, TrafficLight.YELLOW]
        return order[(order.index(self) + 1) % len(order)]


light = TrafficLight.RED
print("\nTraffic light sequence:")
for _ in range(4):
    print(" ", light.value, "->", end=" ")
    light = light.next_light()
print(light.value)

# Key takeaways:
# - Plain strings/ints for a fixed set of options are typo-prone and
#   self-documenting only via comments; Enum makes the valid options
#   explicit, checkable, and impossible to misspell past import time.
# - Enum members are singletons: OrderStatus.PENDING is always the exact
#   same object, so `is` and `==` agree, and members work great as
#   match/case patterns or dict keys.
# - Members from DIFFERENT Enum classes are never equal, even with
#   identical underlying values -- Enums prevent exactly the kind of
#   silent mix-up raw constants allow.
# - auto() assigns values automatically when only the distinct names
#   matter; IntEnum members behave like real ints when you need that
#   interoperability (e.g. comparing/sorting, or matching a numeric API).
# - An Enum is a normal class -- it can define its own methods, giving you
#   a natural home for small per-member behavior.
