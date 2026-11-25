"""Direct time-domain Maxwell surface integration on latitude/longitude points.

1. Run fdtd_3d.custom_current and record E,H on a source-centered sphere.
2. Form Js = n x H, Ms = -n x E, rho = epsilon*n.E, rho_m = mu*n.H.
3. Evaluate the retarded data at t_r = t - |x-y|/c and sum area-weighted terms.

Green function: G(R,t-t') = delta(t-t'-R/c)/(4*pi*R).
The delta function performs the time integral: there is NO extra dt factor.
This evaluates known surface data, not an equation for unknown currents.
The full kernels retain 1/R and 1/R**2 terms; no far-field approximation.

Assumptions: zero initial fields, no incoming waves, all sources/material
contrasts enclosed, and a homogeneous lossless exterior continued to infinity.
PML errors in the recorded fields also affect the reconstructed fields.
Coordinates, fields and time use the same units as fdtd_3d, not ns.
"""

from pathlib import Path
import numpy as np
import fdtd_3d
import yee_solver
from field_extraction import sphere_points, trilinear
from plot_fields import save_sphere_samples, save_exterior_fields
from run_metrics import timed_solve, timed_call

# Grid, source, material, PML and recording duration come from fdtd_3d.py.
RADIUS = None                    # None: midpoint between source and physical wall.
N_THETA = 16                      # Latitude rings; refine to check surface integration.
N_PHI = 32                        # Longitudes per ring.
OBSERVATION_POINT = (2.0, 5.0, 10.0)  # Must be strictly outside the integration sphere.


def sphere_quadrature(physical_bounds, radius=None, n_theta=16, n_phi=32):
    """Return existing sphere geometry plus area weights (Ns,).

    theta_i=(i+1/2)*pi/n_theta, phi_j=j*2*pi/n_phi.
    w_ij=radius**2*dphi*[cos(i*dtheta)-cos((i+1)*dtheta)].
    These are patch areas, not equal weights; sum(w)=4*pi*radius**2.
    The two extra pole samples remain in the data/preview with zero weight:
    the latitude patches already cover the entire sphere, including the caps.
    """
    sphere = sphere_points(physical_bounds, radius, n_theta, n_phi)
    edges = np.linspace(0, np.pi, n_theta + 1)
    ring_weight = sphere["radius"]**2 * (2*np.pi/n_phi) * (
        np.cos(edges[:-1]) - np.cos(edges[1:]))
    sphere["weights"] = np.r_[np.repeat(ring_weight, n_phi), 0.0, 0.0]
    return sphere


def exterior_materials(settings, nodes, centers, sphere):
    """Read epsilon_b, mu_b; check a homogeneous collar and grid exterior.

    Check native Yee material samples from radius-one_cell_diagonal outward.
    The collar keeps interpolation stencils away from material interfaces.
    This sampled check cannot detect unresolved objects or anything outside
    the FDTD box; the user must continue this same background to infinity.
    """
    spacing = np.array([q[1] - q[0] for q in nodes])
    collar = np.linalg.norm(spacing)
    center, radius = sphere["center"], sphere["radius"]
    bounds = sphere["physical_bounds"]
    clearance = min(np.min(center-bounds[:, 0]), np.min(bounds[:, 1]-center))
    if radius <= sphere["source_radius"] + collar or radius + collar >= clearance:
        raise ValueError("Leave one cell diagonal between sphere, source and PML; refine or change RADIUS.")
    background = []
    for name, kind in (("epsilon", "E"), ("mu", "H")):
        constant = None
        for component in range(3):
            axes = [centers[d] if ((d == component) == (kind == "E")) else nodes[d]
                    for d in range(3)]
            xyz = np.meshgrid(*axes, indexing="ij", sparse=True)
            values = yee_solver.sample_material(settings[name], [xyz], name)[0]
            if constant is None:
                constant = float(values.flat[0])
            r_squared = sum((q-center[d])**2 for d, q in enumerate(xyz))
            outside = r_squared >= (radius-collar)**2
            if not np.allclose(values[outside], constant, rtol=1e-12, atol=0):
                raise ValueError(f"{name} varies in the sphere collar/exterior; enlarge RADIUS or move the object.")
        background.append(constant)
    return tuple(background)


