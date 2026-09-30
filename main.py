import ast
import argparse
from scanner import find_python_files
from scorer import calculate_score
from reporter import print_cli_report, write_html_report
from logger import get_logger
from database import init_db, save_scan, get_history
from rules.security import DangerousCallRule, HardcodedPasswordRule
from rules.quality import UnusedImportRule, MissingDocstringRule, LongFunctionRule
from rules.complexity import ComplexityRule

RULES = [DangerousCallRule(), HardcodedPasswordRule(), UnusedImportRule(),
         MissingDocstringRule(), LongFunctionRule(), ComplexityRule()]

log = get_logger()


def analyze_file(path):
    """Parse one file and run every rule on it."""
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (SyntaxError, UnicodeDecodeError, OSError) as e:
        print(f"Skipped {path}: {e}")
        log.warning("Skipped %s: %s", path, e)   # reliability: don't crash
        return []

    issues = []
    for rule in RULES:
        issues.extend(rule.check(tree, path))
    return issues


def show_history():
    """Print the last scans stored in the database."""
    rows = get_history()
    if not rows:
        print("No scans saved yet.")
        return
    print(f"{'ID':<4} {'Date':<20} {'Files':<6} {'Issues':<7} {'Score':<6} Target")
    for sid, when, target, files, count, score in rows:
        print(f"{sid:<4} {when:<20} {files:<6} {count:<7} {score:<6} {target}")


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="CodeSentinel static analyzer")
    parser.add_argument("path", nargs="?", help="Python file or folder to scan")
    parser.add_argument("--html", metavar="FILE", help="Save an HTML report")
    parser.add_argument("--history", action="store_true",
                        help="Show past scans and exit")
    args = parser.parse_args()

    init_db()
    if args.history:
        show_history()
        return
    if not args.path:
        parser.error("please give a path to scan, or use --history")

    log.info("Scan started: %s", args.path)
    files = find_python_files(args.path)
    all_issues = []
    for file in files:
        all_issues.extend(analyze_file(file))
    all_issues.sort(key=lambda x: (x.filename, x.line))

    score = calculate_score(all_issues, len(files))
    print_cli_report(all_issues, score, len(files))
    save_scan(args.path, len(files), all_issues, score)
    log.info("Scan finished: %d files, %d issues, score %d",
             len(files), len(all_issues), score)

    if args.html:
        write_html_report(all_issues, score, len(files), args.html)
        print(f"HTML report saved to {args.html}")


if __name__ == "__main__":
    main()