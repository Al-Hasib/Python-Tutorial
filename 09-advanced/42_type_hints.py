"""
Type Hints & Static Typing

Python is dynamically typed at runtime, but since Python 3.5 it supports
optional type hints (annotations) that describe the expected types of
variables, function parameters, and return values. Type hints do not change
how the code runs -- Python ignores them at execution time -- but they let
external tools like mypy catch bugs before you run the program, and they make
code far easier to read and maintain. Modern Python (3.9+) also lets you use
built-in containers like list[int] directly as generics, reducing the need to
import from `typing` for simple cases.

This file covers:
- Basic annotations for variables and functions
- The typing module: List, Dict, Optional, Union, Tuple, Callable
- Modern built-in generics: list[int], dict[str, int], etc.
- TypeVar for writing generic functions (light introduction)
- Why type hints are NOT enforced at runtime
- Checking types statically with mypy (explained, not run)
- dataclasses as a practical, typed-class example
"""

from typing import List, Dict, Optional, Union, Tuple, Callable, TypeVar
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 1. Basic annotations for variables and functions
# ---------------------------------------------------------------------------
# A variable annotation is just a hint; Python does not check it.
age: int = 30
name: str = "Alice"
price: float = 19.99

print("Basic annotations:")
print("  age =", age, "(annotated int)")
print("  name =", name, "(annotated str)")


def add(a: int, b: int) -> int:
    """Function annotations describe parameter types and the return type."""
    return a + b


def greet(person: str, excited: bool = False) -> str:
    return f"Hello, {person}!" + ("!!!" if excited else "")


print("add(2, 3) =", add(2, 3))
print("greet('Bob', excited=True) =", greet("Bob", excited=True))

# ---------------------------------------------------------------------------
# 2. The typing module: List, Dict, Optional, Union, Tuple, Callable
# ---------------------------------------------------------------------------
# These generic aliases describe the *shape* of composite types.

def average(values: List[float]) -> float:
    return sum(values) / len(values)


def word_lengths(words: List[str]) -> Dict[str, int]:
    return {w: len(w) for w in words}


def find_user(user_id: int) -> Optional[str]:
    """Optional[X] means 'X or None' -- a very common pattern for lookups."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # returns None if not found


def parse_number(text: str) -> Union[int, float]:
    """Union[X, Y] means 'X or Y'."""
    return int(text) if text.isdigit() else float(text)


def min_max(values: List[int]) -> Tuple[int, int]:
    """Tuple[int, int] means a 2-tuple of exactly two ints."""
    return min(values), max(values)


def apply_twice(func: Callable[[int], int], value: int) -> int:
    """Callable[[ArgTypes], ReturnType] describes a function's signature."""
    return func(func(value))


print("\ntyping module examples:")
print("  average([1.0, 2.0, 3.0]) =", average([1.0, 2.0, 3.0]))
print("  word_lengths(['hi', 'world']) =", word_lengths(["hi", "world"]))
print("  find_user(1) =", find_user(1))
print("  find_user(99) =", find_user(99))
print("  parse_number('42') =", parse_number("42"))
print("  parse_number('3.14') =", parse_number("3.14"))
print("  min_max([5, 1, 9, 3]) =", min_max([5, 1, 9, 3]))
print("  apply_twice(lambda x: x * 2, 3) =", apply_twice(lambda x: x * 2, 3))

# ---------------------------------------------------------------------------
# 3. Modern built-in generics (Python 3.9+)
# ---------------------------------------------------------------------------
# Since 3.9, built-in containers support subscripting directly, so you often
# no longer need typing.List / typing.Dict / typing.Tuple at all.

def unique_sorted(values: list[int]) -> list[int]:
    return sorted(set(values))


def counts(items: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        result[item] = result.get(item, 0) + 1
    return result


print("\nModern built-in generics (list[int], dict[str, int]):")
print("  unique_sorted([3, 1, 2, 1, 3]) =", unique_sorted([3, 1, 2, 1, 3]))
print("  counts(['a', 'b', 'a']) =", counts(["a", "b", "a"]))

# Since 3.10, `X | Y` can also replace Union[X, Y], and `X | None` can
# replace Optional[X], e.g.:  def f(x: int | None) -> str | int: ...

# ---------------------------------------------------------------------------
# 4. TypeVar for generic functions (light introduction)
# ---------------------------------------------------------------------------
# TypeVar lets you write a function that works with any type T, while telling
# static checkers that the input and output types are linked.

T = TypeVar("T")


def first_element(items: List[T]) -> T:
    """Works for a list of any type; the return type matches the list's type."""
    return items[0]


print("\nTypeVar generic example:")
print("  first_element([10, 20, 30]) =", first_element([10, 20, 30]))
print("  first_element(['x', 'y']) =", first_element(["x", "y"]))

# ---------------------------------------------------------------------------
# 5. Type hints are NOT enforced at runtime
# ---------------------------------------------------------------------------
# Python happily runs this even though the annotation says int -- hints are
# just metadata stored on the function, not runtime checks.

def double(n: int) -> int:
    return n * 2


print("\nType hints are not enforced at runtime:")
print("  double('ab') =", double("ab"))  # 'ab' is not an int, but this still runs!
print("  __annotations__ of double:", double.__annotations__)

# ---------------------------------------------------------------------------
# 6. Checking types statically with mypy
# ---------------------------------------------------------------------------
# mypy is a separate, popular static type checker. It reads your annotations
# WITHOUT running your code, and reports mismatches like calling double("ab").
#
# You would install it with:   pip install mypy
# And run it from the terminal (not from inside this script):
#   mypy 42_type_hints.py
#
# mypy would flag double("ab") above with something like:
#   error: Argument 1 to "double" has incompatible type "str"; expected "int"
#
# This script intentionally does NOT invoke mypy -- it is a separate tool you
# run as part of your development workflow, e.g. in CI or before committing.

print("\n(mypy would be run from the command line: `mypy 42_type_hints.py`)")

# ---------------------------------------------------------------------------
# 7. dataclasses: a practical typed-class example
# ---------------------------------------------------------------------------
# @dataclass generates __init__, __repr__, and __eq__ automatically based on
# annotated class attributes -- a great showcase of type hints doing real work.

@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    in_stock: bool = True


p1 = Product("Keyboard", 49.99, tags=["electronics", "accessories"])
p2 = Product("Keyboard", 49.99, tags=["electronics", "accessories"])

print("\ndataclass example:")
print("  p1 =", p1)
print("  p1 == p2:", p1 == p2)  # auto-generated __eq__ compares field values


@dataclass(frozen=True)
class Point:
    x: int
    y: int


pt = Point(3, 4)
print("  frozen Point:", pt)
try:
    pt.x = 10  # frozen=True makes instances immutable
except Exception as e:
    print("  Expected error mutating frozen dataclass:", type(e).__name__, e)

# Key takeaways:
# - Type hints document intent for variables, parameters, and return values,
#   but Python does not check or enforce them at runtime.
# - The typing module (List, Dict, Optional, Union, Tuple, Callable) describes
#   composite shapes; modern Python often lets you write list[int] directly.
# - TypeVar enables writing generic functions whose input/output types are linked.
# - Static checkers like mypy read your hints without running your code and
#   catch mismatches early -- run them as a separate development step.
# - @dataclass turns annotated class attributes into a full-featured class with
#   __init__, __repr__, and __eq__ generated for you automatically.
