import ast
from models import Issue
from rules.base_rule import BaseRule


class UnusedImportRule(BaseRule):
    """Flags imports that are never used in the file."""
    name = "unused-import"
    category = "QUALITY"

    def check(self, tree, filename):
        imported = {}   # name -> line number
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = (alias.asname or alias.name).split(".")[0]
                    imported[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported[alias.asname or alias.name] = node.lineno

        used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}

        issues = []
        for name, line in imported.items():
            if name not in used:
                issues.append(Issue(
                    filename, line, self.category, "low",
                    f"Unused import: {name}"))
        return issues
    





class MissingDocstringRule(BaseRule):
    """Flags functions and classes that have no docstring."""
    name = "missing-docstring"
    category = "QUALITY"

    def check(self, tree, filename):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node) is None:
                    issues.append(Issue(
                        filename, node.lineno, self.category, "low",
                        f"Missing docstring in '{node.name}'"))
        return issues


class LongFunctionRule(BaseRule):
    """Flags functions longer than MAX_LINES lines."""
    name = "long-function"
    category = "QUALITY"
    MAX_LINES = 50

    def check(self, tree, filename):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                length = (node.end_lineno or node.lineno) - node.lineno + 1
                if length > self.MAX_LINES:
                    issues.append(Issue(
                        filename, node.lineno, self.category, "medium",
                        f"Function '{node.name}' is {length} lines long (max {self.MAX_LINES})"))
        return issues