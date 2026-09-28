import ast
from models import Issue
from rules.base_rule import BaseRule


class DangerousCallRule(BaseRule):
    """Flags eval() and exec() calls."""
    name = "dangerous-call"
    category = "SECURITY"
    DANGEROUS = {"eval", "exec"}

    def check(self, tree, filename):
        issues = []
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in self.DANGEROUS):
                issues.append(Issue(
                    filename, node.lineno, self.category, "high",
                    f"Use of {node.func.id}() is dangerous"))
        return issues