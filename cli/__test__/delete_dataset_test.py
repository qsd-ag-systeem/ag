from click.testing import CliRunner
from cli.ag import delete_dataset, enroll
import os
from pytest import fixture


@fixture
def runner():
    return CliRunner()


def test_delete_dataset_no_arguments(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(delete_dataset)

        assert "Error: Missing argument 'DATASET'" in result.output
        assert result.exit_code == 2

def test_delete_dataset_not_exist(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(delete_dataset, ['set', '--debug'])

        assert "Dataset 'set' does not exist" in result.output
        assert result.exit_code == 1

def test_delete_dataset(runner: CliRunner):
    runner.invoke(enroll, ['input/pytest'])
    with runner.isolated_filesystem():
        
        result = runner.invoke(delete_dataset, ['input/pytest'])

        assert "" in result.output
        assert result.exit_code == 0