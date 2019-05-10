from xmltodict import parse


class SimulatorRequest():

    def __init__(self):
        self._data_query = {}

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
        if self._data_query.get('INST').get('TRAJ') is not None:
            return self._data_query.get('INST').get('TRAJ').get('TRAJS')
        return []

    def update_vehicle_pos(self, control):
        raise NotImplementedError
