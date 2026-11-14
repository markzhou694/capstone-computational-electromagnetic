"""Example: set parameters, define a current, solve, and save PNG/GIF.

Equations solved (uniform epsilon, mu; normalized units):
    epsilon * dE/dt = curl(H) - J
    mu      * dH/dt = -curl(E)
    drho/dt        = -div(J)
Initial E=H=rho=0; tangential E=0 on the six PEC walls.

To build your own J: set USE_CUSTOM_CURRENT=True and edit custom_current.
Start with J = amplitude * spatial_shape * time_waveform * direction.
For other simulations, call yee_solver.solve directly.
"""

from pathlib import Path
import numpy as np
import yee_solver
from yee_solver import solve
from plot_fields import sample_fields, save_results

# ===== 1. Parameters ===== # very important!

# Normalized length and time. Material defaults are in yee_solver.py:
# epsilon=mu=1, c=1/sqrt(epsilon*mu). No conversion to seconds or nanoseconds.
X_RANGE = (-1.0, 1.0)
Y_RANGE = (-1.0, 1.0)
Z_RANGE = (-1.0, 1.0)
NX, NY, NZ = 60, 60, 60
T_END = 10.0
CFL = 0.7                   # Stability fraction: 0 < CFL <= 1.

# PML occupies these outer cells INSIDE the box; the outer wall stays PEC.
# Keep the current source inside [min+PML_CELLS*d, max-PML_CELLS*d].
USE_PML = True              # False reproduces the original PEC-only solver.
PML_CELLS = 6               # Per side; 2*PML_CELLS < min(NX, NY, NZ).
PML_ORDER = 3               # m in sigma(l) = sigma_max * (l/L)**m.
PML_TARGET_REFLECTION = 1e-6 # Theoretical normal-incidence amplitude ratio.
PML_SIGMA_MAX = None        # Optional normalized scalar or (x,y,z) override.
# None uses sigma_max = -(m+1)*ln(R0)/(2*eta*L), eta=sqrt(mu/epsilon).
# Sources extending into PML (e.g. the box-spanning DC wire) are not a
# source-free absorbing-layer setup. PML does not remove static charge fields.

# Output settings.
PLOT_FIELD = "E"             # "E": electric field; "H": magnetic field.
FRAME_EVERY = 1              # Record every this many steps.
GIF_FPS = 12                 # Playback speed; does not affect the solution.

USE_CUSTOM_CURRENT = True  # True: use only custom_current below.

# DIY source settings.
CUSTOM_AMPLITUDE = 1.0        # Normalized current-density coefficient.
CUSTOM_CENTER = (0.0, 0.0, 0.0)
CUSTOM_RADIUS = 0.25          # Compact spatial support radius.
CUSTOM_DURATION = 6.0        # Current is zero outside [0, duration].
CUSTOM_DIRECTION = (1, -0.5, 1)  # Normalized in custom_current.
CUSTOM_FREQUENCY = 0.5       # Cycles per normalized time unit.

# DC wire along z, through the box; its current is independent of z.
DC_CURRENT = 100.0           # Normalized total current; 0 disables the wire.
DC_WIRE_XY = (0.0, 0.0)      # Wire axis coordinates (x, y).
DC_WIRE_WIDTH = 0.04         # Gaussian cross-section standard deviation.
DC_RAMP = 1.0                # Smooth turn-on duration.

# Optional Gaussian pulse (used when USE_CUSTOM_CURRENT=False).
J_AMPLITUDE = 10.0            # Current-density coefficient.
SOURCE_CENTER = (0.0, 0.0, 0.0)  # Pulse center.
SOURCE_WIDTH = 0.1          # Spatial Gaussian standard deviation.
SOURCE_RADIUS = 0.3         # Cutoff radius; None means no cutoff.
FREQUENCY = 0.5             # Frequency parameter in sin and cos.
PEAK_TIME = 2.0             # Time-envelope center.
PULSE_WIDTH = 0.5           # Time-envelope width parameter.


