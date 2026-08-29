"""
One-off: renumber the curriculum to make room for 3 new topics (match/case,
enum, argparse), renaming both .py and .ipynb for every existing file via
`git mv` (two-pass, through a temp name, to avoid collisions).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

# (old_folder, old_stem) -> (new_folder, new_stem)
# Only entries that actually change are listed; folder stays the same for
# every existing topic (no topic moves to a different phase folder).
RENAMES = {
    ("03-data-structures", "10_lists"): "11_lists",
    ("03-data-structures", "11_tuples"): "12_tuples",
    ("03-data-structures", "12_dictionaries"): "13_dictionaries",
    ("03-data-structures", "13_sets"): "14_sets",
    ("03-data-structures", "14_choosing_data_structure"): "15_choosing_data_structure",

    ("04-functions", "15_functions_basics"): "16_functions_basics",
    ("04-functions", "16_function_arguments"): "17_function_arguments",
    ("04-functions", "17_scope_and_namespaces"): "18_scope_and_namespaces",
    ("04-functions", "18_lambda_functions"): "19_lambda_functions",
    ("04-functions", "19_recursion"): "20_recursion",
    ("04-functions", "20_higher_order_functions"): "21_higher_order_functions",

    ("05-modules-and-files", "21_modules_and_packages"): "22_modules_and_packages",
    ("05-modules-and-files", "22_standard_library_tour"): "23_standard_library_tour",
    ("05-modules-and-files", "23_file_handling"): "24_file_handling",
    ("05-modules-and-files", "24_csv_json"): "25_csv_json",

    ("06-error-handling", "25_exceptions"): "27_exceptions",
    ("06-error-handling", "26_custom_exceptions"): "28_custom_exceptions",
    ("06-error-handling", "27_debugging_and_logging"): "29_debugging_and_logging",

    ("07-oop", "28_classes_and_objects"): "30_classes_and_objects",
    ("07-oop", "29_inheritance_and_polymorphism"): "32_inheritance_and_polymorphism",
    ("07-oop", "30_encapsulation"): "33_encapsulation",
    ("07-oop", "31_dunder_methods"): "34_dunder_methods",
    ("07-oop", "32_class_static_methods_properties"): "35_class_static_methods_properties",
    ("07-oop", "33_abstract_classes"): "36_abstract_classes",
    ("07-oop", "34_composition_vs_inheritance"): "37_composition_vs_inheritance",

    ("08-intermediate", "35_iterators_and_generators"): "38_iterators_and_generators",
    ("08-intermediate", "36_decorators"): "39_decorators",
    ("08-intermediate", "37_context_managers"): "40_context_managers",
    ("08-intermediate", "38_comprehensions_deep_dive"): "41_comprehensions_deep_dive",
    ("08-intermediate", "39_dates_and_times"): "42_dates_and_times",
    ("08-intermediate", "40_regular_expressions"): "43_regular_expressions",

    ("09-advanced", "41_advanced_oop"): "44_advanced_oop",
    ("09-advanced", "42_type_hints"): "45_type_hints",
    ("09-advanced", "43_functional_programming"): "46_functional_programming",
    ("09-advanced", "44_threading"): "47_threading",
    ("09-advanced", "45_multiprocessing"): "48_multiprocessing",
    ("09-advanced", "46_async_programming"): "49_async_programming",
    ("09-advanced", "47_memory_management"): "50_memory_management",
    ("09-advanced", "48_performance_optimization"): "51_performance_optimization",

    ("10-testing-and-tooling", "49_unit_testing"): "52_unit_testing",
    ("10-testing-and-tooling", "50_virtual_envs_and_dependencies"): "53_virtual_envs_and_dependencies",
    ("10-testing-and-tooling", "51_code_style_and_linting"): "54_code_style_and_linting",
    ("10-testing-and-tooling", "52_packaging_and_distribution"): "55_packaging_and_distribution",

    ("11-data-and-web", "53_working_with_apis"): "56_working_with_apis",
    ("11-data-and-web", "54_databases"): "57_databases",
    ("11-data-and-web", "55_intro_web_development"): "58_intro_web_development",
    ("11-data-and-web", "56_data_handling_basics"): "59_data_handling_basics",

    ("12-capstone", "57_building_a_real_project"): "60_building_a_real_project",
    ("12-capstone", "58_next_steps"): "61_next_steps",
}


def run(cmd):
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", cmd)
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(1)


def main():
    # Pass 1: old -> tmp (for both .py and .ipynb)
    moves = []  # (tmp_path, new_path) to do in pass 2
    for (folder, old_stem), new_stem in RENAMES.items():
        for ext in (".py", ".ipynb"):
            old = f"{folder}/{old_stem}{ext}"
            tmp = f"{folder}/__tmp__{new_stem}{ext}"
            new = f"{folder}/{new_stem}{ext}"
            if not (ROOT / old).exists():
                print("MISSING (skip):", old)
                continue
            run(["git", "mv", old, tmp])
            moves.append((tmp, new))

    # Pass 2: tmp -> new
    for tmp, new in moves:
        run(["git", "mv", tmp, new])

    print(f"Renamed {len(moves)} files ({len(moves)//2} topics x 2 exts).")


if __name__ == "__main__":
    main()
