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


def test_search_export_success(runner: CliRunner):
    # Create test folder with fake images
    pass
