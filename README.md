# Python Tutorial — Scratch to Advanced

A sequential, hands-on Python curriculum: 12 phases, 58 topics, one runnable `.py` file per topic.
Every file is self-contained — a module docstring explains the concept, the code demonstrates it with
`print()` output, and a "Key takeaways" block closes it out. Just run a file to learn from it:

```bash
python 01-fundamentals/01_introduction_and_setup.py
```

See [docs/TOPICS.md](docs/TOPICS.md) for the original one-page curriculum outline.

## Prerequisites

- Python 3.10+ (some files use modern syntax like built-in generic types, e.g. `list[int]`)
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

### Phase 3 — Data Structures ([03-data-structures/](03-data-structures/))
| # | Topic | File |
|---|---|---|
| 10 | Lists | [10_lists.py](03-data-structures/10_lists.py) |
| 11 | Tuples | [11_tuples.py](03-data-structures/11_tuples.py) |
| 12 | Dictionaries | [12_dictionaries.py](03-data-structures/12_dictionaries.py) |
| 13 | Sets | [13_sets.py](03-data-structures/13_sets.py) |
| 14 | Choosing the Right Data Structure | [14_choosing_data_structure.py](03-data-structures/14_choosing_data_structure.py) |

### Phase 4 — Functions ([04-functions/](04-functions/))
| # | Topic | File |
|---|---|---|
| 15 | Functions Basics | [15_functions_basics.py](04-functions/15_functions_basics.py) |
| 16 | Function Arguments | [16_function_arguments.py](04-functions/16_function_arguments.py) |
| 17 | Scope & Namespaces | [17_scope_and_namespaces.py](04-functions/17_scope_and_namespaces.py) |
| 18 | Lambda Functions | [18_lambda_functions.py](04-functions/18_lambda_functions.py) |
| 19 | Recursion | [19_recursion.py](04-functions/19_recursion.py) |
| 20 | Higher-Order Functions | [20_higher_order_functions.py](04-functions/20_higher_order_functions.py) |

### Phase 5 — Modules & Files ([05-modules-and-files/](05-modules-and-files/))
| # | Topic | File |
|---|---|---|
| 21 | Modules & Packages | [21_modules_and_packages.py](05-modules-and-files/21_modules_and_packages.py) |
| 22 | Standard Library Tour | [22_standard_library_tour.py](05-modules-and-files/22_standard_library_tour.py) |
| 23 | File Handling | [23_file_handling.py](05-modules-and-files/23_file_handling.py) |
| 24 | Working with CSV/JSON | [24_csv_json.py](05-modules-and-files/24_csv_json.py) |

### Phase 6 — Error Handling ([06-error-handling/](06-error-handling/))
| # | Topic | File |
|---|---|---|
| 25 | Exceptions & Error Handling | [25_exceptions.py](06-error-handling/25_exceptions.py) |
| 26 | Raising Custom Exceptions | [26_custom_exceptions.py](06-error-handling/26_custom_exceptions.py) |
| 27 | Debugging Techniques & Logging | [27_debugging_and_logging.py](06-error-handling/27_debugging_and_logging.py) |

### Phase 7 — Object-Oriented Programming ([07-oop/](07-oop/))
| # | Topic | File |
|---|---|---|
| 28 | Classes & Objects | [28_classes_and_objects.py](07-oop/28_classes_and_objects.py) |
| 29 | Inheritance & Polymorphism | [29_inheritance_and_polymorphism.py](07-oop/29_inheritance_and_polymorphism.py) |
| 30 | Encapsulation & Access Modifiers | [30_encapsulation.py](07-oop/30_encapsulation.py) |
| 31 | Magic/Dunder Methods | [31_dunder_methods.py](07-oop/31_dunder_methods.py) |
| 32 | Class Methods, Static Methods & Properties | [32_class_static_methods_properties.py](07-oop/32_class_static_methods_properties.py) |
| 33 | Abstract Classes & Interfaces | [33_abstract_classes.py](07-oop/33_abstract_classes.py) |
| 34 | Composition vs Inheritance | [34_composition_vs_inheritance.py](07-oop/34_composition_vs_inheritance.py) |

