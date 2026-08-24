"""
Working with CSV/JSON
-----------------------
CSV (Comma-Separated Values) and JSON (JavaScript Object Notation) are
two of the most common data interchange formats you will meet in real
projects - CSV for tabular/spreadsheet-style data, JSON for structured,
nested data used heavily by web APIs and config files. Python's standard
library has built-in `csv` and `json` modules that handle the parsing and
formatting details for you, so you rarely need to write this logic by
hand. This file demonstrates both modules and highlights a few pitfalls
that trip up beginners.

This file covers:
- The `csv` module: `reader`, `writer`, `DictReader`, `DictWriter`
- The `json` module: `dumps`, `loads`, `dump`, `load`
- Converting between Python objects and JSON
- Handling nested JSON structures
- Common pitfalls (JSON has no tuples/sets, CSV is all strings)
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
SAMPLE_DIR = BASE_DIR / "sample_files"
SAMPLE_DIR.mkdir(exist_ok=True)

csv_file = SAMPLE_DIR / "people.csv"
json_file = SAMPLE_DIR / "people.json"

# ---------------------------------------------------------------------------
# 1. Writing CSV with csv.writer
# ---------------------------------------------------------------------------
# csv.writer works with plain rows (lists/tuples). newline="" is
# recommended on all platforms to avoid extra blank lines being inserted.
print("-- csv.writer --")
rows = [
    ["name", "age", "city"],
    ["Alice", "30", "New York"],
    ["Bob", "25", "London"],
    ["Charlie", "35", "Sydney"],
]
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
print("Wrote CSV rows to:", csv_file)

# ---------------------------------------------------------------------------
# 2. Reading CSV with csv.reader
# ---------------------------------------------------------------------------
# csv.reader yields each row as a plain list of strings.
print("\n-- csv.reader --")
with open(csv_file, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print("  Row:", row)

# ---------------------------------------------------------------------------
# 3. Writing CSV with csv.DictWriter
# ---------------------------------------------------------------------------
# DictWriter lets you write rows as dictionaries, matched to column names
# given by "fieldnames". writeheader() writes the header row for you.
print("\n-- csv.DictWriter --")
people = [
    {"name": "Diana", "age": 28, "city": "Paris"},
    {"name": "Ethan", "age": 40, "city": "Tokyo"},
]
with open(csv_file, "w", newline="") as f:
    fieldnames = ["name", "age", "city"]
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    for person in people:
        dict_writer.writerow(person)
print("Wrote CSV via DictWriter to:", csv_file)

# ---------------------------------------------------------------------------
# 4. Reading CSV with csv.DictReader
# ---------------------------------------------------------------------------
# DictReader treats the first row as headers and yields each subsequent
# row as an OrderedDict/dict mapping header -> value.
print("\n-- csv.DictReader --")
with open(csv_file, "r", newline="") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        print("  Row as dict:", dict(row))

# ---------------------------------------------------------------------------
# 5. Pitfall: CSV values are always strings
# ---------------------------------------------------------------------------
# Even though we wrote the number 28 as an integer into the dictionary,
# reading it back from CSV always gives a string, since CSV has no
# concept of data types - everything is just text.
print("\n-- Pitfall: CSV is all strings --")
with open(csv_file, "r", newline="") as f:
    dict_reader = csv.DictReader(f)
    first_row = next(dict_reader)
print("Type of 'age' read from CSV:", type(first_row["age"]))
print("Value:", repr(first_row["age"]))
age_as_int = int(first_row["age"])
print("After manual conversion, type:", type(age_as_int))

# ---------------------------------------------------------------------------
# 6. Converting Python objects to JSON with json.dumps
# ---------------------------------------------------------------------------
# json.dumps() converts a Python object into a JSON-formatted string.
print("\n-- json.dumps --")
person_data = {
    "name": "Alice",
    "age": 30,
    "is_admin": False,
    "skills": ["python", "sql", "docker"],
    "address": None,
}
json_string = json.dumps(person_data, indent=2)
print("JSON string:")
print(json_string)

# ---------------------------------------------------------------------------
# 7. Converting JSON back to Python objects with json.loads
# ---------------------------------------------------------------------------
# json.loads() parses a JSON-formatted string back into Python objects
# (dict, list, str, int, float, bool, None).
print("\n-- json.loads --")
parsed_back = json.loads(json_string)
print("Parsed back into a Python dict:", parsed_back)
print("Type of parsed_back:", type(parsed_back))
print("Type of parsed_back['skills']:", type(parsed_back["skills"]))

# ---------------------------------------------------------------------------
# 8. Writing JSON directly to a file with json.dump
# ---------------------------------------------------------------------------
print("\n-- json.dump (writing to a file) --")
nested_data = {
    "company": "Acme Corp",
    "founded": 1995,
    "employees": [
        {"name": "Alice", "role": "Engineer", "skills": ["python", "sql"]},
        {"name": "Bob", "role": "Manager", "skills": ["leadership"]},
    ],
    "locations": {
        "headquarters": "New York",
        "branches": ["London", "Tokyo", "Sydney"],
    },
}
with open(json_file, "w") as f:
    json.dump(nested_data, f, indent=2)
print("Wrote nested JSON structure to:", json_file)

# ---------------------------------------------------------------------------
# 9. Reading JSON directly from a file with json.load
# ---------------------------------------------------------------------------
print("\n-- json.load (reading from a file) --")
with open(json_file, "r") as f:
    loaded_data = json.load(f)
print("Company name:", loaded_data["company"])
print("First employee name:", loaded_data["employees"][0]["name"])
print("Branch locations:", loaded_data["locations"]["branches"])

# ---------------------------------------------------------------------------
# 10. Handling nested JSON structures
# ---------------------------------------------------------------------------
# Nested JSON just means dicts and lists containing further dicts/lists.
# Walking them is done with regular Python indexing and loops.
print("\n-- Walking a nested JSON structure --")
for employee in loaded_data["employees"]:
    skill_list = ", ".join(employee["skills"])
    print(f"  {employee['name']} ({employee['role']}): {skill_list}")

# ---------------------------------------------------------------------------
# 11. Pitfall: JSON has no tuples or sets
# ---------------------------------------------------------------------------
# JSON only knows objects (dict), arrays (list), strings, numbers,
# booleans, and null. Python tuples and sets are silently converted:
# tuples become JSON arrays (and come back as lists, not tuples), while
# sets cannot be serialized at all and raise a TypeError.
print("\n-- Pitfall: JSON has no tuples or sets --")
data_with_tuple = {"coordinates": (10, 20)}
tuple_as_json = json.dumps(data_with_tuple)
print("Tuple serialized to JSON:", tuple_as_json)
round_tripped = json.loads(tuple_as_json)
print("Type after round-trip (list, not tuple!):", type(round_tripped["coordinates"]))

data_with_set = {"unique_tags": {"python", "json"}}
try:
    json.dumps(data_with_set)
except TypeError as error:
    print("Trying to serialize a set raised TypeError:", error)
    print("Fix: convert the set to a list first, e.g. list(my_set)")

# ---------------------------------------------------------------------------
# 12. Cleanup - remove everything this script created
# ---------------------------------------------------------------------------
print("\n-- Cleanup --")
for created_file in (csv_file, json_file):
    if created_file.exists():
        created_file.unlink()
        print("Removed:", created_file.name)

if SAMPLE_DIR.exists() and not any(SAMPLE_DIR.iterdir()):
    SAMPLE_DIR.rmdir()
    print("Removed empty directory:", SAMPLE_DIR)

# Key takeaways:
# - csv.reader/writer work with plain row lists; DictReader/DictWriter
#   work with dictionaries and a header row of field names.
# - Every value read from a CSV file is a string - convert types (int,
#   float, etc.) manually after reading.
# - json.dumps/loads convert to and from JSON strings in memory; json.dump
#   /load do the same directly against an open file.
# - JSON supports dict/list/str/number/bool/None only - tuples become
#   plain lists after a round trip, and sets cannot be serialized without
#   converting them to a list first.
