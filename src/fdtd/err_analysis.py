"""Simple PML/reference runs. All quantities use normalized units."""

from math import ceil, isclose, sqrt
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import fdtd_3d
import yee_solver
from plot_fields import save_error_history, save_error_norms
from run_metrics import timed_solve, timed_call

def uniform_materials():
    """Read material functions on the original Yee grid for uniform-medium timing.

    The current reflection-time analysis is homogeneous-only. Reject spatial
    variation rather than silently using the old vacuum constants.
    """
    bounds = (fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE)
    cells = (fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ)
    nodes = [np.linspace(low, high, n+1) for (low, high), n in zip(bounds, cells)]
    centers = [(q[:-1]+q[1:])/2 for q in nodes]
    constants = []
    for material, kind in ((fdtd_3d.epsilon, "E"), (fdtd_3d.mu, "H")):
        coordinates = []
        for component in range(3):
            axes = [centers[d] if ((d == component) == (kind == "E")) else nodes[d]
                    for d in range(3)]
            coordinates.append(np.meshgrid(*axes, indexing="ij", sparse=True))
        fields = yee_solver.sample_material(material, coordinates, kind)
        value = float(fields[0].flat[0])
        if any(not np.allclose(field, value, rtol=1e-12, atol=0) for field in fields):
            raise ValueError("err_analysis timing currently requires uniform epsilon and mu.")
        constants.append(value)
    return tuple(constants)


def simulation_time(a, b, B, c, dt):
    """Return the last safe simulation time, rounded to a multiple of dt.

    a: source half-width;
    b: sample half-width;
    B: simulation half-width.
    The centered boxes are [-a,a]^3, [-b,b]^3 and [-B,B]^3.

    c: uniform wave speed, equal to 1/sqrt(epsilon*mu).

    Assume zero initial fields and a source starting at t=0.
    Reserve three timesteps in total, including the forward H half-step.
    """
    if not 0 <= a <= b < B or c <= 0 or dt <= 0:
        raise ValueError("Require 0 <= a <= b < B, c > 0 and dt > 0.")

    distance = (B - a) + (B - b)
    t_return = distance / c

    safety = 50 * dt  # Total reserve; includes the forward H half-step. #important
    n = ceil((t_return - safety) / dt) - 1

    if n < 0:
        raise ValueError("The domain is too small for this safety margin.")

    return n * dt


def fdtd_with_pml(T, dt, on_frame=None):
    """Run PML with custom_current; return fields and simulation information.

    T and dt use normalized time; T must be a positive integer multiple of dt.
    Grid and PML parameters come from fdtd_3d. PML and custom_current are
    always used. Optional on_frame receives (time, E, centers, aligned H).
    E and H retain their native Yee locations;
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
    pml_cells = fdtd_3d.pml_length_to_cells(
        fdtd_3d.PML_length,
        (fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE),
        (fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ),
    )

    result = timed_solve("PML",
        bounds=(fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE),
        cells=(fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ),
        end_time=T, time_steps=steps, cfl=fdtd_3d.CFL,
        epsilon=fdtd_3d.epsilon, mu=fdtd_3d.mu,
        on_frame=on_frame,
        current_density=fdtd_3d.custom_current,
        pml_cells=pml_cells,
        pml_order=fdtd_3d.PML_ORDER,
        pml_reflection=fdtd_3d.PML_TARGET_REFLECTION,
        pml_sigma_max=fdtd_3d.PML_SIGMA_MAX,
    )
    physical_bounds = result["physical_bounds"]
    result["physical_lengths"] = physical_bounds[:, 1] - physical_bounds[:, 0]
    return result


def fdtd_reference(pml_result, B, on_frame=None):
    """Run custom_current without PML on a larger cube containing [-A,A]^3.

    pml_result: result from fdtd_with_pml, on a centered cube with equal spacing.
    B: requested reference half-width, greater than the original A.
    B is rounded outward by whole cells to keep the same Yee locations.
    Time, dt and material constants match the PML run. The outer wall is PEC.
    Returns full-grid E/H and solver information; physical_bounds/lengths
    still describe the original region of interest. padding_cells is the
    number of cells added on each side of the original computational box.
    Keep the custom-current settings unchanged between the two runs.
    Optional on_frame receives (time, E, centers, aligned H) every step.
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
    epsilon, mu = uniform_materials()
    c = 1 / sqrt(epsilon * mu)
    if T > simulation_time(a, b, B, c, dt):
        raise ValueError("Increase B: the reference is too small for this final time.")

    result = timed_solve("Reference",
        bounds=[(-B, B)] * 3, cells=(N_ref, N_ref, N_ref),
        end_time=T, time_steps=pml_result["steps"], cfl=pml_result["cfl"],
        epsilon=pml_result["epsilon"], mu=pml_result["mu"],
        on_frame=on_frame,
        current_density=fdtd_3d.custom_current, pml_cells=0,
    )
    result["physical_bounds"] = pml_result["physical_bounds"].copy()
    result["physical_lengths"] = pml_result["physical_lengths"].copy()
    result["padding_cells"] = padding
    return result

