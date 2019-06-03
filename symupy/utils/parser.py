from xmltodict import parse


class SimulatorRequest():

    def __init__(self):
        self._data_query = {}

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return 'Sim Time: {}, VehInNetwork: {}'.format(self.get_current_time, self.get_current_nbveh) if self._data_query else 'Simulation has not started'

    def parse_data(self, response: str = None) -> dict:
        """Parses response from simulator to data

        :param response: Simulator response
        :type response: str
        :return: Full simulator response
        :rtype: dict
        """
        self._str_response = response
        self._data_query = parse(self._str_response)

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

        :param response: Simulator response
        :type response: str
        :return: list of vehicles in the network
        :rtype: list of dictionaries
        """
        if self._data_query.get('INST').get('TRAJS') is not None:
            veh_data = self._data_query.get('INST').get('TRAJS')
            if isinstance(veh_data, list):
                return veh_data
            return [veh_data]
        return []

    def get_vehicle_id(self) -> list:
        """Extracts vehicle ids information from simulators response

        :return: list of vehicle ids
        :rtype: list
        """
        veh_data = self.get_vehicle_data()
        if veh_data:
            return [int(veh.get('TRAJ').get('@id')) for veh in veh_data]
        return []

    def query_vehicle_link(self, vehid: int) -> tuple:
        """Extracts current vehicle link information from simulators response

        :param vehid: vehicle link
        :type vehid: int
        :return: vehicle link in tuple form (checks duplicity)
        :rtype: tuple
        """
        return tuple(veh['TRAJ']['@tron'] for veh in self.get_vehicle_data())

    def query_vehicle_position(self, vehid: int) -> tuple:
        """Extracts current vehicle distance information from simulators response

        :param vehid: vehicle distance information
        :type vehid: int
        :return: vehicle position float in tuple form (checks duplicity)
        :rtype: tuple
        """
        return tuple(float(veh['TRAJ']['@dst'])
                     for veh in self.get_vehicle_data())

    def query_vehicle_neighbors(self):
        pass

    def vehicle_in_network(self, vehid: int) -> bool:
        """True if veh id is in the network at current state

        :param vehid: Integer of vehicle id
        :type vehid: int
        :return: True if vehicle is in the network otherwise false
        :rtype: bool
        """
        return vehid in self.get_vehicle_id()

    @property
    def get_current_time(self) -> str:
        return self._data_query.get('INST').get('@val')

    @property
    def get_current_nbveh(self) -> int:
        return self._data_query.get('INST').get('@nbVeh')
