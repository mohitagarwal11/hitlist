import click

from .logic import (
    STATUS_PROMPT,
    add_job,
    delete_jobs,
    list_jobs,
    truncate_jobs,
    update_job,
)


@click.group()
def cli():
    pass


@cli.command(name="add")
@click.option("--role", prompt="Enter job role", type=str)
@click.option("--company", prompt="Enter company name", type=str)
@click.option("--location", prompt="Enter Job Location", type=str)
@click.option("--pay", prompt="Enter est. monthly Pay", type=int)
@click.option(
    "--status",
    prompt=STATUS_PROMPT,
    type=str,
)
def add_command(role, company, location, pay, status):
    try:
        click.echo(add_job(role, company, location, pay, status))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command(name="update")
@click.argument("id", type=int)
@click.option("--role", required=False, type=str)
@click.option("--company", required=False, type=str)
@click.option("--location", required=False, type=str)
@click.option("--pay", required=False, type=int)
@click.option("--status", required=False, type=str)
def update_command(id, role, company, location, pay, status):
    try:
        click.echo(
            update_job(
                job_id=id,
                role=role,
                company=company,
                location=location,
                pay=pay,
                status=status,
            )
        )
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command(name="delete")
@click.argument("id", required=False, type=int)
@click.option("--role", required=False, type=str)
@click.option("--company", required=False, type=str)
@click.option("--status", required=False, type=str)
def delete_command(id, role, company, status):
    try:
        click.echo(delete_jobs(job_id=id, role=role, company=company, status=status))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command(name="list")
@click.option("--status", required=False, type=str)
@click.option("--role", required=False, type=str)
@click.option("--location", required=False, type=str)
@click.option("--sort", type=str, prompt="Sort: pay(p) / id(i)")
def list_command(status, role, location, sort):
    try:
        click.echo(list_jobs(status, role, location, sort))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command(name="drop")
@click.option("--choice", prompt="Please confirm to delete all jobs(y/n)", type=str)
def truncate_command(choice):
    try:
        click.echo(truncate_jobs(choice))
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


if __name__ == "__main__":
    cli()
