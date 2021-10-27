"""
    Unit tests for symupy.api.connector 
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.runtime.api import Simulation, Simulator
from symupy.utils.constants import DEFAULT_PATH_SYMUFLOW

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return DEFAULT_PATH_SYMUFLOW


@pytest.fixture
def bottleneck_001():
    file_name = "bottleneck_001.xml"
    file_path = ("tests", "mocks", "bottlenecks", file_name)
    return os.path.join(os.getcwd(), *file_path)


@pytest.fixture
def bottleneck_002():
    file_name = "bottleneck_002.xml"
    file_path = ("tests", "mocks", "bottlenecks", file_name)
    return os.path.join(os.getcwd(), *file_path)


# ============================================================================
# BOTTLENECK 001
# ============================================================================


def test_load_bottleneck_001(bottleneck_001):
    sim_case = Simulation(bottleneck_001)
    assert sim_case.filename() == bottleneck_001


def test_constructor_bottleneck_001(bottleneck_001, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_001, symuvia_library_path)
    sim_instance.load_symuvia()
    valid = sim_instance.load_network()
    assert valid == 1


def test_run_bottleneck_001(bottleneck_001, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_001, symuvia_library_path)
    sim_instance.run()


def test_runbystep_bottleneck_001(bottleneck_001, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_001, symuvia_library_path)
    with sim_instance as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False


# ============================================================================
# BOTTLENECK 002
# ============================================================================


def test_load_bottleneck_002(bottleneck_002):
    sim_case = Simulation(bottleneck_002)
    assert sim_case.filename() == bottleneck_002


def test_constructor_bottleneck_002(bottleneck_002, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_002, symuvia_library_path)
    sim_instance.load_symuvia()
    valid = sim_instance.load_network()
    assert valid == 1


def test_run_bottleneck_002(bottleneck_002, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_002, symuvia_library_path)
    sim_instance.run()


def test_runbystep_bottleneck_002(bottleneck_002, symuvia_library_path):
    sim_instance = Simulator.from_path(bottleneck_002, symuvia_library_path)
    with sim_instance as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False
