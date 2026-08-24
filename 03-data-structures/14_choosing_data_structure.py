"""
Choosing the Right Data Structure
====================================
Python offers several built-in collection types - lists, tuples,
dictionaries, and sets - and picking the right one makes code both faster
and clearer. The choice usually comes down to four questions: Does the data
need to change after creation (mutability)? Does order matter (ordering)?
Do you need to look values up by a key or check membership quickly (lookup
speed)? Do duplicates make sense, or must every item be unique (uniqueness)?
This file walks through those questions and gives small, concrete examples
of each data structure being used for the job it is best suited to.

This file covers:
    - A quick comparison table (in comments) of list vs tuple vs dict vs set
    - Mutability: when you need to change data vs freeze it
    - Ordering: when position/order matters vs when it does not
    - Uniqueness: when duplicates are meaningful vs unwanted
    - Lookup speed: O(1) average lookups (dict/set) vs O(n) scans (list)
    - Worked examples: word frequency count, deduplication, fixed records,
      ordered collections
    - A simple decision checklist to apply when unsure
"""

import time

# ---------------------------------------------------------------------------
# 1. Quick comparison
# ---------------------------------------------------------------------------
# +-----------+-----------+---------+-------------+----------------------+
# | Structure | Mutable?  | Ordered?| Duplicates? | Typical lookup       |
# +-----------+-----------+---------+-------------+----------------------+
# | list      | Yes       | Yes     | Allowed     | O(n) "in" / by-index |
# |           |           |         |             | O(1) access          |
# | tuple     | No        | Yes     | Allowed     | O(n) "in" / by-index |
# |           |           |         |             | O(1) access          |
# | dict      | Yes       | Yes*    | Keys unique | O(1) average by key  |
# | set       | Yes       | No      | No dupes    | O(1) average member  |
# +-----------+-----------+---------+-------------+----------------------+
# * dicts preserve insertion order (Python 3.7+), but you look up by key,
#   not by position.

print("See the comparison table in the comments above this section.")

# ---------------------------------------------------------------------------
# 2. Mutability: change data vs freeze it
# ---------------------------------------------------------------------------
# Use a LIST when the collection will grow, shrink, or be reordered.
shopping_cart = ["bread", "milk"]
shopping_cart.append("eggs")
print("mutable shopping cart:", shopping_cart)

# Use a TUPLE when the values should never change after creation, such as
# a fixed geographic coordinate.
office_location = (48.8566, 2.3522)  # (latitude, longitude)
print("immutable coordinate:", office_location)
try:
    office_location[0] = 0
except TypeError as exc:
    print("Tuples reject mutation:", exc)

# ---------------------------------------------------------------------------
# 3. Ordering: position matters vs it does not
# ---------------------------------------------------------------------------
# ORDERED COLLECTION example: a playlist where sequence matters.
playlist = ["intro.mp3", "song1.mp3", "song2.mp3", "outro.mp3"]
print("playlist in order:", playlist)
print("first track:", playlist[0], "| last track:", playlist[-1])

# UNORDERED example: a set of tags has no meaningful "first" or "last".
tags = {"python", "tutorial", "beginner"}
print("tags (order not guaranteed/meaningful):", tags)

# ---------------------------------------------------------------------------
# 4. Uniqueness: duplicates matter vs they must be removed
# ---------------------------------------------------------------------------
# Deduplication with a SET: quickly reduce a list to unique values.
visitor_log = ["alice", "bob", "alice", "carol", "bob", "alice"]
unique_visitors = set(visitor_log)
print("visitor_log:", visitor_log)
print("unique_visitors:", unique_visitors)
print("total visits:", len(visitor_log), "| unique visitors:", len(unique_visitors))

# ---------------------------------------------------------------------------
# 5. Lookup speed: O(1) dict/set vs O(n) list scan
# ---------------------------------------------------------------------------
# Membership testing in a list requires scanning items one by one (O(n)).
# In a set or dict, hashing gives average O(1) lookups regardless of size.
size = 200_000
big_list = list(range(size))
big_set = set(big_list)
target = size - 1  # worst case for a list scan: item is near the end

