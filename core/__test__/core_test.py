from click.testing import CliRunner
from cli.ag import enroll


def test_enrollment_folder():
    runner = CliRunner()
    result = runner.invoke(enroll, ['../../input/test'])
    assert "Enrollment finished" in result.output
    assert result.exit_code == 0
