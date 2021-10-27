"""Unit tests for symupy.utils.configurator 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import symupy.utils.constants as CT
from symupy.utils.configurator import Configurator

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return CT.DEFAULT_PATH_SYMUFLOW


def test_default_configurator_constructor(symuvia_library_path):
    config = Configurator()
    # Checks default parameters
    assert len(config.buffer_string.raw) == CT.BUFFER_STRING
    assert config.library_path == symuvia_library_path
    assert config.trace_flow == CT.TRACE_FLOW
    assert config.total_steps == CT.TOTAL_SIMULATION_STEPS
    assert config.step_launch_mode == CT.LAUNCH_MODE
