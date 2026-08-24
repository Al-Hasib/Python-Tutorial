"""
Strings in Depth

Strings represent text and are one of the most heavily used data types in
any Python program. Python offers several ways to create string literals,
powerful indexing and slicing syntax to pull out parts of a string, and a
rich set of built-in methods for cleaning, searching, and transforming
text. A crucial fact about strings is that they are immutable: once
created, a string's contents can never be changed in place -- any
"modification" actually produces a brand new string object. This file
explores string creation, slicing, immutability, common methods, and the
different ways to build formatted text.

This file covers:
- Creating strings: quotes, triple-quoted, and raw strings
- Indexing individual characters
- Slicing, including the step argument
- Immutability and what it implies in practice
- Common string methods (upper, lower, strip, split, join, replace, find,
  startswith, endswith, format)
- Concatenation vs f-strings
- Escape characters
"""

# ---------------------------------------------------------------------------
# 1. Creating strings: quotes, triple-quoted, raw strings
# ---------------------------------------------------------------------------
single = 'Hello'
double = "World"
print("single:", single, "| double:", double)

# Triple-quoted strings can span multiple lines and are also used for
# docstrings (like the one at the top of this file).
multiline = """This is line one.
This is line two.
This is line three."""
print("multiline string:\n" + multiline)

# Raw strings (prefix r) treat backslashes literally -- no escape
# sequences are processed. Very useful for file paths and regex patterns.
normal_path = "C:\\Users\\name\\folder"  # backslashes must be escaped
raw_path = r"C:\Users\name\folder"       # raw string: no escaping needed
print("normal_path:", normal_path)
print("raw_path:   ", raw_path)
print("Are they equal?", normal_path == raw_path)

# ---------------------------------------------------------------------------
# 2. Indexing
# ---------------------------------------------------------------------------
s = "Python"
print("s =", s)
print("s[0] (first character):     ", s[0])
print("s[1] (second character):    ", s[1])
print("s[-1] (last character):     ", s[-1])
print("s[-2] (second-to-last char):", s[-2])

# ---------------------------------------------------------------------------
# 3. Slicing (with step)
# ---------------------------------------------------------------------------
# Slicing syntax: s[start:stop:step]. `start` is inclusive, `stop` is
# exclusive, `step` controls direction/spacing (default 1).
s = "Hello, World!"
print("s =", s)
print("s[0:5]   (chars 0 up to 5):", s[0:5])
print("s[7:]    (from index 7 to end):", s[7:])
print("s[:5]    (from start to index 5):", s[:5])
print("s[:]     (full copy):", s[:])
print("s[::2]   (every 2nd char):", s[::2])
print("s[::-1]  (reversed string):", s[::-1])
print("s[1:10:2](chars 1..9, step 2):", s[1:10:2])

# ---------------------------------------------------------------------------
# 4. Immutability and what it implies
# ---------------------------------------------------------------------------
# You CANNOT change a character in place; this would raise a TypeError:
#     s[0] = "h"   # TypeError: 'str' object does not support item assignment
#
# Instead, any "modification" builds and returns a NEW string.
original = "cat"
modified = original.replace("c", "b")  # creates a new string "bat"
print("original:", original, "| modified:", modified)
print("original is unchanged:", original == "cat")

# Repeated concatenation in a loop creates many intermediate string objects
# because each `+=` builds a brand new string -- worth knowing for
# performance-sensitive code (str.join is more efficient for many pieces).
pieces = ["a", "b", "c"]
built = ""
for piece in pieces:
    built += piece  # each iteration creates a new string object
print("built via += loop:", built)

# ---------------------------------------------------------------------------
# 5. Common string methods
# ---------------------------------------------------------------------------
text = "  Hello, Python World!  "
print("original text:", repr(text))
print("upper():      ", text.upper())
print("lower():      ", text.lower())
print("strip():      ", repr(text.strip()))          # removes leading/trailing whitespace
print("split(','):   ", text.strip().split(","))      # splits into a list by delimiter
print("split():      ", text.split())                 # splits on any whitespace by default
print("join():       ", "-".join(["2026", "08", "24"]))  # opposite of split
print("replace():    ", text.replace("Python", "Amazing"))
print("find('Python'):", text.find("Python"))          # index of first match, -1 if absent
print("find('Java'):  ", text.find("Java"))
print("startswith():  ", text.strip().startswith("Hello"))
print("endswith():    ", text.strip().endswith("!"))
print("format():      ", "{} has {} letters".format("Python", len("Python")))

# ---------------------------------------------------------------------------
# 6. Concatenation vs f-strings
# ---------------------------------------------------------------------------
first = "Py"
second = "thon"

# Concatenation with + requires all pieces to already be strings.
combined = first + second
print("concatenation (+):", combined)

# For mixing in non-string values, + requires manual str() conversion...
count = 3
message_concat = "You have " + str(count) + " new messages"
print("concat with str():", message_concat)

# ...while f-strings handle the conversion automatically and read more
# clearly, especially when combining several values.
message_fstring = f"You have {count} new messages"
print("f-string:         ", message_fstring)

# ---------------------------------------------------------------------------
# 7. Escape characters
# ---------------------------------------------------------------------------
# A backslash introduces an escape sequence inside a normal string.
print("Newline:\nSecond line")
print("Tab:\tAfter tab")
print("Backslash: \\")
print('Single quote inside double quotes: "it\'s fine"')
print("Double quote inside double quotes: \"quoted text\"")
print("Carriage return demo ->", "A\rB")  # \r moves cursor to line start

# Key takeaways:
# - Strings can be single, double, or triple-quoted; raw strings (r"...")
#   disable escape sequence processing, useful for paths and regex.
# - Indexing accesses one character; slicing s[start:stop:step] extracts
#   a substring, and a negative step (e.g. s[::-1]) reverses it.
# - Strings are immutable -- methods like replace() and upper() always
#   return a NEW string rather than modifying the original.
# - Common methods (upper, lower, strip, split, join, replace, find,
#   startswith, endswith, format) cover most everyday text processing.
# - f-strings are generally the clearest way to mix variables into text,
#   automatically converting non-string values for you.
