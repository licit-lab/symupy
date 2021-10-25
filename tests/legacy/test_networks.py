import os
import unittest

# from symupy.api import Simulation, Simulator
# from symupy.components import RoadSideUnit, V2INetwork, Vehicle, VehicleList
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

#     # @unittest.skip("Skipping momentary")
#     def test_create_rsu_bottleneck_001(self):
#         sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

#         rsu = RoadSideUnit("Zone_001", 0.0)
#         v2i_net = V2INetwork()
#         v2i_net.register_element(rsu)

#         sim_instance.register_network(v2i_net)

#         with sim_instance as s:
#             while s.do_next:
#                 s.run_step()
#                 if s.state.is_vehicle_in_network("0"):
#                     s.state.create_vehicle_list()
#                     x = 1
#                     # v = Vehicle("0")
#                     # v.plug_vehicle_to_sim(s)
#                     # s.log_vehicle_in_network(v, v2i_net)
#                     ## TODO: To finish
#         x = 2
#         self.assertEqual(self.mocks_path, sim_instance.casename)


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

#     def test_create_rsu_bottleneck_002(self):
#         sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

#         rsu = RoadSideUnit("Zone_001", 0.0)
#         v2i_net = V2INetwork()
#         v2i_net.register_element(rsu)

#         sim_instance.register_network(v2i_net)

#         with sim_instance as s:
#             while s.do_next:
#                 s.run_step()
#                 if s.state.is_vehicle_in_network("0"):
#                     s.state.update_vehicle_list()
#                 if s.state.is_vehicle_in_network("1"):
#                     s.state.update_vehicle_list()
#                 if s.state.is_vehicle_in_network("2"):
#                     s.state.update_vehicle_list()
#         x = 2
#         self.assertEqual(self.mocks_path, sim_instance.casename)


# if __name__ == "__main__":
#     unittest.main()
