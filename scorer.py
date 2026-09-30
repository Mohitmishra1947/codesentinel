PENALTY = {"high": 10, "medium": 5, "low": 2}


def calculate_score(issues, file_count):
    """Score from 0-100. Each issue costs points by severity,
    averaged over the number of files scanned."""
    if file_count == 0:
        return 100
    total = sum(PENALTY.get(i.severity, 1) for i in issues)
    return max(0, round(100 - total / file_count))


def get_grade(score):
    """Convert a numeric score into a letter grade."""
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"