"""
    Unit tests for symupy.components.vehicles.models
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils import SimulatorRequest
from symupy.components.vehicles import Vehicle, VehicleList

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def simrequest():
    return SimulatorRequest()


@pytest.fixture
def one_vehicle_xml():
    """ Emulates a XML response for 1 vehicle trajectory"""
    STREAM = b'<INST nbVeh="1" val="2.00"><CREATIONS><CREATION entree="Ext_In" id="1" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="25.00" acc="0.00" dst="25.00" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def one_vehicle_forced_xml():
    """ Emulates a XML response for 1 vehicle forced trajectory"""
    STREAM = b'<INST nbVeh="1" val="3.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="48.00" acc="-2.00" dst="48.00" etat_pilotage="force (ecoulement respecte)" id="0" ord="0.00" tron="Zone_001" type="VL" vit="23.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def two_vehicle_one_forced_xml():
    """ Emulates a XML response for 1 vehicle forced amont 2 trajectories"""
    STREAM = b'<INST nbVeh="1" val="3.00"><CREATIONS><CREATION entree="Ext_In" id="2" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="50.00" acc="0.00" dst="50.00" etat_pilotage="force (ecoulement respecte)" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="19.12" acc="0.00" dst="19.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def two_vehicle_xml():
    """ Emulates  a XML response for 2 vehicle trajectories"""
    STREAM = b'<INST nbVeh="2" val="4.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="75.00" acc="0.00" dst="75.00" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="44.12" acc="0.00" dst="44.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


def test_create_default_vehicle(simrequest):
    v = Vehicle(simrequest)
    assert v.abscissa == 0.0


def test_create_specific_vehicle(simrequest, one_vehicle_xml):
    simrequest.query = one_vehicle_xml
    d = simrequest.get_vehicle_data()[0]
    v = Vehicle(simrequest, **d)
    assert v.distance == 25.00
    assert v.driven == False


def test_create_specific_driven_vehicle(simrequest, one_vehicle_forced_xml):
    simrequest.query = one_vehicle_forced_xml
    d = simrequest.get_vehicle_data()[0]
    v = Vehicle(simrequest, **d)
    assert v.distance == 48.00
    assert v.driven == True


def test_create_update_vehicle_state(simrequest, one_vehicle_xml):
    v = Vehicle(simrequest)
    assert v.distance == 0.00
    simrequest.query = one_vehicle_xml
    assert v.distance == 25.00


def test_create_2_update_vehicle_states(simrequest, two_vehicle_one_forced_xml):
    v1 = Vehicle(simrequest, vehid=0)
    v2 = Vehicle(simrequest, vehid=1)
    assert v1.distance == 0.0
    assert v2.distance == 0.0
    simrequest.query = two_vehicle_one_forced_xml
    assert v1.distance == 50.00
    assert v2.distance == 19.12


def test_create_vehicle_list_empty(simrequest):
    vl = VehicleList(simrequest)
    assert len(vl) == 0


def test_create_vehicle_list_1_vehicle(simrequest, one_vehicle_xml):
    simrequest.query = one_vehicle_xml
    vl = VehicleList(simrequest)
    assert len(vl) == 1


def test_create_vehicle_list_2_vehicles(simrequest, two_vehicle_one_forced_xml):
    simrequest.query = two_vehicle_one_forced_xml
    vl = VehicleList(simrequest)
    assert len(vl) == 2


def test_create_vehicle_list_1_vehicle_update(
    simrequest, one_vehicle_xml, one_vehicle_forced_xml
):
    simrequest.query = one_vehicle_xml
    vl = VehicleList(simrequest)
    assert len(vl) == 1
    assert vl[0].distance == 25.00
    simrequest.query = one_vehicle_forced_xml
    assert len(vl) == 1
    assert vl[0].distance == 48.00


def test_create_vehicle_list_2_vehicles_gradual_update(
    simrequest, one_vehicle_xml, two_vehicle_xml
):
    simrequest.query = one_vehicle_xml
    vl = VehicleList(simrequest)
    assert len(vl) == 1
    assert vl[0].distance == 25.00
    simrequest.query = two_vehicle_xml
    vl.update_list()
    assert len(vl) == 2
    assert vl[0].distance == 75.00
    assert vl[1].distance == 44.12
