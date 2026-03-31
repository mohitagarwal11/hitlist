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

    if fetch_job_by_id(job_id) is None:
        raise ValueError(f"Job #{job_id} not found.")

    update_job_by_id(job_id, updates)
    updated_job = fetch_job_by_id(job_id)
    return f"Updated job #{job_id}.\n{format_job(updated_job)}"


def delete_jobs(job_id=None, role=None, company=None, status=None):
    actions = []

    if job_id is not None:
        deleted_count = delete_job_by_id(job_id)
        if deleted_count:
            actions.append(f"Deleted job #{job_id}.")
        else:
            actions.append(f"Job #{job_id} not found.")

    if role or company:
        if not (role and company):
            raise ValueError("Both role and company are required to delete by role.")

        deleted_count = delete_job_by_role_company(role, company)
        if deleted_count:
            actions.append(
                f"Deleted {format_count(deleted_count, 'job')} for {role} at {company}."
            )
        else:
            actions.append(f"No jobs found for {role} at {company}.")

    if status:
        normalized_status = normalize_status(status)
        deleted_count = delete_jobs_by_status(normalized_status)
        if deleted_count:
            actions.append(
                f"Deleted {format_count(deleted_count, 'job')} with status {normalized_status}."
            )
        else:
            actions.append(f"No jobs found with status {normalized_status}.")

    if not actions:
        raise ValueError(
            "Provide at least one delete filter: id, role with company, or status."
        )

    return "\n".join(actions)


def truncate_jobs(choice):
    if choice.lower() != "y":
        return "Delete all cancelled."

    truncate_jobs_query()
    return "Deleted all jobs."


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
        return "No jobs found."

    return "\n".join(format_job(job) for job in jobs)


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
