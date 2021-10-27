import os
import unittest
from symupy.runtime.api import Simulation, Simulator

# from symupy.components.vehicles import VehicleControl
import platform

# DCT_PATH = {"Darwin": "osx-64"}
# DCT_LFN = {"Darwin": "libSymuFlow.dylib"}
# _platform = platform.system()
# _libpath = DCT_PATH.get(_platform)
# _libfilen = DCT_LFN.get(_platform)


# class TestBottleneck001(unittest.TestCase):
#     def setUp(self):
#         self.get_simulator()
#         self.get_bottleneck_001()

#     def get_simulator(self):
#         self.libpath = ("lib", _libpath, _libfilen)
#         self.sim_path = os.path.join(os.getcwd(), *self.libpath)

#     def get_bottleneck_001(self):
#         self.file_name = "bottleneck_001.xml"
#         file_path = ("tests", "mocks", "bottlenecks", self.file_name)
#         self.mocks_path = os.path.join(os.getcwd(), *file_path)

#     def test_load_bottleneck_001(self):
#         sim_case = Simulation(self.mocks_path)
#         self.assertEqual(sim_case.filename, self.mocks_path)

#     def test_reduce_speed_bottleneck_001(self):
#         sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)
#         flag = False
#         link = sim_instance.simulation.get_network_links()[0]
#         with sim_instance as s:
#             while s.do_next:
#                 s.run_step()
#                 if s.state.is_vehicle_in_link("0", link):
#                     flag = True

#         self.assertTrue(flag)


# class TestBottleneck002(unittest.TestCase):
#     def setUp(self):
#         self.get_simulator()
#         self.get_bottleneck_002()

#     def get_simulator(self):
#         self.libpath = ("lib", _libpath, _libfilen)
#         self.sim_path = os.path.join(os.getcwd(), *self.libpath)

#     def get_bottleneck_002(self):
#         self.file_name = "bottleneck_002.xml"
#         file_path = ("tests", "mocks", "bottlenecks", self.file_name)
#         self.mocks_path = os.path.join(os.getcwd(), *file_path)

#     def test_load_bottleneck_002(self):
#         sim_case = Simulation(self.mocks_path)
#         self.assertEqual(sim_case.filename, self.mocks_path)

#     def test_reduce_speed_bottleneck_002(self):
#         sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)
#         flag = False
#         links = sim_instance.simulation.get_network_links()[0]
#         with sim_instance as s:
#             while s.do_next:
#                 s.run_step()
#                 if s.state.is_vehicle_in_link("0", links) and s.state.is_vehicle_in_link(
#                     "1", links
#                 ):
#                     flag = True
#         self.assertTrue(flag)

#     def test_is_vehicle_in_network_bottleneck_002(self):
#         sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

#         flag0, flag1, flag2 = False, False, False
#         with sim_instance as s:
#             while s.do_next:
#                 s.run_step()
#                 if s.state.is_vehicle_in_network("0", "1"):
#                     flag0 = True
#                 if s.state.is_vehicle_in_network("1"):
#                     flag1 = True
#                 if s.state.is_vehicle_in_network("2"):
#                     flag2 = True
#         self.assertTrue(flag0)
#         self.assertTrue(flag1)
#         self.assertTrue(flag2)
