from distutils.dir_util import copy_tree
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
    with runner.isolated_filesystem():
        input_folder = os.path.join(os.getcwd(), "input", "pytest")
        os.makedirs(input_folder)

        copy_tree(os.path.abspath(os.path.join(__file__, "..",
                  "..", "..", "input", "pytest")), input_folder)

        result = runner.invoke(enroll, ['input/pytest'])

        assert "Enrollment finished" in result.output
        assert result.exit_code == 0

        result = runner.invoke(
            search, ['input/pytest', "-d", "input/pytest", '--export'])

        output_folder = os.path.abspath(os.path.join(os.getcwd(), "output"))

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

        input_folder = os.path.join(os.getcwd(), "input", "pytest")
        os.makedirs(input_folder)

        copy_tree(os.path.abspath(os.path.join(__file__, "..",
                  "..", "..", "input", "pytest")), input_folder)

        result = runner.invoke(enroll, ['input/pytest'])

        assert "Enrollment finished" in result.output
        assert result.exit_code == 0

        result = runner.invoke(
            search, ['exists', "-d", "input/pytest", '--export'])

        assert "No matches found" in result.output
