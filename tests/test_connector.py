"""
    Unit tests for symupy.api.connector 
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.api import Simulation, Simulator
import symupy.utils.constants as CT

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return CT.DCT_DEFAULT_PATHS[("symuvia", platform.system())]


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
# GENERAL API
# ============================================================================


def test_load_default_symuvia_via_api(symuvia_library_path):
    simulator = Simulator()
    assert simulator.libraryPath == symuvia_library_path


def test_load_symuvia_via_api(symuvia_library_path):
    simulator = Simulator(libraryPath=symuvia_library_path)
    simulator.load_symuvia()
    assert simulator.libraryPath == symuvia_library_path


# ============================================================================
# BOTTLENECK 001
# ============================================================================


def test_load_bottleneck_001(bottleneck_001):
    symuvia = Simulation(bottleneck_001)
    assert symuvia.filename() == bottleneck_001


def test_default_load_constructor_bottleneck_001(bottleneck_001):
    symuvia = Simulator()
    symuvia.register_simulation(bottleneck_001)
    symuvia.load_symuvia()
    valid = symuvia.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_001, symuvia_library_path)
    symuvia.load_symuvia()
    valid = symuvia.load_network()
    assert valid == 1


def test_run_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_001, symuvia_library_path)
    symuvia.run()


def test_runbystep_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_001, symuvia_library_path)
    with symuvia as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False


# ============================================================================
# BOTTLENECK 002
# ============================================================================


def test_load_bottleneck_002(bottleneck_002):
    symuvia = Simulation(bottleneck_002)
    assert symuvia.filename() == bottleneck_002


def test_default_load_constructor_bottleneck_002(bottleneck_002):
    symuvia = Simulator()
    symuvia.register_simulation(bottleneck_002)
    symuvia.load_symuvia()
    valid = symuvia.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_002, symuvia_library_path)
    symuvia.load_symuvia()
    valid = symuvia.load_network()
    assert valid == 1


def test_run_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_002, symuvia_library_path)
    symuvia.run()


def test_runbystep_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuvia = Simulator.from_path(bottleneck_002, symuvia_library_path)
    with symuvia as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False
