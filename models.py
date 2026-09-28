from dataclasses import dataclass


@dataclass
class Issue:
    """One problem found in a source file."""
    filename: str
    line: int
    category: str   # SECURITY / QUALITY / COMPLEXITY
    severity: str   # high / medium / low
    message: str