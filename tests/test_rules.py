import ast
import os
import sys
import unittest

# Let the tests import modules from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rules.security import DangerousCallRule, HardcodedPasswordRule
from rules.quality import UnusedImportRule, MissingDocstringRule, LongFunctionRule
from rules.complexity import ComplexityRule
from scorer import calculate_score, get_grade
from models import Issue


def run(rule, code):
    """Parse a code string and run one rule on it."""
    return rule.check(ast.parse(code), "test.py")


class TestSecurityRules(unittest.TestCase):
    def test_eval_is_flagged(self):
        self.assertEqual(len(run(DangerousCallRule(), "eval('1+1')")), 1)

    def test_exec_is_flagged(self):
        self.assertEqual(len(run(DangerousCallRule(), "exec('x=1')")), 1)

    def test_safe_call_not_flagged(self):
        self.assertEqual(len(run(DangerousCallRule(), "print('hi')")), 0)

    def test_hardcoded_password_flagged(self):
        self.assertEqual(len(run(HardcodedPasswordRule(), 'password = "abc"')), 1)

    def test_password_from_input_not_flagged(self):
        self.assertEqual(len(run(HardcodedPasswordRule(), "password = input()")), 0)


class TestQualityRules(unittest.TestCase):
    def test_unused_import_flagged(self):
        self.assertEqual(len(run(UnusedImportRule(), "import os")), 1)

    def test_used_import_not_flagged(self):
        code = "import os\nprint(os.name)"
        self.assertEqual(len(run(UnusedImportRule(), code)), 0)

    def test_missing_docstring_flagged(self):
        self.assertEqual(len(run(MissingDocstringRule(), "def f():\n    pass")), 1)

    def test_docstring_present_not_flagged(self):
        code = 'def f():\n    """Doc."""\n    pass'
        self.assertEqual(len(run(MissingDocstringRule(), code)), 0)

    def test_long_function_flagged(self):
        code = "def f():\n" + "    x = 1\n" * 60
        self.assertEqual(len(run(LongFunctionRule(), code)), 1)


class TestComplexityRule(unittest.TestCase):
    def test_simple_function_score_is_1(self):
        func = ast.parse("def f():\n    return 1").body[0]
        self.assertEqual(ComplexityRule().calculate(func), 1)

    def test_if_adds_one(self):
        func = ast.parse("def f(a):\n    if a:\n        return 1").body[0]
        self.assertEqual(ComplexityRule().calculate(func), 2)

    def test_and_adds_one(self):
        func = ast.parse("def f(a, b):\n    if a and b:\n        return 1").body[0]
        self.assertEqual(ComplexityRule().calculate(func), 3)


class TestScorer(unittest.TestCase):
    def test_no_issues_gives_100(self):
        self.assertEqual(calculate_score([], 5), 100)

    def test_high_issue_costs_10_points(self):
        issues = [Issue("a.py", 1, "SECURITY", "high", "x")]
        self.assertEqual(calculate_score(issues, 1), 90)

    def test_score_never_below_zero(self):
        issues = [Issue("a.py", 1, "SECURITY", "high", "x")] * 50
        self.assertEqual(calculate_score(issues, 1), 0)

    def test_grades(self):
        self.assertEqual(get_grade(95), "A")
        self.assertEqual(get_grade(80), "B")
        self.assertEqual(get_grade(30), "F")


if __name__ == "__main__":
    unittest.main()