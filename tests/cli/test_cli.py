"""
    Unit tests for symupy.cli
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest
from click.testing import CliRunner

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.cli.cli import main

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_main(runner):
    """ Run: general"""
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_cli_main_help(runner):
    """ Run: symupy --help """
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_main_launch(runner):
    """ Run: symupy launch --help """
    result = runner.invoke(main, ["launch", "--help"])
    assert result.exit_code == 0


def test_main_analyze(runner):
    """ Run: symupy analyze --help """
    result = runner.invoke(main, ["analyze", "--help"])
    assert result.exit_code == 0
