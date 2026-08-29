"""
Regular Expressions
====================

Regular expressions (regex) are a compact language for describing patterns
in text, letting you search, validate, extract, and replace substrings far
more powerfully than plain string methods like `str.find()` or `str.split()`.
Python's built-in `re` module implements this language. Regex is especially
useful for tasks like validating input formats, pulling structured data
(numbers, dates, emails) out of free text, and doing pattern-based find and
replace. It has a reputation for being cryptic, but a handful of building
blocks -- character classes, quantifiers, anchors, and groups -- cover the
vast majority of real-world use cases.

This file covers:
- The re module
- match vs search vs findall vs finditer
- Common patterns: character classes, quantifiers, anchors, groups
- re.sub for replacement
- Compiling patterns with re.compile
- Named groups
- Practical examples: a simple email-like validator, extracting numbers
"""

import re

# ---------------------------------------------------------------------------
# 1. The re module -- a first look
# ---------------------------------------------------------------------------
text = "The rain in Spain falls mainly on the plain."

result = re.search(r"ain", text)
print("re.search(r'ain', text) found at index:", result.start() if result else None)
print("Matched text:", result.group() if result else None)

# ---------------------------------------------------------------------------
# 2. match vs search vs findall vs finditer
# ---------------------------------------------------------------------------
# re.match()    -> only checks for a match at the START of the string.
# re.search()   -> scans the whole string for the first match, anywhere.
# re.findall()  -> returns ALL matches as a list of strings (or tuples).
# re.finditer() -> returns ALL matches as an iterator of match objects
#                  (lazy, and gives you position info via .start()/.end()).

sample = "cat hat bat mat"

print("\nre.match(r'cat', sample)    ->", re.match(r"cat", sample))
print("re.match(r'hat', sample)    ->", re.match(r"hat", sample))  # None: not at start
print("re.search(r'hat', sample)   ->", re.search(r"hat", sample))
print("re.findall(r'\\w at', sample) ->", re.findall(r"\wat", sample))

print("re.finditer(r'\\wat', sample):")
for m in re.finditer(r"\wat", sample):
    print(f"  matched {m.group()!r} at [{m.start()}:{m.end()}]")

# ---------------------------------------------------------------------------
# 3. Common patterns: character classes
# ---------------------------------------------------------------------------
# \d  digit           \D  non-digit
# \w  word char        \W  non-word char
# \s  whitespace       \S  non-whitespace
# [abc]  any of a, b, c        [^abc]  anything except a, b, c
# [a-z]  lowercase letter range   [0-9]  digit range

mixed = "Order #4521 shipped on 2026-08-24, cost $19.99!"

print("\nCharacter classes:")
print("  \\d+ (digit runs):     ", re.findall(r"\d+", mixed))
print("  \\w+ (word chars):     ", re.findall(r"\w+", mixed)[:5], "...")
print("  [A-Z][a-z]+ (Capitalized words):", re.findall(r"[A-Z][a-z]+", mixed))
print("  \\S+ (non-space runs): ", re.findall(r"\S+", mixed)[:4], "...")

# ---------------------------------------------------------------------------
# 4. Common patterns: quantifiers
# ---------------------------------------------------------------------------
# *      0 or more       +      1 or more       ?      0 or 1 (optional)
# {n}    exactly n        {n,}   n or more       {n,m}  between n and m

print("\nQuantifiers:")
print("  colou?r matches 'color' and 'colour':", re.findall(r"colou?r", "color colour colouur"))
print("  a{2,3} matches 2-3 a's:", re.findall(r"a{2,3}", "a aa aaa aaaa"))
print("  \\d{4} matches exactly 4 digits:", re.findall(r"\d{4}", "12 1234 123456"))

# ---------------------------------------------------------------------------
# 5. Common patterns: anchors
# ---------------------------------------------------------------------------
# ^   start of string (or line, with re.MULTILINE)
# $   end of string (or line, with re.MULTILINE)
# \b  word boundary

print("\nAnchors:")
print("  ^The matches start of string:", bool(re.match(r"^The", text)))
print("  plain\\.$ matches end of string:", bool(re.search(r"plain\.$", text)))
print("  \\bain\\b (whole word 'ain'):", re.findall(r"\bain\b", "ain Spain ain't"))
print("  \\brain\\b (whole word 'rain'):", re.findall(r"\brain\b", text))

# ---------------------------------------------------------------------------
# 6. Common patterns: groups
# ---------------------------------------------------------------------------
# Parentheses ( ) capture part of a match so you can pull it out separately.

