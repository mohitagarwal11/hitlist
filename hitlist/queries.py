from .database import execute


def insert_job(role, company, location, pay, status):
    query = """
        INSERT INTO hitlist (role, company, location, pay, status)
        VALUES (?, ?, ?, ?, ?)
    """
    return execute(query, (role, company, location, pay, status), return_lastrowid=True)


def fetch_jobs(status=None, role=None, location=None, sort=None, order=None):
    filters = []
    params = []

    if status is not None:
        filters.append("status = ?")
        params.append(status)

    if role is not None:
        filters.append("role = ?")
        params.append(role)

    if location is not None:
        filters.append("location = ?")
        params.append(location)

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    order_column = sort if sort in {"id", "pay"} else "id"
    order_direction = "DESC" if order == "DESC" else "ASC"

    query = f"""
        SELECT *
        FROM hitlist
        {where_clause}
        ORDER BY {order_column} {order_direction}
    """
    return execute(query, tuple(params), fetch=True)


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
