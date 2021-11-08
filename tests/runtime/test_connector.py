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

from symupy.runtime.api import Simulation, Simulator
import symupy.utils.constants as CT

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return CT.DEFAULT_PATH_SYMUFLOW


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
    assert simulator.library_path == symuvia_library_path


def test_load_symuvia_via_api(symuvia_library_path):
    simulator = Simulator(library_path=symuvia_library_path)
    simulator.load_symuvia()
    assert simulator.library_path == symuvia_library_path


# ============================================================================
# BOTTLENECK 001
# ============================================================================


def test_load_bottleneck_001(bottleneck_001):
    symuflow = Simulation(bottleneck_001)
    assert symuflow.filename() == bottleneck_001


def test_default_load_constructor_bottleneck_001(bottleneck_001):
    symuflow = Simulator()
    symuflow.register_simulation(bottleneck_001)
    symuflow.load_symuvia()
    valid = symuflow.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_001, symuvia_library_path)
    symuflow.load_symuvia()
    valid = symuflow.load_network()
    assert valid == 1


def test_run_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_001, symuvia_library_path)
    symuflow.run()


def test_runbystep_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_001, symuvia_library_path)
    with symuflow as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False


def test_create_vehicle_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_001, symuvia_library_path)

    symuflow._set_manual_initialization()
    veh_id = symuflow.create_vehicle("VL", "Ext_In", "Ext_Out")

    assert veh_id == 0


def test_create_drive_vehicle_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator(library_path=symuvia_library_path, step_launch_mode="full")
    symuflow.register_simulation(bottleneck_001)

    with symuflow as s:
        while s.do_next:
            s.request_answer()  # Initialize
            s.request_answer()  # Vehicle 0

            # Vehicle instantiation
            veh_id = s.create_vehicle("VL", "Ext_In", "Ext_Out")
            force_driven = s.request.is_vehicle_driven("1")
            s.request_answer()

            # Data retrieveal
            drive_status = s.drive_vehicle(veh_id, 20.0, "Zone_001")
            force_driven = s.request.is_vehicle_driven(1)
            position = s.request.filter_vehicle_property("distance", 1)[0]

            s.stop_step()

        assert force_driven == True
        assert veh_id >= 0
        assert float(position) == pytest.approx(20.0)
        # assert drive_status == 4 # This depends on the OS


def test_drive_vehicle_bottleneck_001(bottleneck_001, symuvia_library_path):
    symuflow = Simulator(library_path=symuvia_library_path, step_launch_mode="full")
    symuflow.register_simulation(bottleneck_001)

    with symuflow as s:
        while s.do_next:
            s.run_step()
            if s.request.is_vehicle_in_network(0):
                drive_status = s.drive_vehicle(0, 1.0)
                force_driven = s.request.is_vehicle_driven(0)
                position = s.request.filter_vehicle_property("distance", 0)[0]
                s.stop_step()
            else:
                continue
        assert force_driven == True
        assert float(position) == pytest.approx(1.0)
        # assert drive_status == 6 # This depends on the OS


# ============================================================================
# BOTTLENECK 002
# ============================================================================


def test_load_bottleneck_002(bottleneck_002):
    symuflow = Simulation(bottleneck_002)
    assert symuflow.filename() == bottleneck_002


def test_default_load_constructor_bottleneck_002(bottleneck_002):
    symuflow = Simulator()
    symuflow.register_simulation(bottleneck_002)
    symuflow.load_symuvia()
    valid = symuflow.load_network()
    assert valid == 1


def test_load_constructor_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_002, symuvia_library_path)
    symuflow.load_symuvia()
    valid = symuflow.load_network()
    assert valid == 1


def test_run_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_002, symuvia_library_path)
    symuflow.run()


def test_runbystep_bottleneck_002(bottleneck_002, symuvia_library_path):
    symuflow = Simulator.from_path(bottleneck_002, symuvia_library_path)
    with symuflow as s:
        while s.do_next:
            s.run_step()
        assert s.do_next == False
