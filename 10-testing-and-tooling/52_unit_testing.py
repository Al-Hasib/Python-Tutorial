"""
Unit Testing: Verifying Your Code Actually Works

Unit testing means writing small, automated checks that exercise a single
"unit" of code (a function, a method, a class) and verify it behaves as
expected. Python's standard library ships a full-featured testing framework
called `unittest`, inspired by JUnit, so you never need a third-party
package to get started. Tests matter because they catch regressions before
users do, they document expected behavior in a runnable form, and they give
you the confidence to refactor code without fear of silently breaking it.
This file builds real `unittest` test cases and runs them right here in the
script, then explains (in comments) how the same tests look with `pytest`.

This file covers:
- Writing tests with `unittest.TestCase`
- Common assertions: assertEqual, assertTrue, assertRaises, and friends
- setUp/tearDown for shared test fixtures
- Running tests programmatically inside a script (no `python -m unittest` needed)
- Test naming conventions and why they matter
- The equivalent tests written with pytest (explained only, not executed)
"""

import unittest


# ---------------------------------------------------------------------------
# 1. The code under test
# ---------------------------------------------------------------------------
# In a real project this would live in its own module (e.g. calculator.py)
# and the test file would import it. We define it here so this file is
# fully self-contained and runnable on its own.

class Calculator:
    """A tiny calculator used purely to demonstrate testing techniques."""

    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def is_even(self, n):
        return n % 2 == 0


# ---------------------------------------------------------------------------
# 2. Writing tests with unittest.TestCase
# ---------------------------------------------------------------------------
# - Test classes inherit from unittest.TestCase.
# - Test method names must start with "test_" (this is how the test runner
#   discovers them) -- this is the core naming convention to remember.
# - Each test method should check one logical behavior and be independent
#   of the others (no test should rely on another test having run first).

class TestCalculator(unittest.TestCase):

    # setUp runs before EVERY test method in this class. It is the place
    # to create fresh objects so tests do not share state and interfere
    # with each other.
    def setUp(self):
        self.calc = Calculator()
        print("  [setUp] fresh Calculator created")

    # tearDown runs after EVERY test method, even if the test failed.
    # Useful for cleanup (closing files, deleting temp data, etc.).
    def tearDown(self):
        print("  [tearDown] cleaning up")

    def test_add_two_positive_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(self.calc.add(-2, -3), -5)

    def test_is_even_true_case(self):
        self.assertTrue(self.calc.is_even(4))

    def test_is_even_false_case(self):
        self.assertFalse(self.calc.is_even(7))

    def test_divide_normal_case(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero_raises(self):
        # assertRaises checks that a specific exception type is raised.
        # Used as a context manager, it also lets you inspect the exception.
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.divide(1, 0)
        self.assertIn("zero", str(ctx.exception))

    def test_common_assertions_showcase(self):
        # A few more assertions you will use constantly:
        self.assertIsNone(None)
        self.assertIsNotNone(42)
        self.assertIn(3, [1, 2, 3])
        self.assertNotIn(9, [1, 2, 3])
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)
        self.assertListEqual([1, 2], [1, 2])


# ---------------------------------------------------------------------------
# 3. Test naming conventions and why they matter
# ---------------------------------------------------------------------------
# - Test files are conventionally named test_<module>.py or <module>_test.py
#   so discovery tools (unittest discover, pytest) can find them automatically.
# - Test classes are conventionally named Test<ClassUnderTest>.
# - Test methods must start with "test_" for unittest's default loader to
#   pick them up, and should describe the SCENARIO, not just the method:
#       test_divide_by_zero_raises   (good: describes behavior)
#       test_divide2                 (bad: meaningless)
# - Clear names double as documentation: a failing test name alone often
#   tells you what broke without reading the assertion.


# ---------------------------------------------------------------------------
# 4. Running tests programmatically inside this script
# ---------------------------------------------------------------------------
# Normally you would run tests from the command line:
#     $ python -m unittest 52_unit_testing.py
#     $ python -m unittest discover
# But this file needs to be self-contained and runnable directly with
# `python 52_unit_testing.py`, so we run the tests programmatically instead,
# using two different techniques below.

def run_with_unittest_main():
    """Technique A: unittest.main() with argv/exit tweaked for script use."""
    print("\n--- Running tests via unittest.main(argv=..., exit=False) ---")
    unittest.main(
        argv=["ignored_program_name"],
        exit=False,       # don't call sys.exit() -- let the script continue
        verbosity=2,
    )


def run_with_test_suite():
    """Technique B: build a TestSuite explicitly and run it with a runner."""
    print("\n--- Running tests via TestSuite + TextTestRunner ---")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(f"Tests run: {result.testsRun}, failures: {len(result.failures)}, "
          f"errors: {len(result.errors)}")


# ---------------------------------------------------------------------------
# 5. The same tests, the pytest way (explained only -- not executed here)
# ---------------------------------------------------------------------------
# pytest is a third-party package (pip install pytest) that is extremely
# popular because it removes most of the boilerplate of unittest:
#
# - Plain functions instead of classes/methods; plain `assert` instead of
#   assertEqual/assertTrue/etc. pytest rewrites assert statements to give
#   rich failure diffs automatically.
# - Fixtures (via the @pytest.fixture decorator) replace setUp/tearDown and
#   are far more flexible (they can be shared across files, parametrized,
#   scoped to function/class/module/session).
# - pytest.raises(...) replaces assertRaises(...).
#
# Example of what tests/test_calculator.py would look like with pytest:
#
#     import pytest
#     from calculator import Calculator
#
#     @pytest.fixture
#     def calc():
#         return Calculator()  # equivalent of setUp, re-run per test
#
#     def test_add_two_positive_numbers(calc):
#         assert calc.add(2, 3) == 5
#
#     def test_divide_by_zero_raises(calc):
#         with pytest.raises(ValueError, match="zero"):
#             calc.divide(10, 0)
#
# You would then run it from the shell with:
#     $ pytest -v
#
# Notice there is no TestCase subclass, no self, and no assertEqual --
# just `assert expression`. This is why many teams prefer pytest for new
# projects, while still using plain `unittest` (as in this file) whenever
# they want zero extra dependencies.


# ---------------------------------------------------------------------------
# 6. Why testing matters (summary)
# ---------------------------------------------------------------------------
# - Tests catch regressions: a change that breaks old behavior fails loudly
#   instead of shipping silently to users.
# - Tests document intent: reading test_divide_by_zero_raises tells you the
#   expected contract without reading the implementation.
# - Tests enable safe refactoring: with good coverage you can restructure
#   internals and trust the test suite to tell you if you broke something.
# - Automated tests are cheaper than manual testing every single time you
#   make a change.


if __name__ == "__main__":
    run_with_test_suite()
    run_with_unittest_main()


# Key takeaways:
# - unittest.TestCase gives you assertEqual/assertTrue/assertRaises/etc. and
#   setUp/tearDown for fixtures, all from the standard library.
# - Tests can be run programmatically with unittest.main(argv=..., exit=False)
#   or by building a TestSuite and running it with TextTestRunner.
# - Test methods must start with "test_" for discovery, and clear, scenario-
#   based names make failing tests self-documenting.
# - pytest offers the same capabilities with plain assert statements,
#   fixtures instead of setUp/tearDown, and pytest.raises instead of
#   assertRaises -- but it is a separate package you must install.
# - Automated tests catch regressions early, document behavior, and make
#   refactoring safe.
