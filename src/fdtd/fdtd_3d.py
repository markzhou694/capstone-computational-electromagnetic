"""Example: set parameters, define a current, solve, and save PNG/GIF.

Equations solved (uniform epsilon, mu; SI units):
    epsilon * dE/dt = curl(H) - J
    mu      * dH/dt = -curl(E)
    drho/dt        = -div(J)
Initial E=H=rho=0; tangential E=0 on the six PEC walls.

To build your own J: set USE_CUSTOM_CURRENT=True and edit custom_current.
Start with J = amplitude * spatial_shape * time_waveform * direction.
For other simulations, call yee_solver.solve directly; see ../docs/API.md.
"""

from pathlib import Path
import numpy as np
from yee_solver import solve
from plot_fields import sample_fields, save_results

# ===== 1. Parameters ===== # very important!

# Box bounds [m], cell counts, and final time [ns].
X_RANGE = (-1.0, 1.0)
Y_RANGE = (-1.0, 1.0)
Z_RANGE = (-1.0, 1.0)
NX, NY, NZ = 90, 90,90
T_END_NS = 12.0
CFL = 0.8                   # Stability fraction: 0 < CFL <= 1.

# PML occupies these outer cells INSIDE the box; the outer wall stays PEC.
# Keep the current source inside [min+PML_CELLS*d, max-PML_CELLS*d].
USE_PML = True              # False reproduces the original PEC-only solver.
PML_CELLS = 8               # Per side; 2*PML_CELLS < min(NX, NY, NZ).
PML_ORDER = 3               # m in sigma(l) = sigma_max * (l/L)**m.
PML_TARGET_REFLECTION = 1e-6 # Theoretical normal-incidence amplitude ratio.
PML_SIGMA_MAX = None        # Optional scalar or (x,y,z) override [S/m].
# None uses sigma_max = -(m+1)*ln(R0)/(2*eta*L), eta=sqrt(mu/epsilon).
# Sources extending into PML (e.g. the box-spanning DC wire) are not a
# source-free absorbing-layer setup. PML does not remove static charge fields.

# Output settings.
PLOT_FIELD = "H"             # "E": electric field; "H": magnetic field.
FRAME_EVERY = 1              # Record every this many steps.
GIF_FPS = 12                 # Playback speed; does not affect the solution.

USE_CUSTOM_CURRENT = True  # True: use only custom_current below.

# DC wire along z, through the box; its current is independent of z.
DC_CURRENT_A = 100.0         # Current coefficient [A]; 0 disables the wire.
DC_WIRE_XY = (0.0, 0.0)      # Wire axis coordinates (x, y) [m].
DC_WIRE_WIDTH = 0.04         # Gaussian cross-section standard deviation [m].
DC_RAMP_NS = 1.0             # Smooth turn-on duration [ns].

# Optional Gaussian pulse; currently disabled by J_AMPLITUDE = 0.
J_AMPLITUDE = 10.0            # Current-density coefficient [A/m^2].
SOURCE_CENTER = (0.0, 0.0, 0.0)  # Pulse center [m].
SOURCE_WIDTH = 0.1          # Spatial Gaussian standard deviation [m].
SOURCE_RADIUS = 0.3         # Cutoff radius [m]; None means no cutoff.
FREQUENCY_GHZ = 0.5         # Frequency parameter in sin and cos [GHz].
PEAK_TIME_NS = 2.0          # Time-envelope center [ns].
PULSE_WIDTH_NS = 0.5        # Time-envelope width parameter [ns].


