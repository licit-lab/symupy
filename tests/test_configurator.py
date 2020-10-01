"""
    Unit tests for symupy.utils.configurator 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform
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
    return CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]

def test_default_configurator_constructor(symuvia_library_path):
    config = Configurator()
    # Checks default parameters
    assert len(config.bufferString) == CT.BUFFER_STRING
    assert config.libraryPath == symuvia_library_path
    assert config.traceFlow == CT.TRACE_FLOW
    assert config.totalSteps == CT.TOTAL_SIMULATION_STEPS
    assert config.stepLaunchMode == CT.LAUNCH_MODE
