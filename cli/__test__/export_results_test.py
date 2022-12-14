from pathlib import Path
from click.testing import CliRunner
from cli.ag import enroll, search
import os
from pytest import fixture


@fixture
def runner():
    return CliRunner()


def test_search_export_fails(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(search, ['--export'])

        assert result.exit_code == 2
        assert "Usage: search [OPTIONS] FOLDER" in result.output


def test_search_export_output_created(runner: CliRunner):
    # Create test folder with fake images
    result = runner.invoke(enroll, ['input/pytest'])

    assert "Enrollment finished!" in result.output
    assert result.exit_code == 0

    result = runner.invoke(
        search, ['input/pytest', "-d", "input/pytest", '--export'])

    output_folder = Path(os.path.join(os.path.curdir, "output"))

    assert "Exporting results to" in result.output
    assert result.exit_code == 0
    assert os.path.exists(output_folder)


def test_search_export_no_match(runner: CliRunner):
    # Create test folder with fake images
    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test1.jpg', 'w') as f:
            f.write('test')
        with open('exists/test2.png', 'w') as f:
            f.write('test')
        with open('exists/test3.jpeg', 'w') as f:
            f.write('test')
        result = runner.invoke(enroll, ['exists'])

        assert "Enrollment finished!" in result.output
        assert result.exit_code == 0

        result = runner.invoke(search, ['exists', "-d", "exists", '--export'])

        assert "Exporting results to" not in result.output
