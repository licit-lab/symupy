"""
    Unit tests for loading library on python 

    Tests here are just to verify that solution of the platform is correctly loading
    
    Important: Define SYMUVIALIB as a an environment variable
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import cdll
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.constants import DEFAULT_PATH_SYMUFLOW

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return DEFAULT_PATH_SYMUFLOW


def test_loadlibrary(symuvia_library_path):
    try:
        simulator = cdll.LoadLibrary(symuvia_library_path)
    except OSError:
        simulator = 1
    assert simulator != 1
