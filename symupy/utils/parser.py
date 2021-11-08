"""
Stream Parser
=============
This module handles the Simulation response converting it into proper formats for querying data afterwards.

The parser object converts a request from the simulator into the correct format for the
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from ctypes import create_string_buffer
from typing import Union, Dict, List, Tuple
from collections import defaultdict

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.runtime.logic.publisher import Publisher
from symupy.tsc.vehicles import Vehicle, VehicleList
from symupy.parser.xmlparser import XMLTrajectory
from symupy.utils.exceptions import SymupyError
from symupy.utils.constants import BUFFER_STRING, FIELD_DATA, FIELD_FORMAT

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SimulatorRequest(Publisher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datatraj = XMLTrajectory(b"")

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return (
            "Sim Time: {}, VehInNetwork: {}".format(
                self.current_time, self.current_nbveh
            )
            if self.data_query
            else "Simulation has not started"
        )

    # =========================================================================
    # MEMORY HANDLING
    # =========================================================================

    @property
    def query(self):
        """String response from the simulator"""
        return self.datatraj._xml

    @query.setter
    def query(self, response: bytes):
        self.datatraj = XMLTrajectory(response)
        for c in self._channels:
            self.dispatch(c)

    @property
    def current_time(self) -> float:
        return self.datatraj.inst

    @property
    def current_nbveh(self) -> int:
        return self.datatraj.nbveh

    @property
    def data_query(self):
        """Direct parsing from the string buffer

        Returns:
            simdata (OrderedDict): Simulator data parsed from XML
        """

        return self.datatraj.todict

    # =========================================================================
    # METHODS
    # =========================================================================

    def get_vehicle_data(self) -> tuple:
        """Extracts vehicles information from simulators response

        Returns:
            t_veh_data (list): list of dictionaries containing vehicle data with correct formatting

        """
        return self.data_query

    def get_vehicles_property(self, property_key: str) -> tuple:
        """Extracts a specific property and returns a tuple containing this
        property for all vehicles in the buffer string

        Args:
            property_key (str):
                one of the following options abscissa, acceleration, distance, elevation, lane, link, ordinate, speed, vehid, vehtype,

        Returns:
            values (tuple):
                tuple with corresponding values e.g (0,1), (0,),(None,)
        """
        return tuple(x.get(property_key) for x in self.data_query)

    def filter_vehicle_property(self, property: str, *args):
        """Filter out a property for a subset of vehicles

        Args:
            property (str):
                one of the following options abscissa, acceleration, distance, elevation, lane, link, ordinate, speed, vehid, vehtype,

            vehids (int):
                separate the ``vehid`` via commas to get the corresponding property
        """
        if args:
            sargs = set(args)
            vehids = set(self.get_vehicles_property("vehid"))
            fin_ids = vehids.intersection(sargs)
            return tuple(
                veh.get(property)
                for veh in self.get_vehicle_data()
                if veh.get("vehid") in fin_ids
            )
        return self.get_vehicles_property(property)

    def get_vehicle_properties(self, vehid: int) -> dict:
        """Return all properties for a given vehicle id

        Returns:
            vehdata (dict): Dictionary with all vehicle properties
        """
        data = self.get_vehicle_data()
        for v in data:
            if v["vehid"] == vehid:
                return v
        return {}

    def is_vehicle_in_network(self, vehid: int, *args) -> bool:
        """True if veh id is in the network at current state, for multiple
        arguments. True if all veh ids are in the network.

        Args:
            vehid (int): Integer of vehicle id, comma separated if testing for multiple

        Returns:
            present (bool): True if vehicle is in the network otherwise false.

        """
        all_vehs = self.get_vehicles_property("vehid")
        if not args:
            return vehid in all_vehs
        vehids = set((vehid, *args))
        return set(vehids).issubset(set(all_vehs))

    def vehicles_in_link(self, link: str, lane: int = 1) -> tuple:
        """Returns a tuple containing vehicle ids traveling on the same
        (link,lane) at current state

        Args:
            link (str): link name
            lane (int): lane number

        Returns:
            vehs (tuple): set of vehicles in link/lane

        """
        return tuple(
            veh.get("vehid")
            for veh in self.get_vehicle_data()
            if veh.get("link") == link and veh.get("lane") == lane
        )

    def is_vehicle_in_link(self, veh: int, link: str) -> bool:
        """Returns true if a vehicle is in a link at current state

        Args:
            vehid (int): vehicle id
            link (str): link name

        Returns:
            present (bool): True if veh is in link

        """
        veh_ids = self.vehicles_in_link(link)
        return set((veh,)).issubset(set(veh_ids))

    def is_vehicle_driven(self, vehid: int) -> bool:
        """Returns true if the vehicle state is exposed to a driven state

        Args:
            vehid (str):
                vehicle id

        Returns:
            driven (bool): True if veh is driven
        """
        if self.is_vehicle_in_network(vehid):

            forced = tuple(
                veh.get("driven") == True
                for veh in self.get_vehicle_data()
                if veh.get("vehid") == vehid
            )
            return any(forced)
        return False

    def vehicle_downstream_of(self, vehid: int) -> tuple:
        """Get ids of vehicles downstream to vehid

        Args:
            vehid (str):
                vehicle id

        Returns:
            vehid (tuple):
                vehicles downstream of vehicle id
        """
        link = self.filter_vehicle_property("link", vehid)[0]
        vehpos = self.filter_vehicle_property("distance", vehid)[0]

        vehids = set(self.vehicles_in_link(link))
        neigh = vehids.difference(set((vehid,)))

        neighpos = self.filter_vehicle_property("distance", *neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos > vehpos)

    def vehicle_upstream_of(self, vehid: str) -> tuple:
        """Get ids of vehicles upstream to vehid

        Args:
            vehid (str):
                vehicle id

        Returns:
            vehid (tuple):
                vehicles upstream of vehicle id
        """
        link = self.filter_vehicle_property("link", vehid)[0]
        vehpos = self.filter_vehicle_property("distance", vehid)[0]

        vehids = set(self.vehicles_in_link(link))
        neigh = vehids.difference(set((vehid,)))

        neighpos = self.filter_vehicle_property("distance", *neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if npos < vehpos)

    def get_vehicle_in_link(self) -> dict:
        """Get a map of vehicle ids and their correspnding link.

        Returns:
            map (dict):
                zone - ids of vehicles
        """
        return {str(i["vehid"]): i["link"] for i in self.get_vehicle_data()}
