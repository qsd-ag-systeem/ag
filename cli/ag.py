import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('folder', type=click.Path(exists=True))
def enroll(folder: str) -> None:
    click.echo(f'Enroll {folder}')


@cli.command()
@click.option("--dataset", "-d", "dataset", type=str, required=True, help="De naam van een bestaande dataset. In het geval dat bij de enrollment een naam is gekozen anders dan de folder naam kan ook de folder naam alsnog gebruikt worden bij het verwijderen.")
def search(dataset: str) -> None:
    click.echo(f'Search: {dataset}')
