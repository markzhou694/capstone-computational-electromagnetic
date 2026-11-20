"""Example: set parameters, define a current, solve, and save PNG/GIF.

Equations solved (stationary isotropic epsilon(x,y,z), mu(x,y,z); normalized units):
    epsilon * dE/dt = curl(H) - J
    mu      * dH/dt = -curl(E)
    drho/dt        = -div(J)
Initial E=H=rho=0; tangential E=0 on the six PEC walls.

Edit epsilon, mu and custom_current below to define the medium and source.
Start with J = amplitude * spatial_shape * time_waveform * direction.
For other simulations, call yee_solver.solve directly.
"""

from pathlib import Path
import numpy as np
import yee_solver
from run_metrics import timed_solve, timed_call, print_progress
from plot_fields import sample_fields, save_results



## PML_length to PML_CELLS conversion: PML_length = PML_CELLS * d, where d is the cell size.
def pml_length_to_cells(pml_length, bounds, cells):
    """Convert a physical PML length to a number of grid cells.

    Inputs: pml_length is a positive float; bounds is ((x_min,x_max),...);
            cells is (NX,NY,NZ). Returns an integer PML_CELLS >= 0.
    """
    if pml_length <= 0:
        raise ValueError("PML length must be positive.")
    if len(bounds) != 3 or len(cells) != 3:
        raise ValueError("Bounds and cells must have three dimensions.")
    d = [(b[1] - b[0]) / n for b, n in zip(bounds, cells)] #  cell sizes in x,y,z
    min_d = min(d)
    pml_cells = int(np.ceil(pml_length / min_d)) # determine the number of cells needed for the PML length, use ceil to round up to the nearest whole cell
    print("actual PML length:", pml_cells * min_d, "normalized units; cell size:", min_d)
    if pml_cells * 2 >= min(cells):
        raise ValueError("PML length too large for the grid; reduce it.")
    return pml_cells


# ===== 1. Parameters ===== # very important!

# Normalized length and time. Edit epsilon(x,y,z) and mu(x,y,z) below.
# Local wave speed c=1/sqrt(epsilon*mu). No conversion to seconds or nanoseconds.
X_RANGE = (-1.0, 1.0)
Y_RANGE = (-1.0, 1.0)
Z_RANGE = (-1.0, 1.0)
NX, NY, NZ = 120,120,120
T_END = 1.5
CFL = 0.7                   # Stability fraction: 0 < CFL <= 1.

REFERENCE_HALF_WIDTH = 1.5 # the reference run uses a larger box to avoid reflections from the PEC walls. BIGGER BOX





# PML occupies these outer cells INSIDE the box; the outer wall stays PEC.
# Keep the current source inside [min+PML_CELLS*d, max-PML_CELLS*d].
USE_PML =True             # False reproduces the original PEC-only solver.
PML_length = 0.4             # Physical length of the PML layer.
PML_CELLS = pml_length_to_cells(PML_length, (X_RANGE, Y_RANGE, Z_RANGE), (NX, NY, NZ))
PML_ORDER = 3               # m in sigma(l) = sigma_max * (l/L)**m.
PML_TARGET_REFLECTION = 1e-10 # Theoretical normal-incidence amplitude ratio.
PML_SIGMA_MAX = None        # Optional normalized scalar or (x,y,z) override.
# None uses sigma_max = -(m+1)*ln(R0)/(2*eta*L), eta=sqrt(mu/epsilon).
# Keep the custom source outside the absorbing layers. PML does not remove static charge fields.

# Output settings.

FRAME_EVERY = 1              # Record every this many steps.
GIF_FPS = 12                 # Playback speed; does not affect the solution.

# DIY source settings.!!
CUSTOM_AMPLITUDE = 1.0        # Normalized current-density coefficient.
CUSTOM_CENTER = (0.0, 0.0, 0.0)
CUSTOM_RADIUS = 0.05          # Compact spatial support radius.
CUSTOM_DURATION = 1.0        # Current is zero outside [0, duration].
CUSTOM_DIRECTION = (1, 0, 1)  # Normalized in custom_current.
CUSTOM_FREQUENCY = 0.5       # Cycles per normalized time unit.

