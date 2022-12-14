import os
from datetime import datetime
from distutils.dir_util import copy_tree

from click.testing import CliRunner

from cli.ag import export, enroll


# Test that the command creates the 'output' directory if it doesn't already exist
def test_export_creates_output_dir():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(export, ['example'])
        assert result.exit_code == 0
        assert os.path.isdir(os.path.join(os.getcwd(), "output"))

# Test that the command creates the output file with the correct name and location
def test_export_creates_output_file():
    runner = CliRunner()

    with runner.isolated_filesystem():
        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Running export command with variable date as argument
        result = runner.invoke(export, [date, '--debug'])

        output_file = os.path.join(os.getcwd(), "output", f"{date}.csv")

        assert result.exit_code == 0
        assert os.path.isfile(output_file)

# Test that the command generates the expected output in the file
def test_export_generates_expected_output():
    runner = CliRunner()

    dataset = "input/pytest"

    with runner.isolated_filesystem():
        #Copy test dataset to isolated filesystem
        input_dir = os.path.join(os.getcwd(), "input", "pytest")
        os.makedirs(input_dir)

        copy_tree(os.path.abspath(os.path.join(__file__, "..", "..", "..", "input", "pytest")), input_dir)

        # Enrolling test dataset with one image
        enroll_result = runner.invoke(enroll, [dataset, '--no-cuda', "--debug"])
        assert enroll_result.exit_code == 0

        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Running export command with variable date as argument, using only dataset input/pytest in debug mode.
        export_result = runner.invoke(export, [date, "-d", dataset, "--debug"])
        assert export_result.exit_code == 0

        output_file = os.path.join(os.getcwd(), "output", f"{date}.csv")

        # Read the contents of the output file
        with open(output_file, 'r', encoding="utf-8") as f:
            output = f.read()

        # Compare the output to a known good reference
        assert "input/pytest,1.jpg,1024,1024" in output

# Test that the command handles invalid or missing arguments correctly
def test_export_handles_errors():
    runner = CliRunner()
    result = runner.invoke(export)
    assert result.exit_code == 2  # exit code 2 indicates a user error
    assert "Error: Missing argument 'FILE_NAME'." in result.output
