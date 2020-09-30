"""
    Unit tests for symupy.utils.constants 

    Tests here are just to verify that solution of the platform is the right one and verify the existance of the platform in the system
    
    Important: Define SYMUVIALIB as a an environment variable
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


import os
from pathlib import Path
import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.constants import DCT_DEFAULT_PATHS
from symupy.api import Simulation, Simulator

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def env_path_default():
    path_env = os.environ.get("SYMUVIALIB")
    return path_env


def test_environment_variable(env_path_default):
    assert Path(env_path_default).exists() == True


def test_detection_symupy(env_path_default):
    path_symupy = DCT_DEFAULT_PATHS[("symuvia", platform.system())]
    assert Path(path_symupy) == Path(env_path_default)
