"""
Magic / Dunder Methods
=======================

"Dunder" methods (short for "double underscore") are special methods
Python calls automatically for built-in operations: creating an object,
printing it, comparing it, adding two objects with `+`, indexing it with
`[]`, iterating over it, or even calling it like a function. Implementing
these methods lets your custom classes integrate naturally with Python's
built-in syntax and functions, instead of requiring users to call special
named methods. This is how Python achieves its consistent, expressive
feel across both built-in and user-defined types.

This file covers:
- __init__ (recap)
- __str__ vs __repr__ (and why both matter)
- __eq__ and __lt__ (comparisons / ordering)
- __len__
- __getitem__ / __setitem__
- __iter__ / __next__ (brief; generators covered later)
- __add__ (operator overloading)
- __call__
"""

# ---------------------------------------------------------------------------
# 1. __init__ (recap) and __str__ vs __repr__
# ---------------------------------------------------------------------------
# __str__: human-friendly text, used by print()/str(). Aim for readable.
# __repr__: unambiguous, developer-facing text, used by repr(), the REPL,
# and inside containers (e.g. printing a list of objects). Aim for
# something that ideally looks like valid Python code to recreate the object.
# If __str__ is missing, Python falls back to __repr__ for print() too --
# so it's good practice to always define __repr__ at minimum.

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"Card(rank={self.rank!r}, suit={self.suit!r})"


card = Card("Ace", "Spades")
print("str():", str(card))
print("repr():", repr(card))
print("Inside a list (uses repr):", [card])


# ---------------------------------------------------------------------------
# 2. __eq__ and __lt__ -- comparisons and ordering
# ---------------------------------------------------------------------------
# By default, objects compare by identity (are they the same object in
# memory?). __eq__ lets us define "equal" in terms of the data they hold.
# __lt__ ("less than") enables ordering with <, and lets sorted()/sort()
# work on our objects too.

class Money:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __repr__(self):
        return f"Money({self.amount})"


m1 = Money(10)
m2 = Money(10)
m3 = Money(25)

print("\nm1 == m2:", m1 == m2)   # True: same amount, thanks to __eq__
print("m1 == m3:", m1 == m3)     # False
print("m1 < m3:", m1 < m3)       # True, thanks to __lt__

wallet = [Money(50), Money(5), Money(20)]
print("Sorted wallet:", sorted(wallet))  # sorted() uses __lt__ internally


# ---------------------------------------------------------------------------
# 3. __len__
# ---------------------------------------------------------------------------
# Implementing __len__ lets len(obj) work on your custom class.

class Playlist:
    def __init__(self, songs):
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)


playlist = Playlist(["Song A", "Song B", "Song C"])
print("\nlen(playlist):", len(playlist))


# ---------------------------------------------------------------------------
# 4. __getitem__ / __setitem__ -- indexing like a list/dict
# ---------------------------------------------------------------------------
# __getitem__ enables obj[index]; __setitem__ enables obj[index] = value.
# Together they make a custom class behave like a sequence or mapping.

class Playlist2:
    def __init__(self, songs):
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __setitem__(self, index, value):
        self.songs[index] = value


pl = Playlist2(["Intro", "Chapter 1", "Chapter 2"])
print("\npl[0]:", pl[0])
pl[1] = "Chapter 1 (remastered)"
print("After __setitem__, pl[1]:", pl[1])
print("Iterating with a for-loop (uses __getitem__ under the hood):")
for i in range(len(pl)):
    print(" -", pl[i])


# ---------------------------------------------------------------------------
# 5. __iter__ / __next__ -- making an object directly iterable
# ---------------------------------------------------------------------------
# __iter__ should return an iterator object; __next__ produces the next
# value each time and raises StopIteration when exhausted. This is a
# brief introduction -- generators (a much simpler way to write iterators)
# are covered in a later file.

class CountUp:
    """Iterates from `start` to `end` (inclusive)."""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


print("\nCountUp(1, 5) via for-loop:")
for number in CountUp(1, 5):
    print(" ->", number)


# ---------------------------------------------------------------------------
# 6. __add__ -- operator overloading
# ---------------------------------------------------------------------------
# Defining __add__ lets instances of your class respond to the `+`
# operator with custom, meaningful behavior.

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"


v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)
print("\nv1 + v2 =", v1 + v2)  # calls v1.__add__(v2)


# ---------------------------------------------------------------------------
# 7. __call__ -- making instances callable like functions
# ---------------------------------------------------------------------------
# Implementing __call__ lets you use `instance(...)` just like calling a
# function. Useful for objects that wrap a bit of configurable behavior.

class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor


double = Multiplier(2)
triple = Multiplier(3)
print("\ndouble(5):", double(5))   # calls double.__call__(5)
print("triple(5):", triple(5))


# Key takeaways:
# - __str__ is for humans (print), __repr__ is for developers/debugging -- define both.
# - __eq__ and __lt__ let your objects support == and < (and sorted()/sort()).
# - __len__, __getitem__/__setitem__, and __iter__/__next__ make objects act like built-in containers.
# - __add__ (and its siblings __sub__, __mul__, etc.) enable operator overloading.
# - __call__ makes an instance usable as if it were a function: instance(args).