# ===== 2. Current equations =====
def current_density(x, y, z, t , dc = False, sym = False):
    """Select the DIY current or add the example pulse and wire currents.

    Inputs: x,y,z are scalars or broadcastable NumPy arrays; t is normalized time.
    Returns: (Jx,Jy,Jz), each scalar or broadcastable to xyz.
    Default equation: J = (0, 0, J_pulse + J_wire).
    With USE_CUSTOM_CURRENT=True: J = custom_current(x,y,z,t) instead.
    Reads the source parameters above; does not change input arrays.
    """
    if USE_CUSTOM_CURRENT:
        return custom_current(x, y, z, t)

    x0, y0, z0 = SOURCE_CENTER
    if sym:
        r = np.sqrt((x - x0)**2 + (y - y0)**2 + (z - z0)**2)
        r_safe = np.where(r > 0, r, 1.0)        # avoid 0/0 at the center
        p = pulse_current(x, y, z, t)           # g(r) f(t)
        Jx = p * np.where(r > 0, (x - x0) / r_safe, 0.0)
        Jy = p * np.where(r > 0, (y - y0) / r_safe, 0.0)
        Jz = p * np.where(r > 0, (z - z0) / r_safe, 0.0)
    else:

        Jx = 0
        Jy = 0
        Jz = pulse_current(x, y, z, t) + dc_wire_current(x, y, t) if dc else pulse_current(x, y, z, t)
        
    
    
    return Jx, Jy, Jz


