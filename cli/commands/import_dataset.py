from pathlib import Path
import click
import os
from core.import_dataset import import_all


@click.command("import", help="Importeert een dataset van een csv bestand naar de database.")
@click.argument('file_name', type=str)
def import_dataset(file_name: str) -> None:
    """
    Imports datasets from a csv file into the database.
    """

    if not file_name.endswith('.csv'):
        file_name = f"{file_name}.csv"

    file_path = os.path.join(os.getcwd(), f"{file_name}")
    file = Path(file_path)

    if not file.is_file():
        click.echo(f"Error: a file with this name '{file_path}' doesn't exist.", err=True)
        return

    import_all(file_path)

    click.echo(f'Done')
