from click.testing import CliRunner
from cli.ag import cross_search
import os
from pytest import fixture


@fixture
def runner():
    return CliRunner()


def test_cross_search_dataset_no_arguments_d1(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(cross_search)
        assert "Error: Missing option '--dataset1' / '-d1'." in result.output
        assert result.exit_code == 2

def test_cross_search_dataset_no_arguments_d2(runner: CliRunner):
    with runner.isolated_filesystem():
        os.mkdir('db1')
        result = runner.invoke(cross_search, args=["-d1", "db1"])
        assert "Error: Missing option '--dataset2' / '-d2'." in result.output
        assert result.exit_code == 2

def test_cross_search_dataset_not_exist(runner: CliRunner):
    with runner.isolated_filesystem():
        os.mkdir('db1')
        os.mkdir('db2')
        result = runner.invoke(cross_search, args=["-d1", "db1", "-d2", "db2"])
        assert "" in result.output
        assert result.exit_code == 1

def test_cross_search_matches_found(runner: CliRunner):
    result = runner.invoke(cross_search, args=["-d1", "input/pytest", "-d2", "input/pytest"])

    assert "| input/pytest | input/pytest | 1.jpg    | 1.jpg                 |" in result.output
    assert result.exit_code == 0