import sqlite3

DATABASE_NAME = "hitlist.db"
SCHEMA = """
    CREATE TABLE IF NOT EXISTS hitlist(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role VARCHAR(100) NOT NULL,
        company VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        pay DECIMAL(10,2) NOT NULL,
        status VARCHAR(100) NOT NULL
    )
"""


def get_connection():
    con = sqlite3.connect(DATABASE_NAME)

    con.row_factory = sqlite3.Row
    return con


def ensure_schema(con):
    cursor = con.cursor()
    cursor.execute(SCHEMA)


def execute(query, params=(), fetch=False, return_rowcount=False):
    con = None
    try:
        con = get_connection()
        ensure_schema(con)
        cursor = con.cursor()
        cursor.execute(query, params)
        rowcount = cursor.rowcount

        if fetch:
            result = cursor.fetchall()
        elif return_rowcount:
            result = rowcount
        else:
            result = None

        con.commit()
        return result
    finally:
        if con is not None:
            con.close()