# ===== 2. Current equations =====
def current_density(x, y, z, t , dc = False, sym = False):
    """Select the DIY current or add the example pulse and wire currents.

    Inputs: x,y,z are scalars or broadcastable NumPy arrays [m]; t is [s].
    Returns: (Jx,Jy,Jz) [A/m^2], each scalar or broadcastable to xyz.
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

    Inputs: x,y,z are scalars or broadcastable arrays [m]; t is a scalar [s].
    Returns: (Jx,Jy,Jz) [A/m^2], arrays/scalars with the broadcast xyz shape.
    No input is modified. All DIY settings are local to this function.

    Mathematical expression (r = distance from center):
        S(r) = max(1 - r^2 / R^2, 0)^2
        A(t) = sin(pi*t/T)^2  for 0 <= t <= T; otherwise 0
        d_hat = direction / sqrt(d_x^2 + d_y^2 + d_z^2)
        J(x,y,z,t) = J0 * S(r) * A(t) * d_hat
    Direction is automatically normalized; e.g. (1,1,0) gives (1,1,0)/sqrt(2).
    Its three components must be finite and the vector must be nonzero.
    The peak current-density magnitude is abs(J0) [A/m^2], not amps.
    R=radius [m], T=duration_ns*1e-9 [s], J0=amplitude [A/m^2].
    The current is exactly zero outside the sphere and outside [0,T].
    It can build charge; the solver updates rho from -div(J).
    """
    # 1. Set strength, location, size, duration, and direction.
    amplitude = 500.0          # J0 [A/m^2]
    center = (0.0, 0.0, 0.0) # [m]
    radius = 0.25            # R > 0 [m]; keep the sphere inside the box. A cut off 
    duration_ns = 6.0       # T > 0 [ns]
    direction = (2.5, -1.3, 0.55)  # Any nonzero direction; normalized below.
    if radius <= 0 or duration_ns <= 0:
        raise ValueError("DIY radius and duration_ns must be positive.")

    
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

    
    # 3. Time waveform: windowed linear chirp, f0 -> f1 over [0, T].
    #    A(t) = sin^2(pi t/T) * sin(2 pi [f0 t + (f1-f0)/(2T) t^2])
    f0_ghz = 0.3            # start frequency [GHz]
    f1_ghz = 1.5            # end frequency [GHz]
    t_ns = t * 1e9
    if 0 < t_ns < duration_ns:
        window = np.sin(np.pi * t_ns / duration_ns)**2
        phase = 2 * np.pi * (f0_ghz * t_ns * np.sin(2 * np.pi * t_ns / duration_ns)
                             + (f1_ghz - f0_ghz) / (2 * duration_ns) * np.exp(t_ns)**2)
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

    Inputs: x,y,z are scalars or broadcastable arrays [m]; t is [s].
    Returns: pulse Jz [A/m^2], a scalar or array of the broadcast xyz shape.
    Uses the pulse parameters above, including the optional spherical cutoff.

    Mathematical expression:
        r^2 = (x-x0)^2 + (y-y0)^2 + (z-z0)^2
        phi = 2*pi*FREQUENCY_GHZ*t_ns, with t_ns=t*1e9
        J_pulse = J0 * exp(-r^2/(2*sigma^2))
                    * exp(-((t_ns-t_peak)/tau)^2) * sin(phi)*cos(phi) * C(r)
    J0=J_AMPLITUDE [A/m^2], sigma=SOURCE_WIDTH [m], center=SOURCE_CENTER [m],
    t_peak=PEAK_TIME_NS [ns], tau=PULSE_WIDTH_NS [ns].
    C(r)=1 everywhere if SOURCE_RADIUS=None; otherwise 1 for r<=SOURCE_RADIUS
    and 0 outside. sin(phi)*cos(phi)=sin(2*phi)/2 doubles the frequency.
    """
    x0, y0, z0 = SOURCE_CENTER
    r_squared = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
    spatial = np.exp(-r_squared / (2 * SOURCE_WIDTH**2))
    if SOURCE_RADIUS is not None:
        if not np.isfinite(SOURCE_RADIUS) or SOURCE_RADIUS <= 0:
            raise ValueError("SOURCE_RADIUS must be None or a positive radius [m].")
        spatial = np.where(r_squared <= SOURCE_RADIUS**2, spatial, 0.0)

    t_ns = t * 1e9
    envelope = np.exp(-((t_ns - PEAK_TIME_NS) / PULSE_WIDTH_NS)**2)
    phase = 2 * np.pi * FREQUENCY_GHZ * t_ns
    oscillation = np.sin(phase) * np.cos(phase)
    return J_AMPLITUDE * spatial * envelope * oscillation


def dc_wire_current(x, y, t):
    """Compute a Gaussian wire profile with a smooth turn-on, then constant DC.

    Inputs: x,y are scalars or broadcastable arrays [m]; t is [s].
    Returns: wire Jz [A/m^2], with the broadcast xy shape, or 0.0 if disabled.
    Uses DC_* parameters above. The profile integrates to DC_CURRENT_A over
    the infinite xy plane after turn-on; a finite sampled box is approximate.

    Mathematical expression, for simulation times t >= 0:
        r_perp^2 = (x-x0)^2 + (y-y0)^2
        J_wire = I/(2*pi*w^2) * exp(-r_perp^2/(2*w^2)) * R(t_ns)
        R(t_ns) = sin(pi*t_ns/(2*tau))^2  for tau>0 and 0<=t_ns<tau
                  1                      otherwise
    I=DC_CURRENT_A [A], w=DC_WIRE_WIDTH [m], (x0,y0)=DC_WIRE_XY [m],
    tau=DC_RAMP_NS [ns], t_ns=t*1e9. This source is independent of z.
    Gaussian describes the prescribed current profile, not wire material.
    """
    if DC_CURRENT_A == 0:
        return 0.0
    x0, y0 = DC_WIRE_XY
    rho_squared = (x - x0)**2 + (y - y0)**2
    gaussian = np.exp(-rho_squared / (2 * DC_WIRE_WIDTH**2))
    profile = gaussian / (2 * np.pi * DC_WIRE_WIDTH**2)

    t_ns = t * 1e9
    if DC_RAMP_NS > 0 and t_ns < DC_RAMP_NS:
        ramp = np.sin(0.5 * np.pi * t_ns / DC_RAMP_NS)**2
    else:
        ramp = 1.0
    return DC_CURRENT_A * profile * ramp


# ===== 3. Run and export =====
def main(output_dir=None):
    """Run this example using the module parameters and export both plots.

    Input: output_dir is a str/Path, or None for capstone_code/outputs.
    Returns: (result, paths); result is the solve dict, paths is the
        save_results dict {'png': Path, 'gif': Path}.
    Creates/replaces the two plot files and prints a short run summary.
    """
    frames = []

    def record_frame(time, electric, centers, magnetic):
        """Copy the selected E/H field into the local frame list.

        Inputs: time [s]; electric and magnetic are Yee field tuples;
                centers=(xc,yc,zc) contains 1D coordinate arrays [m].
        Returns: None. Appends a sample_fields dict; inputs are unchanged.
        """
        if PLOT_FIELD == "E":
            field = electric
        else:
            field = magnetic
        frames.append(sample_fields(time, field, centers, PLOT_FIELD))

    result = solve(
        bounds=(X_RANGE, Y_RANGE, Z_RANGE),
        cells=(NX, NY, NZ),
        end_time=T_END_NS * 1e-9,
        cfl=CFL,
        current_density=custom_current if USE_CUSTOM_CURRENT else current_density,
        on_frame=record_frame,
        frame_every=FRAME_EVERY,
        pml_cells=PML_CELLS if USE_PML else 0,
        pml_order=PML_ORDER,
        pml_reflection=PML_TARGET_REFLECTION,
        pml_sigma_max=PML_SIGMA_MAX,
    )
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    paths = save_results(result, frames, output_dir, fps=GIF_FPS, kind=PLOT_FIELD)
    print(f"Grid: {NX} x {NY} x {NZ}; steps: {result['steps']}")
    print(f"dx,dy,dz [m]: {result['spacing']}; dt [ns]: {result['dt'] * 1e9:.6g}")
    if USE_PML:
        print(f"PML + PEC; physical bounds [m]: {result['physical_bounds'].tolist()}")
        print(f"PML sigma_max (x,y,z) [S/m]: {result['pml']['sigma_max']}")
    else:
        print("PEC-only reflecting walls")
    print(f"Updated PNG and GIF in: {output_dir}")
    return result, paths


if __name__ == "__main__":
    main()
