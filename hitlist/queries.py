from .database import execute


def insert_job(role, company, location, pay, status):
    query = """
        INSERT INTO hitlist (role, company, location, pay, status)
        VALUES (?, ?, ?, ?, ?)
    """
    execute(query, (role, company, location, pay, status))


def fetch_jobs(status=None):
    if status:
        query = """
            SELECT *
            FROM hitlist
            WHERE status = ?
            ORDER BY id
        """
        return execute(query, (status,), fetch=True)

    query = """
        SELECT *
        FROM hitlist
        ORDER BY id
    """
    return execute(query, fetch=True)


def fetch_job_by_id(job_id):
    query = """
        SELECT *
        FROM hitlist
        WHERE id = ?
    """
    jobs = execute(query, (job_id,), fetch=True)
    return jobs[0] if jobs else None


def delete_job_by_id(job_id):
    query = """
        DELETE FROM hitlist WHERE id = ?
        """
    return execute(query, (job_id,), return_rowcount=True)


def delete_job_by_role_company(role, company):
    query = """
        DELETE FROM hitlist WHERE role=? AND company=?
        """
    return execute(query, (role, company), return_rowcount=True)


def delete_jobs_by_status(status):
    query = """
        DELETE FROM hitlist WHERE status=?
        """
    return execute(query, (status,), return_rowcount=True)


def truncate_jobs():
    delete_query = """
        DELETE FROM hitlist
        """
    reset_sequence_query = """
        DELETE FROM sqlite_sequence
        WHERE name = ?
        """
    deleted_count = execute(delete_query, return_rowcount=True)
    execute(reset_sequence_query, ("hitlist",))
    return deleted_count


def update_job_by_id(job_id, updates):
    assignments = ", ".join(f"{column} = ?" for column in updates)
    query = f"""
        UPDATE hitlist
        SET {assignments}
        WHERE id = ?
    """
    params = tuple(updates.values()) + (job_id,)
    return execute(query, params, return_rowcount=True)
