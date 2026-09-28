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