# H is already centered at the same time as E by the solver.
# Compare matching native Yee samples in the physical region [-b,b]^3.
# No spatial averaging is needed.
#
# The continuum reflection-arrival bound is:
# t_return = ((B - a) + (B - b)) / c
# Choose T_end so that T_end + 3*dt < t_return.
#
# Peak-normalized discrete L2 errors, with I = sampled times in [t_start,T_end]:
# error_E(t) = ||E_pml(t) - E_ref(t)||_2 / max_{s in I} ||E_ref(s)||_2
# error_H(t) = ||H_pml(t) - H_ref(t)||_2 / max_{s in I} ||H_ref(s)||_2
# ||F||_2 = sqrt(sum(Fx**2) + sum(Fy**2) + sum(Fz**2)).
# Each sum uses native Yee samples in the shared physical region, without averaging.
# The common sqrt(dx*dy*dz) factor cancels in these ratios.
# Each denominator is fixed over I; an entirely zero reference gives NaN.

def l2_norms(field, reference):
    """Return (absolute difference norm, reference norm) from native Yee sums."""
    difference_squared = 0.0
    reference_squared = 0.0
    for component, ref_component in zip(field, reference):
        if component.shape != ref_component.shape:
            raise ValueError("Compared Yee components must have matching shapes.")
        difference_squared += np.sum((component - ref_component)**2)
        reference_squared += np.sum(ref_component**2)
    return sqrt(difference_squared), sqrt(reference_squared)


