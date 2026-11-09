"""Reusable 3D Yee FDTD for a uniform medium and six PEC walls.

All inputs use SI units. Arrays use axis order (x, y, z).
For cells=(Nx, Ny, Nz), the staggered field shapes are:
    E: (Nx, Ny+1, Nz+1), (Nx+1, Ny, Nz+1), (Nx+1, Ny+1, Nz)
    H: (Nx+1, Ny, Nz),   (Nx, Ny+1, Nz),   (Nx, Ny, Nz+1)
See solve's docstring for the calling contract, units and return values.
This module depends only on NumPy; it does not import example or plotting code.
"""

import numpy as np

C0 = 299_792_458.0
MU0 = 4 * np.pi * 1e-7  # vacuum permeability [H/m]
EPSILON0 = 1 / (MU0 * C0**2)  # vacuum permittivity [F/m]


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


def gauss_law_residual(electric, charge, spacing, epsilon=EPSILON0):
    """Return the discrete interior Gauss-law residual [C/m^3].

    The Yee-grid divergence is evaluated at interior nodes.  PEC surface
    charges are intentionally excluded, so this is an *interior* diagnostic:

        residual = epsilon * div_h(E) - rho.

    Arrays use the same placement as solve() and are not modified.
    """
    return epsilon * divergence_e(electric, spacing) - charge


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


def magnetic_at_e_time(electric, magnetic, spacing, dt, mu=MU0):
    """Align staggered H with the time of E for output only.

    Inputs: electric at t [V/m], magnetic at t-dt/2 [A/m], using E/H shapes;
            spacing=(dx,dy,dz) [m], dt [s], permeability mu [H/m].
    Returns: (Hx,Hy,Hz) at t [A/m], new H-shaped arrays.
    Uses H(t) = H(t-dt/2) - dt/(2*mu)*curl(E(t)); inputs are unchanged.
    """
    curl = curl_e(electric, spacing)
    aligned = []
    for component in range(3):
        aligned.append(magnetic[component] - dt / (2 * mu) * curl[component])
    return tuple(aligned)


def solve(bounds, cells, end_time, cfl=0.8, current_density=None,
          on_frame=None, frame_every=1, *, epsilon=EPSILON0, mu=MU0):
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
        gauss_residual_rms, gauss_residual_max: interior discrete Gauss-law
            residual diagnostics [C/m^3] at the final time.
    Field shapes are listed in the module docstring.

    Notes
    -----
    Uses reflecting PEC walls, no loss, PML, nonuniform mesh or material map.
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
    if on_frame is not None:
        on_frame(0.0, electric, tuple(centers), magnetic)

    # 2. Advance all six field components, then enforce the boundary condition.
    for n in range(steps):
        # H^(n+1/2) = H^(n-1/2) - dt/mu * curl(E^n)
        curl_x, curl_y, curl_z = curl_e(electric, spacing)
        hx -= dt / mu * curl_x
        hy -= dt / mu * curl_y
        hz -= dt / mu * curl_z

        current = sample_current(current_density, e_coordinates, (n + 0.5) * dt)
        jx, jy, jz = current

        # E^(n+1) = E^n + dt/epsilon * (curl(H^(n+1/2)) - J^(n+1/2))
        curl_x, curl_y, curl_z = curl_h(magnetic, spacing)
        ex += dt / epsilon * (curl_x - jx)
        ey += dt / epsilon * (curl_y - jy)
        ez += dt / epsilon * (curl_z - jz)
        apply_pec(electric)
        charge -= dt * divergence_e(current, spacing)

        record_step = (n + 1) % frame_every == 0 or n + 1 == steps
        if on_frame is not None and record_step:
            aligned_h = magnetic_at_e_time(electric, magnetic, spacing, dt, mu)
            on_frame((n + 1) * dt, electric, tuple(centers), aligned_h)

    # 3. Interior charge consistency: eps * div_h(E) - rho should be small.
    residual = gauss_law_residual(electric, charge, spacing, epsilon)
    residual_rms = float(np.sqrt(np.mean(residual**2)))
    residual_max = float(np.max(np.abs(residual)))

    # 4. Return fields at the same physical time, with grid and medium metadata.
    return {
        "electric": electric,
        "magnetic": magnetic_at_e_time(electric, magnetic, spacing, dt, mu),
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
        "gauss_residual_rms": residual_rms,
        "gauss_residual_max": residual_max,
    }
