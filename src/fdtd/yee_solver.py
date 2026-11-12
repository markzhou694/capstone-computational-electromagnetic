"""Reusable 3D Yee FDTD with PEC walls and optional interior PML layers.

All inputs use SI units. Arrays use axis order (x, y, z).
For cells=(Nx, Ny, Nz), the staggered field shapes are:
    E: (Nx, Ny+1, Nz+1), (Nx+1, Ny, Nz+1), (Nx+1, Ny+1, Nz)
    H: (Nx+1, Ny, Nz),   (Nx, Ny+1, Nz),   (Nx, Ny, Nz+1)
See ../docs/API.md for the complete calling contract and runnable examples.
This module depends only on NumPy; it does not import example or plotting code.
"""

import numpy as np

C0 = 299_792_458.0
MU0 = 4 * np.pi * 1e-5 
EPSILON0 = 1 / (MU0 * C0**2)


def curl_e(electric, spacing):
    """Compute curl(E) on Yee faces without changing the input.

    Inputs: electric=(Ex,Ey,Ez), E-shaped arrays [V/m];
            spacing=(dx,dy,dz), three positive lengths [m].
    Returns: (curl_x,curl_y,curl_z), H-shaped arrays [V/m^2].
    E/H shapes are listed in the module docstring.
    """
    ex, ey, ez = electric
    dx, dy, dz = spacing
    curl_x = np.diff(ez, axis=1) / dy - np.diff(ey, axis=2) / dz
    curl_y = np.diff(ex, axis=2) / dz - np.diff(ez, axis=0) / dx
    curl_z = np.diff(ey, axis=0) / dx - np.diff(ex, axis=1) / dy
    return curl_x, curl_y, curl_z


def curl_h(magnetic, spacing):
    """Compute curl(H) on Yee edges, with zero tangential boundary entries.

    Inputs: magnetic=(Hx,Hy,Hz), H-shaped arrays [A/m];
            spacing=(dx,dy,dz) [m]. Inputs are not changed.
    Returns: (curl_x,curl_y,curl_z), E-shaped arrays [A/m^2].
    The boundary entries are placeholders for the PEC electric-field update.
    """
    hx, hy, hz = magnetic
    dx, dy, dz = spacing
    nx, ny, nz = hx.shape[0] - 1, hy.shape[1] - 1, hz.shape[2] - 1
    curl_x = np.zeros((nx, ny + 1, nz + 1))
    curl_y = np.zeros((nx + 1, ny, nz + 1))
    curl_z = np.zeros((nx + 1, ny + 1, nz))
    curl_x[:, 1:-1, 1:-1] = (
        np.diff(hz[:, :, 1:-1], axis=1) / dy
        - np.diff(hy[:, 1:-1, :], axis=2) / dz
    )
    curl_y[1:-1, :, 1:-1] = (
        np.diff(hx[1:-1, :, :], axis=2) / dz
        - np.diff(hz[:, :, 1:-1], axis=0) / dx
    )
    curl_z[1:-1, 1:-1, :] = (
        np.diff(hy[:, 1:-1, :], axis=0) / dx
        - np.diff(hx[1:-1, :, :], axis=1) / dy
    )
    return curl_x, curl_y, curl_z


def divergence_e(fields, spacing):
    """Compute the divergence of any E-shaped vector field at interior nodes.

    Inputs: fields=(Fx,Fy,Fz), E-shaped arrays; spacing=(dx,dy,dz) [m].
    Returns: array of shape (Nx-1,Ny-1,Nz-1), in field units per metre.
    Accepts E or J; does not change inputs or include wall surface charge.
    """
    fx, fy, fz = fields
    dx, dy, dz = spacing
    dfx_dx = np.diff(fx[:, 1:-1, 1:-1], axis=0) / dx
    dfy_dy = np.diff(fy[1:-1, :, 1:-1], axis=1) / dy
    dfz_dz = np.diff(fz[1:-1, 1:-1, :], axis=2) / dz
    return dfx_dx + dfy_dy + dfz_dz


