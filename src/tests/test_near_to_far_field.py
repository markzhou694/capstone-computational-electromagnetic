"""Analytic dipole, causality, material and actual Yee-to-surface checks."""

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import numpy as np

FDTD = Path(__file__).resolve().parents[1] / "fdtd"
sys.path.insert(0, str(FDTD))
spec = importlib.util.spec_from_file_location("near_to_far", FDTD / "near-to-far-field.py")
ntf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ntf)


def dipole_fields(points, times, epsilon=1.0, mu=1.0):
    """Exact causal electric-dipole fields, independent of surface integration.

    Dipole position is (.07,-.04,.03); direction is (1,-.4,.7).
    p(t)=direction*sin(pi*c*t/4)**4 for 0<c*t<4, otherwise zero.
    This smooth pulse supplies p, p_dot, p_ddot analytically.
    Returns (Nt,Np,3) Cartesian E,H, including near and radiation terms.
    """
    c = 1 / np.sqrt(epsilon*mu)
    displacement = np.asarray(points) - np.array([.07, -.04, .03])
    r = np.linalg.norm(displacement, axis=1)[None, :, None]
    n = displacement[None, :, :] / r
    t_retarded = np.asarray(times)[:, None, None] - r/c
    omega = np.pi*c/4
    active = (t_retarded > 0) & (c*t_retarded < 4)
    direction = np.array([1.0, -.4, .7])
    p = active * np.sin(omega*t_retarded)**4 * direction
    p_dot = active * omega*(np.sin(2*omega*t_retarded) - .5*np.sin(4*omega*t_retarded)) * direction
    p_ddot = active * 2*omega**2*(np.cos(2*omega*t_retarded) - np.cos(4*omega*t_retarded)) * direction
    E = ((3*n*np.sum(n*p, axis=2, keepdims=True) - p)/r**3
         + (3*n*np.sum(n*p_dot, axis=2, keepdims=True) - p_dot)/(c*r**2)
         + np.cross(n, np.cross(n, p_ddot))/(c*c*r)) / (4*np.pi*epsilon)
    H = (np.cross(p_dot, n)/r**2 + np.cross(p_ddot, n)/(c*r)) / (4*np.pi)
    return E, H


def analytic_surface(n_theta=16, dt=.01, epsilon=1., mu=1.):
    c = 1 / np.sqrt(epsilon*mu)
    surface = ntf.sphere_quadrature([[-1., 1.]]*3, .5, n_theta, 2*n_theta)
    steps = round(4/dt)
    times = np.linspace(0, 4/c, steps+1)
    E, H = dipole_fields(surface["points"], times, epsilon, mu)
    surface.update(times=times, electric=E, magnetic=H, epsilon=epsilon, mu=mu)
    return surface


def dipole_errors(surface):
    c = 1 / np.sqrt(surface["epsilon"]*surface["mu"])
    errors = []
    for point, time in [([1.2, .2, .3], 3.1/c), ([2., -.7, .3], 4.2/c)]:
        computed = ntf.reconstruct_fields(surface, point, [time])
        exact = dipole_fields([point], [time], surface["epsilon"], surface["mu"])
        for name, reference in zip(("electric", "magnetic"), exact):
            errors.append(np.linalg.norm(computed[name][0]-reference[0, 0]) / np.linalg.norm(reference[0, 0]))
    return np.array(errors)


