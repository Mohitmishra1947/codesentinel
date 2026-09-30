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


class HardcodedPasswordRule(BaseRule):
    """Flags variables like password = "abc123" that hold secrets in plain text."""
    name = "hardcoded-password"
    category = "SECURITY"
    KEYWORDS = ("password", "passwd", "pwd", "secret", "token", "api_key")

    def check(self, tree, filename):
        issues = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            value = node.value
            if not (isinstance(value, ast.Constant)
                    and isinstance(value.value, str)
                    and value.value != ""):
                continue
            for target in node.targets:
                if (isinstance(target, ast.Name)
                        and any(k in target.id.lower() for k in self.KEYWORDS)):
                    issues.append(Issue(
                        filename, node.lineno, self.category, "high",
                        f"Hardcoded secret in variable '{target.id}'"))
        return issues