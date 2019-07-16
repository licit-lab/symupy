""" This module implements a vehicle model.

    Vehicle model acts as an instance to modify vehicle's behaviour according to 
"""

from typing import Dict, List
from collections import OrderedDict
from dataclasses import dataclass, field
import numpy as np

from symupy.utils import constants as ct

from .dynamics import dynamic_3rd_ego, dynamic_2nd_ego

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
    totaldistance: float = field(default=distance, compare=False, metadata={"unit": "m"})

    def update_state(self, dataveh: OrderedDict):
        """Updates data within the structure with 
        
        :param dataveh: [description]
        :type dataveh: OrderedDict
        """
        dct_format = Vehicle.format_dict(dataveh)
        self.__dict__ = dct_format

    @property
    def C(self):
        """Output matrix"""
        return self.__output_matrix

    def activate_sensor(self, **kwargs) -> None:
        """Define the observation matrix and observed states in the vehicle
           
           vehicle.activate_sensor(speed=True,position=True)
        
        :return: Set the observation matrix __output_matrix
        :rtype: None
        """
        dct_idx = {"position": 0, "speed": 1, "acceleration": 2}
        C = np.zeros([len(kwargs.keys()), 3])
        for key in kwargs.keys():
            idx = dct_idx.get(key)
            C[idx][idx] = kwargs.get(key, 0)
        self.__output_matrix = C

    @property
    def vector_state(self) -> np.array:
        """Vehicle state vector (x,v,a)"""
        return np.array((self.distance, self.speed, self.acceleration))

    @property
    def observed_state(self) -> np.array:
        """ Return observed states via C@(x,v,a)"""
        return self.C @ self.vector_state

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
        data = {ct.FIELD_DATA[key]: ct.FIELD_FORMAT[key](val) for key, val in dataveh.items()}
        data["totaldistance"] = data["distance"]  # Complementary information
        return data

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


class VehicleList(object):
    """Class for defining a list of vehicles
    """

    def __init__(self, newvehs: lstvehs):
        self.vehicles = {}
        for veh in newvehs:
            self.vehicles[veh.vehid] = veh

    def update_list(self, newvehs: lstvehs):
        """ Appends a new list of vehicles

        :param vehlist: List of vehicles
        :type vehlist: lstordct
        """
        for veh in newvehs:
            self.vehicles[veh.vehid] = veh

    def __str__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in veh.__dict__.items()) for veh in self.vehicles.values()
        )

    def __repr__(self):
        if not self.vehicles:
            return "No vehicles have been registered"
        return "\n".join(
            ", ".join(f"{k}:{v}" for k, v in veh.__dict__.items()) for veh in self.vehicles.values()
        )

    def __iter__(self):
        self.iterveh = iter(self.vehicles.values())
        return self

    def __next__(self):
        return next(self.iterveh)

    def __contains__(self, veh: Vehicle):
        return veh.vehid in self.get_vehid

    def __getitem__(self, key: int):
        return self.vehicles[key]

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