class DirectRetardedIntegral(unittest.TestCase):
    def test_patch_areas_and_poles(self):
        surface = ntf.sphere_quadrature([[-1., 1.]]*3, .5, 16, 32)
        self.assertEqual(len(surface["weights"]), 514)
        self.assertAlmostEqual(sum(surface["weights"]), 4*np.pi*.5**2, places=13)
        np.testing.assert_array_equal(surface["weights"][-2:], 0.)
        np.testing.assert_allclose(surface["weights"] @ surface["normals"], 0., atol=1e-14)

    def test_analytic_dipole_angular_convergence(self):
        errors = []
        for rings in (8, 16, 32):
            surface = analytic_surface(rings, dt=.005)
            errors.append(dipole_errors(surface))
            del surface
        errors = np.array(errors)
        print("\nDipole relative E1,H1,E2,H2 errors (8/16/32 rings):\n", errors)
        self.assertTrue(np.all(errors[1:] < .4*errors[:-1]))
        self.assertLess(errors[-1].max(), .002)

    def test_time_refinement(self):
        errors = []
        for dt in (.08, .04, .02):
            surface = analytic_surface(32, dt)
            errors.append(dipole_errors(surface).max())
        print("Time-refinement maximum dipole errors:", errors)
        self.assertLess(errors[-1], .3*errors[0])

    def test_nonunit_background(self):
        errors = dipole_errors(analytic_surface(24, epsilon=2.25, mu=4.))
        self.assertLess(errors.max(), .004)

    def test_causality_record_end_and_location(self):
        surface = analytic_surface(8)
        point = [2., 0., 0.]
        fields = ntf.reconstruct_fields(surface, point, [0., .25])
        np.testing.assert_array_equal(fields["electric"], 0.)
        np.testing.assert_array_equal(fields["magnetic"], 0.)
        with self.assertRaisesRegex(ValueError, "future surface data"):
            ntf.reconstruct_fields(surface, point, [6.])
        for point in ([0., 0., 0.], [.5, 0., 0.]):
            with self.assertRaisesRegex(ValueError, "outside the sphere"):
                ntf.reconstruct_fields(surface, point)

    def test_heterogeneous_interior_and_invalid_exterior(self):
        settings = ntf.fdtd_3d.get_simulation_settings()
        nodes = [np.linspace(-1, 1, 25)]*3
        centers = [(q[:-1]+q[1:])/2 for q in nodes]
        surface = ntf.sphere_quadrature([[-.75, .75]]*3, .45)
        def epsilon(x, y, z):
            return np.where(x*x+y*y+z*z < .2**2, 4., 1.)
        settings.update(epsilon=epsilon, mu=2.)
        self.assertEqual(ntf.exterior_materials(settings, nodes, centers, surface), (1., 2.))
        settings["epsilon"] = lambda x, y, z: 1. + .1*x
        with self.assertRaisesRegex(ValueError, "collar/exterior"):
            ntf.exterior_materials(settings, nodes, centers, surface)

    def test_actual_fdtd_history_and_exterior(self):
        settings = ntf.fdtd_3d.get_simulation_settings()
        settings.update(bounds=[(-1., 1.)]*3, cells=(24,)*3, end_time=1.4,
                        pml_cells=3, epsilon=1., mu=1., frame_every=9)
        with patch.object(ntf.fdtd_3d, "CUSTOM_RADIUS", .12), contextlib.redirect_stdout(io.StringIO()):
            surface = ntf.record_surface(settings, radius=.45, n_theta=12, n_phi=24)
        self.assertEqual(len(surface["times"]), round(1.4/surface["dt"])+1)
        self.assertEqual(surface["electric"].shape, (len(surface["times"]), 290, 3))
        np.testing.assert_array_equal(surface["electric"][0], 0.)
        np.testing.assert_array_equal(surface["magnetic"][0], 0.)
        fields = ntf.reconstruct_fields(surface, [2., .1, .2])
        self.assertTrue(np.isfinite(fields["electric"]).all())
        self.assertTrue(np.isfinite(fields["magnetic"]).all())
        self.assertGreater(np.linalg.norm(fields["electric"]), 0.)
        self.assertGreater(np.linalg.norm(fields["magnetic"]), 0.)
        # Integration does not mutate either saved surface history.
        np.testing.assert_array_equal(surface["electric"][0], 0.)

    def test_reconstruction_against_direct_fdtd_probe(self):
        # The probe is outside the sphere but inside the physical FDTD box.
        # This compares two independent routes to the same E/H time traces.
        point = np.array([.62, .11, .07])
        errors = []
        for count in (24, 48):
            settings = ntf.fdtd_3d.get_simulation_settings()
            settings.update(bounds=[(-1., 1.)]*3, cells=(count,)*3, end_time=1.4,
                            pml_cells=count//8, epsilon=1., mu=1., frame_every=1)
            nodes = [np.linspace(-1, 1, count+1)]*3
            centers = [(q[:-1]+q[1:])/2 for q in nodes]
            x, y, z = nodes
            xc, yc, zc = centers
            e_axes = ((xc, y, z), (x, yc, z), (x, y, zc))
            h_axes = ((x, yc, zc), (xc, y, zc), (xc, yc, z))
            times, E, H = [], [], []

            def probe(t, electric, unused_centers, magnetic):
                times.append(t)
                for fields, axes, saved in ((electric, e_axes, E), (magnetic, h_axes, H)):
                    samples = [ntf.trilinear(v, a, point[None, :])[0] for v, a in zip(fields, axes)]
                    saved.append(samples)

            with patch.object(ntf.fdtd_3d, "CUSTOM_RADIUS", .12), contextlib.redirect_stdout(io.StringIO()):
                surface = ntf.record_surface(settings, radius=.45, n_theta=24, n_phi=48)
                ntf.yee_solver.solve(**settings, on_frame=probe)
            computed = ntf.reconstruct_fields(surface, point, times)
            errors.append([np.linalg.norm(computed[key]-reference)/np.linalg.norm(reference)
                           for key, reference in (("electric", np.array(E)), ("magnetic", np.array(H)))])
        errors = np.array(errors)
        print("Direct-FDTD comparison, relative time-L2 E,H errors (24/48 cells):\n", errors)
        self.assertTrue(np.all(errors[-1] < .4*errors[0]))
        self.assertLess(errors[-1].max(), .02)


if __name__ == "__main__":
    unittest.main()
