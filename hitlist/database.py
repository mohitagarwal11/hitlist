import sqlite3


# to get a connection with the sqlite db
def get_connection():
    con = sqlite3.connect("hitlist.db")
    con.row_factory = sqlite3.Row
    return con


# custom execute wrapper so i can get outputs or no outputs depending on fetch param
def execute(query, params=(), fetch=False):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(query, params)

    if fetch:
        result = cursor.fetchall()
    else:
        result = None

    con.commit()
    con.close()
    return result


def init_db():
    query = """
        CREATE TABLE IF NOT EXISTS hitlist(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role VARCHAR(100) NOT NULL,
            company VARCHAR(100) NOT NULL,
            location VARCHAR(100) NOT NULL,
            pay DECIMAL(10,2) NOT NULL,
            status VARCHAR(100) NOT NULL
        )
    """
    con = get_connection()
    cur = con.cursor()
    cur.execute(query)

    con.commit()
    con.close()
