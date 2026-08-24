"""
Memory Management & Garbage Collection

Python manages memory automatically, but understanding how helps you write
programs that don't silently leak memory. CPython primarily uses reference
counting: every object tracks how many references point to it, and is freed
the instant that count hits zero. Reference counting alone cannot free
objects that reference each other in a cycle (like two objects pointing at
each other), so Python also runs a generational garbage collector that
periodically detects and cleans up such cycles. Knowing about `id()`,
`weakref`, and the `gc` module gives you the tools to reason about object
lifetime and identity precisely.

This file covers:
- Reference counting with sys.getrefcount
- The gc module: generational garbage collection, gc.collect()
- Reference cycles and how the garbage collector handles them
- The weakref module (brief introduction)
- id() and object identity
- Why this matters for avoiding memory leaks
"""

import sys
import gc
import weakref

# ---------------------------------------------------------------------------
# 1. Reference counting with sys.getrefcount
# ---------------------------------------------------------------------------
# Every Python object has a reference count. When it reaches zero, CPython
# immediately deallocates the object -- no waiting for a GC pass. Note:
# sys.getrefcount() itself creates one temporary extra reference (the argument
# passed to it), so the reported count is always 1 higher than you might expect.

my_list = [1, 2, 3]
print("Reference counting:")
print("  refcount of my_list right after creation:", sys.getrefcount(my_list))

another_name = my_list  # a second reference to the same object
print("  refcount after adding another_name reference:", sys.getrefcount(my_list))

del another_name  # remove that reference
print("  refcount after deleting another_name:", sys.getrefcount(my_list))

# ---------------------------------------------------------------------------
# 2. id() and object identity
# ---------------------------------------------------------------------------
# id() returns a unique integer identifying an object for its lifetime (in
# CPython, this is the object's memory address). Two names refer to the SAME
# object if their id()s match; use `is` to check identity, `==` for equality.

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print("\nObject identity with id():")
print("  id(a):", id(a))
print("  id(b):", id(b))
print("  id(c):", id(c))
print("  a == b (equal values):", a == b)
print("  a is b (same object)?:", a is b)
print("  a is c (same object)?:", a is c)

# ---------------------------------------------------------------------------
# 3. Reference cycles and the generational garbage collector
# ---------------------------------------------------------------------------
# Reference counting cannot free two objects that reference each other, since
# neither count ever drops to zero on its own. Python's `gc` module runs a
# generational, cycle-detecting collector to reclaim these periodically.

class Node:
    def __init__(self, name):
        self.name = name
        self.partner = None

    def __repr__(self):
        return f"Node({self.name})"

    def __del__(self):
        print(f"  __del__ called for {self.name}")


print("\nCreating a reference cycle:")
node_a = Node("A")
node_b = Node("B")
node_a.partner = node_b  # A references B
node_b.partner = node_a  # B references A -- a cycle!

print("  node_a and node_b now reference each other")
del node_a
del node_b  # both names are gone, but the objects still reference each other

print("  Deleted both external references; objects not freed yet (still cyclic)")
collected = gc.collect()  # force a garbage collection pass
print(f"  gc.collect() ran and collected {collected} objects (cycle broken and freed)")

# ---------------------------------------------------------------------------
# 4. The gc module: generations and thresholds
# ---------------------------------------------------------------------------
# The cyclic GC organizes tracked objects into 3 generations (0, 1, 2). New
# objects start in generation 0. Objects that survive a collection pass move
# to an older generation, which is collected less often -- the assumption
# being that older objects are less likely to become garbage soon.

print("\ngc module info:")
print("  gc.isenabled():", gc.isenabled())
print("  gc.get_threshold() (gen0, gen1, gen2 thresholds):", gc.get_threshold())
print("  gc.get_count() (current object counts per generation):", gc.get_count())

# ---------------------------------------------------------------------------
# 5. weakref: referencing without keeping an object alive
# ---------------------------------------------------------------------------
# A weak reference points to an object WITHOUT increasing its reference
# count. This means a weakly-referenced object can still be garbage collected
# as if the weak reference didn't exist -- useful for caches, observer lists,
# or breaking cycles without changing your data structures.

class Resource:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"Resource({self.label})"


resource = Resource("cache-entry")
weak_ref = weakref.ref(resource)

print("\nweakref example:")
print("  weak_ref() while resource alive:", weak_ref())

del resource  # the only strong reference is gone
print("  weak_ref() after deleting the only strong reference:", weak_ref())
# -> None, because the weak reference did not keep the object alive.

# ---------------------------------------------------------------------------
# 6. Why this matters: avoiding memory leaks
# ---------------------------------------------------------------------------
# Common causes of "memory leaks" in Python (objects living far longer than
# intended) include:
#   - Growing caches or logs (lists/dicts) that are never cleared
#   - Reference cycles combined with __del__ methods that used to prevent
#     collection in old Python versions (modern CPython handles this, but
#     cycles still delay collection until the GC runs)
#   - Holding strong references in global registries/observer lists when a
#     weakref would be more appropriate
#   - Closures or callbacks that capture large objects unintentionally
#
# Tools to investigate suspected leaks:
#   - gc.collect() to force collection and see what gets freed
#   - gc.get_objects() / gc.garbage to inspect uncollectable objects
#   - sys.getrefcount() to check if something is unexpectedly still referenced
#   - weakref for caches/registries that should not keep objects alive

print("\nSummary: use gc.collect(), sys.getrefcount(), and weakref to diagnose")
print("unexpectedly long-lived objects and avoid unintentional memory growth.")

# Key takeaways:
# - CPython frees most objects instantly via reference counting when their
#   refcount hits zero; sys.getrefcount() reports this count (plus one, for
#   its own temporary reference).
# - id() gives an object's unique identity; use `is` to compare identity and
#   `==` to compare value equality.
# - Reference cycles (objects referencing each other) are not freed by simple
#   refcounting -- the generational `gc` module detects and collects them.
# - weakref lets you reference an object without keeping it alive, useful for
#   caches and registries.
# - Understanding these tools helps diagnose and avoid memory leaks caused by
#   unintended long-lived references or uncollected cycles.
