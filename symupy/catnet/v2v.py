"""
    This module contains information related to different 
    networks existing in a traffic simulator 

    - V2V network 
    - Infrastructure network 
    - V2I network 
"""

import networkx as nx


class VehicleNetwork(object):
    pass


# class VehicleNetwork(dict):
#     """
#     Network of vehicles

#     sim_par: simulation parameter
#     vehicles: list of vehicle class
#     """

#     def __init__(self, sim_par: SimParameter,  vehicles: vehtype)->None:
#         self.sim_par = sim_par
#         self.veh_number = 0
#         self.veh_currentids = []
#         self.vehicles = OrderedDict()
#         self.append_vehicles(vehicles)
#         self.graph = None

#     def __iter__(self)->Iterable:
#         """
#         Iterator over all vehicles in the network
#         """
#         self.run = iter(self.vehicles.items())
#         return self.run

#     def __next__(self)->Tuple:
#         """
#         Iterate over all vehicles in the network
#         """
#         return next(self.run)

#     def __getitem__(self, key):
#         return self.vehicles[key]

#     def __len__(self):
#         return len(self.__dict__)

#     def initialize_vehicles(self, veh_init: Dict)-> None:
#         """
#         Initialize condition of a single or a set of vehicles
#         """
#         for veh_id, state0 in veh_init.items():
#             self.vehicles[veh_id].initialize_condition(state0)

#     def append_vehicles(self, vehicles: vehtype)->None:
#         """
#         Add a single or a set of vehicles to the network
#         """
#         if isinstance(vehicles, Vehicle):
#             self.vehicles[vehicles.id] = vehicles
#             self.veh_currentids.append(vehicles.id)
#             self.veh_number += 1
#             return
#         for veh in vehicles:
#             self.vehicles[veh.id] = veh
#             self.veh_currentids.append(veh.id)
#             self.veh_number += 1

#     def pop_vehicles(self, vehicles: vehtype)->None:
#         """
#         Delete a single or a set of vehicles to the network
#         """
#         if isinstance(vehicles, Vehicle):
#             del self.vehicles[vehicles.id]
#             self.veh_currentids.remove(vehicles.id)
#             self.veh_number -= 1
#             return
#         for veh in vehicles:
#             del self.vehicles[veh.id]
#             self.veh_currentids.remove(veh.id)
#             self.veh_number -= 1

#     def create_network(self)->None:
#         """
#         Creates a network object that allows to query leaders
#         information
#         """
#         self.graph = nx.DiGraph()
#         for veh_id, veh in self:
#             self.graph.add_node(veh)

#     def register_vehicle_link(self, veh_link: Dict)->None:
#         """
#         Register a list of predetermined edges for a vehicle

#         veh_link = {receiver: leader}
#         """
#         self.veh_link = veh_link

#         if not self.graph:
#             self.create_network()

#         for veh_id, leader_id in veh_link.items():
#             self.graph.add_edge(self.vehicles[veh_id],
#                                 self.vehicles[leader_id])

#     def get_neighbors(self, vehicle: Vehicle)->Vehicle:
#         """
#         Return the neighbors of a vehicle
#         """
#         return self.graph.neighbors(vehicle)

#     def launch_simulation(self)->None:
#         """
#         Start a simulation
#         """
#         # MISSING / USE CONNECTOR FOR SIMUYVIA
#         for it_step, t_step in self.sim_par:
#             print(it_step, t_step)
#             # self.OpCtrl.compute_control(self)
#             # self.apply_control()
