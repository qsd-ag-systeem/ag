from pathlib import Path
from click.testing import CliRunner
from cli.ag import enroll, search
import os


def test_search_export_fails():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(search, ['--export'])

        assert result.exit_code == 2
        assert "Usage: search [OPTIONS] FOLDER" in result.output


def test_search_creates_output_folder():
    runner = CliRunner()

    with runner.isolated_filesystem():
        Path('input/tests').mkdir(parents=True, exist_ok=True)
        with open('input/tests/test1.jpg', 'w') as f:
            f.write('test')
        with open('input/tests/test2.png', 'w') as f:
            f.write('test')
        with open('input/tests/test3.jpeg', 'w') as f:
            f.write('test')

        output_folder = Path(os.path.join(os.path.curdir, "output"))

        runner.invoke(enroll, ['exists'])
        runner.invoke(search, ['exists', '--export'])

        assert os.path.exists(output_folder)
