"""
Unit tests for commands
=======================
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest
from click.testing import CliRunner

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.api.commands import NoCommand

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def runner():
    return CliRunner()


def test_no_command(runner):
    NoCommand().execute()
