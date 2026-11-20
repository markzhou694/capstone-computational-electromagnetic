"""Dielectric bunny on the existing Yee grid; one solve, E and H plots.

Grid, time, PML and custom_current come from fdtd_3d.py. Only the material
is replaced here. Units are the same as fdtd_3d. No boundary integral.
Requires trimesh and rtree: python -m pip install trimesh rtree
"""

from pathlib import Path
import numpy as np
import trimesh
import fdtd_3d
from run_metrics import timed_solve
from plot_fields import sample_fields, save_results, save_dielectric_geometry

# ===== 1. Bunny parameters =====
BUNNY_CENTER = (0.3, 0.0, 0.0)  # Center of the bounding box, not center of mass.
BUNNY_SIZE = 0.40               # Longest bounding-box side; uniform scale.
BUNNY_EPSILON = 4.0
MESH_PATH = Path(__file__).parent / "assets" / "bunny.off"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "bunny"


def load_bunny(settings):
    """Load a closed solid, rotate upright (z-up), scale and check placement.

    Require one grid cell of background between the bunny and the PML.
    Also keep the compact source outside the bunny's bounding box.
    """
    if not np.isfinite(BUNNY_SIZE) or BUNNY_SIZE <= 0:
        raise ValueError("BUNNY_SIZE must be positive and finite.")
    mesh = trimesh.load_mesh(MESH_PATH)
    if not mesh.is_volume:
        raise ValueError("The bunny must be a watertight, consistently oriented solid.")
    vertices = mesh.vertices[:, [0, 2, 1]].copy()
    vertices[:, 1] *= -1  # Rotate original y-up geometry to z-up.
    vertices -= (vertices.min(axis=0) + vertices.max(axis=0)) / 2
    vertices *= BUNNY_SIZE / np.ptp(vertices, axis=0).max()
    mesh.vertices = vertices + np.asarray(BUNNY_CENTER)

    bounds = np.asarray(settings["bounds"], dtype=float)
    h = (bounds[:, 1] - bounds[:, 0]) / settings["cells"]
    physical = bounds + settings["pml_cells"] * h[:, None] * [1, -1]
    if (not np.isfinite(mesh.vertices).all()
            or np.any(mesh.bounds[0] <= physical[:, 0] + h)
            or np.any(mesh.bounds[1] >= physical[:, 1] - h)):
        raise ValueError("Move/shrink the bunny: leave one cell before the PML interface.")
    source = np.asarray(fdtd_3d.CUSTOM_CENTER)
    nearest = np.clip(source, mesh.bounds[0], mesh.bounds[1])
    if np.linalg.norm(source - nearest) <= fdtd_3d.CUSTOM_RADIUS:
        raise ValueError("Move the bunny away from the compact source.")
    source_bounds = fdtd_3d.get_source_bounds()
    if np.any(source_bounds[:, 0] <= physical[:, 0]) or np.any(source_bounds[:, 1] >= physical[:, 1]):
        raise ValueError("Keep the source strictly inside the physical domain.")
    return mesh, physical


def bunny_permittivity(mesh):
    """Return epsilon(x,y,z), sampled once on each native electric grid.

    epsilon = BUNNY_EPSILON inside the mesh, 1 outside; mu = 1 everywhere.
    Point-in-solid masks give a sharp staircase dielectric representation.
    This is not subpixel smoothing. No interpolation of E/H is performed.
    """
    if not np.isfinite(BUNNY_EPSILON) or BUNNY_EPSILON <= 0:
        raise ValueError("BUNNY_EPSILON must be positive and finite.")

    def epsilon(x, y, z):
        xyz = np.broadcast_arrays(x, y, z)
        points = np.column_stack([coordinate.ravel() for coordinate in xyz])
        values = np.ones(len(points))
        # Only test points in the bounding box; batches limit ray-query memory.
        candidates = np.flatnonzero(np.all(
            (points >= mesh.bounds[0]) & (points <= mesh.bounds[1]), axis=1))
        for start in range(0, len(candidates), 2048):
            indices = candidates[start:start + 2048]
            inside = mesh.contains(points[indices])
            values[indices[inside]] = BUNNY_EPSILON
        return values.reshape(xyz[0].shape)

    return epsilon


def main(output_dir=OUTPUT_DIR):
    """Read shared settings, check geometry, solve once and save E/H PNG/GIF."""
    settings = fdtd_3d.get_simulation_settings()
    mesh, physical_bounds = load_bunny(settings)
    settings["epsilon"] = bunny_permittivity(mesh)
    settings["mu"] = 1.0
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    geometry = save_dielectric_geometry(mesh.vertices, mesh.faces, physical_bounds,
                                       fdtd_3d.CUSTOM_CENTER, fdtd_3d.CUSTOM_RADIUS,
                                       output_dir / "bunny_geometry.png")
    print(f"Bunny bounds: {mesh.bounds.tolist()}; epsilon={BUNNY_EPSILON:g}")
    print(f"Geometry: {geometry}")
    frames = {"E": [], "H": []}

    def record_frame(time, electric, centers, magnetic):
        frames["E"].append(sample_fields(time, electric, centers, "E", BUNNY_CENTER))
        frames["H"].append(sample_fields(time, magnetic, centers, "H", BUNNY_CENTER))

    result = timed_solve("Bunny FDTD", **settings, on_frame=record_frame)
    result["geometry_mesh"] = mesh  # Display overlay only; solver fields are unchanged.
    paths = {"geometry": geometry}
    for kind in ("E", "H"):
        paths[kind] = save_results(result, frames[kind], output_dir,
                                   fps=fdtd_3d.GIF_FPS, kind=kind)
        frames[kind].clear()
        print(f"Saved {kind}: {paths[kind]}")
    return result, paths


if __name__ == "__main__":
    main()
