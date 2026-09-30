import sqlite3
from datetime import datetime

DB_FILE = "scans.db"


def _connect():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Create the tables if they don't exist yet."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scanned_at TEXT NOT NULL,
                target TEXT NOT NULL,
                file_count INTEGER NOT NULL,
                issue_count INTEGER NOT NULL,
                score INTEGER NOT NULL
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL REFERENCES scans(id),
                filename TEXT NOT NULL,
                line INTEGER NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL
            )""")


def save_scan(target, file_count, issues, score):
    """Store one scan and all its issues. Returns the scan id."""
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO scans (scanned_at, target, file_count, issue_count, score) "
            "VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             target, file_count, len(issues), score))
        scan_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO issues (scan_id, filename, line, category, severity, message) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [(scan_id, i.filename, i.line, i.category, i.severity, i.message)
             for i in issues])
        return scan_id


def get_history(limit=10):
    """Return the most recent scans, newest first."""
    with _connect() as conn:
        return conn.execute(
            "SELECT id, scanned_at, target, file_count, issue_count, score "
            "FROM scans ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        