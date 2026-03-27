import click

from .queries import delete_job_id, insert_job, list_jobs
from .database import init_db

STATUS_CHOICES = {
    "p": "applied",
    "i": "interviewed",
    "r": "rejected",
    "a": "accepted",
    "d": "declined",
    "g": "ghosted",
}


@click.group()
def cli():
    pass


@cli.command()
def init():
    init_db()
    click.echo("\nHITLIST IS ALIVE!!\n")


@cli.command()
@click.option("--role", prompt="Enter job role", type=str)
@click.option("--company", prompt="Enter company name", type=str)
@click.option("--location", prompt="Enter Job Location", type=str)
@click.option("--pay", prompt="Enter est. monthly Pay", type=int)
@click.option(
    "--status",
    prompt="Status \n[p=applied, i=interviewed, r=rejected, a=accepted, d=declined, g=ghosted]",
    type=str,
)
def add(role, company, location, pay, status):
    insert_job(role, company, location, pay, STATUS_CHOICES[status.lower()])
    click.echo(
        f"\nAdded {role} at {company} currently {STATUS_CHOICES[status.lower()]}.\n"
    )


@cli.command()
@click.argument("id", required=False, type=int)
def delete(id):
    if id is not None:
        delete_job_id(id)
        click.echo(f"\nJob #{id} deleted successfully.\n")


@cli.command()
def list():
    jobs = list_jobs()

    if not jobs:
        click.echo("\nNo jobs found.\n")
        return

    output = []
    for job in jobs:
        line = f"{job['id']} | {job['role']} | {job['company']} | {job['location']} | {job['pay']} | {job['status']}"
        output.append(line)

    click.echo("\n".join(output))


if __name__ == "__main__":
    cli()