def record_surface(settings=None, radius=None, n_theta=16, n_phi=32):
    """Run one PML simulation; return only sphere histories and metadata.

    Default settings are read from fdtd_3d. E,H have shape (Nt,Ns,3), with
    Cartesian x,y,z columns, at times (Nt,). Record EVERY solver step,
    independent of the visualization FRAME_EVERY. H is already time-aligned.
    Full-grid snapshots are not retained. Memory scales as Nt*Ns, not Nt*Nx*Ny*Nz.
    """
    settings = dict(fdtd_3d.get_simulation_settings() if settings is None else settings)
    pml_cells = settings.get("pml_cells", 0)
    if pml_cells <= 0:
        raise ValueError("Enable PML for this outgoing-field experiment.")
    if 2*pml_cells >= min(settings["cells"]):
        raise ValueError("PML must leave a physical interior.")
    nodes = [np.linspace(low, high, n+1)
             for (low, high), n in zip(settings["bounds"], settings["cells"])]
    centers = [(q[:-1] + q[1:])/2 for q in nodes]
    physical_bounds = np.array([(q[pml_cells], q[-pml_cells-1]) for q in nodes])
    sphere = sphere_quadrature(physical_bounds, radius, n_theta, n_phi)
    epsilon, mu = exterior_materials(settings, nodes, centers, sphere)

    x, y, z = nodes
    xc, yc, zc = centers
    e_axes = ((xc, y, z), (x, yc, z), (x, y, zc))
    h_axes = ((x, yc, zc), (xc, y, zc), (xc, yc, z))
    times, electric_history, magnetic_history = [], [], []

    def record(time, electric, unused_centers, magnetic):
        times.append(time)
        for fields, axes, history in ((electric, e_axes, electric_history),
                                      (magnetic, h_axes, magnetic_history)):
            samples = np.empty((len(sphere["points"]), 3))
            for component in range(3):
                # Interpolate from each component's own edges/faces, not cell centers.
                samples[:, component] = trilinear(fields[component], axes[component], sphere["points"])
            history.append(samples)

    print(f"Grid: {settings['cells']}; recording to t={settings['end_time']:g}", flush=True)
    print(f"Sphere: R={sphere['radius']:g}, {len(sphere['points'])} points; exterior epsilon={epsilon:g}, mu={mu:g}")
    settings.update(frame_every=1, on_frame=record)
    result = timed_solve("Surface FDTD", **settings)
    sphere.update(times=np.array(times), electric=np.array(electric_history),
                  magnetic=np.array(magnetic_history), epsilon=epsilon, mu=mu,
                  dt=result["dt"], cells=np.array(result["cells"]), spacing=result["spacing"])
    return sphere  # The full-grid solver result can now be released.


def delayed_values(times, values, retarded_times):
    """Linear interpolation of (Nt,3) data; zero before t=0, never pad the future."""
    if np.any(retarded_times > times[-1] + 1e-12*max(1, abs(times[-1]))):
        raise ValueError("Missing future surface data; increase fdtd_3d.T_END.")
    query = np.minimum(retarded_times, times[-1])  # Only absorb endpoint roundoff.
    result = np.empty((len(query), 3))
    for component in range(3):
        result[:, component] = np.interp(query, times, values[:, component], left=0.0)
    return result


