"""
Data Handling Basics
=====================
Plain Python lists and dicts work fine for small amounts of data, but
real-world data work (science, analytics, machine learning) usually
involves large tables of numbers that need to be processed quickly and
expressively. `numpy` provides fast, memory-efficient arrays and
vectorized math operations (no manual for-loops needed), while `pandas`
builds on top of numpy to provide "DataFrames": labeled, spreadsheet-like
tables with powerful selection, filtering, and summary tools. Together
they form the foundation of almost the entire Python data ecosystem.

This file covers:
- Why numpy and pandas matter for data work
- numpy: array creation and vectorized operations
- pandas: DataFrame creation, selecting columns/rows, describe(), filtering
- A pure-Python fallback (lists of dicts) that teaches the same concepts
  if numpy/pandas are not installed, so the script always runs to completion
"""

# ---------------------------------------------------------------------------
# 1. Why numpy and pandas?
# ---------------------------------------------------------------------------
# numpy: gives you the `ndarray`, a fixed-type array stored compactly in
#        memory. Operations like adding two arrays happen element-wise,
#        in fast compiled code, instead of a slow Python-level loop.
# pandas: gives you the `DataFrame`, a table with named columns and an
#        index, plus convenient tools for selecting, filtering, grouping,
#        and summarizing data - similar to a spreadsheet or a SQL table,
#        but manipulated with Python code.
# Both are guarded with try/except so this script still teaches the same
# ideas (using plain lists/dicts) even if they are not installed.

print("=== 1. Why numpy/pandas matter ===")
print("numpy   -> fast arrays + vectorized math (no manual loops)")
print("pandas  -> labeled tables (DataFrames) with selection/filtering/summary")

try:
    import numpy as np
    HAS_NUMPY = True
    print("numpy is installed - version:", np.__version__)
except ImportError:
    HAS_NUMPY = False
    print("NOTE: 'numpy' is not installed. Will use a plain-Python fallback.")
    print("Install it with: pip install numpy")

try:
    import pandas as pd
    HAS_PANDAS = True
    print("pandas is installed - version:", pd.__version__)
except ImportError:
    HAS_PANDAS = False
    print("NOTE: 'pandas' is not installed. Will use a plain-Python fallback.")
    print("Install it with: pip install pandas")

# ---------------------------------------------------------------------------
# 2. numpy: array creation and vectorized operations
# ---------------------------------------------------------------------------
print("\n=== 2. numpy arrays ===")
if HAS_NUMPY:
    scores = np.array([90, 85, 78, 95, 60])
    print("Array:", scores)
    print("Mean:", scores.mean())
    print("Max:", scores.max())

    # Vectorized operations: apply to every element at once, no loop needed.
    curved = scores + 5
    print("Curved (+5 to every score):", curved)

    passed_mask = scores >= 80  # a boolean array, one value per element
    print("Passed mask (>= 80):", passed_mask)
    print("Passing scores only:", scores[passed_mask])
else:
    # Plain-Python fallback: the same ideas, using a list and a loop/comprehension.
    scores = [90, 85, 78, 95, 60]
    print("List:", scores)
    print("Mean:", sum(scores) / len(scores))
    print("Max:", max(scores))

    curved = [s + 5 for s in scores]  # "vectorized" by hand with a comprehension
    print("Curved (+5 to every score):", curved)

    passing_scores = [s for s in scores if s >= 80]
    print("Passing scores only:", passing_scores)

# ---------------------------------------------------------------------------
# 3. pandas: DataFrame creation, selection, describe(), filtering
# ---------------------------------------------------------------------------
print("\n=== 3. pandas DataFrame ===")

raw_data = {
    "name": ["Alice", "Bob", "Charlie", "Dana", "Eve"],
    "grade": [90, 85, 78, 95, 60],
    "age": [20, 22, 21, 23, 20],
}

if HAS_PANDAS:
    df = pd.DataFrame(raw_data)
    print("Full DataFrame:")
    print(df)

    # Selecting a single column returns a Series; a list of columns returns
    # a smaller DataFrame.
    print("\nJust the 'name' column:")
    print(df["name"])

    print("\nSelecting rows by position (first two rows) with .iloc:")
    print(df.iloc[0:2])

    print("\nSummary statistics with describe():")
    print(df["grade"].describe())

    print("\nFiltering: students with grade >= 80")
    passing_df = df[df["grade"] >= 80]
    print(passing_df)
else:
    # Plain-Python fallback: represent a "table" as a list of dicts (one
    # dict per row) - a common, simple stand-in for a DataFrame.
    table = [
        {"name": n, "grade": g, "age": a}
        for n, g, a in zip(raw_data["name"], raw_data["grade"], raw_data["age"])
    ]
    print("Table (list of dicts), one dict per row:")
    for row in table:
        print(" ", row)

    print("\nJust the 'name' column (manual column selection):")
    names_only = [row["name"] for row in table]
    print(names_only)

    print("\nSelecting rows by position (first two rows):")
    print(table[0:2])

    grades = [row["grade"] for row in table]
    count = len(grades)
    mean = sum(grades) / count
    minimum = min(grades)
    maximum = max(grades)
    variance = sum((g - mean) ** 2 for g in grades) / count
    std_dev = variance ** 0.5
    print("\nSummary statistics for 'grade' (manual describe()):")
    print(f"  count: {count}")
    print(f"  mean:  {mean:.2f}")
    print(f"  std:   {std_dev:.2f}")
    print(f"  min:   {minimum}")
    print(f"  max:   {maximum}")

    print("\nFiltering: students with grade >= 80")
    passing_rows = [row for row in table if row["grade"] >= 80]
    for row in passing_rows:
        print(" ", row)

# ---------------------------------------------------------------------------
# 4. Putting it together
# ---------------------------------------------------------------------------
print("\n=== 4. Summary ===")
if HAS_NUMPY and HAS_PANDAS:
    print("numpy and pandas were available - ran the real array/DataFrame demos.")
else:
    print("Some libraries were missing - ran the plain-Python fallback instead.")
    print("The underlying concepts (arrays, vectorized ops, tables, filtering,")
    print("summary stats) are the same either way.")

# Key takeaways:
# - numpy provides fast, memory-efficient arrays and vectorized operations
#   that avoid writing manual Python loops for numeric work.
# - pandas builds on numpy to provide DataFrames: labeled tables with
#   convenient column/row selection, filtering, and summary tools like describe().
# - Selecting a column returns a Series (or a single list of values in the
#   plain-Python version); filtering uses a boolean condition on a column.
# - Always guard third-party imports with try/except and provide a plain-Python
#   fallback so your data scripts remain runnable and educational anywhere.
