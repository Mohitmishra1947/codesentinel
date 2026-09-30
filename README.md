# CodeSentinel

A static code analyzer for Python, built on the `ast` module.

## Overview
CodeSentinel reads Python files without running them, converts each into an
Abstract Syntax Tree, and applies a set of rules to find security risks, code
quality problems and overly complex functions. It gives each project a 0-100
quality score and saves every scan to a database so quality can be tracked over
time.

## Features
- Security rules: `eval()`/`exec()` usage, hardcoded passwords and secrets
- Quality rules: unused imports, missing docstrings, long functions
- Complexity rule: cyclomatic complexity per function
- Quality score and letter grade
- Terminal report and styled HTML report
- Scan history in SQLite
- Logging to `codesentinel.log`
- Skips files with syntax errors instead of crashing

## Technologies
Python 3.12, `ast`, `argparse`, `sqlite3`, `logging`, `unittest`, Git

## Project Structure
codesentinel/
├── main.py # CLI entry point
├── scanner.py # finds .py files
├── models.py # Issue data class
├── scorer.py # quality score and grade
├── reporter.py # terminal and HTML reports
├── database.py # SQLite scan history
├── logger.py # file logging
├── rules/
│ ├── base_rule.py # abstract Rule class
│ ├── security.py
│ ├── quality.py
│ └── complexity.py
└── tests/
└── test_rules.py


## Installation and Running
Requires Python 3.9 or newer. No external packages are needed.

git clone https://github.com/YOUR-USERNAME/codesentinel.git
cd codesentinel
python main.py sample.py
python main.py . --html report.html
python main.py --history


## Testing

python -m unittest discover tests -v


## Adding a New Rule
1. Create a class that inherits from `BaseRule` and implement `check()`.
2. Add an instance of it to the `RULES` list in `main.py`.

## Screenshots
(Add screenshots of the terminal output and the HTML report here.)