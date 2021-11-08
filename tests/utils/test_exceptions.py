"""Test suite for exceptions
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.exceptions import (
    SymupyError,
    SymupyFileLoadError,
    SymupyLoadLibraryError,
    SymupyDriveVehicleError,
    SymupyVehicleCreationError,
    SymupyWarning,
)


def test_symupyerror():
    assert str(SymupyError("Error raised", "a")) == "Error raised with args: a"
    with pytest.raises(SymupyError):
        raise SymupyError("Test Error", "")


def test_symupyloadlibraryerror():
    assert str(SymupyLoadLibraryError("Error raised", "a")) == "Error raised at: a"
    with pytest.raises(SymupyLoadLibraryError):
        raise SymupyLoadLibraryError("Test Error", "")


def test_symupyfileloaderror():
    assert str(SymupyFileLoadError("Error raised", "a")) == "Error raised at: a"
    with pytest.raises(SymupyFileLoadError):
        raise SymupyFileLoadError("Test Error", "")


def test_symupydrivevehicleerror():
    assert str(SymupyDriveVehicleError("Error raised", "a")) == "Error raised at: a"
    with pytest.raises(SymupyDriveVehicleError):
        raise SymupyDriveVehicleError("Test Error", "")


def test_symupyvehiclecreationerror():
    assert str(SymupyVehicleCreationError("Error raised", "a")) == "Error raised at: a"
    with pytest.raises(SymupyVehicleCreationError):
        raise SymupyVehicleCreationError("Test Error", "")


def test_symupywarning():
    SymupyWarning("Test Warning")
    assert True
