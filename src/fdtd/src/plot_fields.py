"""Plot E or H from a Yee solver result; see ../docs/API.md for formats.

Workflow: sample_fields(...) -> frames -> save_results(...).
Only drawing/export needs Matplotlib and Pillow. Sampling needs only NumPy.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np


def cell_center_fields(field, kind="E"):
    """Average a staggered field to cell centers, without changing inputs.

    Inputs: field=(Fx,Fy,Fz), three Yee arrays; kind is "E" or "H".
        E shapes: (Nx,Ny+1,Nz+1), (Nx+1,Ny,Nz+1), (Nx+1,Ny+1,Nz).
        H shapes: (Nx+1,Ny,Nz), (Nx,Ny+1,Nz), (Nx,Ny,Nz+1).
    Returns: (Fx_center,Fy_center,Fz_center), each shape (Nx,Ny,Nz).
    Units are unchanged: E in [V/m], H in [A/m]. This is for display only.
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
    """Copy three magnitude slices and sparse vectors into one small frame.

    Inputs: time [s]; field=(Fx,Fy,Fz) with Yee shapes for kind="E" or "H";
            centers=(xc,yc,zc), 1D arrays of lengths Nx,Ny,Nz [m].
    Returns: dict with time [s], kind, maximum (float), vectors (3 arrays),
        planes=(xy,xz,yz) of shapes (Nx,Ny), (Nx,Nz), (Ny,Nz).
        vectors use strides max(1,Nx//8), max(1,Ny//8), max(1,Nz//8).
        Magnitudes/vectors use [V/m] for E or [A/m] for H.
    The slices pass through indices Nx//2, Ny//2, Nz//2. Returned arrays own
    their data and may be kept after the solver advances. See API.md for keys.
    """
    fx, fy, fz = cell_center_fields(field, kind)
    magnitude = np.sqrt(fx**2 + fy**2 + fz**2)
    nx, ny, nz = magnitude.shape
    ix, iy, iz = nx // 2, ny // 2, nz // 2
    if tuple(len(q) for q in centers) != (nx, ny, nz):
        raise ValueError("centers must match the cell-centered field shape.")
    samples = (
        slice(None, None, max(1, nx // 8)),
        slice(None, None, max(1, ny // 8)),
        slice(None, None, max(1, nz // 8)),
    )
    return {
        "time": float(time),
        "kind": kind,
        "maximum": float(magnitude.max()),
        "vectors": (fx[samples].copy(), fy[samples].copy(), fz[samples].copy()),
        "planes": (
            magnitude[:, :, iz].copy(),
            magnitude[:, iy, :].copy(),
            magnitude[ix, :, :].copy(),
        ),
    }


def field_view(result, maximum, kind="E"):
    """Create an empty 3D-vector panel and three magnitude-slice panels.

    Inputs: result dict from solve (uses bounds and centers); maximum is a
        nonnegative common field scale; kind is "E" or "H".
    Returns: a view dict for draw_frame, containing figure, vector_ax,
        positions=(x,y,z) sampled grids [m], arrow_scale, maximum, arrows,
        images (three slice artists), title, and kind. No file is written.
    Uses a noninteractive Matplotlib backend. Caller must close view['figure'].
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if kind not in ("E", "H"):
        raise ValueError('kind must be "E" or "H".')
    if not np.isfinite(maximum) or maximum < 0:
        raise ValueError("maximum must be nonnegative and finite.")
    bounds, centers = result["bounds"], result["centers"]
    maximum = max(maximum, 1e-30)
    unit = "V/m" if kind == "E" else "A/m"
    fig = plt.figure(figsize=(10, 8), layout="constrained")
    vector_ax = fig.add_subplot(2, 2, 1, projection="3d")
    sampled_centers = []
    for q in centers:
        sampled_centers.append(q[::max(1, len(q) // 8)])
    positions = np.meshgrid(*sampled_centers, indexing="ij")
    vector_ax.set(
        xlim=bounds[0], ylim=bounds[1], zlim=bounds[2],
        xlabel="x [m]", ylabel="y [m]", zlabel="z [m]",
        title=f"3D {kind} vectors (sampled; fixed scale)",
    )
    lengths = bounds[:, 1] - bounds[:, 0]
    vector_ax.set_box_aspect(lengths)
    arrow_scale = 0.12 * min(lengths) / maximum

    images = []
    # Each tuple gives (horizontal axis, vertical axis, fixed axis): xy,xz,yz.
    for panel, (a, b, fixed) in enumerate(((0, 1, 2), (0, 2, 1), (1, 2, 0)), start=2):
        ax = fig.add_subplot(2, 2, panel)
        blank = np.zeros((len(centers[b]), len(centers[a])))
        image = ax.imshow(
            blank, origin="lower", extent=(*bounds[a], *bounds[b]),
            cmap="magma", vmin=0, vmax=maximum, aspect="equal",
        )
        position = centers[fixed][len(centers[fixed]) // 2]
        ax.set(
            xlabel=f"{'xyz'[a]} [m]", ylabel=f"{'xyz'[b]} [m]",
            title=f"|{kind}| at {'xyz'[fixed]} = {position:.3g} m",
        )
        fig.colorbar(image, ax=ax, label=f"|{kind}| [{unit}]")
        images.append(image)
    return {
        "figure": fig,
        "vector_ax": vector_ax,
        "positions": positions,
        "arrow_scale": arrow_scale,
        "maximum": maximum,
        "arrows": None,
        "images": images,
        "title": fig.suptitle(""),
        "kind": kind,
    }


def draw_frame(frame, view):
    """Update an existing view with one sampled frame.

    Inputs: frame dict from sample_fields; view dict from field_view.
    Returns: None. Updates view's artists and arrows in place; does not
    change the frame. Frame and view must use the same grid and field kind.
    """
    if frame["kind"] != view["kind"]:
        raise ValueError("Frame and view must use the same field kind.")
    if view["arrows"] is not None:
        view["arrows"].remove()
    x, y, z = view["positions"]
    fx, fy, fz = frame["vectors"]
    magnitude = np.sqrt(fx**2 + fy**2 + fz**2)
    keep = magnitude > 0.03 * view["maximum"]
    scale = view["arrow_scale"]
    view["arrows"] = view["vector_ax"].quiver(
        x[keep], y[keep], z[keep],
        scale * fx[keep], scale * fy[keep], scale * fz[keep],
        color="steelblue", linewidth=0.7,
    )
    for image, plane in zip(view["images"], frame["planes"]):
        image.set_data(plane.T)
    view["title"].set_text(
        f"3D FDTD | t = {frame['time'] * 1e9:.2f} ns | PEC reflecting walls"
    )


def save_results(result, frames, output_dir, fps=12, kind="E"):
    """Save the last frame as PNG and the frame sequence as a looping GIF.

    Inputs: result dict from solve; nonempty chronological list of frames
        from sample_fields on that same grid and kind; output_dir (str/Path);
        positive fps (playback frames/s); kind="E" or "H".
    Returns: {'png': Path, 'gif': Path} for fdtd_3d_current.png/.gif.
    Creates output_dir and replaces those two files on success. Both use
    one common color/arrow scale. Rendering completes in a temporary folder
    before replacing outputs; rendering errors leave previous files intact.
    Closes the figure even when rendering fails. Inputs are not changed.
    """
    if not frames:
        raise ValueError("frames must contain at least one sampled frame.")
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("fps must be positive and finite.")
    if any(frame["kind"] != kind for frame in frames):
        raise ValueError("All frames must match the requested field kind.")
    if any(a["time"] > b["time"] for a, b in zip(frames, frames[1:])):
        raise ValueError("frames must be in chronological order.")
    maximum = max(frame["maximum"] for frame in frames)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "png": output_dir / "fdtd_3d_current.png",
        "gif": output_dir / "fdtd_3d_current.gif",
    }
    view = field_view(result, maximum, kind)
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
