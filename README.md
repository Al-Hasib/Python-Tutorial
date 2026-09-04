# Python Tutorial — Scratch to Advanced

A sequential, hands-on Python curriculum: 12 phases, 61 topics, one runnable `.py` file per topic
(plus a matching `.ipynb` notebook for every topic, split into markdown explanation + code cells).
Every file is self-contained — a module docstring explains the concept, the code demonstrates it with
`print()` output, and a "Key takeaways" block closes it out. Just run a file to learn from it:

```bash
python 01-fundamentals/01_introduction_and_setup.py
```

...or open its notebook (`01_introduction_and_setup.ipynb`) in Jupyter/VS Code to step through it
cell by cell.

See [docs/TOPICS.md](docs/TOPICS.md) for the original one-page curriculum outline.

## Prerequisites

- Python 3.10+ (some files use modern syntax like built-in generic types, e.g. `list[int]`, and the
  `match`/`case` statement)
- No installs required for phases 1–10 (standard library only)
- Phase 11 (`11-data-and-web/`) can optionally use `requests`, `flask`, `numpy`, and `pandas` for a
  richer demo — see [requirements.txt](requirements.txt). Every file in that folder still runs and
  teaches the concept without them, via a plain-Python fallback.

## Learning Path

### Phase 1 — Fundamentals ([01-fundamentals/](01-fundamentals/))
| # | Topic | File |
|---|---|---|
| 1 | Introduction to Python & Setup | [01_introduction_and_setup.py](01-fundamentals/01_introduction_and_setup.py) |
| 2 | Variables & Data Types | [02_variables_and_data_types.py](01-fundamentals/02_variables_and_data_types.py) |
| 3 | Basic Input & Output | [03_input_output.py](01-fundamentals/03_input_output.py) |
| 4 | Operators | [04_operators.py](01-fundamentals/04_operators.py) |
| 5 | Strings in Depth | [05_strings_in_depth.py](01-fundamentals/05_strings_in_depth.py) |
| 6 | Type Conversion & Type Checking | [06_type_conversion.py](01-fundamentals/06_type_conversion.py) |

### Phase 2 — Control Flow ([02-control-flow/](02-control-flow/))
| # | Topic | File |
|---|---|---|
| 7 | Conditional Statements | [07_conditional_statements.py](02-control-flow/07_conditional_statements.py) |
| 8 | Loops | [08_loops.py](02-control-flow/08_loops.py) |
| 9 | Nested Loops & Loop Patterns | [09_nested_loops_and_patterns.py](02-control-flow/09_nested_loops_and_patterns.py) |
| 10 | Structural Pattern Matching (`match`/`case`) | [10_match_case_statements.py](02-control-flow/10_match_case_statements.py) |

### Phase 3 — Data Structures ([03-data-structures/](03-data-structures/))
| # | Topic | File |
|---|---|---|
| 11 | Lists | [11_lists.py](03-data-structures/11_lists.py) |
| 12 | Tuples | [12_tuples.py](03-data-structures/12_tuples.py) |
| 13 | Dictionaries | [13_dictionaries.py](03-data-structures/13_dictionaries.py) |
| 14 | Sets | [14_sets.py](03-data-structures/14_sets.py) |
| 15 | Choosing the Right Data Structure | [15_choosing_data_structure.py](03-data-structures/15_choosing_data_structure.py) |

### Phase 4 — Functions ([04-functions/](04-functions/))
| # | Topic | File |
|---|---|---|
| 16 | Functions Basics | [16_functions_basics.py](04-functions/16_functions_basics.py) |
| 17 | Function Arguments | [17_function_arguments.py](04-functions/17_function_arguments.py) |
| 18 | Scope & Namespaces | [18_scope_and_namespaces.py](04-functions/18_scope_and_namespaces.py) |
| 19 | Lambda Functions | [19_lambda_functions.py](04-functions/19_lambda_functions.py) |
| 20 | Recursion | [20_recursion.py](04-functions/20_recursion.py) |
| 21 | Higher-Order Functions | [21_higher_order_functions.py](04-functions/21_higher_order_functions.py) |

### Phase 5 — Modules & Files ([05-modules-and-files/](05-modules-and-files/))
| # | Topic | File |
|---|---|---|
| 22 | Modules & Packages | [22_modules_and_packages.py](05-modules-and-files/22_modules_and_packages.py) |
| 23 | Standard Library Tour | [23_standard_library_tour.py](05-modules-and-files/23_standard_library_tour.py) |
| 24 | File Handling | [24_file_handling.py](05-modules-and-files/24_file_handling.py) |
| 25 | Working with CSV/JSON | [25_csv_json.py](05-modules-and-files/25_csv_json.py) |
| 26 | Command-Line Arguments (`argparse`) | [26_command_line_arguments.py](05-modules-and-files/26_command_line_arguments.py) |

### Phase 6 — Error Handling ([06-error-handling/](06-error-handling/))
| # | Topic | File |
|---|---|---|
| 27 | Exceptions & Error Handling | [27_exceptions.py](06-error-handling/27_exceptions.py) |
| 28 | Raising Custom Exceptions | [28_custom_exceptions.py](06-error-handling/28_custom_exceptions.py) |
| 29 | Debugging Techniques & Logging | [29_debugging_and_logging.py](06-error-handling/29_debugging_and_logging.py) |

