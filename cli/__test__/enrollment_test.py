from click.testing import CliRunner
from cli.ag import enroll
import os
from pytest import fixture


@fixture
def runner():
    return CliRunner()


def test_enrollment_folder_no_arguments(runner: CliRunner):
    with runner.isolated_filesystem():
        result = runner.invoke(enroll)
        assert "Error: Missing argument 'FOLDER'" in result.output
        assert result.exit_code == 2


def test_enrollment_folder_not_exists(runner: CliRunner):
    # Create a temporary directory
    with runner.isolated_filesystem():
        result = runner.invoke(enroll, ['not_exists', '--debug'])

        assert "Error: Invalid value for 'FOLDER': Path 'not_exists' does not exist." in result.output
        assert result.exit_code == 2


def test_enrollment_folder_exists(runner: CliRunner):
    # Create a temporary directory
    with runner.isolated_filesystem():
        os.mkdir('exists')
        result = runner.invoke(enroll, ['exists'])

        print(result.output)

        assert "is empty" in result.output
        assert result.exit_code == 0


def test_enrollment_wrong_file(runner: CliRunner):
    # Create a temporary directory
    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test.txt', 'w') as f:
            f.write('test')
        result = runner.invoke(enroll, ['exists', '--debug'])

        print(result.output)

        assert "File not supported" in result.output
        assert result.exit_code == 0


def test_enrollment_folder_with_valid_image_files(runner: CliRunner):
    # Create a temporary directory and add some valid image files
    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test1.jpg', 'w') as f:
            f.write('test')
        with open('exists/test2.png', 'w') as f:
            f.write('test')
        with open('exists/test3.jpeg', 'w') as f:
            f.write('test')
        result = runner.invoke(enroll, ['exists'])

        assert "Enrollment finished" in result.output
        assert result.exit_code == 0


def test_enrollment_folder_with_invalid_image_files(runner: CliRunner):
    # Create a temporary directory and add some invalid image files
    with runner.isolated_filesystem():
        os.mkdir('exists')
        with open('exists/test1.txt', 'w') as f:
            f.write('test')
        with open('exists/test2.doc', 'w') as f:
            f.write('test')
        with open('exists/test3.pdf', 'w') as f:
            f.write('test')
        result = runner.invoke(enroll, ['exists'])

        assert "Enrollment finished" in result.output
        assert result.exit_code == 0