def run_simulations(B, dt):
    """Run both domains; return final fields and the error observation interval.

    B: requested reference half-width; dt: shared timestep.
    Both runs start at zero. Record peak-normalized E/H errors every dt from
    t_start through T_end, using native Yee samples in the physical box.
    Temporary PML snapshots are deleted after comparison; RAM stays bounded.
    The continuum travel-time bound is not a discrete error guarantee.
    """
    A = fdtd_3d.X_RANGE[1]  # Half-width of the small box [-A,A]^3, including PML.
    N = fdtd_3d.NX  # Number of cells per direction in the small box.
    bounds = (fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE)  # Bounds along x, y and z.
    cells = (fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ)  # Cell counts along x, y and z.
    if any(tuple(box) != (-A, A) for box in bounds) or cells != (N, N, N):  # Require a centered cube with equal spacing.
        raise ValueError("Use a centered cube with equal cell counts.")  # Stop if the geometry is incompatible.
    if dt <= 0:  # The timestep must be positive.
        raise ValueError("Require dt > 0.")

    h = 2 * A / N  # Grid spacing: side length divided by cell count.
    pml_cells = fdtd_3d.pml_length_to_cells(fdtd_3d.PML_length, bounds, cells)  # Round requested thickness up to whole cells.
    pml_length = pml_cells * h  # Actual PML thickness; may exceed the requested length.
    b = A - pml_length  # Physical half-width; b + pml_length = A.
    if B <= A:  # Require B > b + pml_length; use A to avoid roundoff from reconstruction.
        raise ValueError("Require B > b + actual PML thickness (= A).")
    a = max(abs(x) for x in fdtd_3d.CUSTOM_CENTER) + fdtd_3d.CUSTOM_RADIUS  # Half-width of a centered cube enclosing the source.
    epsilon, mu = uniform_materials()
    c = 1 / sqrt(epsilon * mu)  # Wave speed in the uniform medium.
    if dt > fdtd_3d.CFL * h / (c * sqrt(3)):  # CFL timestep limit for a uniform 3D grid.
        raise ValueError("dt exceeds the requested CFL limit.")

    padding = ceil((B - A) / h)  # Whole cells added per side to cover the requested reference box.
    B_actual = A + padding * h  # Rounded reference half-width; shared Yee locations stay aligned.
    T_end = simulation_time(a, b, B_actual, c, dt)  # Last safe grid time, reserving 3 timesteps.
    t_start = ceil(((b - a) / c) / dt) * dt  # Estimated PML entry time, rounded up to the time grid.
    if T_end <= 0 or t_start > T_end:  # Require a nonempty observation interval.
        raise ValueError("Increase B: no safe observation interval remains.")

    n_start = round(t_start / dt)
    times, absolute_E, absolute_H = [], [], []
    reference_E, reference_H = [], []
    pml_E, pml_H = [], []

    # Run PML first; keep only physical-domain snapshots, temporarily on disk.
    with TemporaryDirectory(prefix="pml_samples_") as folder:
        def record_pml(time, electric, centers, magnetic):
            n = round(time / dt)
            if n < n_start:
                return
            s = slice(pml_cells, -pml_cells)  # Retains the native edge/face shapes.
            fields = [field[s, s, s] for field in electric + magnetic]
            np.savez(Path(folder) / f"{n}.npz", *fields)

        # Run the reference from zero too; compare matching snapshots as it advances.
        def compare_reference(time, electric, centers, magnetic):
            n = round(time / dt)
            if n < n_start:
                return
            trim = padding + pml_cells  # Remove reference padding AND small-domain PML.
            s = slice(trim, -trim)
            fields = [field[s, s, s] for field in electric + magnetic]
            path = Path(folder) / f"{n}.npz"
            with np.load(path) as saved:
                small = [saved[f"arr_{i}"] for i in range(6)]
            times.append(time)
            difference_E, norm_E = l2_norms(small[:3], fields[:3])
            difference_H, norm_H = l2_norms(small[3:], fields[3:])
            absolute_E.append(difference_E)
            absolute_H.append(difference_H)
            reference_E.append(norm_E)
            reference_H.append(norm_H)
            # PML field norms, not errors: ||F_pml||_2 = sqrt(sum_x,y,z sum(F_component**2)).
            pml_E.append(sqrt(sum(np.sum(component**2) for component in small[:3])))
            pml_H.append(sqrt(sum(np.sum(component**2) for component in small[3:])))
            path.unlink()  # This snapshot is no longer needed.

        pml_result = fdtd_with_pml(T_end, dt, on_frame=record_pml)
        reference_result = fdtd_reference(pml_result, B, on_frame=compare_reference)

    # Normalize only after the full observation interval supplies both peaks.
    absolute_E, absolute_H = np.asarray(absolute_E), np.asarray(absolute_H)
    peak_E, peak_H =max(reference_E), max(reference_H)

    error_E = absolute_E / peak_E if peak_E > 0 else np.full_like(absolute_E, np.nan)
    error_H = absolute_H / peak_H if peak_H > 0 else np.full_like(absolute_H, np.nan)


    return dict(
        absolute_E=absolute_E, absolute_H=absolute_H,  # Unweighted discrete L2 differences.
        reference_E=np.asarray(reference_E), reference_H=np.asarray(reference_H),
        pml_L2_E=np.asarray(pml_E), pml_L2_H=np.asarray(pml_H),  # Same physical-domain norm.
        peak_E=peak_E, peak_H=peak_H,  # Fixed denominators over the observation interval.
        times=np.asarray(times),  # Sample times in the observation interval.
        error_E=np.asarray(error_E),  # Peak-normalized electric-field error.
        error_H=np.asarray(error_H),  # Peak-normalized magnetic-field error.
        pml=pml_result,  # Final small-domain E/H and grid information.
        reference=reference_result,  # Final reference E/H and grid information.
        t_start=t_start,  # First grid time in the observation interval.
        T_end=T_end,  # Common final time and end of the observation interval.
        t_return=(2 * B_actual - a - b) / c,  # Continuum bound for reference-wall reflection returning to the physical region.
    )


