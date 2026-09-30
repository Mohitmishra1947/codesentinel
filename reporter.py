import html
from scorer import get_grade


def print_cli_report(issues, score, file_count):
    """Print the results in the terminal."""
    for i in issues:
        print(f"{i.filename}:{i.line} [{i.category}/{i.severity}] {i.message}")
    print(f"\nFiles scanned: {file_count}")
    print(f"Issues found:  {len(issues)}")
    print(f"Quality score: {score}/100 (Grade {get_grade(score)})")


def write_html_report(issues, score, file_count, output_path):
    """Save the results as a styled HTML page."""
    colors = {"high": "#d9534f", "medium": "#f0ad4e", "low": "#5bc0de"}
    rows = ""
    for i in issues:
        rows += (
            "<tr>"
            f"<td>{html.escape(i.filename)}</td>"
            f"<td>{i.line}</td>"
            f"<td>{i.category}</td>"
            f"<td style='color:{colors.get(i.severity, '#333')};"
            f"font-weight:bold'>{i.severity}</td>"
            f"<td>{html.escape(i.message)}</td>"
            "</tr>"
        )
    if not rows:
        rows = "<tr><td colspan='5'>No issues found. Great job!</td></tr>"

    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>CodeSentinel Report</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f6fa; }}
  h1 {{ color: #2c3e50; }}
  .cards {{ display: flex; gap: 20px; margin-bottom: 30px; }}
  .card {{ background: white; padding: 20px 30px; border-radius: 8px;
           box-shadow: 0 1px 4px rgba(0,0,0,0.15); text-align: center; }}
  .card .num {{ font-size: 36px; font-weight: bold; color: #2c3e50; }}
  table {{ border-collapse: collapse; width: 100%; background: white; }}
  th, td {{ padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }}
  th {{ background: #2c3e50; color: white; }}
</style>
</head>
<body>
<h1>CodeSentinel Report</h1>
<div class="cards">
  <div class="card"><div class="num">{score}/100</div>Quality Score</div>
  <div class="card"><div class="num">{get_grade(score)}</div>Grade</div>
  <div class="card"><div class="num">{file_count}</div>Files Scanned</div>
  <div class="card"><div class="num">{len(issues)}</div>Issues Found</div>
</div>
<table>
<tr><th>File</th><th>Line</th><th>Category</th><th>Severity</th><th>Message</th></tr>
{rows}
</table>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page)