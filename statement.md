# Problem Statement

## Problem
Developers often ship Python code containing security risks (such as `eval()` and
hardcoded passwords), unused code, missing documentation and overly complex
functions. Manual code review is slow, inconsistent and easy to skip, and
existing tools are large and hard to understand or extend.

## Scope
CodeSentinel is a command-line static analysis tool for Python source files. It
parses code into an Abstract Syntax Tree (AST), applies pluggable rules,
computes a 0-100 quality score, produces terminal and HTML reports, and stores
scan history in SQLite. It does not execute the code it scans, and it analyses
Python files only.

## Target Users
- Students who want feedback on their own Python code
- Developers who want a quick quality and security check
- Teachers or reviewers who need to compare code quality over time

## High-Level Features
- Recursive scanning of a file or folder
- Six rules across security, quality and complexity
- Cyclomatic complexity calculation per function
- Quality score (0-100) with letter grade
- Terminal and HTML reports
- Scan history stored in SQLite (`--history`)
- Logging to file and graceful handling of files with syntax errors
- Plugin-style rule system: a new rule is one new class

