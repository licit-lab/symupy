""" This module implements a vehicle model.

    Vehicle model acts as an instance to modify vehicle's behaviour according to 
"""

from typing import List
from collections import OrderedDict
from dataclasses import dataclass, field
import numpy as np

from symupy.utils import constants as ct


@dataclass
class Vehicle(object):
    """Class for defining a vehicle
    """

    # Vehicle identity (comparison values)
    vehtype: str = field(default="")
    vehid: int = field(default=None)

    # Location
    abscisa: float = field(default=0.0, compare=False, metadata={"unit": "m"})
    ordinate: float = field(default=0.0, compare=False, metadata={"unit": "m"})
    link: str = field(default="", compare=False)
    lane: str = field(default="", compare=False)

    # State
    distance: float = field(default=0.0, compare=False, metadata={"unit": "m"})
    speed: float = field(default=0.0, compare=False, metadata={"unit": "m/s"})
    acceleration: float = field(default=0.0, compare=False, metadata={"unit": "m/s^2"})
    elevation: float = field(default=0.0, compare=False, metadata={"unit": "m"})

    # Internal states
    totaldistance: float = field(default=0.0, compare=False, metadata={"unit": "m"})

    def update_state(self, dataveh: OrderedDict):
        """Updates data within the structure with 
        
        :param dataveh: [description]
        :type dataveh: OrderedDict
        """
        dct_format = Vehicle.format_dict(dataveh)
        self.__dict__ = dct_format

    def vehicle_sensor(self):
        """ Implement vehicle sensor 
        """
        return np.array((self.distance, self.speed, self.acceleration))

    # TODO: Accept other car following laws
    # TODO: Get environment
    # TODO: Organice matrix external info
    # TODO: Implement xi+ =  f(yi,ui) ->vector
    # TODO: Implement xi+ =  f(yi,ui,yinb,uinb) ->vector?
    # TODO: Implement xi+= f(y,u) ->vector
    # TODO: Perform update coherently via update_state or

    @staticmethod
    def format_dict(dataveh: OrderedDict) -> dict:
        """ This function creates the dictionary 
               {"abscisa":       float(data),
                "acceleration":  float(data),
                "distance":      float(data),
                "vehid":         int(data),
                "ordinate":      float(data),
                "link":          str (data),
                "vehtype":       str (data),
                "speed":         float(data),
                "lane":          str (data),
                "elevation":     float(data),
               } 
        
        :param dataveh: Ordered Dictionary from XML query
        :type dataveh: OrderedDict
        :return: Dictionary as in description
        :rtype: [type]
        """
        return {ct.FIELD_DATA[key]: ct.FIELD_FORMAT[key](val) for key, val in dataveh.items()}

    @classmethod
    def from_response(cls, dataveh: OrderedDict):
        """Constructor for the class from a specific dictionary
        
        :param dataveh: Ordered dictionary from XML query
        :type dataveh: OrderedDict
        :return: Vehicle object
        :rtype: [type]
        """
        return cls(**Vehicle.format_dict(dataveh))


lstordct = List[OrderedDict]
lstvehs = List[Vehicle]


@dataclass
class VehicleList(object):
    """Class for defining a list of vehicles
    """

    vehicles: List[Vehicle] = field(default_factory=list)

    def update_list(self, newvehs: lstvehs):
        """ Appends a new list of vehicles

        :param vehlist: List of vehicles
        :type vehlist: lstordct
        """
        for veh in newvehs:
            if veh not in self.vehicles:
                self.vehicles.append(veh)

    def __str__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in veh.__dict__.items()) for veh in self.vehicles
        )

    def __repr__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in veh.__dict__.items()) for veh in self.vehicles
        )

    def __iter__(self):
        self.iterveh = iter(self.vehicles)
        return self

    def __next__(self):
        return next(self.iterveh)

    def __contains__(self, veh: Vehicle):
        return veh.vehid in self.get_vehid

    @classmethod
    def from_request(cls, vehlistdct: lstordct):
        """Constructs a vehicle list from a list of ordered dictionaries (simulator repsonse)

        :param vehlist: list containing vehicle data in ordered dict format
        :type vehlist: list
        :return: vehicle list containing list of vehicle data classes
        :rtype: VehicleList
        """
        return cls([Vehicle.from_response(d) for d in vehlistdct])

    @property
    def get_vehid(self):
        return [v.vehid for v in self.vehicles]