start = time.perf_counter()
found_in_list = target in big_list
list_time = time.perf_counter() - start

start = time.perf_counter()
found_in_set = target in big_set
set_time = time.perf_counter() - start

print(f"'in' on list of {size}: {list_time:.6f}s (found={found_in_list})")
print(f"'in' on set of {size}:  {set_time:.6f}s (found={found_in_set})")
print("-> sets/dicts stay fast as size grows; list scans get slower.")

# ---------------------------------------------------------------------------
# 6. Worked example: word frequency count with a dict
# ---------------------------------------------------------------------------
text = "the quick brown fox jumps over the lazy dog the fox runs"
words = text.split()

word_counts = {}
for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1

print("word_counts:", word_counts)
print("most frequent word:", max(word_counts, key=word_counts.get))

# ---------------------------------------------------------------------------
# 7. Worked example: deduplicating with a set
# ---------------------------------------------------------------------------
emails_submitted = [
    "a@example.com",
    "b@example.com",
    "a@example.com",
    "c@example.com",
    "b@example.com",
]
unique_emails = set(emails_submitted)
print("unique_emails:", unique_emails)
print("duplicate submissions removed:", len(emails_submitted) - len(unique_emails))

# ---------------------------------------------------------------------------
# 8. Worked example: fixed records with a tuple
# ---------------------------------------------------------------------------
# Each record has a known, fixed shape that should not change - a tuple
# communicates "this is a stable record" better than a list would.
employee_record = ("Alice", "Engineering", 2021)  # (name, department, year_joined)
name, department, year_joined = employee_record
print(f"{name} joined {department} in {year_joined}")

employee_records = [
    ("Alice", "Engineering", 2021),
    ("Bob", "Design", 2019),
    ("Carol", "Marketing", 2022),
]
for rec_name, rec_dept, rec_year in employee_records:
    print(f"record -> name={rec_name}, dept={rec_dept}, year={rec_year}")

# ---------------------------------------------------------------------------
# 9. Worked example: ordered collection with a list
# ---------------------------------------------------------------------------
# A task queue where processing order matters and items are added/removed
# over time - a list (or collections.deque for heavy queue use) fits well.
task_queue = []
task_queue.append("send email")
task_queue.append("generate report")
task_queue.append("backup database")
print("task_queue:", task_queue)

next_task = task_queue.pop(0)  # process tasks in the order they arrived
print("processing:", next_task)
print("remaining queue:", task_queue)

# ---------------------------------------------------------------------------
# 10. Decision checklist
# ---------------------------------------------------------------------------
# Ask yourself, in order:
#   1. Do I need to look things up by a key (name -> value)?
#        -> Yes: use a dict.
#   2. Do I only care whether items exist, with no duplicates, and want
#      fast membership checks or set math (union/intersection/etc.)?
#        -> Yes: use a set.
#   3. Will the collection's contents change after creation (add/remove/
#      reorder items)?
#        -> Yes: use a list.
#        -> No, it's a fixed, order-sensitive record: use a tuple.
#   4. Still unsure? Start with a list (the most flexible general-purpose
#      choice) and switch to a more specific structure once the access
#      pattern becomes clear.

print("Use the checklist in the comments above to pick a data structure.")

# Key takeaways:
# - Reach for a dict when you look things up by key; for a set when you
#   need uniqueness or fast membership/set-math; for a list when order
#   matters and contents change; for a tuple when the record is fixed.
# - dict and set give average O(1) lookups via hashing; list and tuple
#   require an O(n) scan to check membership by value.
# - Tuples and lists both preserve order; only tuples are immutable.
# - Sets and dict keys enforce uniqueness automatically - use that to your
#   advantage for deduplication instead of writing manual loops.
# - When in doubt, start simple (a list) and refine the choice once you
#   know how the data will actually be accessed.
