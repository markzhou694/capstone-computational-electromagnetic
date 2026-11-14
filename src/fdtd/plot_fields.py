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


def sample_fields(time, field, centers, kind="E"):
    """Copy three signed-component slices and sparse vectors into one frame.

    Inputs: time; field=(Fx,Fy,Fz) with Yee shapes for kind="E" or "H";
            centers=(xc,yc,zc), 1D arrays of lengths Nx,Ny,Nz.
    Returns: dict with time, kind, component, maximum=max|F|, vectors (3 arrays),
        planes=(xy,xz,yz) of shapes (Nx,Ny), (Nx,Nz), (Ny,Nz).
        vectors use strides max(1,Nx//10), max(1,Ny//10), max(1,Nz//10).
        Slices show SLICE_COMPONENT, retaining its sign and field units.
    The slices pass through indices Nx//2, Ny//2, Nz//2. Returned arrays own
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
    samples = (
        slice(None, None, max(1, nx // 10)),
        slice(None, None, max(1, ny // 10)),
        slice(None, None, max(1, nz // 10)),
    )
    return {
        "time": float(time),
        "kind": kind,
        "component": SLICE_COMPONENT,
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
        "signed_dark", ["#73cfff", "#000000", "#ffb34d"], N=257,
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
        images.append(image)
    return {
        "figure": fig,
        "vector_ax": vector_ax,
        "positions": positions,
        "arrow_length": arrow_length,
        "maximum": maximum,
        "arrows": None,
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
        color="midnightblue", linewidth=1.2, arrow_length_ratio=0.4, pivot="middle",
    )
    for image, plane in zip(view["images"], frame["planes"]):
        image.set_data(plane.T)
    view["title"].set_text(
        f"{frame['kind']}{frame['component']} | t = {frame['time']:.3f} | "
        f"{view['boundary_label']}"
    )


def save_results(result, frames, output_dir, fps=12, kind="E"):
    """Save the last frame as PNG and the frame sequence as a looping GIF.

    Inputs: result dict from solve; nonempty chronological list of frames
        from sample_fields on that same grid and kind; output_dir (str/Path);
        positive fps (playback frames/s); kind="E" or "H".
    Returns: {'png': Path, 'gif': Path} for fdtd_3d_current.png/.gif.
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
        "png": output_dir / "fdtd_3d_current.png",
        "gif": output_dir / "fdtd_3d_current.gif",
    }
    view = field_view(result, maximum, kind, component)
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
            animation.save(temporary / paths["gif"].name, writer=PillowWriter(fps=fps), dpi=90)
            draw_frame(frames[-1], view)
            fig.savefig(temporary / paths["png"].name, dpi=150)
            for path in paths.values():
                (temporary / path.name).replace(path)
    finally:
        plt.close(fig)
    return paths