def reconstruct_fields(surface, point, times=None):
    """Return E,H (No,3) and observation times (No,) at one exterior point.

    surface comes from record_surface or np.load('surface_history.npz').
    With r=|point-y| and u=(point-y)/r, evaluate ALL source terms at t-r/c:

      Js=n x H, Ms=-n x E, rho=epsilon*n.E, rho_m=mu*n.H
      E = sum w/(4*pi) * [-mu*Js_dot/r
            + u/epsilon*(rho/r**2 + rho_dot/(c*r))
            + u x (Ms/r**2 + Ms_dot/(c*r))]
      H = sum w/(4*pi) * [-u x (Js/r**2 + Js_dot/(c*r))
            - epsilon*Ms_dot/r + u/mu*(rho_m/r**2 + rho_m_dot/(c*r))]

    Dots: second-order finite differences in time, then linear interpolation.
    Normal traces supply the equivalent charges; tangential-current terms
    alone would omit part of the exact finite-distance field.

    Default output times: surface times + minimum sphere-to-point travel time.
    No output uses unrecorded future data. A short record may not contain the
    entire pulse; increase T_END for a longer waveform. Points on/inside the
    sphere are rejected; points very close to it need finer angular sampling.
    """
    source_times = np.asarray(surface["times"], dtype=float)
    electric = np.asarray(surface["electric"], dtype=float)
    magnetic = np.asarray(surface["magnetic"], dtype=float)
    points, normals = np.asarray(surface["points"]), np.asarray(surface["normals"])
    weights = np.asarray(surface["weights"])
    epsilon, mu = float(surface["epsilon"]), float(surface["mu"])
    if not np.isfinite([epsilon, mu]).all() or min(epsilon, mu) <= 0:
        raise ValueError("Exterior epsilon and mu must be positive finite constants.")
    if (source_times.ndim != 1 or len(source_times) < 3 or source_times[0] != 0
            or not np.isfinite(source_times).all() or np.any(np.diff(source_times) <= 0)):
        raise ValueError("Need at least three increasing surface times, starting at zero.")
    shape = (len(source_times), len(points), 3)
    for field in (electric, magnetic):
        if field.shape != shape or not np.isfinite(field).all() or np.any(field[0] != 0):
            raise ValueError("E,H must be finite (Nt,Ns,3) arrays with zero initial fields.")
    point = np.asarray(point, dtype=float)
    if point.shape != (3,) or not np.isfinite(point).all():
        raise ValueError("point must contain three finite coordinates.")
    gap = np.linalg.norm(point-surface["center"]) - float(surface["radius"])
    if gap <= 0:
        raise ValueError("Observation point must be strictly outside the sphere.")
    c = 1 / np.sqrt(epsilon*mu)
    if times is None:
        times = source_times + gap/c
    times = np.asarray(times, dtype=float)
    if times.ndim != 1 or len(times) == 0 or not np.isfinite(times).all():
        raise ValueError("Observation times must be a finite nonempty one-dimensional array.")
    if np.max(times) > source_times[-1] + gap/c + 1e-12*max(1, source_times[-1]):
        raise ValueError("Observation time needs future surface data; increase fdtd_3d.T_END.")

    # Uniform-grid interior: F_dot[n] = (F[n+1]-F[n-1])/(2*dt).
    # At both record endpoints, use second-order one-sided differences.
    dE = np.gradient(electric, source_times, axis=0, edge_order=2)
    dH = np.gradient(magnetic, source_times, axis=0, edge_order=2)
    E_out, H_out = np.zeros((len(times), 3)), np.zeros((len(times), 3))
    for q in range(len(points)):
        if weights[q] == 0:  # The poles are preview samples, not extra surface patches.
            continue
        displacement = point - points[q]
        r = np.linalg.norm(displacement)
        u, n = displacement/r, normals[q]
        t_retarded = times - r/c
        E = delayed_values(source_times, electric[:, q], t_retarded)
        H = delayed_values(source_times, magnetic[:, q], t_retarded)
        E_dot = delayed_values(source_times, dE[:, q], t_retarded)
        H_dot = delayed_values(source_times, dH[:, q], t_retarded)

        Js, Js_dot = np.cross(n, H), np.cross(n, H_dot)
        Ms, Ms_dot = -np.cross(n, E), -np.cross(n, E_dot)
        rho, rho_dot = epsilon*(E @ n), epsilon*(E_dot @ n)
        rho_m, rho_m_dot = mu*(H @ n), mu*(H_dot @ n)

        E_term = (-mu*Js_dot/r
                  + (rho/r**2 + rho_dot/(c*r))[:, None]*u/epsilon
                  + np.cross(u, Ms/r**2 + Ms_dot/(c*r)))
        H_term = (-np.cross(u, Js/r**2 + Js_dot/(c*r))
                  - epsilon*Ms_dot/r
                  + (rho_m/r**2 + rho_m_dot/(c*r))[:, None]*u/mu)
        E_out += weights[q]/(4*np.pi) * E_term
        H_out += weights[q]/(4*np.pi) * H_term
    return dict(times=times, electric=E_out, magnetic=H_out, point=point,
                epsilon=epsilon, mu=mu)


def main(output_dir=None):
    """Run once, integrate, and save reusable surface data plus exterior E/H."""
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs" / "near_to_far_field"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    surface = record_surface(radius=RADIUS, n_theta=N_THETA, n_phi=N_PHI)
    np.savez(output_dir / "surface_history.npz", **surface)
    exterior, seconds = timed_call("Retarded surface integral", reconstruct_fields,
                                   surface, OBSERVATION_POINT)
    np.savez(output_dir / "exterior_fields.npz", **exterior)
    figure = save_exterior_fields(exterior, output_dir)
    save_sphere_samples(surface, output_dir)
    print(f"Observation point: {exterior['point']}; t=[{exterior['times'][0]:.6g}, {exterior['times'][-1]:.6g}]")
    print(f"Saved surface_history.npz, exterior_fields.npz and sphere_samples.png in {output_dir}")
    print(f"Saved field plot: {figure}")
    return surface, exterior


if __name__ == "__main__":
    main()
