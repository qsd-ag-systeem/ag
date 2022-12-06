from click.testing import CliRunner
from cli.ag import enroll
import os


def test_enrollment_folder_no_arguments():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(enroll)
        assert "Error: Missing argument 'FOLDER'" in result.output
        assert result.exit_code == 2


def test_enrollment_folder_not_exists():
    runner = CliRunner()

    # Create a temporary directory
    with runner.isolated_filesystem():
        result = runner.invoke(enroll, ['not_exists'])
        assert "Error: Invalid value for 'FOLDER': Path 'not_exists' does not exist." in result.output
        assert result.exit_code == 2


def test_enrollment_folder_exists():
    runner = CliRunner()

    # Create a temporary directory
    with runner.isolated_filesystem():
        os.mkdir('exists')
        result = runner.invoke(enroll, ['exists'])

        assert "Enrollment finished!" in result.output
        assert result.exit_code == 0