log_line = "2026-08-24 14:30:00 ERROR Connection timed out"
m = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)", log_line)
print("\nGroups from a log line:")
if m:
    print("  full match:", m.group(0))
    print("  group 1 (date):", m.group(1))
    print("  group 2 (time):", m.group(2))
    print("  group 3 (level):", m.group(3))
    print("  group 4 (message):", m.group(4))
    print("  all groups as a tuple:", m.groups())

# ---------------------------------------------------------------------------
# 7. re.sub for replacement
# ---------------------------------------------------------------------------
# re.sub(pattern, replacement, string) replaces every match. The
# replacement can reference captured groups with backreferences (\1, \2...).

censored = re.sub(r"\d", "*", "Call 555-1234 now")
print("\nre.sub replacing digits with '*':", censored)

reformatted = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", "Date: 2026-08-24")
print("re.sub reformatting a date with backreferences:", reformatted)

# A replacement function can also be passed instead of a string.
def shout_match(match):
    return match.group().upper()


shouted = re.sub(r"\b\w{4,}\b", shout_match, "the quick brown fox jumps")
print("re.sub with a function (uppercase words of length>=4):", shouted)

# ---------------------------------------------------------------------------
# 8. Compiling patterns with re.compile
# ---------------------------------------------------------------------------
# Compiling a pattern once and reusing it is more efficient when the same
# pattern is applied many times, and it keeps the pattern readable as a
# named object.

word_pattern = re.compile(r"\b[A-Za-z]+\b")
sentences = ["Hello world!", "Regex is fun.", "Compile once, use often."]

print("\nUsing a compiled pattern across multiple strings:")
for sentence in sentences:
    print(f"  {sentence!r} -> {word_pattern.findall(sentence)}")

# ---------------------------------------------------------------------------
# 9. Named groups
# ---------------------------------------------------------------------------
# (?P<name>...) lets you refer to a captured group by name instead of by
# position, which makes complex patterns much easier to read and maintain.

named_pattern = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
)
match = named_pattern.search("Event date: 2026-08-24")
print("\nNamed groups:")
if match:
    print("  year :", match.group("year"))
    print("  month:", match.group("month"))
    print("  day  :", match.group("day"))
    print("  as a dict:", match.groupdict())

# ---------------------------------------------------------------------------
# 10. Practical example: a simple email-like validator
# ---------------------------------------------------------------------------
# Real email validation is notoriously tricky; this is a simplified pattern
# good enough for basic sanity-checking, not full RFC compliance.

email_pattern = re.compile(r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$")

candidates = [
    "abdullah@nybsys.com",
    "not-an-email",
    "user.name+tag@example.co",
    "missing-at-sign.com",
    "user@no-dot",
]

print("\nSimple email-like validation:")
for candidate in candidates:
    is_valid = bool(email_pattern.match(candidate))
    print(f"  {candidate!r:35s} -> {'valid' if is_valid else 'invalid'}")

# ---------------------------------------------------------------------------
# 11. Practical example: extracting numbers from text
# ---------------------------------------------------------------------------
report = "Revenue grew 12.5% to $4,500,000 with 320 new customers in Q3 2026."

# Extract integers and decimals (a simple approach: digits with an optional
# decimal point; commas are stripped separately since \d+ won't match them).
plain_numbers = re.findall(r"\d+\.\d+|\d+", report.replace(",", ""))
print("\nExtracting numbers from a report:")
print("  text:", report)
print("  numbers found:", plain_numbers)

# Extract just the currency amount using a more targeted pattern.
currency_match = re.search(r"\$[\d,]+", report)
print("  currency amount:", currency_match.group() if currency_match else None)

# Key takeaways:
# - re.match anchors at the string's start, re.search scans anywhere,
#   re.findall collects all matches as strings, re.finditer yields match
#   objects lazily (useful for positions via .start()/.end()).
# - Character classes (\d, \w, \s and their negations), quantifiers
#   (*, +, ?, {n,m}), and anchors (^, $, \b) are the core vocabulary for
#   building most patterns.
# - Parentheses create capturing groups; (?P<name>...) creates named groups
#   accessible via match.group("name") or match.groupdict().
# - re.sub replaces matches with a string (optionally using \1, \2
#   backreferences) or the result of a callback function.
# - re.compile(pattern) is worth using when a pattern is applied repeatedly
#   -- it is both more efficient and easier to name and reuse.