def sample_current(current_density, coordinates, time):
    """Evaluate each current component at its own Yee edge locations.

    Inputs: current_density(x,y,z,t) -> (Jx,Jy,Jz), or None for zero;
            coordinates=[xyz_for_Ex, xyz_for_Ey, xyz_for_Ez], each xyz a
            tuple/list of three sparse meshgrid arrays [m]; time is in [s].
    Returns: (Jx,Jy,Jz), finite E-shaped arrays [A/m^2]. Treat as read-only.
    Source components may be scalar or broadcastable to their grid.
    Raises ValueError for a wrong component count, shape or non-finite values.
    """
    current = []
    for component in range(3):
        x, y, z = coordinates[component]
        shape = np.broadcast_shapes(x.shape, y.shape, z.shape)
        if current_density is None:
            values = (0.0, 0.0, 0.0)
        else:
            values = current_density(x, y, z, time)
        if not isinstance(values, (tuple, list, np.ndarray)):
            raise ValueError("current_density must return (Jx, Jy, Jz).")
        if isinstance(values, np.ndarray) and values.ndim == 0:
            raise ValueError("current_density must return (Jx, Jy, Jz).")
        if len(values) != 3:
            raise ValueError("current_density must return (Jx, Jy, Jz).")
        if np.iscomplexobj(values[component]):
            raise ValueError("Current components must be real-valued.")
        try:
            value = np.asarray(values[component], dtype=float)
            value = np.broadcast_to(value, shape)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Current component {component} must broadcast to {shape}.") from error
        if not np.isfinite(value).all():
            raise ValueError("Current components must be finite.")
        current.append(value)
    return tuple(current)


def apply_pec(electric):
    """Set tangential E to zero on all six walls, in place.

    Input: electric=(Ex,Ey,Ez), writable E-shaped arrays [V/m].
    Returns: None. Normal components are unchanged.
    """
    ex, ey, ez = electric
    ex[:, [0, -1], :] = 0
    ex[:, :, [0, -1]] = 0
    ey[[0, -1], :, :] = 0
    ey[:, :, [0, -1]] = 0
    ez[[0, -1], :, :] = 0
    ez[:, [0, -1], :] = 0


def _pml_coefficients(coordinates, physical_bounds, thickness, sigma_max,
                      order, epsilon, dt):
    """Sample Jin's polynomial loss at each component's own Yee location.

    coordinates contains three sparse xyz grids (one per field component).
    Return coefficients[component][axis] = (a, b), where
    a = 1 - sigma*dt/(2*epsilon), b = 1 + sigma*dt/(2*epsilon).
    These are Jin (8.5.70)'s alpha,beta multiplied by dt/epsilon.
    sigma is in S/m; sigma/epsilon is the matched loss rate for BOTH E and H.
    Each axis depends only on its own coordinate; all three act at corners.
    """
    coefficients = []
    for xyz in coordinates:
        component_coefficients = []
        for axis, coordinate in enumerate(xyz):
            low, high = physical_bounds[axis]
            depth = np.maximum(np.maximum(low - coordinate, coordinate - high), 0.0)
            fraction = np.clip(depth / thickness[axis], 0.0, 1.0)
            sigma = sigma_max[axis] * fraction**order
            loss = sigma * dt / (2 * epsilon)
            component_coefficients.append((1 - loss, 1 + loss))
        coefficients.append(tuple(component_coefficients))
    return tuple(coefficients)


def _pml_step(field, auxiliary, drive, coefficients, dt, material):
    """Advance B->H or D->E by Jin (8.5.78)-(8.5.83); no input mutation.

    For B,H: drive=-curl(E), material=mu, old/new times n-1/2,n+1/2.
    For D,E: drive=curl(H)-J, material=epsilon, old/new times n,n+1.
    Auxiliary and physical components share array shapes and locations.
    (p,q,r) cycles through (x,y,z), (y,z,x), (z,x,y).
    """
    new_auxiliary, new_field = [], []
    for p in range(3):
        q, r = (p + 1) % 3, (p + 2) % 3
        a_p, b_p = coefficients[p][p]
        a_q, b_q = coefficients[p][q]
        a_r, b_r = coefficients[p][r]
        auxiliary_new = (a_q * auxiliary[p] + dt * drive[p]) / b_q
        field_new = (a_r * field[p]
                     + (b_p * auxiliary_new - a_p * auxiliary[p]) / material) / b_r
        new_auxiliary.append(auxiliary_new)
        new_field.append(field_new)
    return tuple(new_auxiliary), tuple(new_field)


