import pytest
from symupy.runtime.monitor.monitors import *
from symupy.parser.xmlparser import XMLTrajectory


_test_string_0 = b'''<INST nbVeh="3" val="6.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="843554.88" acc="2.00" deltaN="1.00" dst="43.56" id="0" lead="-1" ord="6519864.04" tron="Rue_Crequi_SN_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843559.27" acc="0.00" deltaN="1.00" dst="17.41" id="1" lead="0" ord="6519838.26" tron="Rue_Crequi_SN_1" type="VL" vit="99.00" voie="1" z="0.00"/><TRAJ abs="843163.80" acc="0.00" deltaN="1.00" dst="19.01" id="2" lead="-1" ord="6519886.77" tron="Cr_Lafayette_OE_1" type="VL" vit="14.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="E_Corneille" nb_veh_en_attente="0"/><ENTREE id="E_Crequi_S" nb_veh_en_attente="0"/><ENTREE id="E_Duguesclin_N" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_E" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_O" nb_veh_en_attente="0"/><ENTREE id="E_Moliere_S" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_N" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_S" nb_veh_en_attente="0"/><ENTREE id="E_Vendome_N" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'''
_test_string_1 = b'''<INST nbVeh="3" val="7.00"><CREATIONS><CREATION entree="E_Duguesclin_N" id="3" sortie="S_Duguesclin_S" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="843552.53" acc="0.00" deltaN="1.00" dst="57.56" id="0" lead="-1" ord="6519877.84" tron="Rue_Crequi_SN_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843556.92" acc="0.00" deltaN="1.00" dst="31.41" id="1" lead="0" ord="6519852.06" tron="Rue_Crequi_SN_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843177.80" acc="0.00" deltaN="1.00" dst="33.01" id="2" lead="-1" ord="6519887.01" tron="Cr_Lafayette_OE_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843630.04" acc="0.00" deltaN="1.00" dst="3.61" id="3" lead="-1" ord="6520018.11" tron="Rue_Duguesclin_NS_1" type="VL" vit="14.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="E_Corneille" nb_veh_en_attente="0"/><ENTREE id="E_Crequi_S" nb_veh_en_attente="0"/><ENTREE id="E_Duguesclin_N" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_E" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_O" nb_veh_en_attente="0"/><ENTREE id="E_Moliere_S" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_N" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_S" nb_veh_en_attente="0"/><ENTREE id="E_Vendome_N" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'''
_test_string_2 = b'''<INST nbVeh="4" val="8.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="843550.39" acc="0.00" deltaN="1.00" dst="3.18" id="0" lead="-1" ord="6519891.67" tron="CAF_Laf_Crequi_D0_Rue_Crequi_SN_1_Div_CAF_Laf_Crequi_2" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843554.57" acc="0.00" deltaN="1.00" dst="45.41" id="1" lead="0" ord="6519865.86" tron="Rue_Crequi_SN_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843191.79" acc="0.00" deltaN="1.00" dst="47.01" id="2" lead="-1" ord="6519887.25" tron="Cr_Lafayette_OE_1" type="VL" vit="14.00" voie="1" z="0.00"/><TRAJ abs="843632.46" acc="0.00" deltaN="1.00" dst="17.61" id="3" lead="-1" ord="6520004.32" tron="Rue_Duguesclin_NS_1" type="VL" vit="14.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="E_Corneille" nb_veh_en_attente="0"/><ENTREE id="E_Crequi_S" nb_veh_en_attente="0"/><ENTREE id="E_Duguesclin_N" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_E" nb_veh_en_attente="0"/><ENTREE id="E_Lafayette_O" nb_veh_en_attente="0"/><ENTREE id="E_Moliere_S" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_N" nb_veh_en_attente="0"/><ENTREE id="E_Saxe_S" nb_veh_en_attente="0"/><ENTREE id="E_Vendome_N" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'''

def test_monitorVEH_speed():
    monitor = SymuFlowMonitorVEH([0,1], "speed")
    res = monitor.update(6, XMLTrajectory(_test_string_0), 0)
    assert res == (6, 14)
    res = monitor.update(6, XMLTrajectory(_test_string_0), 1)
    assert res == (6, 99)


def test_monitorVEH_acc():
    monitor = SymuFlowMonitorVEH([0,1], "acceleration")
    res = monitor.update(6, XMLTrajectory(_test_string_0), 0)
    assert res == (6, 2)
    res = monitor.update(6, XMLTrajectory(_test_string_0), 1)
    assert res == (6, 0)


def test_monitorVEH_distance():
    monitor = SymuFlowMonitorVEH([0,1], "distance")
    res = monitor.update(6, XMLTrajectory(_test_string_0), 0)
    assert res == (6, 0)
    res = monitor.update(6, XMLTrajectory(_test_string_1), 0)
    assert res == (6, 13.998660650031834)


def test_monitorMFD():
    monitor = SymuFlowMonitorMFD()
    res = monitor.update(6, XMLTrajectory(_test_string_0), None)
    assert res == (3, 127.0)


def test_monitorAccumulation():
    monitor = SymuFlowMonitorAccumulation()
    res = monitor.update(6, XMLTrajectory(_test_string_0), None)
    assert res == (6, 3)


def test_monitorTTT():
    monitor = SymuFlowMonitorTTT(['Rue_Crequi_SN_1'])
    res = monitor.update(6, XMLTrajectory(_test_string_0), None)
    res = monitor.update(7, XMLTrajectory(_test_string_1), None)
    assert res == (7, 2)


def test_monitorTTD():
    monitor = SymuFlowMonitorTTD(['Rue_Crequi_SN_1'])
    res = monitor.update(6, XMLTrajectory(_test_string_0), None)
    res = monitor.update(7, XMLTrajectory(_test_string_1), None)
    assert res == (7, 27.997321300063668)


def test_monitorFlux():
    monitor = SymuFlowMonitorFlux(['Rue_Duguesclin_NS_1'])
    res = monitor.update(6, XMLTrajectory(_test_string_0), 0)
    res = monitor.update(7, XMLTrajectory(_test_string_1), 0)
    assert res == (7, 1)


def test_monitorFlow():
    monitor = SymuFlowMonitorFlow(['Rue_Duguesclin_NS_1'])
    res = monitor.update(6, XMLTrajectory(_test_string_0), 0)
    assert res == ([843554.88, 843559.27, 843163.8], [6519864.04, 6519838.26, 6519886.77])