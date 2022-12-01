from click.testing import CliRunner

from cli.ag import setup, enroll


# def test_setup():
#     runner = CliRunner()
#     result = runner.invoke(setup)
#     assert result.exit_code == 0


def test_enrollment_folder():
    runner = CliRunner()
    result = runner.invoke(enroll, ['../../input/test'])
    assert "Enrollment finished" in result.output
    assert result.exit_code == 0
