from click.testing import CliRunner
from cli.ag import enroll
import os


def test_enrollment_folder_no_arguments():
    runner = CliRunner()
    result = runner.invoke(enroll)
    assert "Error: Missing argument 'FOLDER'" in result.output
    assert result.exit_code == 2


def test_enrollment_folder_not_exists():
    runner = CliRunner()

    path = os.path.join("input", "test2")

    print('path', path)

    result = runner.invoke(enroll, [path])

    print(result.output)

    assert f"does not exist." in result.output
    assert result.exit_code == 2
