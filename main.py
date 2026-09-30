import ast
import argparse
from scanner import find_python_files
from rules.security import DangerousCallRule, HardcodedPasswordRule
from rules.quality import UnusedImportRule, MissingDocstringRule, LongFunctionRule

RULES = [DangerousCallRule(), HardcodedPasswordRule(), UnusedImportRule(),
         MissingDocstringRule(), LongFunctionRule()]



def analyze_file(path):
    """Parse one file and run every rule on it."""
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Skipped {path}: {e}")   # reliability: don't crash
        return []

    issues = []
    for rule in RULES:
        issues.extend(rule.check(tree, path))
    return issues


def main():
    parser = argparse.ArgumentParser(description="CodeSentinel static analyzer")
    parser.add_argument("path", help="Python file or folder to scan")
    args = parser.parse_args()

    all_issues = []
    for file in find_python_files(args.path):
        all_issues.extend(analyze_file(file))

    for i in sorted(all_issues, key=lambda x: (x.filename, x.line)):
        print(f"{i.filename}:{i.line} [{i.category}/{i.severity}] {i.message}")
    print(f"\n{len(all_issues)} issue(s) found")


if __name__ == "__main__":
    main()