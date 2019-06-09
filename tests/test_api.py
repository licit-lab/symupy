# sim_instance.run_simulation(sim_file)

import os
import unittest
from symupy.api import Simulation, Simulator


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.get_simulator()

    def test_load_symuvia_osx(self):
        self.sim_instance = Simulator(self.sim_path)
        self.sim_instance.load_symuvia()
        self.assertEqual(self.sim_instance.libraryname,
                         self.sim_path)

    def get_simulator(self):
        self.libpath = ("symupy", "lib", "darwin", "libSymuVia.dylib")
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)


class TestBottleneck001(unittest.TestCase):

    def setUp(self):
        self.get_simulator()
        self.get_bottleneck_001()

    def test_load_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        self.assertEqual(sim_case.filename, self.mocks_path)

    def test_get_simulation_data_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_param = sim_case.get_simulation_parameters()
        PAR = ({'id': 'simID',
                'pasdetemps': '1',
                'debut': '00:00:00',
                'fin': '00:00:30',
                'loipoursuite': 'exacte',
                'comportementflux': 'iti',
                'date': '1985-01-17',
                'titre': '',
                'proc_deceleration': 'false',
                'seed': '1'},
               {'id': 'simID2',
                'pasdetemps': '1',
                'debut': '00:00:00',
                'fin': '00:00:30',
                'loipoursuite': 'exacte',
                'comportementflux': 'iti',
                'date': '1985-01-17',
                'titre': '',
                'proc_deceleration': 'false',
                'seed': '1'})
        self.assertTupleEqual(sim_param, PAR)

    def test_get_vehicletype_data_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_vehtype = sim_case.get_vehicletype_information()
        VEH_TYPE = ({'id': 'VL',
                     'w': '-5.8823',
                     'kx': '0.17',
                     'vx': '25'},
                    {'id': 'VL2',
                     'w': '-5.8823',
                     'kx': '0.17',
                     'vx': '25'})
        self.assertTupleEqual(sim_vehtype, VEH_TYPE)

    def test_get_network_endpoints_botleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_endpoints = sim_case.get_network_endpoints()
        END_POINTS = ('Ext_In',
                      'Ext_Out',)
        self.assertTupleEqual(sim_endpoints, END_POINTS)

    def test_run_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.load_symuvia()
        sim_instance.run_simulation(sim_case)

    @unittest.skip("Skipping momentary")
    def test_initialize_container_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        with sim_instance as s:
            while s.do_next:
                # TODO: This needs some work on Parser.py
                s.data.get_vehicle_data()

    def test_create_vehicle_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

      # with
        sim_instance.load_symuvia()
        sim_instance.load_network()
        sim_instance.init_simulation()
        veh_id = sim_instance.create_vehicle("VL", "Ext_In", "Ext_Out")
        self.assertGreaterEqual(veh_id, 0)

    def test_create_drive_vehicle_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        # with
        # REVIEW: For the sake of simplicity the vehicle will be created after an entering vehicle has been created.
        with sim_instance as s:
            while s.do_next:
                s.request_answer()  # Initialize
                s.request_answer()  # Vehicle 0
                veh_id = s.create_vehicle("VL", "Ext_In", "Ext_Out")
                s.request_answer()  # Vehicle instantiation
                drive_status = s.drive_vehicle(veh_id, 20.0, "Zone_001")
                s.stop_step()

        self.assertGreaterEqual(veh_id, 0)
        self.assertEqual(drive_status, 1)
        self.assertAlmostEqual(
            float(sim_instance.data.query_vehicle_position('1')[0]), 20.0)

    def test_drive_vehicle_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

      # with
        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.data.vehicle_in_network('0'):
                    drive_status = s.drive_vehicle(0, 1.0)
                    s.run_step()
                    s.stop_step()
                    continue
                else:
                    continue
            self.assertEqual(drive_status, 1)
            self.assertAlmostEqual(
                float(sim_instance.data.query_vehicle_position('0')[0]), 1.0)

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

    def test_query_vehicles_upstream_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.data.vehicle_in_network('2'):
                    nup, = s.data.vehicle_upstream('1')
                    s.stop_step()
                    continue
                else:
                    continue
        self.assertEqual(nup, '2')

    def test_query_vehicles_downstream_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.data.vehicle_in_network('2'):
                    ndown, = s.data.vehicle_downstream('1')
                    s.stop_step()
                    continue
                else:
                    continue
        self.assertEqual(ndown, '0')

    def test_query_vehicle_neighbors_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        pass

    def test_fixed_leader_neighbors_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        pass

    def get_simulator(self):
        self.libpath = ("symupy", "lib", "darwin", "libSymuVia.dylib")
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)

    def get_bottleneck_002(self):
        self.file_name = "bottleneck_002.xml"
        file_path = ("symupy", "tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)


if __name__ == '__main__':
    unittest.main()
