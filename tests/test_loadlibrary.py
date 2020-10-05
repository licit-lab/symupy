"""
    Unit tests for loading library on python 

    Tests here are just to verify that solution of the platform is correctly loading
    
    Important: Define SYMUVIALIB as a an environment variable
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from symupy.utils.constants import DCT_DEFAULT_PATHS


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import platform
import pytest
from ctypes import cdll

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return DCT_DEFAULT_PATHS[("symuvia", platform.system())]


def test_loadlibrary(symuvia_library_path):
    try:
        simulator = cdll.LoadLibrary(symuvia_library_path)
    except OSError:
        simulator = 1
    assert simulator != 1
