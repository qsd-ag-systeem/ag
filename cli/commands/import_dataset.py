from pathlib import Path
import click
import os
from core.import_dataset import import_all


@click.command("import")
@click.argument('file_name', type=str)
def import_dataset(file_name: str) -> None:
    file_path = os.path.join(os.getcwd(), "input", f"{file_name}.csv")
    file = Path(file_path)

    if not file.is_file():
        click.echo(f"Error: a file with this name '{file_path}' doesn't exist.", err=True)
        return

    import_all(file_path)

    click.echo(f'Done')