def magnetic_at_e_time(electric, magnetic, spacing, dt, mu=MU0, *,
                       pml_b=None, pml_coefficients=None):
    """Align staggered H with the time of E for output only.

    Inputs: electric at t [V/m], magnetic at t-dt/2 [A/m], using E/H shapes;
            spacing=(dx,dy,dz) [m], dt [s], permeability mu [H/m].
    Returns: (Hx,Hy,Hz) at t [A/m], new H-shaped arrays.
    Uses H(t) = H(t-dt/2) - dt/(2*mu)*curl(E(t)); inputs are unchanged.
    For PML, supply auxiliary B at t-dt/2 and full-dt H-grid coefficients.
    Predict H(t+dt/2) with the PML equations and average the two half levels.
    This is second-order time interpolation; the prediction is output only.
    """
    curl = curl_e(electric, spacing)
    if pml_b is not None or pml_coefficients is not None:
        if pml_b is None or pml_coefficients is None:
            raise ValueError("PML time alignment needs both B and coefficients.")
        drive = tuple(-value for value in curl)
        _, next_h = _pml_step(magnetic, pml_b, drive, pml_coefficients, dt, mu)
        return tuple((old + new) / 2 for old, new in zip(magnetic, next_h))
    aligned = []
    for component in range(3):
        aligned.append(magnetic[component] - dt / (2 * mu) * curl[component])
    return tuple(aligned)


