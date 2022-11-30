from faker import Faker
fake = Faker()

class SearchResult:
    name = ""
    match = ""
    location = ""

    def __init__(self, name, match, location):
        self.name = name
        self.match = match
        self.location = location

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

    def printTable(self):
        widths = [len(cell) for cell in self.header]
        for row in self.rows:
            for i, cell in enumerate(row.cells):
                widths[i] = max(widths[i], len(str(cell)))

        print("+" + "+".join("-" * (width + 2) for width in widths) + "+")
        formatted_row = "| " + " | ".join("{:{}}".format(cell, width) for cell, width in zip(self.header, widths)) + " |"
        print(formatted_row.format(*self.header))
        print("+" + "+".join("-" * (width + 2) for width in widths) + "+")
        for row in self.rows:
            formatted_row = "| " + " | ".join("{:{}}".format(cell, width) for cell, width in zip(row.cells, widths)) + " |"
            print(formatted_row.format(*row.cells))
            print("+" + "+".join("-" * (width + 2) for width in widths) + "+")

class SearchResults:
    results = []
    searchFileName = ""

    def __init__(self, searchFileName, results):
        self.searchFileName = searchFileName
        self.results = results

    def sort(self):
        self.results.sort(key=lambda x: x.match, reverse=True)

    def printResults(self, limit = 10):
        rows = []
        header = ["Rank", "Naam", "Match (%)", "Location"]
        top10 = self.results[0:limit]
        for i, result in enumerate(top10):
            rows.append(TableRow([i + 1, result.name, result.match, result.location]))

        table = Table(rows, header)

        print("Matches found!")
        print("File: " + self.searchFileName)
        table.printTable()

results = []
for i in range(100):
    name = fake.name()
    results.append(SearchResult(name, fake.random_int(min=0, max=100), "./images/" + name.replace(" ", "_").lower() + ".png"))

searchResults = SearchResults("./unknown_images/yilong_ma.png", results)
searchResults.sort()
searchResults.printResults()
