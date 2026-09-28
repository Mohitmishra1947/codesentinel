import ast
from abc import ABC, abstractmethod
from models import Issue


class BaseRule(ABC):
    """Every rule inherits from this and implements check()."""
    name = "base"
    category = "QUALITY"

    @abstractmethod
    def check(self, tree: ast.AST, filename: str) -> list[Issue]:
        """Inspect the AST and return a list of Issues."""