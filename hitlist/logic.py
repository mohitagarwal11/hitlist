from .queries import (
    delete_job_by_id,
    delete_job_by_role_company,
    delete_jobs_by_status,
    fetch_job_by_id,
    fetch_jobs,
    insert_job,
    truncate_jobs as truncate_jobs_query,
    update_job_by_id,
)

STATUS_CHOICES = {
    "p": "applied",
    "i": "interviewed",
    "r": "rejected",
    "a": "accepted",
    "d": "declined",
    "g": "ghosted",
}

VALID_STATUSES = set(STATUS_CHOICES.values())
STATUS_PROMPT = (
    "Status "
    "\n[p=applied, i=interviewed, r=rejected, a=accepted, d=declined, g=ghosted]"
)


def add_job(role, company, location, pay, status):
    normalized_status = normalize_status(status)
    job_id = insert_job(role, company, location, pay, normalized_status)
    return dict(fetch_job_by_id(job_id))


def update_job(job_id, role=None, company=None, location=None, pay=None, status=None):
    updates = {}

    if role is not None:
        updates["role"] = role

    if company is not None:
        updates["company"] = company

    if location is not None:
        updates["location"] = location

    if pay is not None:
        updates["pay"] = pay

    if status is not None:
        updates["status"] = normalize_status(status)

    if not updates:
        raise ValueError("Provide at least one field to update.")

    job = fetch_job_by_id(job_id)

    if job is None:
        raise ValueError(f"Job #{job_id} not found.")

    update_job_by_id(job_id, updates)
    return dict(fetch_job_by_id(job_id))


def delete_jobs(job_id=None, role=None, company=None, status=None):
    deleted_count = 0
    if job_id is not None:
        if delete_job_by_id(job_id):
            deleted_count += 1
        else:
            raise ValueError(f"Job #{job_id} not found.")

    if role or company:
        if not (role and company):
            raise ValueError("Both role and company are required to delete by role.")

        rowCount = delete_job_by_role_company(role, company)
        if rowCount > 0:
            deleted_count += rowCount
        else:
            raise ValueError(f"No jobs found for {role} at {company}.")

    if status:
        normalized_status = normalize_status(status)
        rowCount = delete_jobs_by_status(normalized_status)
        if rowCount > 0:
            deleted_count += rowCount
        else:
            raise ValueError(f"No jobs found with status {normalized_status}.")

    return deleted_count


def truncate_jobs(choice):
    if choice.lower() != "y":
        return {"deleted_count": 0, "cancelled": True}

    return {"deleted_count": truncate_jobs_query(), "cancelled": False}


def list_jobs(status=None, role=None, location=None, sort=None):
    normalized_status = normalize_status(status) if status else None

    sort_key = "id"
    order = "ASC"
    if sort:
        token = sort.lower()
        if token in {"p", "pay"}:
            sort_key = "pay"
            order = "DESC"
        elif token in {"i", "id"}:
            sort_key = "id"
            order = "ASC"
        else:
            raise ValueError("Invalid sort. Use p/pay or i/id.")

    jobs = fetch_jobs(
        status=normalized_status,
        role=role,
        location=location,
        sort=sort_key,
        order=order,
    )

    if not jobs:
        return []

    return [dict(job) for job in jobs]


def normalize_status(status):
    normalized = STATUS_CHOICES.get(status.lower(), status.lower())
    if normalized not in VALID_STATUSES:
        raise ValueError(
            "Invalid status. Use p, i, r, a, d, g or the full status name."
        )
    return normalized


def format_job(job):
    return (
        f"{job['id']} | {job['role']} | {job['company']} | "
        f"{job['location']} | {job['pay']} | {job['status']}"
    )


def format_count(count, noun):
    suffix = "" if count == 1 else "s"
    return f"{count} {noun}{suffix}"
