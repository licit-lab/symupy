import os
from ctypes import cdll, create_string_buffer, c_int, byref, c_bool, c_double
from lxml import etree
from datetime import datetime

from symupy.utils import SymupyLoadLibraryError, SymupyFileLoadError
from symupy.utils import SimulatorRequest
from symupy.utils import timer_func
from symupy.utils import constants as ct

import typing


class Simulation(object):

    def __init__(self, file_name: str) -> None:
        if os.path.exists(file_name):
            self._file_name = file_name
        else:
            raise SymupyFileLoadError("File not found", file_name)

    def load_xml_tree(self) -> None:
        """ Load XML file_name"""
        tree = etree.parse(self._file_name)
        root = tree.getroot()
        self._xml_tree = root

    def get_simulation_parameters(self) -> dict:
        """ Get simulation parameters 

        :return: dictionary with XML parameters
        :rtype: dict
        """
        self.load_xml_tree()
        branch_tree = 'SIMULATIONS/SIMULATION'
        return self._xml_tree.xpath(branch_tree)[0].attrib

    def get_simulation_steps(self) -> int:
        t1 = datetime.strptime(
            self.get_simulation_parameters().get('debut'), ct.HOUR_FORMAT)
        t2 = datetime.strptime(
            self.get_simulation_parameters().get('fin'), ct.HOUR_FORMAT)
        t = t2 - t1
        n = t.seconds / \
            float(self.get_simulation_parameters().get('pasdetemps'))
        return range(int(n))

    @property
    def get_xml(self):
        return self._xml_tree

    @property
    def filename(self):
        return self._file_name

    @property
    def filename_enc(self):
        return self._file_name.encode('UTF8')


class Simulator(object):

    def __init__(self, path: str) -> None:
        self._path = path

    def load_symuvia(self) -> None:
        """ load SymuVia shared library """
        try:
            lib_symuvia = cdll.LoadLibrary(self._path)
        except OSError:
            raise SymupyLoadLibraryError("Library not found", self._path)
        self._library = lib_symuvia

    def load_network(self) -> None:
        """ load SymuVia Simulation File """
        if not hasattr(self, '_sim'):
            raise SymupyFileLoadError("File not provided", "")
        self._library.SymLoadNetworkEx(self._sim.filename_enc)

    def init_simulation(self) -> None:
        """ Initializes conditions for a step by step simulation"""
        # Pointers
        self._s_response = create_string_buffer(ct.BUFFER_STRING)
        self._b_end = c_int()
        # self._b_second = c_bool(True)
        # self._b_force = c_int(1)
        self.data = SimulatorRequest()

    @timer_func
    def run_simulation(self, sim_object: Simulation) -> None:
        """ Run simulation in a single shot

        Args:
            sim_object (Simulation): Valid simulation scenario

        Returns:
            None: No returns provided, only internal updates
        """
        self.register_simulation(sim_object)
        self.load_symuvia()
        self._library.SymRunEx(self._sim.filename_enc)

    def register_simulation(self, sim_object: Simulation) -> None:
        """Register simulation file within the simulator

        :param sim_object: Simulation scenario to register
        :type sim_object: Simulation
        :return: No value is returned
        :rtype: None
        """
        self._sim = sim_object

    @property
    def s_response_dec(self):
        """ Obtains instantaneous data from simulator

        :return: last query from simulator
        :rtype: str
        """
        return self._s_response.value.decode('UTF8')

    def run_step(self) -> None:
        """ Run simulation step by step"""
        try:
            self._bContinue = self._library.SymRunNextStepEx(self._s_response,
                                                             1,
                                                             byref(self._b_end)
                                                             )
            self._c_iter = next(self._n_iter)
            print(f"Step: {self._c_iter}")
            self.data.parse_data(self.s_response_dec)
        except StopIteration:
            self._bContinue = False

    def __enter__(self) -> None:
        """ Implementation as a context manager 
            TODO: Implement state machine ???
        """
        self.load_symuvia()
        self.load_network()
        self.init_simulation()
        self._n_iter = iter(self._sim.get_simulation_steps())
        self._c_iter = 0
        self._bContinue = True
        return self

    def __exit__(self, type, value, traceback) -> bool:
        return False

    @property
    def do_next(self) -> bool:
        return self._bContinue

    @property
    def get_request(self) -> dict:
        return self.data._data_query
