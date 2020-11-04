"""Unit tests for symupy.utils.constants

    Tests here are just to verify that solution of the platform is the right
    one and verify the existance of the platform in the system
    
    Important: Define SYMUVIALIB as a an environment variable
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================


import os
from pathlib import Path
import platform
import pytest
from decouple import config

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.constants import DEFAULT_PATH_SYMUVIA

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def env_path_default():
    path_env = DEFAULT_PATH_SYMUVIA
    return path_env


def test_environment_variable(env_path_default):
    assert Path(env_path_default).exists() == True


def test_detection_default_symupy(env_path_default):
    DEFAULT_LIB_LINUX = config("DEFAULT_LIB_LINUX")
    DEFAULT_LIB_WINDOWS = config("DEFAULT_LIB_WINDOWS")
    DEFAULT_LIB_OSX = config("DEFAULT_LIB_OSX")
    assert env_path_default in (
        DEFAULT_LIB_LINUX,
        DEFAULT_LIB_WINDOWS,
        DEFAULT_LIB_OSX,
    )
    assert Path(env_path_default).exists()