def main():
    """Read fdtd_3d parameters and run only the two analysis simulations.

    dt follows the grid, medium and CFL. The reference size determines the
    safe T_end; fdtd_3d.T_END belongs to the ordinary visualization run.
    Returns final fields, time bounds and peak-normalized error histories; saves PNG/CSV.
    """
    h = (fdtd_3d.X_RANGE[1] - fdtd_3d.X_RANGE[0]) / fdtd_3d.NX
    epsilon, mu = uniform_materials()
    c = 1 / sqrt(epsilon * mu)
    dt = fdtd_3d.CFL * h / (c * sqrt(3))  # Automatic timestep; run_simulations checks the cube.
    print(f"Running PML/reference only; requested B={fdtd_3d.REFERENCE_HALF_WIDTH:g}, dt={dt:.6g}", flush=True)
    runs, total_seconds = timed_call("Analysis pair total", run_simulations,
                                     fdtd_3d.REFERENCE_HALF_WIDTH, dt)
    runs["wall_seconds"] = total_seconds
    pair_flops = sum(runs[key]["performance"]["estimated_core_flops"] for key in ("pml", "reference"))
    print(f"Analysis pair: estimated core FLOPs = {pair_flops:,}")
    print(f"Actual PML length: {runs['pml']['pml']['thickness'][0]:.6g}")
    print(f"Actual B: {runs['reference']['bounds'][0, 1]:.6g}")
    print(f"Actual b: {runs['pml']['physical_bounds'][0, 1]:.6g}")
    print(f"Cells: with PML {runs['pml']['cells']}, reference {runs['reference']['cells']}")
    print(f"Observation interval: [{runs['t_start']:.6g}, {runs['T_end']:.6g}]")
    path, plot_seconds = timed_call("Error plot", save_error_history,
                                    runs["times"], runs["error_E"], runs["error_H"])
    runs["plot_seconds"] = plot_seconds
    norm_path, norm_seconds = timed_call(
        "Norm plot", save_error_norms, runs["times"],
        runs["absolute_E"], runs["absolute_H"],
        runs["reference_E"], runs["reference_H"])
    runs["plot_seconds"] += norm_seconds
    np.savetxt(path.with_suffix(".csv"),
               np.column_stack((runs["times"], runs["error_E"], runs["error_H"],
                                runs["absolute_E"], runs["absolute_H"],
                                runs["reference_E"], runs["reference_H"],
                                runs["pml_L2_E"], runs["pml_L2_H"])),
               delimiter=",", header="time,peak_normalized_E,peak_normalized_H,absolute_L2_E,absolute_L2_H,reference_L2_E,reference_L2_H,pml_L2_E,pml_L2_H",
               comments="")
    print(f"Saved: {path}")
    print(f"Saved: {norm_path}")
    return runs


if __name__ == "__main__":
    runs = main()
