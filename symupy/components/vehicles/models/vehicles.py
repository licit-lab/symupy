""" 
Vehicle Model
=============
This module implements a vehicle model.

Vehicle model acts as an instance to trace individual vehicle data and modify vehicle behavior according to given dynamics
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

from typing import Dict, List
from collections import OrderedDict
import itertools
import numpy as np
import pandas as pd
from dataclasses import dataclass, asdict


# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.logic.subscriber import Subscriber
from symupy.utils import constants as ct
from .dynamics import VehicleDynamic
from symupy.logic.sorted_frozen_set import SortedFrozenSet

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


@dataclass
class Vehicle(Subscriber):
    """ Vehicle class defined for storing data on a single vehicle: 

        You need a Publisher from where the vehicle is going to take data: 

        Args: 
            request (Publisher): Parser or object publishing data
        
        Retunrns: 
            vehicle (Vehicle): A Dataclass with vehicle parameters

        ============================  =================================
        **Variable**                  **Description**
        ----------------------------  ---------------------------------
        ``abscissa``                    Current coordinate on y axis
        ``acceleration``                Current acceleration
        ``distance``                    Current distance traveled on link
        ``elevation``                   Current elevation
        ``lane``                        Current lane
        ``link``                        Current road vehicle is traveling
        ``ordinate``                    Current coordinate x axis
        ``speed``                       Current speed
        ``vehid``                       Vehicle id
        ``vehtype``                     Vehicle class
        ============================  =================================

        Example: 
            This is one example on how to register a new vehicle ::

            >>> req = SimulatorRequest()
            >>> veh = Vehicle(req)
            >>> req.dispatch() # This will update vehicle data

        When having multiple vehicles please indicate the `vehid` before launching the dispatch method. This is because the vehicle object is looks for a vehicle id within the data. 

        Example: 
            This is one example on how to register two vehicles ::

            >>> req = SimulatorRequest()
            >>> veh1 = Vehicle(req, vehid=0)
            >>> veh2 = Vehicle(req, vehid=1)
            >>> req.dispatch() # This will update vehicle data on both vehicles


    """

    counter = itertools.count()
    abscissa: float = 0.0
    acceleration: float = 0.0
    distance: float = 0.0
    driven: bool = False
    elevation: float = 0.0
    lane: int = 1
    link: str = "Zone_001"
    ordinate: float = 0.0
    speed: float = 25.0
    vehid: int = 0
    vehtype: str = ""

    def __init__(self, request, **kwargs):
        """ This initializer creates a Vehicle
        """
        # Undefined properties
        self.count = next(self.__class__.counter)
        self.dynamic = VehicleDynamic()
        self.itinerary = []

        # Optional properties
        for key, value in kwargs.items():
            setattr(self, key, value)

        super().__init__(request)

    def __hash__(self):
        return hash((type(self), self.vehid))

    def __eq__(self, veh):
        if not isinstance(veh, type(self)):
            return NotImplemented
        return self.vehid == veh.vehid

    def update(self):
        """ Updates data from publisher 
        """
        dataveh = self._publisher.get_vehicle_properties(self.vehid)
        self.__dict__.update(**dataveh)

        link = getattr(self, "link")
        if link not in getattr(self, "itinerary"):
            self.itinerary.append(link)

    @property
    def x(self):
        """Vehicle state vector (x,v,a)"""
        return np.array((self.distance, self.speed, self.acceleration))


lstordct = List[OrderedDict]
lstvehs = List[Vehicle]


class VehicleList(SortedFrozenSet):
    """ Class defining a set of vehicles 
    """

    def __init__(self, request):
        self._request = request
        data = [Vehicle(request, **v) for v in request.get_vehicle_data()]
        super().__init__(data)

    def update_list(self):
        """ Update vehicle data according to an update in the request.
        """
        data = self + VehicleList(self._request)
        self._items = data._items

    def _get_vehicles_attribute(self, attribute: str) -> pd.Series:
        """ Retrieve list of parameters 
        
            Args: 
                attribute (str): One of the vehicles attribute e.g. 'distance'
            
            Returns 
                dataframe (series): Returns values for a set of vehicles 
        """
        return self._to_pandas()[attribute]

    @property
    def acceleration(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("acceleration")

    @property
    def speed(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("speed")

    @property
    def distance(self) -> pd.Series:
        """
            Returns all vehicle's accelerations 
        """
        return self._get_vehicles_attribute("distance")

    def _to_pandas(self) -> pd.DataFrame:
        """ Transforms vehicle list into a pandas for rendering purposes 
        
            Returns: 
                df (DataFrame): Returns a table with pandas data.

        """
        return pd.DataFrame([asdict(v) for v in self._items])

    def __str__(self):
        if not self._items:
            return "No vehicles have been registered"
        return str(self._to_pandas())

    def __repr__(self):
        if not self._items:
            return "No vehicles have been registered"
        return repr(self._to_pandas())
