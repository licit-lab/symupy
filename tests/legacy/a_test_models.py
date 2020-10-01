"""
    Unit test for Models
"""

# ---------------------------IMPORTS------------------------------------------

# Internals
from symupy.func import dynamic_2nd, dynamic_3rd, VehDynamic, Vehicle
from symupy.func import VehParameter, SimParameter

# Utils
import unittest
import numpy as np
from numpy.testing import assert_almost_equal

# ---------------------------CONSTANTS----------------------------------------

# Create a simulation timings
T_STP = 0.01
T_HOR = 0.5
T_SIM = 60

sim_par = SimParameter(T_STP, T_HOR, T_SIM)

# Create a vehicle model / Provided originally by the simulator
U_FFS = 25.0
K_X = 0.16
W_CGT = 6.25
L_VEH = 4.0

S0 = 10.0

veh_par = VehParameter.VehParameterSym(U_FFS, K_X, W_CGT, L_VEH)

# ---------------------------TESTS-------------------------------------------


class TestModel(unittest.TestCase):
    def test_constructor(self):
        """
        Test Vehicle class generation
        """
        # veh_par = VehParameter()
        veh_1 = Vehicle(sim_par, veh_par, dynamic_2nd)
        self.assertTrue(isinstance(veh_1, Vehicle))
        self.assertEqual(veh_1.n_veh, 1)

    def test_consistancy(self):
        """
        consistancy VehDynamic i.e. #inputs = #outputs
        """
        self.assertTrue(True)

    def test_dynamics2nd(self):
        """
        Check outcomes from 2nd order dynamics
        """
        veh_par = VehParameter()
        sim_par = SimParameter()
        self.assertEqual(sim_par.t_stp, 0.01)

        # Matrix dynamics
        A = np.array([[1, 0, sim_par.t_stp], [0, 1, 0], [0, 0, 1]])
        B1 = np.array([[0], [sim_par.t_stp], [-sim_par.t_stp]])
        B2 = np.array([[0], [0], [sim_par.t_stp]])

        # invariant
        veh_cst = np.array([0.0, 25.0, 0])
        veh_nif = np.array([0])
        veh_ctr = np.array([0])
        veh_ust = dynamic_2nd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)

        # change
        veh_ctr = np.array([0.01])
        veh_ust = dynamic_2nd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)

        # propagation from veh_ust
        veh_cst = veh_ust
        veh_ust = dynamic_2nd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)

    def test_dynamics3rd(self):
        """
        Check outcomes from 3rd order dynamics
        """
        veh_par = VehParameter()
        sim_par = SimParameter()
        self.assertEqual(sim_par.t_stp, 0.01)

        # Matrix dynamics
        A = np.array(
            [
                [1, 0, sim_par.t_stp, 0],
                [0, 1, 0, sim_par.t_stp],
                [0, 0, 1, -sim_par.t_stp],
                [0, 0, 0, (1 - sim_par.t_stp / veh_par.v_lag)],
            ]
        )
        B1 = np.array([[0], [0], [0], [sim_par.t_stp / veh_par.v_lag]])
        B2 = np.array([[0], [0], [0], [-sim_par.t_stp / veh_par.v_lag]])

        # invariant
        veh_cst = np.array([0.0, 25.0, 0, 0])
        veh_nif = np.array([0])
        veh_ctr = np.array([0])
        veh_ust = dynamic_3rd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)

        # change
        veh_ctr = np.array([0.01])
        veh_ust = dynamic_3rd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)

        # propagation
        veh_cst = veh_ust
        veh_ust = dynamic_3rd(veh_cst, veh_nif, veh_ctr, veh_par, sim_par)
        val_ust = A @ veh_cst + B1 @ veh_ctr + B2 @ veh_nif
        assert_almost_equal(veh_ust, val_ust)


if __name__ == "__main__":
    unittest.main()
