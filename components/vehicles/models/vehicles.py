from collections import OrderedDict


class Vehicle(object):
    """Class for defining a vehicle
    """

    clsvehid = 0

    def __init__(self, vehid: str):
        self.__class__.clsvehid += 1
        self.vehid = vehid

    def __repr__(self):
        return f"{self.__class__.__name__}({self.vehid})"

    def __str__(self):
        return f"Vehicle id: {self.vehid}, Vehicle clsid:{self.clsvehid}"

    def plug_vehicle_to_sim(self):
        raise NotImplementedError

    def attach_veh_data(self):
        raise NotImplementedError

    @classmethod
    def from_response(cls):
        raise NotImplementedError