### Phase 7 — Object-Oriented Programming ([07-oop/](07-oop/))
| # | Topic | File |
|---|---|---|
| 30 | Classes & Objects | [30_classes_and_objects.py](07-oop/30_classes_and_objects.py) |
| 31 | Enums (Named Constants) | [31_enums.py](07-oop/31_enums.py) |
| 32 | Inheritance & Polymorphism | [32_inheritance_and_polymorphism.py](07-oop/32_inheritance_and_polymorphism.py) |
| 33 | Encapsulation & Access Modifiers | [33_encapsulation.py](07-oop/33_encapsulation.py) |
| 34 | Magic/Dunder Methods | [34_dunder_methods.py](07-oop/34_dunder_methods.py) |
| 35 | Class Methods, Static Methods & Properties | [35_class_static_methods_properties.py](07-oop/35_class_static_methods_properties.py) |
| 36 | Abstract Classes & Interfaces | [36_abstract_classes.py](07-oop/36_abstract_classes.py) |
| 37 | Composition vs Inheritance | [37_composition_vs_inheritance.py](07-oop/37_composition_vs_inheritance.py) |

### Phase 8 — Intermediate Concepts ([08-intermediate/](08-intermediate/))
| # | Topic | File |
|---|---|---|
| 38 | Iterators & Generators | [38_iterators_and_generators.py](08-intermediate/38_iterators_and_generators.py) |
| 39 | Decorators | [39_decorators.py](08-intermediate/39_decorators.py) |
| 40 | Context Managers | [40_context_managers.py](08-intermediate/40_context_managers.py) |
| 41 | Comprehensions Deep Dive | [41_comprehensions_deep_dive.py](08-intermediate/41_comprehensions_deep_dive.py) |
| 42 | Working with Dates & Times | [42_dates_and_times.py](08-intermediate/42_dates_and_times.py) |
| 43 | Regular Expressions | [43_regular_expressions.py](08-intermediate/43_regular_expressions.py) |

### Phase 9 — Advanced Python ([09-advanced/](09-advanced/))
| # | Topic | File |
|---|---|---|
| 44 | Advanced OOP (MRO, `__slots__`, metaclasses) | [44_advanced_oop.py](09-advanced/44_advanced_oop.py) |
| 45 | Type Hints & Static Typing | [45_type_hints.py](09-advanced/45_type_hints.py) |
| 46 | Functional Programming Patterns | [46_functional_programming.py](09-advanced/46_functional_programming.py) |
| 47 | Concurrency: Threading | [47_threading.py](09-advanced/47_threading.py) |
| 48 | Concurrency: Multiprocessing | [48_multiprocessing.py](09-advanced/48_multiprocessing.py) |
| 49 | Asynchronous Programming | [49_async_programming.py](09-advanced/49_async_programming.py) |
| 50 | Memory Management & Garbage Collection | [50_memory_management.py](09-advanced/50_memory_management.py) |
| 51 | Performance Optimization & Profiling | [51_performance_optimization.py](09-advanced/51_performance_optimization.py) |

### Phase 10 — Testing, Tooling & Best Practices ([10-testing-and-tooling/](10-testing-and-tooling/))
| # | Topic | File |
|---|---|---|
| 52 | Unit Testing | [52_unit_testing.py](10-testing-and-tooling/52_unit_testing.py) |
| 53 | Virtual Environments & Dependency Management | [53_virtual_envs_and_dependencies.py](10-testing-and-tooling/53_virtual_envs_and_dependencies.py) |
| 54 | Code Style & Linting | [54_code_style_and_linting.py](10-testing-and-tooling/54_code_style_and_linting.py) |
| 55 | Packaging & Distributing Python Projects | [55_packaging_and_distribution.py](10-testing-and-tooling/55_packaging_and_distribution.py) |

### Phase 11 — Working with Data & Web ([11-data-and-web/](11-data-and-web/))
| # | Topic | File |
|---|---|---|
| 56 | Working with APIs | [56_working_with_apis.py](11-data-and-web/56_working_with_apis.py) |
| 57 | Databases in Python | [57_databases.py](11-data-and-web/57_databases.py) |
| 58 | Introduction to Web Development | [58_intro_web_development.py](11-data-and-web/58_intro_web_development.py) |
| 59 | Data Handling Basics (pandas/numpy) | [59_data_handling_basics.py](11-data-and-web/59_data_handling_basics.py) |

### Phase 12 — Capstone ([12-capstone/](12-capstone/))
| # | Topic | File |
|---|---|---|
| 60 | Building a Real Project | [60_building_a_real_project.py](12-capstone/60_building_a_real_project.py) |
| 61 | Next Steps | [61_next_steps.py](12-capstone/61_next_steps.py) |

## Running the examples

Run any single file directly:

```bash
python 07-oop/30_classes_and_objects.py
```

Or run every file in the curriculum as a smoke test (checks each one executes without errors):

```bash
python run_all.py
```

## Optional extras (Phase 11 only)

```bash
pip install -r requirements.txt
```

This is entirely optional — every file degrades gracefully to a standard-library-only demo if these
aren't installed.