# ===== 2. Material functions =====
SPHERE_CENTER = (0.0, 0.0, 0.0)
SPHERE_RADIUS = 0.15
SPHERE_EPSILON = 6
DEFAULT_EPSILON = 1.0


def epsilon(x, y, z , default = False):
    """Positive, real permittivity; x,y,z are broadcastable coordinates.

    Evaluated once at Ex/Ey/Ez locations. Keep the PML and its interface
    in one homogeneous background. Example dielectric sphere:
        return np.where(x*x + y*y + z*z < 0.1**2, 4.0, 1.0)
    """
    if default:
        return DEFAULT_EPSILON
    xb, yb, zb = SPHERE_CENTER
    r_squared = (x - xb)**2 + (y - yb)**2 + (z - zb)**2
    return np.where(r_squared < SPHERE_RADIUS**2,
                        SPHERE_EPSILON, 1.0)


def mu(x, y, z):
    """Positive, real permeability, evaluated once at Hx/Hy/Hz locations.

    Spatial variation is allowed inside the physical domain; the PML
    and its interface must have one constant background value.
    """
    return 1.0


# ===== 3. Custom current =====
def custom_current(x, y, z, t):
    """Build a localized current from a shape, waveform, and direction.

    Inputs: x,y,z are scalars or broadcastable arrays; t is a scalar.
    Returns: (Jx,Jy,Jz), arrays/scalars with the broadcast xyz shape.
    No input is modified. Reads the CUSTOM_* settings above.
    Edit the equations below to change the source model.

    Mathematical expression (r = distance from center):
        S(r) = max(1 - r^2 / R^2, 0)^2
        A(t) = sin(pi*t/T) * sin(2*pi*t/T) * sin(2*pi*f*t)  for 0 < t < T; otherwise 0
        d_hat = direction / sqrt(d_x^2 + d_y^2 + d_z^2)
        J(x,y,z,t) = J0 * S(r) * A(t) * d_hat
    Direction is automatically normalized; e.g. (1,1,0) gives (1,1,0)/sqrt(2).
    Its three components must be finite and the vector must be nonzero.
    The current-density magnitude is at most abs(J0).
    R=CUSTOM_RADIUS, T=CUSTOM_DURATION, f=CUSTOM_FREQUENCY, J0=CUSTOM_AMPLITUDE.
    The current is exactly zero outside the sphere and outside [0,T].
    It can build charge; the solver updates rho from -div(J).
    """
    # 1. Read the shared strength, geometry, duration, and direction.
    amplitude = CUSTOM_AMPLITUDE
    center = CUSTOM_CENTER
    radius = CUSTOM_RADIUS
    duration = CUSTOM_DURATION
    direction = CUSTOM_DIRECTION
    if radius <= 0 or duration <= 0:
        raise ValueError("DIY radius and duration must be positive.")


    ## just normalize the direction vector to avoid overflow for large weights
    # Unit direction: d_hat = d / |d|. Strength is controlled by amplitude.
    direction = np.asarray(direction, dtype=float)
    if direction.shape != (3,) or not np.isfinite(direction).all():
        raise ValueError("DIY direction must contain three finite numbers.")
    direction_scale = np.max(np.abs(direction))
    if direction_scale == 0:
        raise ValueError("DIY direction must be nonzero; use amplitude=0 to disable.")
    direction = direction / direction_scale  # Avoid overflow for large weights.
    unit_direction = direction / np.linalg.norm(direction)

    # 2. Spatial shape: a smooth, compact profile, with no Gaussian tails.
    x0, y0, z0 = center
    r_squared = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
    spatial = np.maximum(1 - r_squared / radius**2, 0.0)**2 # cut off at r=R, smooth inside.
    # Alternative: uniform inside the same sphere (a sharp boundary).
    # spatial = np.where(r_squared <= radius**2, 1.0, 0.0)


    # 3. Time waveform: sin(pi*t/T) * sin(2*pi*t/T) * sin(2*pi*f*t).
    if 0 < t < duration:
        window = np.sin(np.pi * t / duration)*np.sin(2*np.pi * t / duration) # smooth turn-on and turn-off
        phase = 2 * np.pi * CUSTOM_FREQUENCY * t
        waveform = window * np.sin(phase)
    else:
        waveform = 0.0

    # 4. Assemble the three components. You can replace these independently.
    value = amplitude * spatial * waveform
    Jx = unit_direction[0] * value
    Jy = unit_direction[1] * value
    Jz = unit_direction[2] * value
    return Jx, Jy, Jz


