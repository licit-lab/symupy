""" This module computes/modifies data for XML creation for the simulator 
"""
from lxml import etree as ET
from .constants import (
    DCT_SIMULATION_INFO,
    DCT_EXPORT_INFO,
    DCT_TRAFIC_INFO,
    DCT_NETWORK_INFO,
    DCT_SCENARIO_INFO,
)


def create_DCT_SIMULATION_INFO(
    title: str,
    simid: str,
    timestep: float,
    time_start: str,
    time_end: str,
    date: str,
    seed: int,
    cfl: str,
    flow: str,
    decel: bool,
) -> dict:
    """Computes dictionary DCT_SIMULATION_INFO header for XML file

    :param title: Simulation title
    :type title: str
    :param simid: Simulation ID
    :type simid: str
    :param timestep: time step (seconds)
    :type timestep: float
    :param time_start: start time H%:%M:%S
    :type time_start: str
    :param time_end: start time H%:%M:%S
    :type time_end: str
    :param date: simulation date Y%-%m-%d
    :type date: str
    :param seed: random seed
    :type seed: int
    :param cfl: car following law
    :type cfl: str
    :param flow: flow behaviour
    :type flow: str
    :param decel: deceleration procedure activation
    :type decel: bool
    :return: dictionary with metadata for xml creation
    :rtype: dict
    """
    DCT_SIMULATION_INFO.update({"id": f"{simid}"})
    DCT_SIMULATION_INFO.update({"pasdetemps": f"{str(timestep)}"})
    DCT_SIMULATION_INFO.update({"debut": f"{time_start}"})
    DCT_SIMULATION_INFO.update({"fin": f"{time_end}"})
    DCT_SIMULATION_INFO.update({"loipoursuite": f"{cfl}"})
    DCT_SIMULATION_INFO.update({"comportementflux": f"{flow}"})
    DCT_SIMULATION_INFO.update({"date": f"{date}"})
    DCT_SIMULATION_INFO.update({"titre": f"{title}"})
    DCT_SIMULATION_INFO.update({"proc_deceleration": f"{str(decel).lower()}"})
    DCT_SIMULATION_INFO.update({"seed": f"{str(seed)}"})

    return DCT_SIMULATION_INFO


def create_DCT_NETWORK_INFO(networkid: str) -> dict:
    """Computes dictionary DCT_NETWORK_INFO for XML file

    :param networkid: network identifier
    :type networkid: str
    :return: dict
    :rtype: [type]
    """
    DCT_NETWORK_INFO.update({"id": networkid})
    return DCT_NETWORK_INFO


def create_DCT_TRAFIC_INFO(
    trafid: str,
    bounded_acc: bool = True,
    relaxation: float = 4,
    ghost_lanechange: bool = False,
) -> dict:
    """Computes dictionary DCT_TRAFIC_INFO for XML file

    :param trafid: traffic identifier
    :type trafid: str
    :param bounded_acc: bounds acceleration True/False
    :type bounded_acc: bool
    :param relaxation: relaxation coefficient lane change
    :type relaxation: float
    :param ghost_lanechange: keep lane change ghost True/False
    :type ghost_lanechange: bool
    :return: dictionary with metadata for xml creation
    :rtype: dict
    """
    DCT_TRAFIC_INFO.update({"id": str(trafid)})
    DCT_TRAFIC_INFO.update({"accbornee": str(bounded_acc)})
    DCT_TRAFIC_INFO.update({"coeffrelax": str(relaxation)})
    DCT_TRAFIC_INFO.update({"chgtvoie_ghost": str(ghost_lanechange)})
    return DCT_TRAFIC_INFO


def create_DCT_EXPORT_INFO(
    trace_rout: bool = False, trajectories: bool = True, csv: bool = True
) -> dict:
    """Computes dictionary DCT_SCENARIO_INFO for XML file

    :param trace_rout: trace routes True/False
    :type trace_rout: bool
    :param trajectories: export trajectories True/False
    :type trajectories: bool
    :param csv: export trajectories in csv
    :type csv: bool
    :return: dictionary with metadata for xml creation
    :rtype: dict
    """
    DCT_EXPORT_INFO.update({"trace_route": str(trace_rout).lower()})
    DCT_EXPORT_INFO.update({"trajectoires": str(trajectories).lower()})
    DCT_EXPORT_INFO.update({"csv": str(csv).lower()})
    return DCT_EXPORT_INFO


def create_DCT_SCENARIO_INFO(
    scnid: str,
    dirout: str,
    prefout: str,
    dct_sim: dict,
    dct_traffic: dict,
    dct_network: dict,
) -> dict:
    """Computes dictionary DCT_SCENARIO_INFO for XML file

    :param scnid: Scenario identifier
    :type scnid: str
    :param dirout: Output directory
    :type dirout: str
    :param prefout: Prefix
    :type prefout: str
    :param dct_sim: DCT_SIMULATION_INFO
    :type dct_sim: dict
    :param dct_traffic: DCT_TRAFIC_INFO
    :type dct_traffic: dict
    :param dct_network: DCT_NETWORK_INFO
    :type dct_network: dict
    :return: dictionary with metadata for xml creation
    :rtype: dict
    """
    DCT_SIMULATION_INFO.update({"id": f"{scnid}"})
    DCT_SIMULATION_INFO.update({"simulation_id": f"{dirout}"})
    DCT_SIMULATION_INFO.update({"trafic_id": f"{prefout}"})
    DCT_SIMULATION_INFO.update({"reseau_id": f"{dct_sim.get('id')}"})
    DCT_SIMULATION_INFO.update({"dirout": f"{dct_traffic.get('id')}"})
    DCT_SIMULATION_INFO.update({"prefout": f"{dct_network.get('id')}"})
    return DCT_SCENARIO_INFO


def fix_values(element: ET.ElementTree, dct_values: dict) -> ET.ElementTree:
    """Fix a set of values within a dictionary as attributes of an XML subelement

    :param element: XML tree element
    :type element: ET.ElementTree
    :param dct_values: attributes to fix
    :type dct_values: dict
    :return: Tranformed XML tree element
    :rtype: ET.ElementTree
    """
    for k, v in dct_values.items():
        element.set(k, v)
    return element


class XMLGenerator(object):
    """A class to handle XML generator for SymuFlow"""

    xmlns = "http://www.w3.org/2001/XMLSchema-instance"
    namespace = "noNamespaceSchemaLocation"
    nsmap = {"xsi": xmlns}

    def __init__(self, path_xsd: str = ""):
        # Create a general scheme
        attr_qname = ET.QName(self.xmlns, self.namespace)
        self.root = ET.Element(
            "ROOT_SYMUBRUIT",
            {attr_qname: "reseau.xsd"},
            version="2.05",
            nsmap=self.nsmap,
        )
