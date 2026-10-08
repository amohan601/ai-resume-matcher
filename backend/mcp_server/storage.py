import sqlite3
from pathlib import Path
import os
from schema import Application
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr,   # explicit, never stdout
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("resume-matcher-database")


DB_PATH = Path(
    os.environ.get(
        "JOBAPPLICATIONS_DB_PATH",
        "/tmp/jobapplications.db"
    )
)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            source TEXT ,
            job_description TEXT,
            applied_date TEXT NOT NULL,
            status TEXT DEFAULT 'Applied'
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    if count == 0:
        seed = [
            ("ashley_m", "Appify", "Software Engineer", "http://linkedin.com/123", "Software engineer with knowledge of Python", "2026-09-01", "Applied"),
            ("richard_r", "Meta", "Software Engineer", "http://linkedin.com/456", "Software engineer with knowledge of Python", "2026-09-10", "Applied"),
            ("diana_q", "Apple", "Software Engineer", "http://linkedin.com/233", "Software engineer with knowledge of Python", "2026-09-08", "Suspended"),
            ("stanley", "Google", "Software Engineer", "http://linkedin.com/345", "Software engineer with knowledge of Python", "2026-09-09", "Cancelled"),
            ("ashley_m", "Visa", "AI Engineer", "http://linkedin.com/789", "AI engineer with knowledge of Python", "2026-09-07", "Cancelled"),
        ]
        conn.executemany(
            "INSERT INTO applications (user_id, company, role, source, job_description,applied_date, status) "
            "VALUES (?, ?, ?, ?, ?,?,?)",
            seed,
        )
        conn.commit()
    conn.close()


init_db()

def _row_to_dict(row: sqlite3.Row) -> Application:
    """Convert a database row into the application dictionary shape."""
    return Application(
        id=row["id"],
        user_id=row["user_id"],
        company=row["company"],
        role=row["role"],
        source=row["source"],
        job_description=row["job_description"],
        applied_date=row["applied_date"],
        status=row["status"],
    )
    


def list_all_applications() -> list[Application]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM applications ORDER BY applied_date DESC, id DESC").fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]

def create_application(application: Application) -> Application:
    logger.info("create_application called with %s", application.model_dump())
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO applications (user_id, company, role, source, job_description, applied_date, status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (application.user_id, application.company, application.role, application.source, application.job_description, application.applied_date, application.status),
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return _row_to_dict(row)