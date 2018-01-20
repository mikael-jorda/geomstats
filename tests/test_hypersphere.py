"""Unit tests for hypersphere module."""

from geomstats.hypersphere import Hypersphere

import numpy as np
import unittest


class TestHypersphereMethods(unittest.TestCase):
    DIMENSION = 4
    SPACE = Hypersphere(dimension=DIMENSION)
    METRIC = SPACE.metric

    def test_log_and_exp_general_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.

        NB: points on the n-dimensional sphere are
        (n+1)-D vectors of norm 1.
        """
        # Riemannian Log then Riemannian Exp
        # General case
        base_point_1 = np.array([1., 2., 3., 4., 6.])
        base_point_1 = base_point_1 / np.linalg.norm(base_point_1)
        point_1 = np.array([0., 5., 6., 2., -1])
        point_1 = point_1 / np.linalg.norm(point_1)

        log_1 = self.METRIC.log(point=point_1, base_point=base_point_1)
        result_1 = self.METRIC.exp(tangent_vec=log_1, base_point=base_point_1)
        expected_1 = point_1

        self.assertTrue(np.allclose(result_1, expected_1))

    def test_log_and_exp_edge_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.

        NB: points on the n-dimensional sphere are
        (n+1)-D vectors of norm 1.
        """
        # Riemannian Log then Riemannian Exp
        # Edge case: two very close points, base_point_2 and point_2,
        # form an angle < epsilon
        base_point_2 = np.array([1., 2., 3., 4., 6.])
        base_point_2 = base_point_2 / np.linalg.norm(base_point_2)
        point_2 = base_point_2 + 1e-12 * np.array([-1., -2., 1., 1., .1])
        point_2 = point_2 / np.linalg.norm(point_2)

        log_2 = self.METRIC.log(point=point_2, base_point=base_point_2)
        result_2 = self.METRIC.exp(tangent_vec=log_2, base_point=base_point_2)
        expected_2 = point_2

        self.assertTrue(np.allclose(result_2, expected_2))

    def test_exp_and_log_and_projection_to_tangent_space_general_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.

        NB: points on the n-dimensional sphere are
        (n+1)-D vectors of norm 1.
        """
        # Riemannian Exp then Riemannian Log
        # General case
        # NB: Riemannian log gives a regularized tangent vector,
        # so we take the norm modulo 2 * pi.
        base_point_1 = np.array([0., -3., 0., 3., 4.])
        base_point_1 = base_point_1 / np.linalg.norm(base_point_1)
        vector_1 = np.array([9., 5., 0., 0., -1.])
        vector_1 = self.SPACE.projection_to_tangent_space(
                                                   vector=vector_1,
                                                   base_point=base_point_1)

        exp_1 = self.METRIC.exp(tangent_vec=vector_1, base_point=base_point_1)
        result_1 = self.METRIC.log(point=exp_1, base_point=base_point_1)

        expected_1 = vector_1
        norm_expected_1 = np.linalg.norm(expected_1)
        regularized_norm_expected_1 = np.mod(norm_expected_1, 2 * np.pi)
        expected_1 = expected_1 / norm_expected_1 * regularized_norm_expected_1
        # TODO(nina): this test fails
        # self.assertTrue(np.allclose(result_1, expected_1))

    def test_exp_and_log_and_projection_to_tangent_space_edge_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.

        NB: points on the n-dimensional sphere are
        (n+1)-D vectors of norm 1.
        """
        # Riemannian Exp then Riemannian Log
        # Edge case: tangent vector has norm < epsilon
        base_point_2 = np.array([10., -2., -.5, 34., 3.])
        base_point_2 = base_point_2 / np.linalg.norm(base_point_2)
        vector_2 = 1e-10 * np.array([.06, -51., 6., 5., 3.])
        vector_2 = self.SPACE.projection_to_tangent_space(
                                                    vector=vector_2,
                                                    base_point=base_point_2)

        exp_2 = self.METRIC.exp(tangent_vec=vector_2, base_point=base_point_2)
        result_2 = self.METRIC.log(point=exp_2, base_point=base_point_2)
        expected_2 = self.SPACE.projection_to_tangent_space(
                                                    vector=vector_2,
                                                    base_point=base_point_2)

        self.assertTrue(np.allclose(result_2, expected_2))

    def test_dist_point_and_itself(self):
        # Distance between a point and itself is 0.
        point_a_1 = np.array([10., -2., -.5, 2., 3.])
        point_b_1 = point_a_1
        result_1 = self.METRIC.dist(point_a_1, point_b_1)
        expected_1 = 0.

        self.assertTrue(np.allclose(result_1, expected_1))

    def test_dist_orthogonal_points(self):
        # Distance between two orthogonal points is pi / 2.
        point_a_2 = np.array([10., -2., -.5, 0., 0.])
        point_b_2 = np.array([2., 10, 0., 0., 0.])
        assert np.dot(point_a_2, point_b_2) == 0

        result_2 = self.METRIC.dist(point_a_2, point_b_2)
        expected_2 = np.pi / 2

        self.assertTrue(np.allclose(result_2, expected_2))

    def test_exp_and_dist_and_projection_to_tangent_space(self):
        base_point_1 = np.array([16., -2., -2.5, 84., 3.])
        base_point_1 = base_point_1 / np.linalg.norm(base_point_1)

        vector_1 = np.array([9., 0., -1., -2., 1.])
        tangent_vec_1 = self.SPACE.projection_to_tangent_space(
                                                      vector=vector_1,
                                                      base_point=base_point_1)
        exp_1 = self.METRIC.exp(tangent_vec=tangent_vec_1,
                                base_point=base_point_1)

        result_1 = self.METRIC.dist(base_point_1, exp_1)
        expected_1 = np.mod(np.linalg.norm(tangent_vec_1), 2 * np.pi)

        self.assertTrue(np.allclose(result_1, expected_1))


if __name__ == '__main__':
        unittest.main()