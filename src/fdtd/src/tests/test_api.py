"""Numerical and integration checks for the reusable calling contract."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from yee_solver import solve, EPSILON0, MU0, curl_e, divergence_e
from plot_fields import cell_center_fields, sample_fields, save_results


def source(x, y, z, t):
    value = 0.01 * np.exp(-(x*x + y*y + z*z) / 0.1) * np.sin(1e9 * t)
    return value, -0.3 * value, 0.7 * value


class SolverAPI(unittest.TestCase):
    def test_default_zero_source_and_grid_metadata(self):
        result = solve(((2, 4), (-3, 0), (1, 2)), (6, 8, 10), 1e-9)
        self.assertEqual(result['cells'], (6, 8, 10))
        for n, nodes, centers in zip(result['cells'], result['nodes'], result['centers']):
            self.assertEqual(nodes.shape, (n + 1,))
            self.assertEqual(centers.shape, (n,))
            np.testing.assert_array_equal(centers, (nodes[:-1] + nodes[1:]) / 2)
        for field in (*result['electric'], *result['magnetic'], result['charge']):
            self.assertTrue(np.all(field == 0))

    def test_uniform_medium_scaling(self):
        # If epsilon'=a*epsilon, mu'=b*mu and s=sqrt(a*b), Maxwell gives
        # E'(s*t)=E(t), H'(s*t)=sqrt(a/b)*H(t), rho'(s*t)=a*rho(t)
        # when the prescribed current is J'(s*t)=sqrt(a/b)*J(t).
        bounds = ((-1, 1), (-0.8, 0.8), (-0.6, 0.6))
        cells = (8, 10, 12)
        original = solve(bounds, cells, 2e-9, current_density=source)
        for a, b in ((4.0, 1.0), (1.0, 4.0)):
            with self.subTest(epsilon_factor=a, mu_factor=b):
                time_scale = np.sqrt(a * b)
                h_scale = np.sqrt(a / b)

                def scaled_source(x, y, z, t):
                    return tuple(h_scale * j for j in source(x, y, z, t / time_scale))

                changed = solve(
                    bounds, cells, time_scale * 2e-9, current_density=scaled_source,
                    epsilon=a * EPSILON0, mu=b * MU0,
                )
                self.assertEqual(changed['steps'], original['steps'])
                self.assertAlmostEqual(changed['dt'] / original['dt'], time_scale)
                for old, new in zip(original['electric'], changed['electric']):
                    np.testing.assert_allclose(new, old, rtol=1e-12, atol=1e-14)
                for old, new in zip(original['magnetic'], changed['magnetic']):
                    np.testing.assert_allclose(new, h_scale * old, rtol=1e-12, atol=1e-14)
                np.testing.assert_allclose(changed['charge'], a * original['charge'], rtol=1e-12, atol=1e-25)
                residual = changed['epsilon'] * divergence_e(changed['electric'], changed['spacing']) - changed['charge']
                self.assertLess(np.max(np.abs(residual)) / np.max(np.abs(changed['charge'])), 1e-12)

    def test_callback_alignment_cadence_and_no_effect_on_solution(self):
        frames = []

        def record(time, electric, centers, magnetic):
            frames.append((time, tuple(f.copy() for f in electric), tuple(f.copy() for f in magnetic)))

        args = (((-1, 1),) * 3, (6, 8, 10), 3e-9)
        observed = solve(*args, current_density=source, on_frame=record, frame_every=3)
        expected_steps = [0] + list(range(3, observed['steps'] + 1, 3))
        if expected_steps[-1] != observed['steps']:
            expected_steps.append(observed['steps'])
        np.testing.assert_allclose([f[0] for f in frames], np.array(expected_steps) * observed['dt'])
        for saved, returned in zip(frames[-1][2], observed['magnetic']):
            np.testing.assert_array_equal(saved, returned)
        plain = solve(*args, current_density=source)
        for key in ('electric', 'magnetic'):
            for a, b in zip(plain[key], observed[key]):
                np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(plain['charge'], observed['charge'])

        # After one step, internal H is still zero. Output H must already
        # include the half-step correction from the nonzero driven E.
        frames.clear()
        duration = 1e-12
        one = solve(args[0], args[1], duration, current_density=source, on_frame=record)
        self.assertEqual(one['steps'], 1)
        expected_h = curl_e(one['electric'], one['spacing'])
        self.assertGreater(max(np.max(np.abs(f)) for f in expected_h), 0)
        for actual, curl_component in zip(frames[-1][2], expected_h):
            np.testing.assert_array_equal(actual, -duration / (2 * MU0) * curl_component)

    def test_invalid_medium_and_source_contract(self):
        args = (((-1, 1),) * 3, (4, 5, 6), 1e-12)
        for name in ('epsilon', 'mu'):
            for value in (0, -1, np.nan, np.inf, np.ones((2, 2))):
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    solve(*args, **{name: value})
        bad_sources = (
            lambda x, y, z, t: 0.0,
            lambda x, y, z, t: np.array(0.0),
            lambda x, y, z, t: (0.0, 0.0),
            lambda x, y, z, t: (np.ones((2, 2)), 0.0, 0.0),
            lambda x, y, z, t: (np.nan, 0.0, 0.0),
            lambda x, y, z, t: (0.0, 0.0, 1j),
        )
        for bad in bad_sources:
            with self.assertRaises(ValueError):
                solve(*args, current_density=bad)
        with self.assertRaises(ValueError):
            solve(*args, current_density=123)
        with self.assertRaises(ValueError):
            solve(*args, on_frame=123)


class PlotAPI(unittest.TestCase):
    def test_linear_field_averaging_slices_and_copy(self):
        # Linear fields average exactly to cell centers on both Yee layouts.
        cells = (17, 18, 19)
        nodes = [np.linspace(-1, 1, n + 1) for n in cells]
        centers = [(q[:-1] + q[1:]) / 2 for q in nodes]
        x, y, z = np.meshgrid(*centers, indexing='ij')
        exact = (x + 2*y + 3*z, 2*x - y + z, -x + y + 2*z)
        magnitude = np.sqrt(sum(f*f for f in exact))
        for kind in ('E', 'H'):
            fields = []
            for axis in range(3):
                coordinates = list(nodes if kind == 'E' else centers)
                coordinates[axis] = centers[axis] if kind == 'E' else nodes[axis]
                x, y, z = np.meshgrid(*coordinates, indexing='ij')
                fields.append((x + 2*y + 3*z, 2*x - y + z, -x + y + 2*z)[axis])
            for actual, expected in zip(cell_center_fields(fields, kind), exact):
                np.testing.assert_allclose(actual, expected, atol=2e-15)
            frame = sample_fields(1e-9, fields, centers, kind)
            expected_planes = (magnitude[:, :, 9], magnitude[:, 9, :], magnitude[8, :, :])
            for actual, expected in zip(frame['planes'], expected_planes):
                np.testing.assert_allclose(actual, expected, atol=2e-15)
            for actual, expected in zip(frame['vectors'], exact):
                np.testing.assert_allclose(actual, expected[::2, ::2, ::2], atol=2e-15)
            saved = frame['vectors'][0].copy()
            for field in fields:
                field[:] = 123
            np.testing.assert_array_equal(frame['vectors'][0], saved)
            self.assertEqual(frame['kind'], kind)

    def test_e_and_h_exports(self):
        from PIL import Image
        for kind in ('E', 'H'):
            frames = []

            def record(time, electric, centers, magnetic):
                field = electric if kind == 'E' else magnetic
                frames.append(sample_fields(time, field, centers, kind))

            result = solve(((-1, 1),) * 3, (4, 5, 6), 1e-9,
                           current_density=source, on_frame=record, frame_every=2)
            with TemporaryDirectory() as directory:
                paths = save_results(result, frames, directory, fps=12, kind=kind)
                self.assertEqual(set(paths), {'png', 'gif'})
                with Image.open(paths['png']) as picture:
                    picture.load()
                    self.assertEqual(picture.size, (1500, 1200))
                with Image.open(paths['gif']) as picture:
                    self.assertEqual(picture.n_frames, len(frames))
                    picture.seek(picture.n_frames - 1)
                    picture.load()

    def test_zero_export_and_render_failure_preserves_previous_files(self):
        result = solve(((-1, 1),) * 3, (4, 5, 6), 1e-9)
        frame = sample_fields(result['time'], result['electric'], result['centers'])
        with TemporaryDirectory() as directory:
            paths = save_results(result, [frame], directory)
            previous = {key: path.read_bytes() for key, path in paths.items()}
            with patch('matplotlib.animation.FuncAnimation') as animation:
                animation.return_value.save.side_effect = RuntimeError('render failed')
                with self.assertRaisesRegex(RuntimeError, 'render failed'):
                    save_results(result, [frame], directory)
            for key, path in paths.items():
                self.assertEqual(path.read_bytes(), previous[key])
        import matplotlib.pyplot as plt
        self.assertEqual(plt.get_fignums(), [])

    def test_invalid_plot_inputs(self):
        result = solve(((-1, 1),) * 3, (4, 5, 6), 1e-9)
        frame = sample_fields(0, result['electric'], result['centers'])
        with TemporaryDirectory() as directory:
            for frames, kwargs in (([], {}), ([frame], {'fps': 0}), ([frame], {'kind': 'H'})):
                with self.assertRaises(ValueError):
                    save_results(result, frames, directory, **kwargs)
            later = dict(frame, time=1e-9)
            with self.assertRaises(ValueError):
                save_results(result, [later, frame], directory)
        with self.assertRaises(ValueError):
            sample_fields(0, result['electric'], result['centers'], kind='invalid')


if __name__ == '__main__':
    unittest.main()
