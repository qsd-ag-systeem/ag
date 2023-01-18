from click.testing import CliRunner
from cli.ag import search, enroll
import os
from pytest import fixture


@fixture
def runner():
    return CliRunner()


def test_search_folder_no_arguments(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(search)
        assert "Error: Missing argument 'FOLDER'" in result.output
        assert result.exit_code == 2


def test_search_folder_not_exists(runner: CliRunner):
    # Create a temporary directory
    with runner.isolated_filesystem():
        result = runner.invoke(search, ['not_exists', '--debug'])

        assert "Error: Invalid value for 'FOLDER': Path 'not_exists' does not exist." in result.output
        assert result.exit_code == 2


def test_search_folder_exists(runner: CliRunner):
    # Create a temporary directory
    with runner.isolated_filesystem():
        os.mkdir('exists')
        result = runner.invoke(search, ['exists'])

        print(result.output)

        assert "is empty" in result.output
        assert result.exit_code == 0

def test_search_no_matches_found(runner: CliRunner):
    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test1.jpg', 'w') as f:
            f.write('test')
        
        result = runner.invoke(search, ['exists'])

        assert "No matches found" in result.output
        assert result.exit_code == 0

def test_search_match_found(runner: CliRunner):
    #enrolling pytest in-case it's not enrolled
    runner.invoke(enroll, ['input/pytest'])
       
    result = runner.invoke(search, args=["input/pytest", "-d", "input/pytest"])

    assert "| 1.jpg        | input/pytest/1.jpg-0 | input/pytest | 1.jpg       |" in result.output
    assert result.exit_code == 0