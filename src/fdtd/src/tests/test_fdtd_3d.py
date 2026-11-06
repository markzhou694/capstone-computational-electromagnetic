"""Numerical validation kept separate from the user's parameter/current file."""
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from yee_solver import C0, MU0, EPSILON0, solve, divergence_e


def zero_current(x, y, z, t):
    return 0.0, 0.0, 0.0


class FDTD3DChecks(unittest.TestCase):
    def test_zero_current_keeps_zero_fields(self):
        result = solve(((-1,1),)*3, (8,9,10), 1e-9, 0.8, zero_current)
        for field in (*result["electric"], *result["magnetic"], result["charge"]):
            self.assertTrue((field == 0).all())

    def test_source_sign_midpoint_and_yee_locations(self):
        bounds = ((2,4), (-3,0), (1,2))
        cells = (6,8,10)
        def current(x,y,z,t):
            return x+2*y+3*z+t/1e-9, 2*x-y+z+2*t/1e-9, -x+y+2*z+3*t/1e-9
        duration = 1e-12  # One step; initial H is zero.
        result = solve(bounds, cells, duration, 0.8, current)
        self.assertEqual(result["steps"], 1)
        nodes = [np.linspace(a,b,n+1) for (a,b),n in zip(bounds,cells)]
        centers = [(a[1:]+a[:-1])/2 for a in nodes]
        interiors = ((slice(None),slice(1,-1),slice(1,-1)),
                     (slice(1,-1),slice(None),slice(1,-1)),
                     (slice(1,-1),slice(1,-1),slice(None)))
        for axis in range(3):
            coordinates = list(nodes)
            coordinates[axis] = centers[axis]
            x,y,z = np.meshgrid(*coordinates,indexing="ij")
            expected = -duration/EPSILON0 * current(x,y,z,duration/2)[axis]
            np.testing.assert_allclose(result["electric"][axis][interiors[axis]], expected[interiors[axis]], rtol=1e-14)

    def test_driven_3d_exact_solution_converges(self):
        # Translated, rectangular box: checks unequal dx/dy/dz as well as J.
        bounds = np.array(((2.,4.), (-3.,0.), (1.,2.)))
        lengths = bounds[:,1]-bounds[:,0]
        k = np.pi/lengths
        omega = C0*np.linalg.norm(k)
        amplitude = np.array((1.,2.,-3.))/k
        amplitude /= np.max(np.abs(amplitude))  # k dot amplitude = 0.
        def shape(x,y,z):
            X,Y,Z = x-bounds[0,0], y-bounds[1,0], z-bounds[2,0]
            return (amplitude[0]*np.cos(k[0]*X)*np.sin(k[1]*Y)*np.sin(k[2]*Z),
                    amplitude[1]*np.sin(k[0]*X)*np.cos(k[1]*Y)*np.sin(k[2]*Z),
                    amplitude[2]*np.sin(k[0]*X)*np.sin(k[1]*Y)*np.cos(k[2]*Z))
        # E=F*(1-cos(omega*t)), H=-curl(F)/mu*(t-sin(omega*t)/omega)
        # is driven exactly by J=-epsilon*omega^2*t*F, with zero initial fields.
        def current(x,y,z,t):
            return tuple(-EPSILON0*omega**2*t*f for f in shape(x,y,z))
        final_time = 0.30*2*np.pi/omega
        errors = []
        for n in (10,20,40):
            result = solve(bounds,(n,n,n),final_time,0.75,current)
            nodes = [np.linspace(a,b,n+1) for a,b in bounds]
            centers = [(q[1:]+q[:-1])/2 for q in nodes]
            error_squared, norm_squared = 0., 0.
            for axis in range(3):
                coordinates = list(nodes)
                coordinates[axis] = centers[axis]
                xyz = np.meshgrid(*coordinates,indexing="ij",sparse=True)
                e_exact = shape(*xyz)[axis]*(1-np.cos(omega*final_time))
                coordinates = list(centers)
                coordinates[axis] = nodes[axis]
                xyz = np.meshgrid(*coordinates,indexing="ij",sparse=True)
                b,c = (axis+1)%3,(axis+2)%3
                curl_f = k[b]*amplitude[c]-k[c]*amplitude[b]
                for direction in range(3):
                    q = xyz[direction]-bounds[direction,0]
                    curl_f = curl_f*(np.sin(k[direction]*q) if direction==axis else np.cos(k[direction]*q))
                h_exact = -curl_f/MU0*(final_time-np.sin(omega*final_time)/omega)
                impedance_squared = MU0/EPSILON0
                error_squared += np.sum((result["electric"][axis]-e_exact)**2)
                error_squared += impedance_squared*np.sum((result["magnetic"][axis]-h_exact)**2)
                norm_squared += np.sum(e_exact**2)+impedance_squared*np.sum(h_exact**2)
            errors.append(np.sqrt(error_squared/norm_squared))
        orders = np.log2(np.array(errors[:-1])/errors[1:])
        print(f"Driven rectangular 3D mode errors: {errors}; orders: {orders}")
        self.assertTrue(np.all(orders > 1.85))
        self.assertLess(errors[-1],1e-3)

    def test_charge_continuity_and_pec(self):
        def current(x,y,z,t):
            gaussian = np.exp(-((x-.1)**2+y**2+z**2)/.08)
            value = .01*gaussian*np.sin(2*np.pi*0.5e9*t)
            return value, -.3*value, .7*value
        result = solve(((-1,1),)*3, (10,12,14), 3e-9, .8, current)
        rho = result["charge"]
        gauss_error = EPSILON0*divergence_e(result["electric"],result["spacing"])-rho
        relative = np.max(np.abs(gauss_error))/np.max(np.abs(rho))
        hx,hy,hz = result["magnetic"]
        dx,dy,dz = result["spacing"]
        div_h = np.diff(hx,axis=0)/dx+np.diff(hy,axis=1)/dy+np.diff(hz,axis=2)/dz
        print(f"Relative Gauss residual: {relative:.6e}; max divH: {np.max(np.abs(div_h)):.6e}")
        self.assertLess(relative,1e-12)
        self.assertLess(np.max(np.abs(div_h)),1e-13)
        ex,ey,ez = result["electric"]
        for wall in (ex[:,[0,-1],:],ex[:,:,[0,-1]],ey[[0,-1],:,:],ey[:,:,[0,-1]],ez[[0,-1],:,:],ez[:,[0,-1],:]):
            self.assertTrue((wall==0).all())
        for field in (*result["electric"],*result["magnetic"]):
            self.assertTrue(np.isfinite(field).all())

    def test_translation_of_box_and_source(self):
        bounds = np.array(((-1.,1.),(-.5,1.),(-2.,1.)))
        shift = np.array((3.,-4.,2.))
        def current(x,y,z,t):
            return 0., 0., .01*np.exp(-(x*x+y*y+z*z)/.1)*np.sin(1e9*t)
        def shifted_current(x,y,z,t):
            return current(x-shift[0],y-shift[1],z-shift[2],t)
        a=solve(bounds,(8,9,10),1e-9,.8,current)
        b=solve(bounds+shift[:,None],(8,9,10),1e-9,.8,shifted_current)
        for original,moved in zip(a["electric"],b["electric"]):
            np.testing.assert_allclose(original,moved,atol=1e-14,rtol=1e-12)

    def test_cfl_and_invalid_settings(self):
        bounds=((-1,1),(-2,1),(3,4))
        result=solve(bounds,(8,10,12),1e-9,1,zero_current)
        self.assertLessEqual(C0*result["dt"]*np.sqrt(np.sum(1/result["spacing"]**2)),1+1e-14)
        for cfl in (0,100.8,np.nan):
            with self.assertRaises(ValueError):
                solve(bounds,(8,10,12),1e-9,cfl,zero_current)
        with self.assertRaises(ValueError):
            solve(((1,1),)*3,(8,8,8),1e-9,.8,zero_current)
        with self.assertRaises(ValueError):
            solve(bounds,(8,10,12),0,.8,zero_current)


if __name__ == "__main__":
    unittest.main()
