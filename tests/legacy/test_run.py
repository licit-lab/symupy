import os
import unittest
from symupy.runtime.api import Simulation, Simulator
import platform


class TestBottleneck001(unittest.TestCase):
    def setUp(self):
        self.get_simulator()
        self.get_bottleneck_001()

    def get_simulator(self):
        self.libpath = ("lib", _libpath, _libfilen)
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)

    def get_bottleneck_001(self):
        self.file_name = "bottleneck_001.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)

    @unittest.skip("Skipping momentary")
    def test_load_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        self.assertEqual(sim_case.filename, self.mocks_path)

    @unittest.skip("Skipping momentary")
    def test_constructor_bottleneck_001(self):
        sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)
        self.assertEqual(self.mocks_path, sim_instance.casename)

    @unittest.skip("Skipping momentary")
    def test_get_simulation_data_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_param = sim_case.get_simulation_parameters()
        PAR = (
            {
                "id": "simID",
                "pasdetemps": "1",
                "debut": "00:00:00",
                "fin": "00:00:30",
                "loipoursuite": "exacte",
                "comportementflux": "iti",
                "date": "1985-01-17",
                "titre": "",
                "proc_deceleration": "false",
                "seed": "1",
            },
            {
                "id": "simID2",
                "pasdetemps": "1",
                "debut": "00:00:00",
                "fin": "00:00:30",
                "loipoursuite": "exacte",
                "comportementflux": "iti",
                "date": "1985-01-17",
                "titre": "",
                "proc_deceleration": "false",
                "seed": "1",
            },
        )
        self.assertTupleEqual(sim_param, PAR)

    @unittest.skip("Skipping momentary")
    def test_get_vehicletype_data_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_vehtype = sim_case.get_vehicletype_information()
        VEH_TYPE = (
            {"id": "VL", "w": "-5.8823", "kx": "0.17", "vx": "25"},
            {"id": "VL2", "w": "-5.8823", "kx": "0.17", "vx": "25"},
        )
        self.assertTupleEqual(sim_vehtype, VEH_TYPE)

    @unittest.skip("Skipping momentary")
    def test_get_network_endpoints_botleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_endpoints = sim_case.get_network_endpoints()
        END_POINTS = ("Ext_In", "Ext_Out")
        self.assertTupleEqual(sim_endpoints, END_POINTS)

    @unittest.skip("Skipping momentary")
    def test_run_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.load_symuvia()
        sim_instance.run_simulation(sim_case)

    @unittest.skip("Skipping momentary")
    def test_run_simulation_alternative_constructor_bottleneck_001(self):
        sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)
        sim_instance.run_simulation()

    @unittest.skip("Skipping momentary")
    def test_run_stepbystep_bottleneck_001(self):
        # Using new constructor
        sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

        with sim_instance as s:
            while s.do_next:
                s.run_step()

    @unittest.skip("Skipping momentary")
    def test_initialize_container_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        with sim_instance as s:
            while s.do_next:
                # TODO: This needs some work on Parser.py
                s.state.get_vehicle_data()

    @unittest.skip("Skipping momentary")
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

    @unittest.skip("Skipping momentary")
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
            float(sim_instance.state.query_vehicle_position("1")[0]), 20.0
        )

    @unittest.skip("Skipping momentary")
    def test_drive_vehicle_bottleneck_001(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        # with
        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.state.is_vehicle_in_network("0"):
                    drive_status = s.drive_vehicle(0, 1.0)
                    s.run_step()
                    drive_status = s.drive_vehicle(0, 1.0)
                    s.stop_step()
                    continue
                else:
                    continue
            self.assertEqual(drive_status, 1)
            self.assertAlmostEqual(
                float(sim_instance.state.query_vehicle_position("0")[0]), 1.0
            )


class TestBottleneck002(unittest.TestCase):
    def setUp(self):
        self.get_simulator()
        self.get_bottleneck_002()

    def get_simulator(self):
        self.libpath = ("lib", _libpath, _libfilen)
        self.sim_path = os.path.join(os.getcwd(), *self.libpath)

    def get_bottleneck_002(self):
        self.file_name = "bottleneck_002.xml"
        file_path = ("tests", "mocks", "bottlenecks", self.file_name)
        self.mocks_path = os.path.join(os.getcwd(), *file_path)

    @unittest.skip("Skipping momentary")
    def test_load_bottleneck_002(self):
        sim_case = Simulation(self.mocks_path)
        self.assertEqual(sim_case.filename, self.mocks_path)

    @unittest.skip("Skipping momentary")
    def test_run_bottleneck_002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.load_symuvia()
        sim_instance.run_simulation(sim_case)

    @unittest.skip("Skipping momentary")
    def test_run_stepbystep_bottleneck_002(self):
        # Using new constructor
        sim_instance = Simulator.from_path(self.mocks_path, self.sim_path)

        with sim_instance as s:
            while s.do_next:
                s.run_step()

    @unittest.skip("Skipping momentary")
    def test_query_vehicles_upstream_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.state.is_vehicle_in_network("2"):
                    (nup,) = s.state.vehicle_upstream_of("1")
                    s.stop_step()
                    continue
                else:
                    continue
        self.assertEqual(nup, "2")

    @unittest.skip("Skipping momentary")
    def test_query_vehicles_downstream_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)

        with sim_instance as s:
            while s.do_next:
                s.run_step()
                if s.state.is_vehicle_in_network("2"):
                    (ndown,) = s.state.vehicle_downstream_of("1")
                    s.stop_step()
                    continue
                else:
                    continue
        self.assertEqual(ndown, "0")

    @unittest.skip("Skipping momentary")
    def test_query_vehicle_neighbors_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        pass

    @unittest.skip("Skipping momentary")
    def test_fixed_leader_neighbors_bottleneck002(self):
        sim_case = Simulation(self.mocks_path)
        sim_instance = Simulator(self.sim_path)
        sim_instance.register_simulation(sim_case)
        pass
