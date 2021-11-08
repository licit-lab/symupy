"""
**Scenario Module**

    This module contains descriptions that stablish a traffic scenario. A traffic scenario 
    is regularly described by a simulation object that points towards properties of the simulator. 
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
from lxml import etree
from datetime import datetime

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.utils.exceptions import SymupyFileLoadError
from symupy.utils.constants import HOUR_FORMAT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Simulation(object):
    def __init__(self, file_name: str) -> None:
        if os.path.exists(file_name):
            self._file_name = file_name
            self.load_xml_tree()
        else:
            raise SymupyFileLoadError("File not found", file_name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.filename()})"

    def load_xml_tree(self) -> None:
        """Load XML file_name"""
        # TODO: Add validation with DTD
        tree = etree.parse(self._file_name)
        root = tree.getroot()
        self._xml_tree = root

    @property
    def xmltree(self):
        return self._xml_tree

    @xmltree.setter
    def xmltree(self, rootxml):
        self._xml_tree = rootxml

    def get_simulation_parameters(self) -> tuple:
        """Get simulation parameters

        :return: tuple with XML dictionary containing parameters
        :rtype: tuple
        """
        branch_tree = "SIMULATIONS"
        sim_params = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(par.attrib for par in sim_params)

    def get_vehicletype_information(self) -> tuple:
        """Get the vehicle parameters

        :return: tuple of dictionaries containing vehicle parameters
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/TYPES_DE_VEHICULE"
        vehicle_types = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(v.attrib for v in vehicle_types)

    def get_network_endpoints(self) -> tuple:
        """Get networks endpoint names

        :return: tuple containing endpoint names
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/EXTREMITES"
        end_points = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(ep.attrib["id"] for ep in end_points)

    def get_network_links(self) -> tuple:
        """Get network link names

        :return: tuple containing link names
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/TRONCONS"
        links = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(ep.attrib["id"] for ep in links)

    def get_simulation_steps(self, simid: int = 0) -> range:
        """Get simulation steps for an simulation. specify the simulation id  via an integer value

        :param simid: simulation id , defaults to 0
        :type simid: int, optional
        :return:
        :rtype: range
        """
        t1 = datetime.strptime(
            self.get_simulation_parameters()[simid].get("debut"), HOUR_FORMAT
        )
        t2 = datetime.strptime(
            self.get_simulation_parameters()[simid].get("fin"), HOUR_FORMAT
        )
        t = t2 - t1
        n = t.seconds / float(self.get_simulation_parameters()[simid].get("pasdetemps"))
        return range(int(n))

    def get_mfd_sensor_names(self) -> tuple:
        """Get MFD sensors defined for a specific simulation

        :return: tuple of MFD sensors in the network
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/PARAMETRAGE_CAPTEURS/CAPTEURS"
        sensors = self.xmltree.xpath(branch_tree)[0].getchildren()
        return tuple(sn.attrib["id"] for sn in sensors)

    def get_links_in_mfd_sensor(self, sensor_id: str) -> tuple:
        """Get links associated to a particular MFD sensor for a specific simulation

        :param sensor_id: Sensor id
        :type sensor_id: str
        :return: tuple of strings with links covered by the sensor
        :rtype: tuple
        """
        branch_tree = "TRAFICS/TRAFIC/PARAMETRAGE_CAPTEURS/CAPTEURS"
        sensors = self.xmltree.xpath(branch_tree)[0].getchildren()
        try:
            sensor_element = sensors[self.get_mfd_sensor_names().index(sensor_id)]
            links = sensor_element.getchildren()[0].getchildren()
            return tuple(lk.attrib["id"] for lk in links)
        except:
            return ()

    def __contains__(self, value: tuple) -> bool:
        # REVIEW: Implement? in method? maybe useful
        raise NotImplementedError

    def filename(self, encoding: str = None):
        """
        This method returns the value of encoding of the simulation scenario under consideration

        :param encoding: enconder UTF8, defaults to None
        :type encoding: string, optional
        :return: Full path of scenario
        :rtype: string
        """
        if encoding == "UTF8":
            return self._file_name.encode(encoding)
        return self._file_name

    @property
    def time_step(self):
        return float(self.get_simulation_parameters()[0].get("pasdetemps"))
