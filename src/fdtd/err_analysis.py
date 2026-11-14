"""Simple PML/reference runs. All quantities use normalized units."""

from math import ceil, isclose, sqrt
import fdtd_3d
import yee_solver

def simulation_time(a, b, B, c, dt):
    """Return the last safe simulation time, rounded to a multiple of dt.

    a: source half-width;
    b: sample half-width;
    B: simulation half-width.
    The centered boxes are [-a,a]^3, [-b,b]^3 and [-B,B]^3.

    c: uniform wave speed, equal to 1/sqrt(epsilon*mu).

    Assume zero initial fields and a source starting at t=0.
    Reserve one safety step plus the forward H half-step before reflection.
    """
    if not 0 <= a <= b < B or c <= 0 or dt <= 0:
        raise ValueError("Require 0 <= a <= b < B, c > 0 and dt > 0.")

    distance = (B - a) + (B - b)
    t_return = distance / c

    safety = dt + dt / 2
    n = ceil((t_return - safety) / dt) - 1

    if n < 0:
        raise ValueError("The domain is too small for this safety margin.")

    return n * dt


def fdtd_with_pml(T, dt):
    """Run PML with custom_current; return fields and simulation information.

    T and dt use normalized time; T must be a positive integer multiple of dt.
    Grid and PML parameters come from fdtd_3d. PML and custom_current are
    always used. E and H retain their native Yee locations;
    the solver already centers H in time.

    Returns the solver's result dictionary, including:
        electric, magnetic: (Ex,Ey,Ez), (Hx,Hy,Hz) on the full grid at T.
        physical_bounds: [[xmin,xmax], [ymin,ymax], [zmin,zmax]].
        physical_lengths: (Lx,Ly,Lz), excluding the PML layers.
        bounds, cells, spacing, nodes, centers: full computational grid.
        time, dt, steps: actual final time, timestep and step count.
        epsilon, mu, pml: material constants and PML settings.
    """
    if T <= 0 or dt <= 0:
        raise ValueError("T and dt must be positive.")
    steps = round(T / dt)
    if steps < 1 or not isclose(T, steps * dt, rel_tol=1e-12):
        raise ValueError("T must be an integer multiple of dt.")
    if fdtd_3d.PML_CELLS <= 0:
        raise ValueError("Set PML_CELLS > 0 in fdtd_3d.py.")

    result = yee_solver.solve(
        bounds=(fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE),
        cells=(fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ),
        end_time=T, time_steps=steps, cfl=fdtd_3d.CFL,
        epsilon=yee_solver.EPSILON0, mu=yee_solver.MU0,
        current_density=fdtd_3d.custom_current,
        pml_cells=fdtd_3d.PML_CELLS,
        pml_order=fdtd_3d.PML_ORDER,
        pml_reflection=fdtd_3d.PML_TARGET_REFLECTION,
        pml_sigma_max=fdtd_3d.PML_SIGMA_MAX,
    )
    physical_bounds = result["physical_bounds"]
    result["physical_lengths"] = physical_bounds[:, 1] - physical_bounds[:, 0]
    return result


def fdtd_reference(pml_result, B):
    """Run custom_current without PML on a larger cube containing [-A,A]^3.

    pml_result: result from fdtd_with_pml, on a centered cube with equal spacing.
    B: requested reference half-width, greater than the original A.
    B is rounded outward by whole cells to keep the same Yee locations.
    Time, dt and material constants match the PML run. The outer wall is PEC.
    Returns full-grid E/H and solver information; physical_bounds/lengths
    still describe the original region of interest. padding_cells is the
    number of cells added on each side of the original computational box.
    Keep the custom-current settings unchanged between the two runs.
    """
    A = pml_result["bounds"][0, 1]
    N = pml_result["cells"][0]
    h = pml_result["spacing"][0]
    if not (pml_result["bounds"] == [-A, A]).all() or pml_result["cells"] != (N, N, N):
        raise ValueError("Use a centered cube with equal cell counts.")
    if B <= A:
        raise ValueError("B must be larger than the original half-width A.")
    padding = ceil((B - A) / h)
    B = A + padding * h
    N_ref = N + 2 * padding

    T, dt = pml_result["time"], pml_result["dt"]
    a = max(abs(x) for x in fdtd_3d.CUSTOM_CENTER) + fdtd_3d.CUSTOM_RADIUS
    b = pml_result["physical_bounds"][0, 1]
    c = 1 / sqrt(pml_result["epsilon"] * pml_result["mu"])
    if T > simulation_time(a, b, B, c, dt):
        raise ValueError("Increase B: the reference is too small for this final time.")

    result = yee_solver.solve(
        bounds=[(-B, B)] * 3, cells=(N_ref, N_ref, N_ref),
        end_time=T, time_steps=pml_result["steps"], cfl=pml_result["cfl"],
        epsilon=pml_result["epsilon"], mu=pml_result["mu"],
        current_density=fdtd_3d.custom_current, pml_cells=0,
    )
    result["physical_bounds"] = pml_result["physical_bounds"].copy()
    result["physical_lengths"] = pml_result["physical_lengths"].copy()
    result["padding_cells"] = padding
    return result
