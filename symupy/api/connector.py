""" 
**Connector Module**

This module details the implementation of a ``Simulator`` object in charge of handling the connection between the traffic simulator and this interface. The connection with the traffic simulator is handled by an object called ``Connector`` which establishes a messaging protocol with the traffic simulator. 

Example:
    To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

        >>> path = "path/to/simulator.so"
        >>> simulator = Simulator(path) 

Other parameters can also be send to the simulator in order to provide other configurations:

Example: 
    To send make increase the *buffer size* to a specific size:

        >>> simulator = Simulator(path, bufferSize = 1000000)
    
    To increase change the flag that traces the flow:

        >>> simulator = Simulator(path, traceFlow = True)


"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
from itertools import repeat
from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double

import typing
from typing import Union

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

# Error Handling
from symupy.utils.exceptions import (
    SymupyLoadLibraryError,
    SymupyFileLoadError,
    SymupyVehicleCreationError,
    SymupyDriveVehicleError,
    SymupyWarning,
)

#
from symupy.api.scenario import Simulation
from symupy.utils import SimulatorRequest, Configurator

from symupy.utils import timer_func, printer_time
from symupy.utils import constants as ct

from symupy.components import V2INetwork, V2VNetwork
from symupy.components import Vehicle

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

# V2X Connectivity
NetworkType = Union[V2INetwork, V2VNetwork]


class Simulator(object):
    """ 
    
        This object describes is a connector manager for the interface between the    traffic simulator and the 

        Args:
            libraryPath (str): 
                Absolute path towards the simulator library

            bufferSize (int): 
                Size of the buffer for message for data received from simulator

            writeXML (bool): 
                Flag to turn on writting the XML output

            traceFlow (bool):
                Flag to determine tracing or not the flow / trajectories

            totalSteps (int):
                Define the number of iterations of a simulation 

            stepLaunchMode (str):
                Determine to way to launch the ``RunStepEx``. Options ``lite``/``full``

        :raises SymupyLoadLibraryError: 
            Error raised whenever the SymuVia library is not found

        :raises SymupyFileLoadError: 
            Error raised whenever the provided path for an scenario cannot be loaded into the Simulator

        :raises SymupyVehicleCreationError: 
            Error raised when a vehicle cannot be created

        :raises SymupyDriveVehicleError: 
            Error rased when a vehicle state cannot be imposed

        :raises NotImplementedError: 
            Not implemented functionality 

        :return: Simulator manager object 

        :rtype: Simulator
    """

    def __init__(
        self,
        libraryPath: str = "",
        bufferSize: int = ct.BUFFER_STRING,
        writeXML: bool = True,
        traceFlow: bool = False,
        totalSteps: int = 0,
        stepLaunchMode: str = "lite",
        **kwargs,
    ) -> None:
        self.initialize_configurator(
            bufferSize=bufferSize,
            writeXML=writeXML,
            traceFlow=traceFlow,
            libraryPath=libraryPath,
            totalSteps=totalSteps,
            stepLaunchMode=stepLaunchMode,
            **kwargs,
        )
        self._net = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.libraryPath})"

    def initialize_configurator(self, **kwargs) -> None:
        """ 
           This method initialize a ``Configurator`` class that contains a small summary setup to launch a simulation
        """
        self._config = Configurator(**kwargs)

    def load_symuvia(self) -> None:
        """ load SymuVia shared library """
        try:
            lib_symuvia = cdll.LoadLibrary(self.libraryPath)
        except OSError:
            raise SymupyLoadLibraryError("Library not found", self.libraryPath)
        self._library = lib_symuvia

    def load_network(self) -> None:
        """ load SymuVia Simulation File """
        if not hasattr(self, "_sim"):
            raise SymupyFileLoadError("File not provided", "")
        valid = self._library.SymLoadNetworkEx(self._sim.filename_encoded)
        if not valid:
            raise SymupyFileLoadError("Simulation could not be loaded", "")

    def init_simulation(self) -> None:
        """ Initializes conditions for a step by step simulation"""
        # Pointers
        self._s_response = create_string_buffer(ct.BUFFER_STRING)
        self._b_end = c_int()
        self._b_trace = c_bool(False)
        # self._b_force = c_int(1)
        self.state = SimulatorRequest()

    @timer_func
    def run_simulation(self, sim_object: Simulation = "") -> None:
        """ Run simulation in a single shot

        Args:
            sim_object (Simulation): Valid simulation scenario

        Returns:
            None: No returns provided, only internal updates
        """
        if sim_object:
            self.register_simulation(sim_object)

        self.load_symuvia()
        self._library.SymRunEx(self._sim.filename_encoded)

    def register_simulation(self, sim_object: Simulation) -> None:
        """Register simulation file within the simulator

        :param sim_object: Simulation scenario to register
        :type sim_object: Simulation
        :return: No value is returned
        :rtype: None
        """
        self._sim = sim_object

    def register_network(self, network: NetworkType) -> None:
        self._net.append(network)

    def request_answer(self):
        """Request simulator answer and maps the data locally
        """
        if self._config.stepLaunchMode == "lite":
            self._bContinue = self._library.SymRunNextStepLiteEx(self._b_trace, byref(self._b_end))
            return
        self._bContinue = self._library.SymRunNextStepEx(self._s_response, self._b_trace, byref(self._b_end))
        self.state.parse_data(self.s_response_dec)

    # @printer_time
    def run_step(self) -> int:
        """ Run simulation step by step

        :return: iteration step
        :rtype: int
        """
        try:
            self.request_answer()
            self._c_iter = next(self._n_iter)
            return self._c_iter
        except StopIteration:
            self._bContinue = False
            return -1

    def stop_step(self):
        """Stop current current step of running simulation
        """
        self._bContinue = False

    def create_vehicle(self, vehtype: str, origin: str, destination: str, lane: int = 1, simid: int = 0) -> int:
        """Creates a vehicle within the network

        :param vehtype: vehicle type according to simulation definitions
        :type vehtype: str
        :param origin: network endpoint nodeaccording to simulation
        :type origin: str
        :param destination: network endpoint nodeaccording to simulation
        :type destination: str
        :param lane: vehicle lane number, defaults to 1
        :type lane: int, optional
        :param simid: simulation id, defaults to 0
        :type simid: int, optional
        :raises SymupyVehicleCreationError: Exception handling for invalid vehicle types or invalid network points
        :return: Vehicle id of the vehicle created >0
        :rtype: int
        """
        endpoints = self._sim.get_network_endpoints()
        veh_data = self._sim.get_vehicletype_information()
        dbTime = self._sim.sampling_time
        vehid = tuple(v["id"] for v in veh_data)
        if vehtype not in vehid:
            raise SymupyVehicleCreationError("Unexisting Vehicle Class in File: ", self._sim.filename)

        if (origin not in endpoints) or (destination not in endpoints):
            raise SymupyVehicleCreationError("Unexisting Network Endpoint File: ", self._sim.filename)

        vehid = self._library.SymCreateVehicleEx(
            vehtype.encode("UTF8"), origin.encode("UTF8"), destination.encode("UTF8"), c_int(lane), c_double(dbTime),
        )
        return vehid

    def create_vehicle_with_route(
        self, vehtype: str, origin: str, destination: str, lane: int = 1, creation_time: float = 0, route: str = ""
    ) -> int:
        """ Creates a vehicle with a specific route
        
            :param vehtype: vehicle type according to simulation definitions
            :type vehtype: str
            :param origin: network endpoint node according to simulation
            :type origin: str
            :param destination: network endpoint node according to simulation
            :type destination: str
            :param lane: vehicle lane number, defaults to 1
            :type lane: int, optional
            :param creation_time: time instant of creation [0,Ts], defaults to 0
            :type creation_time: float, optional
            :param route: route followed by the vehicle, defaults to ""
            :type route: str, optional

            :return: Vehicle id of the vehicle created >0
            :rtype: int        
        """
        if origin == destination:
            return -1

        endpoints = self._sim.get_network_endpoints()
        veh_data = self._sim.get_vehicletype_information()
        dbTime = self.simulationstep
        vehid = tuple(v["id"] for v in veh_data)

        if vehtype not in vehid:
            raise SymupyVehicleCreationError("Unexisting Vehicle Class in File: ", self._sim.filename)

        if (origin not in endpoints) or (destination not in endpoints):
            raise SymupyVehicleCreationError("Unexisting Network Endpoint File: ", self._sim.filename)

        vehid = self._library.SymCreateVehicleWithRouteEx(
            origin.encode("UTF8"),
            destination.encode("UTF8"),
            vehtype.encode("UTF8"),
            c_int(lane),
            c_double(creation_time - dbTime),
            route.encode("UTF8"),
        )
        return vehid

    def drive_vehicle(self, vehid: int, new_pos: float, destination: str = None, lane: str = 1) -> None:
        """Drives a vehicle to a specific position

        :param vehid: vehicle id to drive 
        :type vehid: int
        :param new_pos: position to place the vehicle
        :type new_pos: float
        :param destination: link of destination, defaults to None
        :type destination: str, optional
        :param lane: lane fo destination, defaults to 1
        :type lane: str, optional
        :raises SymupyDriveVehicleError: Raises error when link does not exist
        :return: Value returned by SymDriveErr 1 ok, negative values are errors.
        :rtype: None
        """
        links = self._sim.get_network_links()

        if not destination:
            destination = self.state.query_vehicle_link(str(vehid))[0]

        if destination not in links:
            raise SymupyDriveVehicleError("Unexisting Network Endpoint File: ", self._sim.filename)

        # TODO: Validate that position do not overpass the max pos
        dr_state = self._library.SymDriveVehicleEx(
            c_int(vehid), destination.encode("UTF8"), c_int(lane), c_double(new_pos), 1
        )
        self.request_answer()
        return dr_state

    def drive_vehicle_with_control(self, vehcontrol, vehid: int, destination: str = None, lane: str = 1):
        # TODO: Basic prototyping
        vehcontrol.set_current_state(self.state)
        new_pos = vehcontrol.new_position
        return self.drive_vehicle(vehid, new_pos, destination, lane)

    def get_vehicle_context(self, vehid: str):
        ## TODO: Implement this
        raise NotImplementedError

    def log_vehicle_in_network(self, veh: Vehicle, network: NetworkType):
        # veh = Vehicle(vehid)
        ## TODO: Finish
        network.register_vehicle(veh)

    def log_vehid_in_network(self, vehid: str, network: NetworkType):
        ## TODO: Optional
        pass

    def init_total_travel_time(self):
        """ Counter initializer for total travel time
        """
        # TODO: Improvement → Better organizadtion
        self._library.SymGetTotalTravelTimeEx.restype = c_double

    def init_total_travel_distance(self):
        """ Counter initializer for total travel time
        """
        # TODO: Improvement → Better organizadtion
        self._library.SymGetTotalTravelDistanceEx.restype = c_double

    def get_total_travel_time(self, zone_id: str = None):
        """ Computes the total travel time of vehicles in a MFD region
        
        :param zone_id: MFD sensor id, defaults to None
        :type zone_id: str, optional
        :return: Associated total travel time
        """
        # TODO: Improvement → Better organizadtion
        if zone_id:
            return self._library.SymGetTotalTravelTimeEx(zone_id.encode("UTF8"))

        sensors = self.simulation.get_mfd_sensor_names()
        return tuple(self._library.SymGetTotalTravelTimeEx(sensor.encode("UTF8")) for sensor in sensors)

    def get_total_travel_distance(self, zone_id: str = None):
        """ Computes the total travel distance of vehicles in a MFD region
        
        :param zone_id: MFD sensor id, defaults to None
        :type zone_id: str, optional
        :return: Associated total travel distance
        """
        # TODO: Improvement → Better organizadtion
        if zone_id:
            return self._library.SymGetTotalTravelDistanceEx(zone_id.encode("UTF8"))

        sensors = self.simulation.get_mfd_sensor_names()
        return tuple(self._library.SymGetTotalTravelDistanceEx(sensor.encode("UTF8")) for sensor in sensors)

    def get_mfd_speed(self, zone_id: str = None):
        """ Computes the total speed of vehicles in a MFD region
        
        :param zone_id: MFD sensor id, defaults to None
        :type zone_id: str, optional
        :return: speed computed as ttt/ttd
        """
        # TODO: Improvement → Better organizadtion
        if zone_id:
            d = self.get_total_travel_distance(zone_id)
            t = self.get_total_travel_time(zone_id)
            spd = d / t if t != 0 else 10
            return spd

        itdsttm = zip(self.get_total_travel_distance(), self.get_total_travel_time())
        spd = []
        for d, t in itdsttm:
            if t != 0:
                spd.append(d / t)
            else:
                spd.append(10)  # minimum speed?
        return tuple(spd)

    def add_control_probability_zone_mfd(self, access_probability: dict, minimum_distance: dict) -> None:
        """
            Add a probability to control the access to a specific zone within the network
        
            :param access_probability: Key (zone name) Value (probability of access)
            :type access_probability: dict
            :param minimum_distance: Key (zone name) Value (distance before entering the zone to activate policy)
            :type minimum_distance: dict
        """
        self.dctidzone = {}

        for tp_zn_pb, tp_zn_md in zip(access_probability.items(), minimum_distance.items()):
            sensor, accrate = tp_zn_pb
            _, min_dst = tp_zn_md
            links = self.simulation.get_links_in_mfd_sensor(sensor)
            links_str = " ".join(links)
            self.dctidzone[sensor] = self._library.SymAddControlZoneEx(
                -1, c_double(accrate), c_double(min_dst), f"'{links_str}'".encode("UTF8"),
            )
        return self.dctidzone

    def modify_control_probability_zone_mfd(self, access_probability: dict) -> None:
        """
            Modifies a probability to control the access to a specific zone within the network
        
            :param access_probability: Key (zone name) Value (probability of access)
            :type access_probability: dict
        """

        for sensor, probablity in access_probability.items():
            self._library.SymModifyControlZoneEx(-1, self.dctidzone[sensor], c_double(probablity))
        return self.dctidzone

    def __enter__(self) -> None:
        """ Implementation as a context manager
            FIXME: Implement state machine ???
        """
        self.load_symuvia()
        self.load_network()
        self.init_simulation()
        self._n_iter = iter(self._sim.get_simulation_steps())
        self._c_iter = next(self._n_iter)
        self._bContinue = True
        # Extra
        self.init_total_travel_distance()
        self.init_total_travel_time()
        self.build_dynamic_param()
        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    def build_dynamic_param(self):
        """Construct parameters for vehicle dynamics
        """
        self.__dct_par = {
            "time_step": self.simulation.sampling_time,
            "engine_tau": ct.ENGINE_CONSTANT,
        }

    @property
    def s_response_dec(self):
        """ 
            Obtains instantaneous data from simulator

            :return: last query from simulator
            :rtype: str
        """
        return self._s_response.value.decode("UTF8")

    @property
    def do_next(self) -> bool:
        """
            Returns true if the simulation shold continue
        
            :return: True if next step continues
            :rtype: bool
        """
        return self._bContinue

    @property
    def get_request(self) -> dict:
        """
            Returns the query received from the simulator
        
            :return: Request from the simulator
            :rtype: dict
        """
        return self.state.data_query

    @property
    def libraryPath(self) -> str:
        """ 
            Simulator library path
        
        :return: Absolute path
        :rtype: str
        """
        return self._config.libraryPath

    @property
    def simulation(self) -> Simulation:
        """
            Simulation scenario 
        
            :return: Object describing senario under simulation
            :rtype: Simulation
        """
        return self._sim

    @property
    def scenariofilename(self) -> str:
        """ 
            Scenario filenamme
        
            :return: Absolute path towards the XML input for SymuVia
            :rtype: str
        """
        return self.simulation.filename

    @property
    def simulationstep(self) -> str:
        """ 
            Current simulation step.

            Example:
                You can use the time step to control actions 

                >>> with simulator as s:
                ...     while s.do_next()
                ...         if s.simulationstep>0:
                ...             print(s.simulationtimestep)
        
            :return: current simulation iteration
            :rtype: str
        """
        return self._c_iter

    @property
    def sampling_time(self) -> float:
        """ 
            Simulation sampling time 
        
            :return: sampling time from XML file
            :rtype: float
        """
        return self.simulation.sampling_time

    @classmethod
    def from_path(cls, filename_path, simuvia_path):
        """ Alternative constructor for the Simulator 

            Example:
                To use this alternative constructor ``Simulator`` declare in a string the ``path`` to the simulator ::

                    >>> path = "path/to/simulator.so"
                    >>> scenario = "path/to/scenario.xml"
                    >>> simulator = Simulator.from_path(path,scenario) 

        """
        case = Simulation(filename_path)
        sim = cls(simuvia_path)
        sim.register_simulation(case)
        return sim
