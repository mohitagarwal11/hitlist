from .database import execute


def insert_job(role, company, location, pay, status):
    query = """
        INSERT INTO hitlist (role, company, location, pay, status)
        VALUES (?, ?, ?, ?, ?)
    """
    execute(query, (role, company, location, pay, status))


def list_jobs():
    query = """
        SELECT *
        FROM hitlist
        ORDER BY id
    """
    return execute(query, fetch=True)


def delete_job_id(id):
    query = """
        DELETE FROM hitlist WHERE id = ?
        """
    execute(query, (id,))