### Phase 8 — Intermediate Concepts ([08-intermediate/](08-intermediate/))
| # | Topic | File |
|---|---|---|
| 35 | Iterators & Generators | [35_iterators_and_generators.py](08-intermediate/35_iterators_and_generators.py) |
| 36 | Decorators | [36_decorators.py](08-intermediate/36_decorators.py) |
| 37 | Context Managers | [37_context_managers.py](08-intermediate/37_context_managers.py) |
| 38 | Comprehensions Deep Dive | [38_comprehensions_deep_dive.py](08-intermediate/38_comprehensions_deep_dive.py) |
| 39 | Working with Dates & Times | [39_dates_and_times.py](08-intermediate/39_dates_and_times.py) |
| 40 | Regular Expressions | [40_regular_expressions.py](08-intermediate/40_regular_expressions.py) |

### Phase 9 — Advanced Python ([09-advanced/](09-advanced/))
| # | Topic | File |
|---|---|---|
| 41 | Advanced OOP (MRO, `__slots__`, metaclasses) | [41_advanced_oop.py](09-advanced/41_advanced_oop.py) |
| 42 | Type Hints & Static Typing | [42_type_hints.py](09-advanced/42_type_hints.py) |
| 43 | Functional Programming Patterns | [43_functional_programming.py](09-advanced/43_functional_programming.py) |
| 44 | Concurrency: Threading | [44_threading.py](09-advanced/44_threading.py) |
| 45 | Concurrency: Multiprocessing | [45_multiprocessing.py](09-advanced/45_multiprocessing.py) |
| 46 | Asynchronous Programming | [46_async_programming.py](09-advanced/46_async_programming.py) |
| 47 | Memory Management & Garbage Collection | [47_memory_management.py](09-advanced/47_memory_management.py) |
| 48 | Performance Optimization & Profiling | [48_performance_optimization.py](09-advanced/48_performance_optimization.py) |

### Phase 10 — Testing, Tooling & Best Practices ([10-testing-and-tooling/](10-testing-and-tooling/))
| # | Topic | File |
|---|---|---|
| 49 | Unit Testing | [49_unit_testing.py](10-testing-and-tooling/49_unit_testing.py) |
| 50 | Virtual Environments & Dependency Management | [50_virtual_envs_and_dependencies.py](10-testing-and-tooling/50_virtual_envs_and_dependencies.py) |
| 51 | Code Style & Linting | [51_code_style_and_linting.py](10-testing-and-tooling/51_code_style_and_linting.py) |
| 52 | Packaging & Distributing Python Projects | [52_packaging_and_distribution.py](10-testing-and-tooling/52_packaging_and_distribution.py) |

### Phase 11 — Working with Data & Web ([11-data-and-web/](11-data-and-web/))
| # | Topic | File |
|---|---|---|
| 53 | Working with APIs | [53_working_with_apis.py](11-data-and-web/53_working_with_apis.py) |
| 54 | Databases in Python | [54_databases.py](11-data-and-web/54_databases.py) |
| 55 | Introduction to Web Development | [55_intro_web_development.py](11-data-and-web/55_intro_web_development.py) |
| 56 | Data Handling Basics (pandas/numpy) | [56_data_handling_basics.py](11-data-and-web/56_data_handling_basics.py) |

### Phase 12 — Capstone ([12-capstone/](12-capstone/))
| # | Topic | File |
|---|---|---|
| 57 | Building a Real Project | [57_building_a_real_project.py](12-capstone/57_building_a_real_project.py) |
| 58 | Next Steps | [58_next_steps.py](12-capstone/58_next_steps.py) |

## Running the examples

Run any single file directly:

```bash
python 07-oop/28_classes_and_objects.py
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
