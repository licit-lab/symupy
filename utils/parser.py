from xmltodict import parse


class SimulatorRequest():

    def __init__(self):
        self._str_response = ""

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

    def get_vehicle_id(self) -> tuple:
        """Extracts vehicle ids information from simulators response

        :return: tuple containing vehicle ids at current state in all network
        :rtype: list
        """
        return tuple(veh.get('@id') for veh in self.get_vehicle_data())

    def query_vehicle_link(self, vehid: str) -> tuple:
        """Extracts current vehicle link information from simulators response

        :param vehid: vehicle link
        :type vehid: int
        :return: vehicle link in tuple form (checks duplicity)
        :rtype: tuple
        """
        return tuple(veh.get('@tron') for veh in self.get_vehicle_data() if veh.get('@id') == vehid)

    def query_vehicle_position(self, vehid: str, *args) -> tuple:
        """Extracts current vehicle distance on link information from simulators response

        :param vehid: vehicle distance information
        :type vehid: int
        :return: vehicle position float in tuple form (checks duplicity)
        :rtype: tuple
        """
        if not args:
            return tuple(float(veh.get('@dst'))
                         for veh in self.get_vehicle_data() if veh.get('@id') == vehid)
        vehids = set((vehid, *args))
        return tuple(float(veh.get('@dst'))
                     for veh in self.get_vehicle_data() if veh.get('@id') in vehids)

    def query_vehicle_neighbors(self):
        pass

    def vehicle_in_network(self, vehid: str, *args) -> bool:
        """True if veh id is in the network at current state, for multiple arguments
           True if all veh ids are in the network

        :param vehid: Integer of vehicle id, comma separated if testing for multiple
        :type vehid: int
        :return: True if vehicle is in the network otherwise false
        :rtype: bool
        """
        all_vehs = self.get_vehicle_id()
        if not args:
            return vehid in all_vehs
        vehids = set((vehid, *args))
        return set(vehids).issubset(set(all_vehs))

    def vehicle_in_link(self, link: str, lane: str = '1') -> tuple:
        """Returns a tuple containing vehicle ids traveling on the same link+lane at current state

        :param link: link name
        :type link: str
        :param lane: lane number, defaults to '1'
        :type lane: str, optional
        :return: tuple containing vehicle ids
        :rtype: tuple
        """
        return tuple(veh.get('@id')
                     for veh in self.get_vehicle_data()
                     if veh.get('@tron') == link and veh.get('@voie') == lane)

    def vehicle_downstream(self, vehid: str) -> tuple:
        """Get ids of vehicles downstream to vehid

        :param vehid: integer describing id of reference veh
        :type vehid: int
        :return: tuple with ids of vehicles ahead (downstream)
        :rtype: tuple
        """
        link = self.query_vehicle_link(vehid)[0]
        vehpos = self.query_vehicle_position(vehid)[0]

        vehids = set(self.vehicle_in_link(link))
        neigh = vehids.difference(set(vehid))

        neighpos = self.query_vehicle_position(*neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if float(npos) > float(vehpos))

    def vehicle_upstream(self, vehid: str) -> tuple:
        """Get ids of vehicles upstream to vehid

        :param vehid: integer describing id of reference veh
        :type vehid: int
        :return: tuple with ids of vehicles behind (upstream)
        :rtype: tuple
        """
        link = self.query_vehicle_link(vehid)[0]
        vehpos = self.query_vehicle_position(vehid)[0]

        vehids = set(self.vehicle_in_link(link))
        neigh = vehids.difference(set(vehid))

        neighpos = self.query_vehicle_position(*neigh)

        return tuple(nbh for nbh, npos in zip(neigh, neighpos) if float(npos) < float(vehpos))

    @property
    def data_query(self):
        return parse(self._str_response)

    @property
    def get_current_time(self) -> str:
        return self.data_query.get('INST').get('@val')

    @property
    def get_current_nbveh(self) -> int:
        return self.data_query.get('INST').get('@nbVeh')
