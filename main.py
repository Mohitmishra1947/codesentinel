import ast
import argparse
from scanner import find_python_files
from scorer import calculate_score
from reporter import print_cli_report, write_html_report
from rules.security import DangerousCallRule, HardcodedPasswordRule
from rules.quality import UnusedImportRule, MissingDocstringRule, LongFunctionRule
from rules.complexity import ComplexityRule

RULES = [DangerousCallRule(), HardcodedPasswordRule(), UnusedImportRule(),
         MissingDocstringRule(), LongFunctionRule(), ComplexityRule()]


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
    parser.add_argument("--html", metavar="FILE", help="Save an HTML report")
    args = parser.parse_args()

    files = find_python_files(args.path)
    all_issues = []
    for file in files:
        all_issues.extend(analyze_file(file))
    all_issues.sort(key=lambda x: (x.filename, x.line))

    score = calculate_score(all_issues, len(files))
    print_cli_report(all_issues, score, len(files))

    if args.html:
        write_html_report(all_issues, score, len(files), args.html)
        print(f"HTML report saved to {args.html}")


if __name__ == "__main__":
    main()