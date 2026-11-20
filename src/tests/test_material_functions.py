"""Checks for stationary material functions on staggered Yee grids.

Run: python -B -m unittest discover -s src/tests -p 'test_material_functions.py'
"""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'fdtd'))
import yee_solver as yee


def current(x, y, z, t):
    inside = x*x + y*y + z*z < 0.2**2
    return inside * (1+t), inside * (-0.5+t), inside * (0.25+t)


def epsilon(x, y, z):
    return np.where(x*x+y*y+z*z < 0.25**2, 4.0, 1.0)


def mu(x, y, z):
    return np.where(x*x+y*y+z*z < 0.25**2, 2.0, 1.0)


class MaterialTests(unittest.TestCase):
    def settings(self, **extra):
        settings = dict(bounds=[(-0.5, 0.5)]*3, cells=(12,12,12),
                        end_time=0.05, time_steps=10, current_density=current)
        settings.update(extra)
        return settings

    def test_constant_functions_match_scalars(self):
        for pml in (0, 2):
            scalar = yee.solve(**self.settings(epsilon=2., mu=3., pml_cells=pml))
            function = yee.solve(**self.settings(epsilon=lambda x,y,z: 2.,
                                                mu=lambda x,y,z: 3., pml_cells=pml))
            for name in ('electric', 'magnetic'):
                for a,b in zip(scalar[name], function[name]):
                    np.testing.assert_array_equal(a,b)

    def test_local_update_and_time_alignment(self):
        result = yee.solve(**self.settings(epsilon=epsilon, mu=mu,
                                          end_time=0.01, time_steps=1))
        x,y,z=result['nodes']; xc,yc,zc=result['centers']
        axes=((xc,y,z),(x,yc,z),(x,y,zc))
        dt=result['dt']
        for p, axis in enumerate(axes):
            xyz=np.meshgrid(*axis,indexing='ij')
            expected=-dt*current(*xyz,dt/2)[p]/epsilon(*xyz)
            np.testing.assert_allclose(result['electric'][p],expected,atol=1e-15)
        # Starting from E=H=0, stored half-step H is zero after one step.
        curls=yee.curl_e(result['electric'],result['spacing'])
        for h,c,m in zip(result['magnetic'],curls,result['mu_fields']):
            np.testing.assert_allclose(h,-dt*c/(2*m),atol=1e-15)

    def test_gauss_and_lossless_pml(self):
        plain=yee.solve(**self.settings(epsilon=epsilon,mu=mu))
        pml=yee.solve(**self.settings(epsilon=epsilon,mu=mu,pml_cells=2,pml_sigma_max=0))
        for name in ('electric','magnetic'):
            for a,b in zip(plain[name],pml[name]):
                np.testing.assert_allclose(a,b,atol=1e-14,rtol=1e-12)
        for result in (plain,pml):
            d=tuple(eps*e for eps,e in zip(result['epsilon_fields'],result['electric']))
            np.testing.assert_allclose(yee.divergence_e(d,result['spacing']),
                                       result['charge'],atol=1e-13,rtol=1e-12)
            bx,by,bz=(m*h for m,h in zip(result['mu_fields'],result['magnetic']))
            dx,dy,dz=result['spacing']
            divb=np.diff(bx,axis=0)/dx+np.diff(by,axis=1)/dy+np.diff(bz,axis=2)/dz
            np.testing.assert_allclose(divb,0,atol=1e-13)

    def test_validation_and_sampling(self):
        calls=[]
        def material(x,y,z):
            calls.append(1)
            return 1.0
        yee.solve(**self.settings(epsilon=material,mu=material,pml_cells=2))
        self.assertEqual(len(calls),6)
        for bad in (lambda x,y,z: -1.,lambda x,y,z: np.nan,lambda x,y,z: 1j):
            with self.assertRaises(ValueError):
                yee.solve(**self.settings(epsilon=bad))
        with self.assertRaises(ValueError):
            yee.solve(**self.settings(epsilon=lambda x,y,z: 2+x,pml_cells=2))
        with self.assertRaises(ValueError):
            yee.solve(**self.settings(epsilon=.01,end_time=.1,time_steps=1))


if __name__ == '__main__':
    unittest.main()