# ===== 4. Shared setup, run, and export =====
def get_simulation_settings():
    """Return current solve keyword arguments for both run and analysis.

    Includes bounds, cells, end_time, CFL, active current callable,
    frame stride, material functions, and PML parameters. Reads the module
    settings at call time; does not solve, draw, or change any settings.
    """
    return dict(
        bounds=(X_RANGE, Y_RANGE, Z_RANGE),
        cells=(NX, NY, NZ),
        end_time=T_END,
        cfl=CFL,
        current_density=custom_current,
        frame_every=FRAME_EVERY,
        epsilon=epsilon,
        mu=mu,
        pml_cells=PML_CELLS if USE_PML else 0,
        pml_order=PML_ORDER,
        pml_reflection=PML_TARGET_REFLECTION,
        pml_sigma_max=PML_SIGMA_MAX,
    )


def get_source_bounds():
    """Return the custom source's enclosing (3,2) box.

    Keep CUSTOM_CENTER/RADIUS consistent with custom_current's support.
    """
    center = CUSTOM_CENTER
    radius = CUSTOM_RADIUS
    if np.ndim(radius) != 0 or not np.isfinite(radius) or radius <= 0:
        raise ValueError("The active source radius in fdtd_3d.py must be positive and finite.")
    center = np.asarray(center, dtype=float)
    if center.shape != (3,) or not np.isfinite(center).all():
        raise ValueError("The active source center in fdtd_3d.py must contain three finite coordinates.")
    return np.column_stack((center - radius, center + radius))


def main(output_dir=None):
    """Solve once and save separate E/H PNGs and GIFs.

    output_dir defaults to src/outputs. Returns (result, paths), where
    paths["E"] and paths["H"] each contain "png" and "gif" paths.
    Both fields use the same sampled times, already aligned by the solver.
    """
    frames = {"E": [], "H": []}

    def record_frame(time, electric, centers, magnetic):
        """Sample both fields from this timestep; no second simulation."""
        frames["E"].append(sample_fields(time, electric, centers, "E"))
        frames["H"].append(sample_fields(time, magnetic, centers, "H"))

    result = timed_solve("FDTD", **get_simulation_settings(), on_frame=record_frame)
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    paths = {}
    plot_seconds = 0.0
    for kind in ("E", "H"):
        paths[kind], seconds = timed_call(
            f"{kind} PNG/GIF export", save_results, result, frames[kind], output_dir,
            fps=GIF_FPS, kind=kind,
            on_progress=lambda done, total: print_progress(done, total, f"{kind} GIF frames"),
        )
        plot_seconds += seconds
        frames[kind].clear()  # Release sampled frames after this field is exported.
    result["performance"]["plot_seconds"] = plot_seconds
    print(f"Solve + export total: {result['performance']['wall_seconds'] + plot_seconds:.3f} s")
    print(f"Grid: {NX} x {NY} x {NZ}; steps: {result['steps']}")
    print(f"Normalized dx,dy,dz: {result['spacing']}; dt: {result['dt']:.6g}")
    if USE_PML:
        print(f"PML + PEC; physical bounds: {result['physical_bounds'].tolist()}")
        print(f"Normalized PML sigma_max (x,y,z): {result['pml']['sigma_max']}")
    else:
        print("PEC-only reflecting walls")
    for kind in ("E", "H"):
        print(f"Saved {kind}: {paths[kind]['png']} and {paths[kind]['gif']}")
    return result, paths


if __name__ == "__main__":
    main()
