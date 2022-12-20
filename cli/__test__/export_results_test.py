from distutils.dir_util import copy_tree
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
    # Create a temporary directory to run the test in
    with runner.isolated_filesystem():
        # Create a directory to store the input images
        input_folder = os.path.join(os.getcwd(), "input", "pytest")
        os.makedirs(input_folder)

        # Copy the test images to the input folder
        copy_tree(os.path.abspath(os.path.join(__file__, "..",
                  "..", "..", "input", "pytest")), input_folder)

        # Run the enrollment command to create the enrollment data
        enroll_result = runner.invoke(enroll, [input_folder])

        # Check that the enrollment command completed successfully
        assert "Enrollment finished!" in enroll_result.output
        assert enroll_result.exit_code == 0

        # Create a directory to store the output data
        output_folder = os.path.abspath(os.path.join(os.getcwd(), "output"))

        # Run the search command again to check that the output is not overwritten
        search_result = runner.invoke(
            search, [input_folder, "-d", input_folder, '--export'])

        assert search_result.exit_code == 0
        assert os.path.exists(output_folder)

# Temporary disabled

# def test_search_export_no_match(runner: CliRunner):
#     # Create test folder with fake images
#     with runner.isolated_filesystem():
#         input_folder = os.path.join(os.getcwd(), "input", "pytest")
#         os.makedirs(input_folder)

#         copy_tree(os.path.abspath(os.path.join(__file__, "..",
#                   "..", "..", "input", "pytest")), input_folder)

#         result = runner.invoke(enroll, ['input/pytest'])

#         assert "Enrollment finished!" in result.output
#         assert result.exit_code == 0

#         no_match_folder = os.path.join(os.getcwd(), "input", "no_match")
#         os.makedirs(no_match_folder)

#         result = runner.invoke(
#             search, ['input/no_match', "-d", "input/pytest", '--export'])

#         assert "No matches found" in result.output
