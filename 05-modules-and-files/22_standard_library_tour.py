"""
Python Standard Library Tour
------------------------------
Python ships with a huge "standard library" of modules that are installed
alongside the interpreter, so you get a lot of functionality for free
without installing anything extra. This file gives a brief, practical
tour of some of the most commonly used modules. Knowing what is already
available in the standard library saves you time and prevents you from
reinventing (or unnecessarily installing) things that Python already
provides.

This file covers:
- `os`: current working directory, listing files, joining paths
- `sys`: command-line arguments and the interpreter's module search path
- `math`: square root, pi, floor/ceil
- `random`: randint, choice, shuffle, seed
- `datetime`: a light look at dates and times (a dedicated topic covers
  this in depth later)
- `collections`: a quick preview of Counter and defaultdict
- `itertools`: a quick preview of count and chain
"""

import os
import sys
import math
import random
import datetime
from collections import Counter, defaultdict
from itertools import count, chain

# ---------------------------------------------------------------------------
# 1. os - operating system interfaces
# ---------------------------------------------------------------------------
print("-- os module --")
current_dir = os.getcwd()
print("Current working directory:", current_dir)

# List entries in the current directory (files and folders)
entries = os.listdir(current_dir)
print("Number of entries in current directory:", len(entries))
print("First 5 entries:", entries[:5])

# os.path.join builds paths correctly for the current operating system
# (using backslash on Windows, forward slash on Linux/macOS).
joined_path = os.path.join(current_dir, "sample_files", "example.txt")
print("Joined path:", joined_path)

# ---------------------------------------------------------------------------
# 2. sys - system-specific parameters and functions
# ---------------------------------------------------------------------------
print("\n-- sys module --")
print("Command-line arguments (sys.argv):", sys.argv)
print("Script name is sys.argv[0]:", sys.argv[0])
print("Number of entries in sys.path:", len(sys.path))
print("Python version running this script:", sys.version.split()[0])

# ---------------------------------------------------------------------------
# 3. math - mathematical functions
# ---------------------------------------------------------------------------
print("\n-- math module --")
print("Square root of 2:", math.sqrt(2))
print("Value of pi:", math.pi)
print("floor(3.7):", math.floor(3.7))
print("ceil(3.2):", math.ceil(3.2))
print("floor(-3.2):", math.floor(-3.2))
print("ceil(-3.7):", math.ceil(-3.7))

# ---------------------------------------------------------------------------
# 4. random - generating pseudo-random values
# ---------------------------------------------------------------------------
print("\n-- random module --")
# seed() makes the "random" results reproducible - same seed, same output.
random.seed(42)
print("randint(1, 100):", random.randint(1, 100))

colors = ["red", "green", "blue", "yellow", "purple"]
print("random.choice from list:", random.choice(colors))

numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print("Shuffled list:", numbers)

# Re-seeding with the same value reproduces the same sequence again.
random.seed(42)
print("randint(1, 100) again after re-seeding:", random.randint(1, 100))

# ---------------------------------------------------------------------------
# 5. datetime - dates and times (light preview only)
# ---------------------------------------------------------------------------
# A dedicated tutorial on dates and times covers this module in depth
# later, so we only touch the basics here.
print("\n-- datetime module (brief preview) --")
today = datetime.date.today()
print("Today's date:", today)

now = datetime.datetime.now()
print("Current date and time:", now)

# Formatting a date as a string
print("Formatted date (YYYY-MM-DD):", today.strftime("%Y-%m-%d"))

# Simple date arithmetic using timedelta
one_week_later = today + datetime.timedelta(days=7)
print("One week from today:", one_week_later)

# ---------------------------------------------------------------------------
# 6. collections - specialized container datatypes (quick preview)
# ---------------------------------------------------------------------------
# collections gets its own deep dive later; this is just a taste.
print("\n-- collections module (quick preview) --")
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_counts = Counter(words)
print("Counter of words:", word_counts)
print("Most common word:", word_counts.most_common(1))

# defaultdict supplies a default value automatically for missing keys,
# so you don't need to check "if key in dict" before appending.
groups = defaultdict(list)
groups["fruits"].append("apple")
groups["fruits"].append("banana")
groups["vegetables"].append("carrot")
print("defaultdict result:", dict(groups))

# ---------------------------------------------------------------------------
# 7. itertools - efficient looping tools (quick preview)
# ---------------------------------------------------------------------------
# itertools also gets its own deep dive later; this is just a taste.
print("\n-- itertools module (quick preview) --")

# count() creates an infinite counter - use it carefully with something
# that stops iteration, like zip() with a finite list.
counter = count(start=10, step=5)
first_three_counts = [next(counter) for _ in range(3)]
print("First 3 values from itertools.count(10, step=5):", first_three_counts)

# chain() links multiple iterables together into one sequence.
list_a = [1, 2, 3]
list_b = ["x", "y", "z"]
chained = list(chain(list_a, list_b))
print("itertools.chain of two lists:", chained)

# Key takeaways:
# - The standard library gives you tools for files, the OS, math, random
#   values, dates, and specialized data structures without installing
#   anything extra.
# - os and sys are your bridge to the operating system and the running
#   interpreter (paths, working directory, arguments, search path).
# - math and random cover common numeric and randomization needs; seeding
#   random makes "random" results reproducible for testing.
# - datetime gives basic date/time handling; collections and itertools
#   offer specialized, efficient tools worth a deeper look later.
