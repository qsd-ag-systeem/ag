import click

class SearchResult:
    name = ""
    match = ""
    location = ""

    def __init__(self, name, match, location):
        self.name = name
        self.match = match
        self.location = location

    def __len__(self):
        return 1

class TableRow:
    cells = []

    def __init__(self, cells):
        self.cells = cells

class Table:
    rows = []
    header = []

    def __init__(self, rows, header):
        self.rows = rows
        self.header = header

    def print_table(self):
        widths = [len(cell) for cell in self.header]
        for row in self.rows:
            for i, cell in enumerate(row.cells):
                widths[i] = max(widths[i], len(str(cell)))

        click.echo("+" + "+".join("-" * (width + 2) for width in widths) + "+")
        formatted_row = "| " + " | ".join("{:{}}".format(cell, width) for cell, width in zip(self.header, widths)) + " |"
        click.echo(formatted_row.format(*self.header))
        click.echo("+" + "+".join("-" * (width + 2) for width in widths) + "+")
        for row in self.rows:
            formatted_row = "| " + " | ".join("{:{}}".format(cell, width) for cell, width in zip(row.cells, widths)) + " |"
            click.echo(formatted_row.format(*row.cells))
            click.echo("+" + "+".join("-" * (width + 2) for width in widths) + "+")

class SearchResults:
    results = []
    search_file_name = ""

    def __init__(self, search_file_name, results):
        self.search_file_name = search_file_name
        self.results = results
        self.sort()

    def sort(self):
        self.results.sort(key=lambda x: x.match)

    def print_results(self, offset = 0, limit = 10):
        rows = []
        header = ["Rank", "Naam", "Afstand", "Location"]
        top10 = self.results[offset:offset + limit]
        for i, result in enumerate(top10):
            rows.append(TableRow([i + offset + 1, result.name, result.match, result.location]))

        table = Table(rows, header)

        click.echo(f"{len(self.results)} Matches found!")
        click.echo("File: " + self.search_file_name)
        table.print_table()