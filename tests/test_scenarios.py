"""
    Unit tests for symupy.runtime.scenario 
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

from symupy.runtime.api import Simulation, Simulator
import symupy.utils.constants as CT
from symupy.utils.constants import TRACE_FLOW

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def symuvia_library_path():
    return CT.DCT_DEFAULT_PATHS[("symuflow", platform.system())]


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


def get_simulation_data_bottleneck_001(bottleneck_001):
    scenario = Simulation(bottleneck_001)
    sim_param = scenario.get_simulation_parameters()
    PAR = (
        {
            "id": "simID",
            "pasdetemps": "1",
            "debut": "00:00:00",
            "fin": "00:00:30",
            "loipoursuite": "exacte",
            "comportementflux": "iti",
            "date": "1985-01-17",
            "titre": "",
            "proc_deceleration": "false",
            "seed": "1",
        },
        {
            "id": "simID2",
            "pasdetemps": "1",
            "debut": "00:00:00",
            "fin": "00:00:30",
            "loipoursuite": "exacte",
            "comportementflux": "iti",
            "date": "1985-01-17",
            "titre": "",
            "proc_deceleration": "false",
            "seed": "1",
        },
    )
    assert sim_param == PAR


def test_get_vehicletype_data_bottleneck_001(bottleneck_001):
    scenario = Simulation(bottleneck_001)
    sim_vehtype = scenario.get_vehicletype_information()
    VEH_TYPE = (
        {"id": "VL", "w": "-5.8823", "kx": "0.17", "vx": "25"},
        {"id": "VL2", "w": "-5.8823", "kx": "0.17", "vx": "25"},
    )
    sim_vehtype == VEH_TYPE


def test_get_network_endpoints_botleneck_001(bottleneck_001):
    scenario = Simulation(bottleneck_001)
    sim_endpoints = scenario.get_network_endpoints()
    END_POINTS = ("Ext_In", "Ext_Out")
    sim_endpoints == END_POINTS
