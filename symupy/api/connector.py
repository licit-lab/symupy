""" 
    This module details the implementation of a ``Simulator`` object in charge of handling the connection between the traffic simulator and this interface. The connection with the traffic simulator is handled by an object called ``Connector`` which establishes a messaging protocol with the traffic simulator. 

    Example:
        To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

            >>> from symupy.api import Simulator
            >>> path_symuvia = "path/to/libSymuyVia.dylib"
            >>> simulator = Simulator(library_path=path_symuvia)

    Other parameters can also be send to the simulator in order to provide other configurations:

    Example: 
        To send make increase the *buffer size* to a specific size:
            
            >>> simulator = Simulator(bufferSize = 1000000)
        
        To increase change the flag that traces the flow:

            >>> simulator = Simulator(trace_flow = True)
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
from itertools import repeat
from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
import click
import platform

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
from .scenario import Simulation
from symupy.utils import SimulatorRequest, Configurator
from symupy.logic import RuntimeDevice
from symupy.components.vehicles import VehicleList

from symupy.utils import timer_func, printer_time
from symupy.utils import constants as CT

from symupy.components import V2INetwork, V2VNetwork
from symupy.components import Vehicle

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================

# V2X Connectivity
NetworkType = Union[V2INetwork, V2VNetwork]

TupleFloat = Union[float, tuple]


class Simulator(Configurator, RuntimeDevice):
    """ 
        Simulator class for containing object to connect and  command a simulation in SymuVia

        Example:
            Call of the default simulator ::

                >>> from symupy.api import Simulator
                >>> simulator = Simulator()

        :return: Symuvia simulator object with simulation parameters
        :rtype: Simulator

        You may also pass suplementary parameters to the object by specifying keys in the call: 

        Example: 
            To use the ``Simulator`` declare in a string the ``path`` to the simulator ::

                >>> from symupy.api import Simulator
                >>> path_symuvia = "path/to/libSymuyVia.dylib"
                >>> simulator = Simulator(library_path=path_symuvia)
    
        This object describes is a configurator manager for the interface between the traffic simulator and the python interface. For more details on the optinal keyword parameters please refer to :py:class:`~symupy.utils.configurator.Configurator` class.

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

    def __init__(self, **kwargs) -> None:
        Configurator.__init__(self, **kwargs)
        RuntimeDevice.__init__(self)
        self._net = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.library_path})"

    # =========================================================================
    # LOADING METHODS
    # =========================================================================

    def load_symuvia(self):
        """ Load SymuVia shared library 

        """
        try:
            lib_symuvia = cdll.LoadLibrary(self.library_path)
        except OSError:
            raise SymupyLoadLibraryError("Library not found", self.library_path)
        self.__library = lib_symuvia

    def load_network(self) -> int:
        """ Load SymuVia Simulation File 

        """
        if not hasattr(self, "_sim"):
            raise SymupyFileLoadError("File not provided", "")
        valid = self.__library.SymLoadNetworkEx(self.scenarioFilename("UTF8"))
        if not valid:
            raise SymupyFileLoadError("Simulation could not be loaded", "")
        return valid

    def register_simulation(self, scenario_path: str):
        """ Register simulation file within the simulator

        """
        self._sim = Simulation(scenario_path)

    def register_network(self, network: NetworkType):
        # TODO: Impleement this connection. This is for V2V
        self._net.append(network)

    # =========================================================================
    # RUNTIME METHODS
    # =========================================================================

    @timer_func
    def run_simulation(self, scenario_path: str = ""):
        """ Run simulation in a single shot

            Args:
                sim_object (Simulation): Valid simulation scenario

        """
        if scenario_path:
            self.register_simulation(scenario_path)

        self.load_symuvia()
        self.__library.SymRunEx(self.scenarioFilename("UTF8"))

    def run(self, scenario_path: str = ""):
        """ Alias method to run simulation

            Args:
                scenario_path (Simulation): Valid simulation scenario

        """
        self.run_simulation(scenario_path)

    def request_answer(self):
        """ Request simulator answer and maps the data locally

        """
        if self.step_launch_mode == "lite":
            self._bContinue = self.__library.SymRunNextStepLiteEx(
                self.write_xml, byref(self._b_end)
            )
            return
        self._bContinue = self.__library.SymRunNextStepEx(
            self.buffer_string, self.write_xml, byref(self._b_end)
        )
        self.request.query = self.buffer_string.value
        self.vehicles.update_list()

    @printer_time
    def run_step(self) -> int:
        """ Run simulation step by step

            :returns it:  Iteration step
            :type it: int

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

    def create_vehicle(
        self,
        vehtype: str,
        origin: str,
        destination: str,
        lane: int = 1,
        simid: int = 0,
    ) -> int:
        """ Creates a vehicle within the network

            :param vehtype: vehicle type according to simulation definitions
            :type vehtype: str
                    
            :param origin: network endpoint nodeaccording to simulation
            :type origin: str
                    
            :param destination: network endpoint nodeaccording to simulation
            :type destination: str
                    
            :param lane: vehicle lane number, defaults to 1
            :type lane: int
                    
            :param simid: simulation id, defaults to 0
            :type simid: int
                    

            :returns vehid: Vehicle id of the vehicle created >0
            :type vehid: int 

            Example: 
                One example to create a vehicle is as follows ::

                >>> with symuvia as s:
                >>>     while s.do_next:
                >>>         s.request_answer()  # Initialize
                >>>         s.request_answer()  # Vehicle 0
                >>>         # Vehicle instantiation
                >>>         veh_id = s.create_vehicle("VL", "Ext_In", "Ext_Out")
                >>>         force_driven = s.request.is_vehicle_driven("1")
                >>>         s.request_answer() 


        """
        endpoints = self._sim.get_network_endpoints()
        veh_data = self._sim.get_vehicletype_information()
        vehid = tuple(v["id"] for v in veh_data)

        # Consistency checks
        if vehtype not in vehid:
            raise SymupyVehicleCreationError(
                "Unexisting Vehicle Class in File: ", self.scenarioFilename()
            )

        if (origin not in endpoints) or (destination not in endpoints):
            raise SymupyVehicleCreationError(
                "Unexisting Network Endpoint File: ", self.scenarioFilename()
            )

        # Vehicle creation
        vehid = self.__library.SymCreateVehicleEx(
            vehtype.encode("UTF8"),
            origin.encode("UTF8"),
            destination.encode("UTF8"),
            c_int(lane),
            c_double(self.simulationstep),
        )
        return vehid

    def create_vehicle_with_route(
        self,
        vehtype: str,
        origin: str,
        destination: str,
        lane: int = 1,
        creation_time: float = 0,
        route: str = "",
    ) -> int:
        """ Creates a vehicle with a specific route

            :param vehtype: vehicle type according to simulation definitions
            :type vehtype: str 
                    
            :param origin: network endpoint nodeaccording to simulation
            :type origin: str 
                    
            :param destination: network endpoint nodeaccording to simulation
            :type destination: str 
                    
            :param lane: vehicle lane number, defaults to 1
            :type lane: int 
                    
            :param route: route followed by the vehicle, defaults to ""
            :type route: str 
 
            :return vehid: Vehicle id of the vehicle created >0
            :type vehid: int

        """
        if origin == destination:
            return -1

        endpoints = self._sim.get_network_endpoints()
        veh_data = self._sim.get_vehicletype_information()
        vehid = tuple(v["id"] for v in veh_data)

        # Consistency checks
        if vehtype not in vehid:
            raise SymupyVehicleCreationError(
                "Unexisting Vehicle Class in File: ", self.scenarioFilename()
            )

        if (origin not in endpoints) or (destination not in endpoints):
            raise SymupyVehicleCreationError(
                "Unexisting Network Endpoint File: ", self.scenarioFilename()
            )

        # Vehicle creation
        vehid = self.__library.SymCreateVehicleWithRouteEx(
            origin.encode("UTF8"),
            destination.encode("UTF8"),
            vehtype.encode("UTF8"),
            c_int(lane),
            c_double(creation_time - self.simulationstep),
            route.encode("UTF8"),
        )
        return vehid

    def drive_vehicle(
        self, vehid: int, new_pos: float, destination: str = None, lane: str = 1
    ):
        """ Drives a vehicle to a specific position

            :param vehtype: vehicle type according to simulation definitions
            :type vehtype: str, optional
                    
            :param new_pos: position to place the vehicle
            :type new_pos: float
                    
            :param destination: link of destination, defaults to None
            :type destination: str
                    
            :param lane: lane fo destination, defaults to 1
            :type lane: int
                    
            :param route: route followed by the vehicle, defaults to ""
            :type route: str    

            Example: 
                One example to drive a vehicle as follows ::

                >>> with symuvia as s:
                >>>     while s.do_next:
                >>>         s.run_step()
                >>>         if s.request.is_vehicle_in_network("0"):
                >>>             drive_status = s.drive_vehicle(0, 1.0)
                >>>             force_driven = s.request.is_vehicle_driven("0")
        """
        links = self._sim.get_network_links()

        if not destination:
            destination = self.request.filter_vehicle_property("link", vehid)[0]

        if destination not in links:
            raise SymupyDriveVehicleError(
                "Unexisting Network Endpoint File: ", self.scenarioFilename()
            )

        # TODO: Validate that position do not overpass the max pos
        dr_state = self.__library.SymDriveVehicleEx(
            c_int(vehid),
            destination.encode("UTF8"),
            c_int(lane),
            c_double(new_pos),
            1,
        )
        self.request_answer()
        return dr_state

    def drive_vehicle_with_control(
        self, vehcontrol, vehid: int, destination: str = None, lane: str = 1
    ):
        # TODO: Basic prototyping
        vehcontrol.set_current_state(self.request)
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
        self.__library.SymGetTotalTravelTimeEx.restype = c_double

    def init_total_travel_distance(self):
        """ Counter initializer for total travel time
        """
        # TODO: Improvement → Better organizadtion
        self.__library.SymGetTotalTravelDistanceEx.restype = c_double

    def get_total_travel_time(self, sensors_mfd: list = []):
        """ Computes the total travel time of vehicles in a MFD region
        
            :param zone_id: MFD sensor id, defaults to None
            :type zone_id: str, optional

            :return ttt: Associated total travel time
            :type ttt: float

        """
        # TODO: Improvement → Better organizadtion
        if isinstance(sensors_mfd, str):
            return self.__library.SymGetTotalTravelTimeEx(
                sensors_mfd.encode("UTF8")
            )

        if not sensors_mfd:
            sensors_mfd = self.simulation.get_mfd_sensor_names()

        return tuple(
            self.__library.SymGetTotalTravelTimeEx(sensor.encode("UTF8"))
            for sensor in sensors_mfd
        )

    def get_total_travel_distance(self, sensors_mfd: list = []):
        """ Computes the total travel distance of vehicles in a MFD region
        
            :param sensors_mfd: MFD sensor ids, defaults to None
            :type sensors_mfd: list, optional

            :return ttd: Associated total travel distance
            :type ttd: float, tuple
            
        """
        if isinstance(sensors_mfd, str):
            return self.__library.SymGetTotalTravelDistanceEx(
                sensors_mfd.encode("UTF8")
            )

        if not sensors_mfd:
            sensors_mfd = self.simulation.get_mfd_sensor_names()

        return tuple(
            self.__library.SymGetTotalTravelDistanceEx(sensor.encode("UTF8"))
            for sensor in sensors_mfd
        )

    def get_mfd_speed(self, sensors_mfd: list = []):
        """ Computes the total speed of vehicles in a MFD region
        
            :param sensors_mfd: MFD sensor ids, defaults to None
            :type sensors_mfd: list, optional

            :return spd: speed computed as ttt/ttd
            :type spd: float, tuple

        """
        if isinstance(sensors_mfd, str):
            d = self.get_total_travel_distance(sensors_mfd)
            t = self.get_total_travel_time(sensors_mfd)
            spd = d / t if t != 0 else 10
            return spd

        itdsttm = zip(
            self.get_total_travel_distance(sensors_mfd),
            self.get_total_travel_time(sensors_mfd),
        )
        spd = []
        for d, t in itdsttm:
            if t != 0:
                spd.append(d / t)
            else:
                spd.append(10)  # minimum speed?
        return tuple(spd)

    def add_control_probability_zone_mfd(
        self, access_probability: dict, minimum_distance: dict
    ):
        """
            Add a probability to control the access to a specific zone within the network
        
            :param access_probability: Key (zone name) Value (probability of access)
            :type access_probability: dict

            :param minimum_distance: Key (zone name) Value (distance before entering the zone to activate policy)
            :type minimum_distance: dict
        """
        self.dctidzone = {}

        for tp_zn_pb, tp_zn_md in zip(
            access_probability.items(), minimum_distance.items()
        ):
            sensor, accrate = tp_zn_pb
            _, min_dst = tp_zn_md
            links = self.simulation.get_links_in_mfd_sensor(sensor)
            links_str = " ".join(links)
            self.dctidzone[sensor] = self.__library.SymAddControlZoneEx(
                -1,
                c_double(accrate),
                c_double(min_dst),
                f"{links_str}".encode("UTF8"),
            )
        # Apply set control
        self.__library.SymApplyControlZonesEx(-1)
        return self.dctidzone

    def modify_control_probability_zone_mfd(self, access_probability: dict):
        """
            Modifies a probability to control the access to a specific zone within the network
        
            :param access_probability: Key (zone name) Value (probability of access)
            :type access_probability: dict
        """

        for sensor, probablity in access_probability.items():
            self.__library.SymModifyControlZoneEx(
                -1, self.dctidzone[sensor], c_double(probablity)
            )
        # Apply set control
        self.__library.SymApplyControlZonesEx(-1)
        return self.dctidzone

    def __enter__(self) -> None:
        """
            This method initializes the usage of the ``Simulator`` class as a context manager. 

            The protocol followed in order to perform the full connection is as follows 

        """

        self.reset_state()

        # Compliance situation
        self.__performCompliance()

        # Connect to platform
        self.__performConnect()

        # Variable initialization
        self.__performInitialize()

        # Extra

        return self

    def __exit__(self, type, value, traceback) -> bool:
        self.__library.SymUnloadCurrentNetworkEx()
        click.echo("Runtime: End")
        return False

    def build_dynamic_param(self):
        """Construct parameters for vehicle dynamics
        """
        self.__dct_par = {
            "time_step": self.simulation.time_step,
            "engine_tau": CT.ENGINE_CONSTANT,
        }

    # =========================================================================
    # STATE MACHINE
    # =========================================================================

    def __performCompliance(self) -> None:
        """
            Perform compliance check
        """
        self.next_state(True)

    def __performConnect(self) -> None:
        """
            Perform simulation connection
        """
        self.load_symuvia()
        self.load_network()
        self.next_state(True)

    def __performInitialize(self) -> None:
        """
            Perform simulation initialization
        """
        self._b_end = c_int()
        self.request = SimulatorRequest()
        self._n_iter = iter(self._sim.get_simulation_steps())
        self._c_iter = next(self._n_iter)
        self._bContinue = True
        self.vehicles = VehicleList(self.request)

        self.init_total_travel_distance()
        self.init_total_travel_time()
        self.build_dynamic_param()

        self.next_state(self.do_next)

    def __performPreRoutine(self) -> None:
        """
            Perform simulator preroutine
        """
        self.next_state(self.do_next)

    def __performQuery(self) -> None:
        """
            Perform simulator Query
        """
        self.next_state(self.do_next)

    def __performControl(self) -> None:
        """
            Perform simulator Control
        """
        self.next_state(self.do_next)

    def _set_manual_initialization(self) -> None:
        """
            This method is a way to set manual initialization of the simulator
            for testing purposes. (Internal use)
        """
        self.__performCompliance()
        self.__performConnect()
        self.__performInitialize()

    # =========================================================================
    # ATTRIBUTES
    # =========================================================================

    def scenarioFilename(self, encoding=None) -> str:
        """ 
            Scenario filenamme
        
            :return: Absolute path towards the XML input for SymuVia
            :rtype: str
        """
        return self.simulation.filename(encoding)

    @property
    def s_response_dec(self):
        """ 
            Obtains instantaneous data from simulator

            :return: last query from simulator
            :rtype: str
        """
        return self.buffer_string.value.decode("UTF8")

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
        return self.request.data_query

    @property
    def simulation(self) -> Simulation:
        """
            Simulation scenario 
        
            :return: Object describing senario under simulation
            :rtype: Simulation
        """
        return self._sim

    @property
    def simulationstep(self) -> float:
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

    @property
    def library(self):
        return self.__library

    # =========================================================================
    # CONSTRUCTORS
    # =========================================================================

    @classmethod
    def from_path(cls, filename_path: str, symuvia_path: str):
        """ Alternative constructor for the Simulator 

            Example:
                To use this alternative constructor ``Simulator`` declare in a string the ``path`` to the simulator ::

                    >>> path = "path/to/simulator.so"
                    >>> scenario = "path/to/scenario.xml"
                    >>> simulator = Simulator.from_path(path,scenario) 

        """
        sim = cls(library_path=symuvia_path)
        sim.register_simulation(filename_path)
        return sim