def solve(bounds, cells, end_time, cfl=0.8, current_density=None,
          on_frame=None, frame_every=1, *, epsilon=EPSILON0, mu=MU0,
          pml_cells=0, pml_order=3, pml_reflection=1e-6, pml_sigma_max=None):
    """Solve 3D Maxwell equations from E=H=rho=0 in a uniform medium.

    Inputs
    ------
    bounds : sequence or float array, shape (3, 2)
        ((xmin,xmax),(ymin,ymax),(zmin,zmax)) [m]; finite min < max.
    cells : sequence of three integers
        (Nx,Ny,Nz), each >= 2. Spacing is uniform within each axis.
    end_time : positive float
        Final simulation time [s]. The last step reaches this time.
    cfl : float in (0, 1], default 0.8
        Fraction of the 3D CFL time-step limit.
    current_density : callable or None
        Function (x,y,z,t) -> (Jx,Jy,Jz) [A/m^2]; None means zero.
        x,y,z are sparse, broadcastable arrays [m]; t is a scalar [s].
        Return real scalars or broadcastable arrays. Called three times per
        step, at the three E grids and at t=(n+1/2)*dt; avoid side effects.
    on_frame : callable or None
        Function (time,electric,centers,magnetic) -> None. Both fields are
        aligned to time [s]. Called at t=0, every frame_every steps, and T.
        Do not modify its arrays; copy data that must survive the callback.
    frame_every : positive integer, default 1
        Output stride; has no effect on the calculated fields.
    epsilon, mu : positive finite scalars, keyword-only
        Uniform permittivity [F/m] and permeability [H/m]; default vacuum.
    pml_cells : nonnegative integer, default 0 (original PEC-only solver)
        PML cell count on EACH of the six sides, INSIDE bounds; requires
        2*pml_cells < min(cells). Bounds, spacing and array shapes stay fixed.
        Keep sources inside the physical interior, away from the PML.
        Currents are not clipped; driving the artificial layer is not the
        intended source-free PML/open-domain model.
    pml_order : positive integer, default 3
        Exponent m in sigma(l)=sigma_max*(l/L)**m.
    pml_reflection : float in (0,1), default 1e-6
        Theoretical normal-incidence round-trip AMPLITUDE reflection R0.
        sigma_max=-(m+1)*log(R0)/(2*sqrt(mu/epsilon)*L), L=pml_cells*spacing.
        This is not a bound on numerical reflection or grazing incidence.
    pml_sigma_max : None, nonnegative scalar, or length-3 sequence [S/m]
        Optional override of sigma_max (x,y,z). Zero permits a lossless check.
        Other PML settings are ignored when pml_cells=0.

    Returns
    -------
    dict with keys:
        electric: (Ex,Ey,Ez) [V/m]; magnetic: (Hx,Hy,Hz) [A/m], both at T.
        charge: interior rho [C/m^3], shape (Nx-1,Ny-1,Nz-1).
        bounds: float array (3,2) [m]; cells: (Nx,Ny,Nz).
        nodes: (x,y,z) arrays of lengths Nx+1,Ny+1,Nz+1 [m].
        centers: (xc,yc,zc) arrays of lengths Nx,Ny,Nz [m].
        spacing: float array (3,) [m]; time,dt: floats [s]; steps: int.
        cfl: actual dt/dt_limit; epsilon,mu: the medium parameters.
        With PML only, also physical_bounds: (3,2) undamped interior [m],
        and pml: dict with cells, order, thickness [m], sigma_max [S/m],
        and theoretical_reflection (three normal-incidence amplitudes).
    Field shapes are listed in the module docstring and ../docs/API.md.

    Notes
    -----
    Jin (2010), Sec. 8.5.3: auxiliary B,H,D,E PML, terminated by PEC.
    D and B are auxiliary fields, not simply epsilon*E and mu*H in PML.
    The original CFL limit is retained. No material map or nonuniform mesh.
    charge always integrates -div(J); epsilon*div(E)=charge applies only
    where the entire divergence stencil lies in the undamped interior.
    Static/evanescent fields are not well absorbed by this conventional PML.
    No plotting or file writes. Invalid settings raise ValueError.
    """
    bounds = np.array(bounds, dtype=float, copy=True)
    if bounds.shape != (3, 2) or not np.isfinite(bounds).all():
        raise ValueError("bounds must be a finite array of shape (3, 2).")
    if np.any(bounds[:, 1] <= bounds[:, 0]):
        raise ValueError("Each bound must have min < max.")
    if len(cells) != 3 or any(not isinstance(n, (int, np.integer)) or n < 2 for n in cells):
        raise ValueError("cells must contain three integers >= 2.")
    if not np.isfinite(cfl) or not 0 < cfl <= 1:
        raise ValueError("cfl must satisfy 0 < cfl <= 1.")
    if not np.isfinite(end_time) or end_time <= 0:
        raise ValueError("end_time must be positive and finite, in seconds.")
    if not isinstance(frame_every, (int, np.integer)) or frame_every < 1:
        raise ValueError("frame_every must be a positive integer.")
    for name, value in (("epsilon", epsilon), ("mu", mu)):
        if np.ndim(value) != 0 or not np.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a positive finite scalar.")
    if current_density is not None and not callable(current_density):
        raise ValueError("current_density must be callable or None.")
    if on_frame is not None and not callable(on_frame):
        raise ValueError("on_frame must be callable or None.")
    if (isinstance(pml_cells, (bool, np.bool_))
            or not isinstance(pml_cells, (int, np.integer)) or pml_cells < 0):
        raise ValueError("pml_cells must be a nonnegative integer.")
    if pml_cells:
        if 2 * pml_cells >= min(cells):
            raise ValueError("PML must leave an interior: 2*pml_cells < min(cells).")
        if (isinstance(pml_order, (bool, np.bool_))
                or not isinstance(pml_order, (int, np.integer)) or pml_order < 1):
            raise ValueError("pml_order must be a positive integer.")
        if (np.ndim(pml_reflection) != 0 or not np.isfinite(pml_reflection)
                or not 0 < pml_reflection < 1):
            raise ValueError("pml_reflection must be between 0 and 1 (exclusive).")

    # 1. Build the grid. Components are stored at their Yee edge/face locations.
    nx, ny, nz = cells
    spacing = (bounds[:, 1] - bounds[:, 0]) / cells
    nodes, centers = [], []
    for (low, high), count in zip(bounds, cells):
        q = np.linspace(low, high, count + 1)
        nodes.append(q)
        centers.append((q[:-1] + q[1:]) / 2)
    x, y, z = nodes
    xc, yc, zc = centers
    e_coordinates = (
        np.meshgrid(xc, y, z, indexing="ij", sparse=True),
        np.meshgrid(x, yc, z, indexing="ij", sparse=True),
        np.meshgrid(x, y, zc, indexing="ij", sparse=True),
    )
    # alternating E/H shapes are listed in the module docstring and ../docs/API.md.
    ex = np.zeros((nx, ny + 1, nz + 1))
    ey = np.zeros((nx + 1, ny, nz + 1))
    ez = np.zeros((nx + 1, ny + 1, nz))
    hx = np.zeros((nx + 1, ny, nz))
    hy = np.zeros((nx, ny + 1, nz))
    hz = np.zeros((nx, ny, nz + 1))
    electric = (ex, ey, ez)
    magnetic = (hx, hy, hz)
    charge = np.zeros((nx - 1, ny - 1, nz - 1))

    wave_speed = 1 / np.sqrt(epsilon * mu)
    dt_limit = 1 / (wave_speed * np.sqrt(np.sum(1 / spacing**2)))
    steps = int(np.ceil(end_time / (cfl * dt_limit)))
    dt = end_time / steps
    alignment = {}
    if pml_cells:
        thickness = pml_cells * spacing
        physical_bounds = bounds.copy()
        # Use the interface nodes themselves to avoid coordinate roundoff.
        for axis in range(3):
            physical_bounds[axis] = (nodes[axis][pml_cells], nodes[axis][-pml_cells-1])
        impedance = np.sqrt(mu / epsilon)
        sigma_max = -(pml_order + 1) * np.log(pml_reflection) / (2 * impedance * thickness)
        if pml_sigma_max is not None:
            sigma_max = np.asarray(pml_sigma_max, dtype=float)
            if sigma_max.shape == ():
                sigma_max = np.full(3, float(sigma_max))
            if sigma_max.shape != (3,) or not np.isfinite(sigma_max).all() or np.any(sigma_max < 0):
                raise ValueError("pml_sigma_max must be nonnegative and finite, scalar or length 3.")
        h_coordinates = (
            np.meshgrid(x, yc, zc, indexing="ij", sparse=True),
            np.meshgrid(xc, y, zc, indexing="ij", sparse=True),
            np.meshgrid(xc, yc, z, indexing="ij", sparse=True),
        )
        e_coefficients = _pml_coefficients(
            e_coordinates, physical_bounds, thickness, sigma_max, pml_order, epsilon, dt)
        h_coefficients = _pml_coefficients(
            h_coordinates, physical_bounds, thickness, sigma_max, pml_order, epsilon, dt)
        auxiliary_d = tuple(np.zeros_like(value) for value in electric)
        auxiliary_b = tuple(np.zeros_like(value) for value in magnetic)
        pml_info = dict(cells=pml_cells, order=pml_order, thickness=thickness,
                        sigma_max=sigma_max.copy(), theoretical_reflection=np.exp(
                            -2 * impedance * sigma_max * thickness / (pml_order + 1)))
    if on_frame is not None:
        on_frame(0.0, electric, tuple(centers), magnetic)

    # 2. Advance all six field components, then enforce the boundary condition.
    for n in range(steps):
        # H^(n+1/2) = H^(n-1/2) - dt/mu * curl(E^n)
        curl_x, curl_y, curl_z = curl_e(electric, spacing)
        if pml_cells:
            auxiliary_b, magnetic = _pml_step(
                magnetic, auxiliary_b, (-curl_x, -curl_y, -curl_z), h_coefficients, dt, mu)
            alignment = dict(pml_b=auxiliary_b, pml_coefficients=h_coefficients)
        else:
            hx -= dt / mu * curl_x
            hy -= dt / mu * curl_y
            hz -= dt / mu * curl_z

        current = sample_current(current_density, e_coordinates, (n + 0.5) * dt)
        jx, jy, jz = current

        # E^(n+1) = E^n + dt/epsilon * (curl(H^(n+1/2)) - J^(n+1/2))
        curl_x, curl_y, curl_z = curl_h(magnetic, spacing)
        if pml_cells:
            auxiliary_d, electric = _pml_step(
                electric, auxiliary_d, (curl_x-jx, curl_y-jy, curl_z-jz),
                e_coefficients, dt, epsilon)
            apply_pec(auxiliary_d)
        else:
            ex += dt / epsilon * (curl_x - jx)
            ey += dt / epsilon * (curl_y - jy)
            ez += dt / epsilon * (curl_z - jz)
        apply_pec(electric)
        charge -= dt * divergence_e(current, spacing)

        record_step = (n + 1) % frame_every == 0 or n + 1 == steps
        if on_frame is not None and record_step:
            aligned_h = magnetic_at_e_time(electric, magnetic, spacing, dt, mu, **alignment)
            on_frame((n + 1) * dt, electric, tuple(centers), aligned_h)

    # 3. Return fields at the same physical time, with grid and medium metadata.
    result = {
        "electric": electric,
        "magnetic": magnetic_at_e_time(electric, magnetic, spacing, dt, mu, **alignment),
        "charge": charge,
        "bounds": bounds,
        "cells": tuple(cells),
        "nodes": tuple(nodes),
        "centers": tuple(centers),
        "spacing": spacing,
        "time": end_time,
        "dt": dt,
        "steps": steps,
        "cfl": dt / dt_limit,
        "epsilon": epsilon,
        "mu": mu,
    }
    if pml_cells:
        result.update(physical_bounds=physical_bounds, pml=pml_info)
    return result
