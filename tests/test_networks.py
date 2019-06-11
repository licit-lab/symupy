import os
import unittest
from symupy.api import Simulation, Simulator
from symupy.components import RoadSideUnit, V2INetwork, Vehicle


class TestBottleneck001(unittest.TestCase):
    def setUp(self):
        self.get_simulator()
        self.get_bottleneck_001()

    def test_load_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        self.assertEqual(sim_case.filename, self.mocks_path)

    def test_create_rsu_bottleneck001(self):
        sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

        rsu = RoadSideUnit("Zone_001", 0.0)
        v2i_net = V2INetwork()
        v2i_net.register_element(rsu)

        sim_instance.register_network(v2i_net)

        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.data.vehicle_in_network("0"):
                    v = Vehicle("0")
                    v.plug_vehicle_to_sim(s)
                    s.log_vehicle_in_network(v, v2i_net)
                    ## TODO: To finish

        self.assertEqual(self.mocks_path, sim_instance.casename)

    def get_simulator(self):
        self.libpath = ("symupy", "lib", "darwin", "libSymuVia.dylib")
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)

    def get_bottleneck_001(self):
        self.file_name = "bottleneck_001.xml"
        file_path = ("symupy", "tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)


class TestBottleneck002(unittest.TestCase):
    def setUp(self):
        self.get_simulator()
        self.get_bottleneck_002()

    def test_load_bottleneck_002(self):
        sim_case = Simulation(self.mocks_path)
        self.assertEqual(sim_case.filename, self.mocks_path)

    def get_simulator(self):
        self.libpath = ("symupy", "lib", "darwin", "libSymuVia.dylib")
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)

    def get_bottleneck_002(self):
        self.file_name = "bottleneck_002.xml"
        file_path = ("symupy", "tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)


if __name__ == "__main__":
    unittest.main()
