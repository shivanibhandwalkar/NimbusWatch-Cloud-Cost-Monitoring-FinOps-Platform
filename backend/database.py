import sqlite3

DB_FILE = "nimbuswatch.db"
DEFAULT_BUDGET = 200.0


def get_connection():
    """Open the database file (it is created automatically if missing)."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # columns by name
    return conn


def init_db():
    """Create the tables the first time the app runs."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS costs (
                date    TEXT NOT NULL,
                service TEXT NOT NULL,
                cost    REAL NOT NULL,
                PRIMARY KEY (date, service)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )


def save_costs(records):
    """Save records. If a (date, service) row exists, update its cost."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO costs (date, service, cost)
            VALUES (:date, :service, :cost)
            ON CONFLICT(date, service) DO UPDATE SET cost = excluded.cost
            """,
            records,
        )
    return len(records)


def load_costs(days=30):
    """Read the most recent days of records, oldest first."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT date, service, cost FROM costs
            WHERE date >= date('now', ?)
            ORDER BY date, service
            """,
            (f"-{days} days",),
        ).fetchall()
    return [dict(row) for row in rows]


def get_budget():
    """Read the monthly budget, or use the default if none is saved yet."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = 'monthly_budget'"
        ).fetchone()
    return float(row["value"]) if row else DEFAULT_BUDGET


def set_budget(amount):
    """Save the monthly budget (insert the first time, update afterwards)."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO settings (key, value) VALUES ('monthly_budget', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (str(amount),),
        )
    return amount