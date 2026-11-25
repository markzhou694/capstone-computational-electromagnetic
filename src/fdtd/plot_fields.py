"""Plot E or H from a normalized-unit Yee solver result.

Workflow: sample_fields(...) -> frames -> save_results(...).
Only drawing/export needs Matplotlib and Pillow. Sampling needs only NumPy.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np


SLICE_COMPONENT = "z"       # Show signed "x", "y", or "z" on all three slices.
ARROW_LENGTH = 0.12          # Longest arrow / shortest box side, per frame.


def cell_center_fields(field, kind="E"):
    """Average a staggered field to cell centers, without changing inputs.

    Inputs: field=(Fx,Fy,Fz), three Yee arrays; kind is "E" or "H".
        E shapes: (Nx,Ny+1,Nz+1), (Nx+1,Ny,Nz+1), (Nx+1,Ny+1,Nz).
        H shapes: (Nx+1,Ny,Nz), (Nx,Ny+1,Nz), (Nx,Ny,Nz+1).
    Returns: (Fx_center,Fy_center,Fz_center), each shape (Nx,Ny,Nz).
    Normalized field units are unchanged. This is for display only.
    """
    fx, fy, fz = field
    if kind == "E":
        # Each cell has four parallel E edges for each component.
        fx = (fx[:, :-1, :-1] + fx[:, 1:, :-1] + fx[:, :-1, 1:] + fx[:, 1:, 1:]) / 4
        fy = (fy[:-1, :, :-1] + fy[1:, :, :-1] + fy[:-1, :, 1:] + fy[1:, :, 1:]) / 4
        fz = (fz[:-1, :-1, :] + fz[1:, :-1, :] + fz[:-1, 1:, :] + fz[1:, 1:, :]) / 4
    elif kind == "H":
        # Each cell has two opposite H faces for each component.
        fx = (fx[:-1, :, :] + fx[1:, :, :]) / 2
        fy = (fy[:, :-1, :] + fy[:, 1:, :]) / 2
        fz = (fz[:, :, :-1] + fz[:, :, 1:]) / 2
    else:
        raise ValueError('kind must be "E" or "H".')
    return fx, fy, fz


def sample_fields(time, field, centers, kind="E", slice_center=None):
    """Copy three signed-component slices and sparse vectors into one frame.

    Inputs: time; field=(Fx,Fy,Fz) with Yee shapes for kind="E" or "H";
            centers=(xc,yc,zc), 1D arrays of lengths Nx,Ny,Nz.
    Returns: dict with time, kind, component, maximum=max|F|, vectors (3 arrays),
        planes=(xy,xz,yz) of shapes (Nx,Ny), (Nx,Nz), (Ny,Nz).
        vectors use strides max(1,Nx//10), max(1,Ny//10), max(1,Nz//10).
        Slices show SLICE_COMPONENT, retaining its sign and field units.
    Optional slice_center=(x,y,z) selects the nearest cell-center slices;
    otherwise use indices Nx//2, Ny//2, Nz//2. Returned arrays own
    their data and may be kept after the solver advances.
    """
    fx, fy, fz = cell_center_fields(field, kind)
    if SLICE_COMPONENT not in ("x", "y", "z"):
        raise ValueError('SLICE_COMPONENT must be "x", "y", or "z".')
    component = (fx, fy, fz)["xyz".index(SLICE_COMPONENT)]
    magnitude = np.sqrt(fx**2 + fy**2 + fz**2)
    nx, ny, nz = magnitude.shape
    ix, iy, iz = nx // 2, ny // 2, nz // 2
    if tuple(len(q) for q in centers) != (nx, ny, nz):
        raise ValueError("centers must match the cell-centered field shape.")
    if slice_center is not None:
        ix, iy, iz = [int(np.argmin(abs(q - value)))
                      for q, value in zip(centers, slice_center)]
    samples = (
        slice(None, None, max(1, nx // 10)),
        slice(None, None, max(1, ny // 10)),
        slice(None, None, max(1, nz // 10)),
    )
    return {
        "time": float(time),
        "kind": kind,
        "component": SLICE_COMPONENT,
        "slice_positions": tuple(centers[d][i] for d, i in enumerate((ix, iy, iz))),
        "maximum": float(magnitude.max()),
        "vectors": (fx[samples].copy(), fy[samples].copy(), fz[samples].copy()),
        "planes": (
            component[:, :, iz].copy(),
            component[:, iy, :].copy(),
            component[ix, :, :].copy(),
        ),
    }


def field_view(result, maximum, kind="E", component=SLICE_COMPONENT):
    """Create a 3D-vector panel and three signed-component slice panels.

    Inputs: result dict from solve (uses bounds and centers); maximum is a
        nonnegative common field scale; kind is "E" or "H"; component is x/y/z.
    Returns: a view dict for draw_frame, containing figure, vector_ax,
        positions=(x,y,z) sampled grids, arrow_length, maximum, arrows,
        images (three slice artists), title, kind and component.
    Colors use one fixed symmetric-log scale: linear below 1% of maximum,
    logarithmic above it. Arrow lengths are rescaled in draw_frame.
    Uses a noninteractive Matplotlib backend. Caller must close view['figure'].
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import SymLogNorm, LinearSegmentedColormap

    if kind not in ("E", "H"):
        raise ValueError('kind must be "E" or "H".')
    if component not in ("x", "y", "z"):
        raise ValueError('component must be "x", "y", or "z".')
    if not np.isfinite(maximum) or maximum < 0:
        raise ValueError("maximum must be nonnegative and finite.")
    bounds, centers = result["bounds"], result["centers"]
    maximum = max(maximum, 1e-30)
    color_scale = SymLogNorm(linthresh=0.01*maximum, vmin=-maximum, vmax=maximum)
    colors = LinearSegmentedColormap.from_list(
        "signed_dark", ["#73cfff", "#000000", "#f80a16"], N=257,
    )
    fig = plt.figure(figsize=(10, 8), layout="constrained")
    vector_ax = fig.add_subplot(2, 2, 1, projection="3d")
    sampled_centers = []
    for q in centers:
        sampled_centers.append(q[::max(1, len(q) // 10)])
    positions = np.meshgrid(*sampled_centers, indexing="ij")
    vector_ax.set(
        xlim=bounds[0], ylim=bounds[1], zlim=bounds[2],
        xlabel="x (m)", ylabel="y (m)", zlabel="z (m)",
        title=f"{kind} vectors (scaled)",
    )
    lengths = bounds[:, 1] - bounds[:, 0]
    vector_ax.set_box_aspect(lengths)
    arrow_length = ARROW_LENGTH * min(lengths)

    mesh = result.get("geometry_mesh")
    if mesh is not None:
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        vector_ax.add_collection3d(Poly3DCollection(
            mesh.vertices[mesh.faces], facecolor="gold", edgecolor="none", alpha=0.25))
        interior = result["physical_bounds"]
        vector_ax.set(xlim=interior[0], ylim=interior[1], zlim=interior[2])
        vector_ax.set_title(f"{kind} vectors | bunny")

    images = []
    # Each tuple gives (horizontal axis, vertical axis, fixed axis): xy,xz,yz.
    for panel, (a, b, fixed) in enumerate(((0, 1, 2), (0, 2, 1), (1, 2, 0)), start=2):
        ax = fig.add_subplot(2, 2, panel)
        blank = np.zeros((len(centers[b]), len(centers[a])))
        image = ax.imshow(
            blank, origin="lower", extent=(*bounds[a], *bounds[b]),
            cmap=colors, norm=color_scale, aspect="equal",
        )
        position = centers[fixed][len(centers[fixed]) // 2]
        if "slice_positions" in result:
            position = result["slice_positions"][fixed]
        ax.set(
            xlabel=f"{'xyz'[a]} (m)", ylabel=f"{'xyz'[b]} (m)",
            title=f"{'xyz'[fixed]} = {position:.3g} m",
        )
        fig.colorbar(
            image, ax=ax, label=f"{kind}{component} (symlog)",
            ticks=[-maximum, -0.01*maximum, 0, 0.01*maximum, maximum], format="%.2g",
        )
        if "pml" in result:
            from matplotlib.patches import Rectangle
            interior = result["physical_bounds"]
            ax.add_patch(Rectangle(
                (interior[a, 0], interior[b, 0]),
                interior[a, 1] - interior[a, 0], interior[b, 1] - interior[b, 0],
                fill=False, edgecolor="cyan", linestyle="--", linewidth=1,
            ))
        if mesh is not None:
            # Actual mesh/plane intersection, not a projected silhouette.
            import matplotlib.patheffects as effects
            origin = np.zeros(3)
            origin[fixed] = position
            normal = np.eye(3)[fixed]
            from trimesh.intersections import mesh_plane
            from matplotlib.collections import LineCollection
            segments = mesh_plane(mesh, plane_normal=normal, plane_origin=origin)
            outline = LineCollection(segments[:, :, [a, b]], colors="gold", linewidths=1.5)
            outline.set_path_effects([effects.Stroke(linewidth=3, foreground="black"),
                                      effects.Normal()])
            ax.add_collection(outline)
            interior = result["physical_bounds"]
            ax.set(xlim=interior[a], ylim=interior[b])
        images.append(image)
    return {
        "figure": fig,
        "vector_ax": vector_ax,
        "positions": positions,
        "arrow_length": arrow_length,
        "maximum": maximum,
        "arrows": None,
        "arrow_color": "#72d6ff" if mesh is not None else "midnightblue",
        "images": images,
        "title": fig.suptitle(""),
        "kind": kind,
        "component": component,
        "boundary_label": ("PML" if "pml" in result else "PEC"),
    }


def draw_frame(frame, view):
    """Update an existing view with one sampled frame.

    Inputs: frame dict from sample_fields; view dict from field_view.
    Returns: None. Updates view's artists and arrows in place; does not
    change the frame. Frame and view must use the same grid, kind and component.
    Arrow length = longest_length * sqrt(|F| / largest_sampled_|F|).
    This makes weak vectors visible. Fixed colorbar values retain amplitudes.
    """
    if frame["kind"] != view["kind"] or frame["component"] != view["component"]:
        raise ValueError("Frame and view must use the same field kind and component.")
    if view["arrows"] is not None:
        view["arrows"].remove()
    x, y, z = view["positions"]
    fx, fy, fz = frame["vectors"]
    magnitude = np.sqrt(fx**2 + fy**2 + fz**2)
    # Square-root lengths reveal weaker vectors; directions are unchanged.
    vector_max = max(float(magnitude.max()), 1e-12*view["maximum"], 1e-30)
    keep = magnitude > 0.02 * vector_max
    length = view["arrow_length"] * np.sqrt(magnitude[keep] / vector_max)
    scale = length / magnitude[keep]
    view["arrows"] = view["vector_ax"].quiver(
        x[keep], y[keep], z[keep],
        scale * fx[keep], scale * fy[keep], scale * fz[keep],
        color=view["arrow_color"], linewidth=1.2, arrow_length_ratio=0.4, pivot="middle",
    )
    for image, plane in zip(view["images"], frame["planes"]):
        image.set_data(plane.T)
    view["title"].set_text(
        f"{frame['kind']}{frame['component']} | t = {frame['time']:.3f} | "
        f"{view['boundary_label']}"
    )


def save_results(result, frames, output_dir, fps=12, kind="E", on_progress=None):
    """Save the last frame as PNG and the frame sequence as a looping GIF.

    Inputs: result dict from solve; nonempty chronological list of frames
        from sample_fields on that same grid and kind; output_dir (str/Path);
        positive fps (playback frames/s); kind="E" or "H".
        Optional on_progress(completed_frames, total_frames) reports rendering.
    Returns: {'png': Path, 'gif': Path} for fdtd_3d_E.png/.gif or fdtd_3d_H.png/.gif.
    Creates output_dir and replaces those two files on success. Signed colors
    have one fixed symmetric-log scale; arrows are rescaled in each frame.
    Rendering completes in a temporary folder
    before replacing outputs; rendering errors leave previous files intact.
    Closes the figure even when rendering fails. Inputs are not changed.
    """
    if not frames:
        raise ValueError("frames must contain at least one sampled frame.")
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("fps must be positive and finite.")
    if any(frame["kind"] != kind for frame in frames):
        raise ValueError("All frames must match the requested field kind.")
    component = frames[0]["component"]
    if any(frame["component"] != component for frame in frames):
        raise ValueError("All frames must show the same component.")
    if any(a["time"] > b["time"] for a, b in zip(frames, frames[1:])):
        raise ValueError("frames must be in chronological order.")
    maximum = max(frame["maximum"] for frame in frames)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "png": output_dir / f"fdtd_3d_{kind}.png",
        "gif": output_dir / f"fdtd_3d_{kind}.gif",
    }
    import matplotlib.pyplot as plt
    # Use the exact slice coordinates recorded with the field data.
    plot_result = dict(result)
    if "slice_positions" in frames[0]:
        plot_result["slice_positions"] = frames[0]["slice_positions"]
    with plt.style.context("dark_background"):
        view = field_view(plot_result, maximum, kind, component)
    fig = view["figure"]
    from matplotlib.animation import FuncAnimation, PillowWriter
    import matplotlib.pyplot as plt

    try:
        with TemporaryDirectory(prefix=".render-", dir=output_dir) as temporary:
            temporary = Path(temporary)
            animation = FuncAnimation(
                fig, draw_frame, frames=frames, fargs=(view,),
                interval=1000 / fps, blit=False, repeat=True,
            )
            if on_progress is not None:
                on_progress(0, len(frames))
            animation.save(
                temporary / paths["gif"].name, writer=PillowWriter(fps=fps), dpi=90,
                progress_callback=(lambda i, total: on_progress(i + 1, total))
                if on_progress is not None else None,
            )
            draw_frame(frames[-1], view)
            fig.savefig(temporary / paths["png"].name, dpi=150)
            for path in paths.values():
                (temporary / path.name).replace(path)
    finally:
        plt.close(fig)
    return paths


def save_final_comparison(pml, reference, output_dir=None):
    """Save final Ez slices on matching native Yee points in the physical box.

    Inputs are the two solver results from run_simulations. Uses the xy
    slice nearest z=0, a shared linear color scale, and no spatial averaging.
    Returns the PNG path. Does not modify fields or calculate an error norm.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    trim = pml["pml"]["cells"]
    nx, ny, nz = pml["cells"]
    k = trim + np.argmin(np.abs(pml["centers"][2][trim:nz-trim]))
    padding = reference["padding_cells"]
    small = pml["electric"][2][trim:nx-trim+1, trim:ny-trim+1, k]
    large = reference["electric"][2][
        padding+trim:padding+nx-trim+1,
        padding+trim:padding+ny-trim+1, padding+k,
    ]
    x = pml["nodes"][0][trim:nx-trim+1]
    y = pml["nodes"][1][trim:ny-trim+1]
    maximum = max(float(np.max(np.abs(small))), float(np.max(np.abs(large))), 1e-30)
    colors = LinearSegmentedColormap.from_list(
        "signed_dark", ["#1d05f2", "#000000", "#f20713"], N=257,
    )
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), layout="constrained")
    for ax, values, title in zip(axes, (small, large), ("PML", "Reference")):
        image = ax.pcolormesh(x, y, values.T, shading="nearest",
                              cmap=colors, vmin=-maximum, vmax=maximum)
        ax.set(title=title, xlabel="x (m)", ylabel="y (m)",
               xlim=pml["physical_bounds"][0], ylim=pml["physical_bounds"][1],
               aspect="equal")
    fig.colorbar(image, ax=axes, label="Ez", format="%.2g")
    fig.suptitle(f"t = {pml['time']:.3f} | z = {pml['centers'][2][k]:.3g} m")
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    path = Path(output_dir) / "pml_reference_final.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def save_error_norms(times, absolute_E, absolute_H, reference_E, reference_H, output_dir=None):
    """Save error/reference norms on log axes, separately for E and H.

    D_F(t) = ||F_pml(t) - F_ref(t)||_2; A_F(t) = ||F_ref(t)||_2.
    Inputs are the unweighted native-Yee norms in the physical domain.
    Zero/nonfinite values are gaps, not replaced with an artificial floor.
    Returns the PNG path; does not change the input arrays.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with plt.style.context("dark_background"):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), sharex=True,
                                 layout="constrained")
        for ax, kind, difference, reference in zip(
                axes, ("E", "H"), (absolute_E, absolute_H), (reference_E, reference_H)):
            for values, label, color, style in (
                    (difference, "Error", "#ffb34d", "-"),
                    (reference, "Reference", "#73cfff", "--")):
                values = np.asarray(values)
                values = np.where(np.isfinite(values) & (values > 0), values, np.nan)
                ax.plot(times, values, label=label, color=color, linestyle=style)
            ax.set(yscale="log", xlabel="t", ylabel="Discrete L2 norm", title=kind)
            ax.grid(alpha=0.2)
            ax.legend()
        fig.suptitle("Error vs reference field")
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "outputs"
        path = Path(output_dir) / "pml_error_norms.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=160)
        plt.close(fig)
    return path


def save_error_history(times, error_E, error_H, output_dir=None):
    """Save peak-normalized L2 errors versus solver time; NaNs are gaps."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with plt.style.context("dark_background"):
        fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
        ax.plot(times, error_E, color="#0f03f4", label="E")
        ax.plot(times, error_H, color="#ed0c0c", label="H")
        ax.set(xlabel="t", ylabel="Peak-normalized L2 error", title="PML vs reference")
        ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
        ax.grid(alpha=0.2)
        ax.legend()
        if not np.all(np.isfinite(error_E)) or not np.all(np.isfinite(error_H)):
            ax.text(0.02, 0.96, "Undefined: zero reference peak", transform=ax.transAxes,
                    va="top", fontsize=9)
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "outputs"
        path = Path(output_dir) / "pml_error_history.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=160)
        plt.close(fig)
    return path


def save_exterior_fields(exterior, output_dir=None):
    """Save reconstructed Ex/Ey/Ez and Hx/Hy/Hz versus observation time.

    exterior contains times (Nt,), electric/magnetic (Nt,3), and point (3,).
    Plot the signed Cartesian components, not field magnitude or surface data.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with plt.style.context("dark_background"):
        fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained")
        for ax, key, label in zip(axes, ("electric", "magnetic"), ("E", "H")):
            for component, (name, color) in enumerate(zip("xyz", ("#73cfff", "#ffb34d", "#9be391"))):
                ax.plot(exterior["times"], exterior[key][:, component], color=color,
                        linestyle=("-", "--", ":")[component], label=label+name)
            ax.set_ylabel(label)
            ax.legend(ncols=3)
            ax.grid(alpha=0.2)
            ax.ticklabel_format(axis="y", style="sci", scilimits=(-3, 3))
        axes[-1].set_xlabel("t")
        coordinates = ", ".join(f"{value:g}" for value in exterior["point"])
        axes[0].set_title(f"Exterior field | ({coordinates})")
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "outputs" / "near_to_far_field"
        path = Path(output_dir) / "near_to_far_field.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=180)
        plt.close(fig)
    return path


def save_sphere_samples(sphere, output_dir=None):
    """Draw sphere sample positions, both poles, source support and physical box.

    sphere is geometry from field_extraction.sphere_points/extract_sphere.
    Returns the PNG path. This is a position plot, not a field-value plot.
    """
    from itertools import product, combinations
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    points = sphere["points"]
    center = sphere["center"]
    bounds = sphere["physical_bounds"]
    theta, phi = np.meshgrid(np.linspace(0, np.pi, 25), np.linspace(0, 2*np.pi, 48))
    a = sphere["source_radius"]
    source = (center[0] + a*np.sin(theta)*np.cos(phi),
              center[1] + a*np.sin(theta)*np.sin(phi), center[2] + a*np.cos(theta))
    with plt.style.context("dark_background"):
        fig = plt.figure(figsize=(11, 5), layout="constrained")
        for panel in range(2):
            ax = fig.add_subplot(1, 2, panel+1, projection="3d")
            ax.scatter(*points[:-2].T, s=9, color="#73cfff", depthshade=False, label="Samples")
            ax.scatter(*points[-2:].T, s=45, color="white", marker="*", depthshade=False, label="Poles")
            ax.plot_surface(*source, color="#ffb34d", alpha=0.3, linewidth=0)
            ax.scatter(*center, color="#ffb34d", s=20, label="Source")
            if panel == 0:
                corners = np.array(list(product(*bounds)))
                for v, w in combinations(corners, 2):
                    if np.count_nonzero(v != w) == 1:
                        ax.plot(*np.stack((v, w)).T, color="gray", linewidth=1)
                limits = bounds
            else:
                limits = np.column_stack((center - 1.12*sphere["radius"],
                                          center + 1.12*sphere["radius"]))
            ax.set(xlabel="x", ylabel="y", zlabel="z", xlim=limits[0], ylim=limits[1],
                   zlim=limits[2], title="Physical domain" if panel == 0 else "Sphere samples")
            ax.set_box_aspect(limits[:, 1] - limits[:, 0])
            ax.view_init(elev=22, azim=32)
            ax.grid(False)
            for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
                axis.pane.fill = False
            ax.legend(fontsize=8, loc="upper left")
        fig.suptitle(f"Sphere | R={sphere['radius']:g} | {len(points)} samples")
        if output_dir is None:
            output_dir = Path(__file__).resolve().parents[1] / "outputs"
        path = Path(output_dir) / "sphere_samples.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=180)
        plt.close(fig)
    return path


def save_dielectric_geometry(vertices, faces, physical_bounds, source_center,
                             source_radius, path):
    """Save a mesh/source preview inside the physical box (display only)."""
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from itertools import product

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with plt.style.context("dark_background"):
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection="3d")
        surface = Poly3DCollection(vertices[faces], facecolor="orange",
                                   edgecolor="none", alpha=0.8)
        ax.add_collection3d(surface)
        corners = np.array(list(product(*physical_bounds)))
        for i, first in enumerate(corners):
            for second in corners[i + 1:]:
                if np.count_nonzero(first != second) == 1:
                    ax.plot(*np.array([first, second]).T, color="cyan", linewidth=0.7)
        theta = np.linspace(0, np.pi, 16)
        phi = np.linspace(0, 2 * np.pi, 24)
        x = source_center[0] + source_radius * np.outer(np.sin(theta), np.cos(phi))
        y = source_center[1] + source_radius * np.outer(np.sin(theta), np.sin(phi))
        z = source_center[2] + source_radius * np.outer(np.cos(theta), np.ones_like(phi))
        ax.plot_surface(x, y, z, color="red", alpha=0.7)
        ax.set(xlim=physical_bounds[0], ylim=physical_bounds[1], zlim=physical_bounds[2],
               xlabel="x", ylabel="y", zlabel="z", title="Bunny + source | physical domain")
        ax.set_box_aspect(np.diff(physical_bounds, axis=1).ravel())
        fig.tight_layout()
        fig.savefig(path, dpi=160)
        plt.close(fig)
    return path
