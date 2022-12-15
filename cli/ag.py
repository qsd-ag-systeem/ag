"""
CLI for the face recognition application.
"""
import click
from core.setup_db import setup_db
from cli.commands.enroll import enroll
from cli.commands.search import search
from cli.commands.datasets import delete_dataset, get_datasets
from cli.commands.export import export
from cli.commands.import_dataset import import_dataset


@click.group()
def cli():
    """
    CLI group for the face recognition application.
    """

cli.add_command(enroll)
cli.add_command(search)
cli.add_command(get_datasets)
cli.add_command(delete_dataset)
cli.add_command(export)
cli.add_command(import_dataset)


# since it is not much, I decided to leave it in here
@cli.command()
def setup() -> None:
    """
    This command sets up the database.
    """
    setup_db()
    click.echo('Done')

if __name__ == '__main__':
    cli()