# ===== DIY: edit this function, then set USE_CUSTOM_CURRENT=True =====
def custom_current(x, y, z, t):
    """Build a localized current from a shape, waveform, and direction.

    Inputs: x,y,z are scalars or broadcastable arrays; t is a scalar.
    Returns: (Jx,Jy,Jz), arrays/scalars with the broadcast xyz shape.
    No input is modified. Reads the CUSTOM_* settings above.
    Edit the equations below to change the source model.

    Mathematical expression (r = distance from center):
        S(r) = max(1 - r^2 / R^2, 0)^2
        A(t) = sin(pi*t/T)^2 * sin(2*pi*f*t)  for 0 < t < T; otherwise 0
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

    
    # 3. Time waveform: sin^2(pi*t/T) * sin(2*pi*f*t).
    if 0 < t < duration:
        window = np.sin(np.pi * t / duration)**2
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


def pulse_current(x, y, z, t):
    """Compute amplitude * spatial Gaussian * time envelope * oscillation.

    Inputs: x,y,z are scalars or broadcastable arrays; t is normalized time.
    Returns: pulse Jz, a scalar or array of the broadcast xyz shape.
    Uses the pulse parameters above, including the optional spherical cutoff.

    Mathematical expression:
        r^2 = (x-x0)^2 + (y-y0)^2 + (z-z0)^2
        phi = 2*pi*FREQUENCY*t
        J_pulse = J0 * exp(-r^2/(2*sigma^2))
                    * exp(-((t-t_peak)/tau)^2) * sin(phi)*cos(phi) * C(r)
    J0=J_AMPLITUDE, sigma=SOURCE_WIDTH, center=SOURCE_CENTER,
    t_peak=PEAK_TIME, tau=PULSE_WIDTH.
    C(r)=1 everywhere if SOURCE_RADIUS=None; otherwise 1 for r<=SOURCE_RADIUS
    and 0 outside. sin(phi)*cos(phi)=sin(2*phi)/2 doubles the frequency.
    """
    x0, y0, z0 = SOURCE_CENTER
    r_squared = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
    spatial = np.exp(-r_squared / (2 * SOURCE_WIDTH**2))
    if SOURCE_RADIUS is not None:
        if not np.isfinite(SOURCE_RADIUS) or SOURCE_RADIUS <= 0:
            raise ValueError("SOURCE_RADIUS must be None or a positive radius.")
        spatial = np.where(r_squared <= SOURCE_RADIUS**2, spatial, 0.0)

    envelope = np.exp(-((t - PEAK_TIME) / PULSE_WIDTH)**2)
    phase = 2 * np.pi * FREQUENCY * t
    oscillation = np.sin(phase) * np.cos(phase)
    return J_AMPLITUDE * spatial * envelope * oscillation


def dc_wire_current(x, y, t):
    """Compute a Gaussian wire profile with a smooth turn-on, then constant DC.

    Inputs: x,y are scalars or broadcastable arrays; t is normalized time.
    Returns: wire Jz, with the broadcast xy shape, or 0.0 if disabled.
    Uses DC_* parameters above. The profile integrates to DC_CURRENT over
    the infinite xy plane after turn-on; a finite sampled box is approximate.

    Mathematical expression, for simulation times t >= 0:
        r_perp^2 = (x-x0)^2 + (y-y0)^2
        J_wire = I/(2*pi*w^2) * exp(-r_perp^2/(2*w^2)) * R(t)
        R(t) = sin(pi*t/(2*tau))^2  for tau>0 and 0<=t<tau
               1                  otherwise
    I=DC_CURRENT, w=DC_WIRE_WIDTH, (x0,y0)=DC_WIRE_XY,
    tau=DC_RAMP. This source is independent of z.
    Gaussian describes the prescribed current profile, not wire material.
    """
    if DC_CURRENT == 0:
        return 0.0
    x0, y0 = DC_WIRE_XY
    rho_squared = (x - x0)**2 + (y - y0)**2
    gaussian = np.exp(-rho_squared / (2 * DC_WIRE_WIDTH**2))
    profile = gaussian / (2 * np.pi * DC_WIRE_WIDTH**2)

    if DC_RAMP > 0 and t < DC_RAMP:
        ramp = np.sin(0.5 * np.pi * t / DC_RAMP)**2
    else:
        ramp = 1.0
    return DC_CURRENT * profile * ramp


# ===== 3. Shared setup, run, and export =====
def get_simulation_settings():
    """Return current solve keyword arguments for both run and analysis.

    Includes bounds, cells, end_time, CFL, active current callable,
    frame stride, material constants, and PML parameters. Reads the module
    settings at call time; does not solve, draw, or change any settings.
    """
    return dict(
        bounds=(X_RANGE, Y_RANGE, Z_RANGE),
        cells=(NX, NY, NZ),
        end_time=T_END,
        cfl=CFL,
        current_density=custom_current if USE_CUSTOM_CURRENT else current_density,
        frame_every=FRAME_EVERY,
        epsilon=yee_solver.EPSILON0,
        mu=yee_solver.MU0,
        pml_cells=PML_CELLS if USE_PML else 0,
        pml_order=PML_ORDER,
        pml_reflection=PML_TARGET_REFLECTION,
        pml_sigma_max=PML_SIGMA_MAX,
    )


def get_source_bounds():
    """Return the active run source's enclosing (3,2) box.

    Uses CUSTOM_CENTER/RADIUS for the DIY source, or SOURCE_CENTER/RADIUS
    for the default pulse (the run uses dc=False). An untruncated Gaussian
    has no finite support and cannot provide a reflection-free time bound.
    Keep this geometry consistent if replacing the spatial source equation.
    """
    center = CUSTOM_CENTER if USE_CUSTOM_CURRENT else SOURCE_CENTER
    radius = CUSTOM_RADIUS if USE_CUSTOM_CURRENT else SOURCE_RADIUS
    if radius is None:
        raise ValueError("The active pulse has no finite support; set SOURCE_RADIUS in fdtd_3d.py.")
    if np.ndim(radius) != 0 or not np.isfinite(radius) or radius <= 0:
        raise ValueError("The active source radius in fdtd_3d.py must be positive and finite.")
    center = np.asarray(center, dtype=float)
    if center.shape != (3,) or not np.isfinite(center).all():
        raise ValueError("The active source center in fdtd_3d.py must contain three finite coordinates.")
    return np.column_stack((center - radius, center + radius))


def main(output_dir=None):
    """Run this example using the module parameters and export both plots.

    Input: output_dir is a str/Path, or None for src/outputs.
    Returns: (result, paths); result is the solve dict, paths is the
        save_results dict {'png': Path, 'gif': Path}.
    Creates/replaces the two plot files and prints a short run summary.
    """
    frames = []

    def record_frame(time, electric, centers, magnetic):
        """Copy the selected E/H field into the local frame list.

        Inputs: time; electric and magnetic are Yee field tuples;
                centers=(xc,yc,zc) contains 1D coordinate arrays.
        Returns: None. Appends a sample_fields dict; inputs are unchanged.
        """
        if PLOT_FIELD == "E":
            field = electric
        else:
            field = magnetic
        frames.append(sample_fields(time, field, centers, PLOT_FIELD))

    result = solve(**get_simulation_settings(), on_frame=record_frame)
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    paths = save_results(result, frames, output_dir, fps=GIF_FPS, kind=PLOT_FIELD)
    print(f"Grid: {NX} x {NY} x {NZ}; steps: {result['steps']}")
    print(f"Normalized dx,dy,dz: {result['spacing']}; dt: {result['dt']:.6g}")
    if USE_PML:
        print(f"PML + PEC; physical bounds: {result['physical_bounds'].tolist()}")
        print(f"Normalized PML sigma_max (x,y,z): {result['pml']['sigma_max']}")
    else:
        print("PEC-only reflecting walls")
    print(f"Updated PNG and GIF in: {output_dir}")
    return result, paths


if __name__ == "__main__":
    main()
