"""
    Unit tests for symupy.api.connector 
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import unittest
import platform
import pytest
from ctypes import create_string_buffer

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.api import Simulation, Simulator, Configurator
import symupy.utils.constants as CT
from symupy.utils.constants import TRACE_FLOW

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


def test_configurator_constructor(symuvia_library_path):
    config = Configurator()
    # Checks default parameters
    assert len(config.bufferString) == CT.BUFFER_STRING
    assert config.libraryPath == symuvia_library_path
    assert config.traceFlow == CT.TRACE_FLOW
    assert config.totalSteps == CT.TOTAL_SIMULATION_STEPS
    assert config.stepLaunchMode == CT.LAUNCH_MODE


# ============================================================================
# BOTTLENECK 001
# ============================================================================


def test_load_bottleneck_001(bottleneck_001):
    sim_case = Simulation(bottleneck_001)
    assert sim_case.filename() == bottleneck_001


def test_default_load_constructor_bottleneck_001(bottleneck_001):
    simulator = Simulator()
    simulator.register_simulation(bottleneck_001)
    simulator.load_symuvia()
    valid = simulator.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_001(bottleneck_001, symuvia_library_path):
    simulator = Simulator.from_path(bottleneck_001, symuvia_library_path)
    simulator.load_symuvia()
    valid = simulator.load_network()
    assert valid == 1


def test_run_bottleneck_001(bottleneck_001, symuvia_library_path):
    simulator = Simulator.from_path(bottleneck_001, symuvia_library_path)
    simulator.run()


def test_runbystep_bottleneck_001(bottleneck_001, symuvia_library_path):
    simulator = Simulator.from_path(bottleneck_001, symuvia_library_path)
    with simulator as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False


# ============================================================================
# BOTTLENECK 002
# ============================================================================


def test_load_bottleneck_002(bottleneck_002):
    sim_case = Simulation(bottleneck_002)
    assert sim_case.filename() == bottleneck_002


def test_default_load_constructor_bottleneck_001(bottleneck_001):
    simulator = Simulator()
    simulator.register_simulation(bottleneck_001)
    simulator.load_symuvia()
    valid = simulator.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_002(bottleneck_002, symuvia_library_path):
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
