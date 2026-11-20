"""Sample native Yee fields on a sphere enclosing custom_current.

Run this file to preview the sampling geometry (no FDTD simulation).
Use extract_sphere(result) to sample an existing solver result at its time.
All coordinates and times use the solver's units.
"""

import numpy as np
import fdtd_3d
from plot_fields import save_sphere_samples

RADIUS = None       # None: halfway between source radius and nearest physical wall.
N_THETA =16        # Latitude rings, excluding the poles.
N_PHI =32         # Samples per ring; each pole is added exactly once.


def sphere_points(physical_bounds, radius=None, n_theta=16, n_phi=32):
    """Return sphere geometry: points/normals (M,3), center, radius and bounds.

    M = n_theta*n_phi + 2. The last two points are north and south poles.
    Angles are uniformly spaced, NOT equal-area quadrature points.
    The sphere strictly encloses CUSTOM_RADIUS and stays inside physical_bounds.
    Keep custom-current settings unchanged between solving and extraction.
    """
    bounds = np.asarray(physical_bounds, dtype=float)
    center = np.asarray(fdtd_3d.CUSTOM_CENTER, dtype=float)
    source_radius = float(fdtd_3d.CUSTOM_RADIUS)
    if bounds.shape != (3, 2) or not np.isfinite(bounds).all():
        raise ValueError("physical_bounds must be a finite (3,2) array.")
    if center.shape != (3,) or not np.isfinite(center).all():
        raise ValueError("CUSTOM_CENTER must contain three finite coordinates.")
    if not isinstance(n_theta, int) or not isinstance(n_phi, int) or n_theta < 1 or n_phi < 3:
        raise ValueError("Require integer n_theta >= 1 and n_phi >= 3.")
    distance = min(np.min(center - bounds[:, 0]), np.min(bounds[:, 1] - center))
    if radius is None:
        radius = (source_radius + distance) / 2
    if not 0 < source_radius < radius < distance:
        raise ValueError("Require 0 < source radius < sphere radius < nearest physical wall.")

    theta = (np.arange(n_theta) + 0.5) * np.pi / n_theta
    phi = np.arange(n_phi) * 2 * np.pi / n_phi
    theta, phi = np.meshgrid(theta, phi, indexing="ij")
    normals = np.column_stack((
        (np.sin(theta) * np.cos(phi)).ravel(),
        (np.sin(theta) * np.sin(phi)).ravel(),
        np.cos(theta).ravel(),
    ))
    normals = np.vstack((normals, [0, 0, 1], [0, 0, -1]))
    return dict(points=center + radius * normals, normals=normals,
                center=center, radius=radius, source_radius=source_radius,
                physical_bounds=bounds.copy())


def trilinear(values, axes, points):
    """Interpolate one component on its own Yee grid; never extrapolate.

    values.shape equals the three axis lengths; points has shape (M,3).
    Each result is a weighted sum of eight neighboring component samples.
    """
    values = np.asarray(values)
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3 or not np.isfinite(points).all():
        raise ValueError("points must be a finite (M,3) array.")
    if values.shape != tuple(len(axis) for axis in axes):
        raise ValueError("Field shape must match its coordinate axes.")
    indices, fractions = [], []
    for direction, axis in enumerate(axes):
        axis = np.asarray(axis)
        if len(axis) < 2 or not np.isfinite(axis).all() or np.any(np.diff(axis) <= 0):
            raise ValueError("Each axis needs at least two increasing finite coordinates.")
        coordinate = points[:, direction]
        if np.any(coordinate < axis[0]) or np.any(coordinate > axis[-1]):
            raise ValueError("Sphere points lie outside the component's interpolation grid.")
        index = np.searchsorted(axis, coordinate, side="right") - 1
        index = np.clip(index, 0, len(axis) - 2)
        fraction = (coordinate - axis[index]) / (axis[index + 1] - axis[index])
        indices.append(index)
        fractions.append(fraction)

    i, j, k = indices
    u, v, w = fractions
    result = np.zeros(len(points), dtype=np.result_type(values.dtype, float))
    # Tensor-product weights: (1-u,u) * (1-v,v) * (1-w,w).
    for di in (0, 1):
        for dj in (0, 1):
            for dk in (0, 1):
                weight = (u if di else 1-u) * (v if dj else 1-v) * (w if dk else 1-w)
                result += weight * values[i+di, j+dj, k+dk]
    return result


def extract_sphere(result, radius=None, n_theta=16, n_phi=32):
    """Return geometry plus electric/magnetic arrays (M,3) at result['time'].

    Columns are Cartesian x,y,z components, not spherical components.
    E/H are already time-aligned by yee_solver. No cell-center averaging.
    Requires physical_bounds, nodes, centers and full-grid solver fields.
    This extracts one snapshot, not a time history or a surface integral.
    """
    sphere = sphere_points(result["physical_bounds"], radius, n_theta, n_phi)
    x, y, z = result["nodes"]
    xc, yc, zc = result["centers"]
    electric_axes = ((xc, y, z), (x, yc, z), (x, y, zc))
    magnetic_axes = ((x, yc, zc), (xc, y, zc), (xc, yc, z))
    for name, axes in (("electric", electric_axes), ("magnetic", magnetic_axes)):
        components = []
        for field, coordinates in zip(result[name], axes):
            components.append(trilinear(field, coordinates, sphere["points"]))
        sphere[name] = np.column_stack(components)
    sphere["time"] = result["time"]
    return sphere


def main():
    """Preview the sphere using saved fdtd_3d settings, without running FDTD."""
    bounds = np.array((fdtd_3d.X_RANGE, fdtd_3d.Y_RANGE, fdtd_3d.Z_RANGE), dtype=float)
    cells = (fdtd_3d.NX, fdtd_3d.NY, fdtd_3d.NZ)
    spacing = (bounds[:, 1] - bounds[:, 0]) / cells
    pml_cells = fdtd_3d.pml_length_to_cells(fdtd_3d.PML_length, bounds, cells)
    physical_bounds = bounds + np.column_stack((pml_cells*spacing, -pml_cells*spacing))
    sphere = sphere_points(physical_bounds, RADIUS, N_THETA, N_PHI)
    path = save_sphere_samples(sphere)
    print(f"Sphere radius: {sphere['radius']:g}; samples: {len(sphere['points'])}")
    print(f"Saved: {path}")
    return sphere


if __name__ == "__main__":
    sphere = main()
