from xmltodict import parse


class SimulatorRequest():

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return 'Sim Time: {}, VehInNetwork: {}'.format(self.get_current_time, self.get_current_nbveh) if self.data_query else 'Simulation has not started'

    def parse_data(self, response: str = None) -> dict:
        """Parses response from simulator to data

        :param response: Simulator response
        :type response: str
        :return: Full simulator response
        :rtype: dict
        """
        self._str_response = response

    def get_vehicle_data(self) -> list:
        """Extracts vehicles information from simulators response

        :param response: Simulator response
        :type response: str
        :return: list of vehicles in the network
        :rtype: list of dictionaries
        """
        if self.data_query.get('INST').get('TRAJS') is not None:
            veh_data = self.data_query.get('INST').get('TRAJS')
            if isinstance(veh_data['TRAJ'], list):
                return veh_data['TRAJ']
            return [veh_data['TRAJ']]
        return []

    def get_vehicle_id(self) -> list:
        """Extracts vehicle ids information from simulators response

        :return: list of vehicle ids
        :rtype: list
        """
        veh_data = self.get_vehicle_data()
        if veh_data:
            return [int(veh.get('@id')) for veh in veh_data]
        return []

    def query_vehicle_link(self, vehid: int) -> tuple:
        """Extracts current vehicle link information from simulators response

        :param vehid: vehicle link
        :type vehid: int
        :return: vehicle link in tuple form (checks duplicity)
        :rtype: tuple
        """
        return tuple(veh.get('@tron') for veh in self.get_vehicle_data())

    def query_vehicle_position(self, vehid: int) -> tuple:
        """Extracts current vehicle distance information from simulators response

        :param vehid: vehicle distance information
        :type vehid: int
        :return: vehicle position float in tuple form (checks duplicity)
        :rtype: tuple
        """
        return tuple(float(veh.get('@dst'))
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

    def vehicles_downstream_link(self, vehid: int) -> tuple:
        """Get ids of vehicles downstream to vehid 

        :param vehid: integer describing id of reference veh
        :type vehid: int
        :return: tuple with ids of vehicles ahead (downstream)
        :rtype: tuple
        """
    @property
    def data_query(self):
        return parse(self._str_response)

    @property
    def get_current_time(self) -> str:
        return self.data_query.get('INST').get('@val')

    @property
    def get_current_nbveh(self) -> int:
        return self.data_query.get('INST').get('@nbVeh')
