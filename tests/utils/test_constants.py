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
import decouple

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.constants import DEFAULT_PATH_SYMUFLOW

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def env_path_default():
    path_env = DEFAULT_PATH_SYMUFLOW
    return path_env


def test_environment_variable(env_path_default):
    assert Path(env_path_default).exists() == True


@pytest.mark.skip(reason="Needs review, probably not required")
def test_detection_default_symupy(env_path_default):

    # Settings.ini location
    ini_config = decouple.Config(os.path.join(os.getcwd(), "..", ""))

    DEFAULT_LIB_LINUX = decouple.config("DEFAULT_LIB_LINUX")
    DEFAULT_LIB_WINDOWS = decouple.config("DEFAULT_LIB_WINDOWS")
    DEFAULT_LIB_OSX = decouple.config("DEFAULT_LIB_OSX")
    assert env_path_default in (
        DEFAULT_LIB_LINUX,
        DEFAULT_LIB_WINDOWS,
        DEFAULT_LIB_OSX,
        DEFAULT_PATH_SYMUVIA,
    )
    assert Path(env_path_default).exists()
