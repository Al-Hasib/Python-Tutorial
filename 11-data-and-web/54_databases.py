"""
Databases in Python
====================
A database stores structured data so it can be reliably saved, searched,
and updated, even across program runs. Relational databases organize
data into tables (like spreadsheets) made of rows (records) and columns
(fields), and you interact with them using SQL (Structured Query
Language). Python's standard library ships with `sqlite3`, a lightweight
file-based (or in-memory) relational database that needs no separate
server, making it perfect for learning and for small applications.
Understanding databases and SQL is a core skill because most real
applications need to persist data somewhere.

This file covers:
- Relational database basics: tables, rows, columns
- Core SQL statements: SELECT, INSERT, UPDATE, DELETE
- Using sqlite3 end-to-end: connect, create table, insert, query, commit, close
- Parameterized queries to prevent SQL injection
- fetchone() vs fetchall()
- ORMs (e.g. SQLAlchemy) explained conceptually, with an illustrative snippet
"""

import sqlite3

# ---------------------------------------------------------------------------
# 1. Relational database basics
# ---------------------------------------------------------------------------
# A relational database organizes data into TABLES.
# Each table has COLUMNS (named fields with a type) and many ROWS (records).
#
# Example "students" table:
#   id | name    | grade
#   ---+---------+------
#   1  | Alice   | 90
#   2  | Bob     | 85
#
# SQL is the language used to define and manipulate this data:
#   SELECT -> read rows
#   INSERT -> add a new row
#   UPDATE -> modify existing rows
#   DELETE -> remove rows

print("=== 1. Relational concepts ===")
print("Tables are made of rows (records) and columns (named fields).")
print("SQL verbs: SELECT (read), INSERT (create), UPDATE (modify), DELETE (remove).")

# ---------------------------------------------------------------------------
# 2. Connecting to sqlite3 and creating a table
# ---------------------------------------------------------------------------
# sqlite3.connect(":memory:") creates a temporary database that lives only
# in RAM for the duration of the program - perfect for demos and tests.
# Use a filename like sqlite3.connect("app.db") to persist data to disk.

print("\n=== 2. Creating an in-memory database ===")
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()  # the cursor executes SQL and gives back results

cursor.execute(
    """
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade INTEGER NOT NULL
    )
    """
)
print("Table 'students' created.")

# ---------------------------------------------------------------------------
# 3. INSERT - adding rows (with parameterized queries)
# ---------------------------------------------------------------------------
# NEVER build SQL by string-formatting user input directly, e.g.:
#   cursor.execute(f"INSERT INTO students (name) VALUES ('{name}')")
# That is vulnerable to SQL injection. Instead, use "?" placeholders and
# pass the values as a tuple - sqlite3 escapes them safely for you.

print("\n=== 3. Inserting rows safely ===")
students_to_add = [
    ("Alice", 90),
    ("Bob", 85),
    ("Charlie", 78),
    ("Dana", 95),
]
cursor.executemany(
    "INSERT INTO students (name, grade) VALUES (?, ?)",
    students_to_add,
)
connection.commit()  # persist the changes (required for on-disk DBs; harmless here)
print(f"Inserted {len(students_to_add)} rows.")

# ---------------------------------------------------------------------------
# 4. SELECT - querying rows
# ---------------------------------------------------------------------------
print("\n=== 4. Querying rows ===")

# fetchall() returns every matching row as a list of tuples.
cursor.execute("SELECT id, name, grade FROM students ORDER BY grade DESC")
all_rows = cursor.fetchall()
print("All students, best grade first:")
for row in all_rows:
    print(" ", row)

# fetchone() returns just the next single row (or None if there are no more).
cursor.execute("SELECT name, grade FROM students WHERE grade >= ?", (90,))
top_student = cursor.fetchone()
print("First student with grade >= 90:", top_student)

# ---------------------------------------------------------------------------
# 5. UPDATE - modifying existing rows
# ---------------------------------------------------------------------------
print("\n=== 5. Updating rows ===")
cursor.execute(
    "UPDATE students SET grade = ? WHERE name = ?",
    (97, "Charlie"),
)
connection.commit()
cursor.execute("SELECT name, grade FROM students WHERE name = ?", ("Charlie",))
print("Charlie's new grade:", cursor.fetchone())

# ---------------------------------------------------------------------------
# 6. DELETE - removing rows
# ---------------------------------------------------------------------------
print("\n=== 6. Deleting rows ===")
cursor.execute("DELETE FROM students WHERE name = ?", ("Dana",))
connection.commit()
cursor.execute("SELECT COUNT(*) FROM students")
remaining = cursor.fetchone()[0]
print("Remaining student count after delete:", remaining)

# ---------------------------------------------------------------------------
# 7. Cleaning up
# ---------------------------------------------------------------------------
# Always close the connection when you are done with it (or use a
# `with sqlite3.connect(...) as connection:` context manager pattern).
cursor.close()
connection.close()
print("\n=== 7. Connection closed ===")

# ---------------------------------------------------------------------------
# 8. ORMs (Object-Relational Mappers) - conceptual overview
# ---------------------------------------------------------------------------
# Writing raw SQL strings works but can get repetitive and easy to typo.
# An ORM like SQLAlchemy lets you work with database rows as if they were
# regular Python objects/classes, and it generates the SQL for you.
#
# The snippet below is illustrative ONLY (not executed, no dependency
# required) - it shows how the same "students" table might look with
# SQLAlchemy's declarative ORM style:
#
#   from sqlalchemy import create_engine, Column, Integer, String
#   from sqlalchemy.orm import declarative_base, Session
#
#   Base = declarative_base()
#
#   class Student(Base):
#       __tablename__ = "students"
#       id = Column(Integer, primary_key=True)
#       name = Column(String, nullable=False)
#       grade = Column(Integer, nullable=False)
#
#   engine = create_engine("sqlite:///:memory:")
#   Base.metadata.create_all(engine)
#
#   with Session(engine) as session:
#       session.add(Student(name="Alice", grade=90))   # like INSERT
#       session.commit()
#
#       # like: SELECT * FROM students WHERE grade >= 90
#       top = session.query(Student).filter(Student.grade >= 90).all()
#
# Notice there is no raw SQL text at all - the ORM translates Python
# objects and method calls into SQL behind the scenes. ORMs trade a small
# amount of directness for a lot of convenience, type safety, and
# protection against SQL injection by default.

print("\n=== 8. ORMs ===")
print("An ORM (e.g. SQLAlchemy) maps Python classes to tables and lets you")
print("query/insert/update using Python objects instead of raw SQL strings.")
print("See the comments above for an illustrative (non-executed) example.")

# Key takeaways:
# - Relational databases store data in tables made of rows and columns.
# - Core SQL verbs: SELECT (read), INSERT (create), UPDATE (modify), DELETE (remove).
# - sqlite3 is a stdlib, file-or-memory-based relational database - no server needed.
# - Always use parameterized queries ("?" placeholders + a tuple of values)
#   instead of string-formatting SQL, to avoid SQL injection.
# - ORMs like SQLAlchemy let you work with rows as Python objects, generating
#   SQL for you, at the cost of an extra dependency and a layer of abstraction.
