"""
    Unit tests for Simulator 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import platform, os
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
def symuvia_library_path():
    return DCT_DEFAULT_PATHS[("symuvia", platform.system())]


@pytest.fixture
def bottleneck_001():
    file_name = "bottleneck_001.xml"
    file_path = ("tests", "mocks", "bottlenecks", file_name)
    return os.path.join(os.getcwd(), *file_path)


def test_load_bottleneck_001(bottleneck_001):
    sim_case = Simulation(bottleneck_001)
    assert sim_case.filename == bottleneck_001


def test_constructor_bottleneck_001(bottleneck_001, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_001, symuvia_library_path)
    sim_instance.casename == bottleneck_001
