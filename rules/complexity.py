import ast
from models import Issue
from rules.base_rule import BaseRule


class ComplexityRule(BaseRule):
    """Flags functions whose cyclomatic complexity is above MAX_COMPLEXITY."""
    name = "high-complexity"
    category = "COMPLEXITY"
    MAX_COMPLEXITY = 10

    BRANCH_NODES = (ast.If, ast.For, ast.While, ast.ExceptHandler,
                    ast.With, ast.IfExp, ast.comprehension)

    def calculate(self, func):
        """Complexity = 1 + number of decision points inside the function."""
        score = 1
        for node in ast.walk(func):
            if isinstance(node, self.BRANCH_NODES):
                score += 1
            elif isinstance(node, ast.BoolOp):
                score += len(node.values) - 1   # each and/or adds a path
        return score

    def check(self, tree, filename):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                score = self.calculate(node)
                if score > self.MAX_COMPLEXITY:
                    issues.append(Issue(
                        filename, node.lineno, self.category, "medium",
                        f"Function '{node.name}' has complexity {score} (max {self.MAX_COMPLEXITY})"))
        return issues