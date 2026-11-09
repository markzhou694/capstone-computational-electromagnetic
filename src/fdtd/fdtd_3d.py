"""Run a 3D Maxwell Yee-FDTD example in a uniform medium with PEC walls.

The solver advances SI-unit electromagnetic fields with a source J [A/m^2]:
    epsilon * dE/dt = curl(H) - J
    mu * dH/dt = -curl(E)
    d(rho)/dt = -div(J)

This baseline is a *closed PEC cavity*, NOT an open-domain/CPML calculation.
Images show qualitative behavior; quantitative checks need reference solutions.
Run this file from the repository root: python src/fdtd/fdtd_3d.py
"""

from pathlib import Path
import numpy as np
from yee_solver import solve
from plot_fields import sample_fields, save_results

# ===== 1. Domain, simulation, and output =====
X_RANGE = (-1.0, 1.0)        # m
Y_RANGE = (-1.0, 1.0)        # m
Z_RANGE = (-1.0, 1.0)        # m
NX, NY, NZ = 50, 50, 50
T_END_NS = 12.0
CFL = 0.8                    # Fraction of the 3D Yee CFL upper bound

PLOT_FIELD = "E"             # E or H
FRAME_EVERY = 8              # Output only; does not affect computed solution
GIF_FPS = 12
SAVE_NUMERICAL_DATA = True  # Save final raw Yee arrays and solver metadata

# ===== 2. Select one of the source configurations =====
USE_CUSTOM_CURRENT = True   # True: custom chirped source; False: Gaussian pulse
RADIAL_PULSE = False        # Only for USE_CUSTOM_CURRENT=False
INCLUDE_DC_WIRE = False     # Only for USE_CUSTOM_CURRENT=False

# Custom compact-support chirp (frequencies in GHz; times in ns).
CUSTOM_AMPLITUDE = 100.0    # A/m^2
CUSTOM_CENTER = (0.0, 0.0, 0.0)  # m
CUSTOM_RADIUS = 0.5         # m
CUSTOM_DURATION_NS = 5.0    # ns
CUSTOM_DIRECTION = (2.0, -1.3, 0.55)
CUSTOM_F0_GHZ = 0.3         # GHz
CUSTOM_F1_GHZ = 0.6         # GHz; 0.6 GHz has ~12.5 cells/wavelength at dx=0.04 m

# Alternative Gaussian-in-space, Gaussian-in-time sinusoidal pulse.
J_AMPLITUDE = 10.0          # A/m^2
SOURCE_CENTER = (0.0, 0.0, 0.0)  # m
SOURCE_WIDTH = 0.1         # m, spatial Gaussian standard deviation
SOURCE_RADIUS = None       # m; None avoids a discontinuous hard cutoff
FREQUENCY_GHZ = 0.5        # GHz; actual sine oscillation frequency
PEAK_TIME_NS = 2.0         # ns
PULSE_WIDTH_NS = 0.5       # ns

# Optional Gaussian DC wire along z, integrated current in amperes.
DC_CURRENT_A = 100.0
DC_WIRE_XY = (0.0, 0.0)     # m
DC_WIRE_WIDTH = 0.04       # m
DC_RAMP_NS = 1.0           # ns


def linear_chirp_phase(t_ns, f0_ghz, f1_ghz, duration_ns):
    """Phase [radians] of a linear chirp, using GHz and ns consistently.

    f(t) = f0 + (f1-f0)*t/T, with t and T in ns and f in GHz.
    """
    if duration_ns <= 0:
        raise ValueError("duration_ns must be positive.")
    return 2 * np.pi * (
        f0_ghz * t_ns
        + (f1_ghz - f0_ghz) * t_ns**2 / (2 * duration_ns)
    )


def custom_current(x, y, z, t):
    """Smooth, compactly supported chirped current J(x,t) [A/m^2].

    J = J0 * max(1-r^2/R^2,0)^2 * sin(pi*t/T)^2 * sin(phi(t)) * d_hat
    for 0 < t < T; zero at all other times.  The unit direction d_hat is
    constant. The source may generate charge via div(J) and the continuity
    equation; it is not assumed to be divergence-free.

    Inputs x,y,z are scalars or broadcastable NumPy arrays [m]; t is in [s].
    Returns a tuple of three broadcastable current components [A/m^2].
    """
    if not np.isfinite(CUSTOM_RADIUS) or CUSTOM_RADIUS <= 0:
        raise ValueError("CUSTOM_RADIUS must be a positive finite length.")
    if not np.isfinite(CUSTOM_DURATION_NS) or CUSTOM_DURATION_NS <= 0:
        raise ValueError("CUSTOM_DURATION_NS must be positive and finite.")
    if not np.isfinite(CUSTOM_AMPLITUDE):
        raise ValueError("CUSTOM_AMPLITUDE must be finite.")
    if not all(np.isfinite(f) and f >= 0 for f in (CUSTOM_F0_GHZ, CUSTOM_F1_GHZ)):
        raise ValueError("Custom chirp frequencies must be nonnegative and finite.")

    direction = np.asarray(CUSTOM_DIRECTION, dtype=float)
    if direction.shape != (3,) or not np.isfinite(direction).all():
        raise ValueError("CUSTOM_DIRECTION must contain three finite numbers.")
    direction_scale = np.max(np.abs(direction))
    if direction_scale == 0:
        raise ValueError("CUSTOM_DIRECTION must be nonzero.")
    direction = direction / direction_scale  # Avoid overflow when normalizing
    direction /= np.linalg.norm(direction)

    x0, y0, z0 = CUSTOM_CENTER
    r2 = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
    spatial = np.maximum(1.0 - r2 / CUSTOM_RADIUS**2, 0.0)**2

    t_ns = t * 1e9
    if 0.0 < t_ns < CUSTOM_DURATION_NS:
        window = np.sin(np.pi * t_ns / CUSTOM_DURATION_NS)**2
        phase = linear_chirp_phase(
            t_ns, CUSTOM_F0_GHZ, CUSTOM_F1_GHZ, CUSTOM_DURATION_NS
        )
        waveform = window * np.sin(phase)
    else:
        waveform = 0.0

    magnitude = CUSTOM_AMPLITUDE * spatial * waveform
    return tuple(float(d) * magnitude for d in direction)


def pulse_current(x, y, z, t):
    """Gaussian spatial and time-envelope pulse, directed along z [A/m^2].

    Jz = J0 * exp(-r^2/(2*sigma^2)) * exp(-((t_ns-t0_ns)/tau_ns)^2)
             * sin(2*pi*f_GHz*t_ns) * C(r).
    C(r)=1 unless SOURCE_RADIUS is given, then C=1 for r<=R and 0 outside.
    The cutoff is discontinuous and may increase high-frequency artifacts.
    """
    if SOURCE_WIDTH <= 0 or not np.isfinite(SOURCE_WIDTH):
        raise ValueError("SOURCE_WIDTH must be positive and finite.")
    if PULSE_WIDTH_NS <= 0 or not np.isfinite(PULSE_WIDTH_NS):
        raise ValueError("PULSE_WIDTH_NS must be positive and finite.")
    x0, y0, z0 = SOURCE_CENTER
    r2 = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
    spatial = np.exp(-r2 / (2 * SOURCE_WIDTH**2))
    if SOURCE_RADIUS is not None:
        if not np.isfinite(SOURCE_RADIUS) or SOURCE_RADIUS <= 0:
            raise ValueError("SOURCE_RADIUS must be None or positive and finite.")
        spatial = np.where(r2 <= SOURCE_RADIUS**2, spatial, 0.0)
    t_ns = t * 1e9
    envelope = np.exp(-((t_ns - PEAK_TIME_NS) / PULSE_WIDTH_NS)**2)
    return (J_AMPLITUDE * spatial * envelope
            * np.sin(2 * np.pi * FREQUENCY_GHZ * t_ns))


def dc_wire_current(x, y, t):
    """Gaussian z-directed wire current density Jz(x,y,t) [A/m^2].

    The transverse profile integrates to DC_CURRENT_A over an infinite plane
    after ramping; the finite discretized domain approximates this integral.
    """
    if DC_CURRENT_A == 0:
        return 0.0
    if not np.isfinite(DC_WIRE_WIDTH) or DC_WIRE_WIDTH <= 0:
        raise ValueError("DC_WIRE_WIDTH must be positive and finite.")
    x0, y0 = DC_WIRE_XY
    r2 = (x - x0)**2 + (y - y0)**2
    profile = np.exp(-r2 / (2 * DC_WIRE_WIDTH**2)) / (2 * np.pi * DC_WIRE_WIDTH**2)
    t_ns = t * 1e9
    if DC_RAMP_NS > 0 and 0 <= t_ns < DC_RAMP_NS:
        ramp = np.sin(np.pi * t_ns / (2 * DC_RAMP_NS))**2
    elif t_ns < 0:
        ramp = 0.0
    else:
        ramp = 1.0
    return DC_CURRENT_A * profile * ramp


def current_density(x, y, z, t, dc=False, sym=False):
    """Example source dispatcher returning (Jx,Jy,Jz) in [A/m^2].

    If USE_CUSTOM_CURRENT is True, return custom_current only.
    Otherwise use a Gaussian pulse: z-directed by default, radial if sym=True.
    The optional z-directed DC wire is included when dc=True.
    This keeps the original positional source API available for experiments.
    """
    if USE_CUSTOM_CURRENT:
        return custom_current(x, y, z, t)

    pulse = pulse_current(x, y, z, t)
    if sym:
        x0, y0, z0 = SOURCE_CENTER
        rx, ry, rz = x - x0, y - y0, z - z0
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        safe_r = np.where(r > 0, r, 1.0)
        jx = pulse * np.where(r > 0, rx / safe_r, 0.0)
        jy = pulse * np.where(r > 0, ry / safe_r, 0.0)
        jz = pulse * np.where(r > 0, rz / safe_r, 0.0)
    else:
        jx, jy, jz = 0.0, 0.0, pulse

    if dc:
        jz = jz + dc_wire_current(x, y, t)
    return jx, jy, jz


def default_output_dir():
    """Return the repository-root outputs/ directory for src/fdtd/fdtd_3d.py."""
    return Path(__file__).resolve().parents[2] / "outputs"


def save_field_data(result, filename, source_name):
    """Save final Yee-grid field arrays, charge, and metadata for analysis.

    This is a single *final-time* snapshot, not a time history or a surface
    recording. The underlying arrays retain their native Yee locations.
    """
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    ex, ey, ez = result["electric"]
    hx, hy, hz = result["magnetic"]
    np.savez_compressed(
        filename,
        Ex=ex, Ey=ey, Ez=ez, Hx=hx, Hy=hy, Hz=hz,
        rho=result["charge"],
        bounds=result["bounds"], spacing=result["spacing"],
        x_nodes=result["nodes"][0], y_nodes=result["nodes"][1],
        z_nodes=result["nodes"][2],
        x_centers=result["centers"][0], y_centers=result["centers"][1],
        z_centers=result["centers"][2],
        time=result["time"], dt=result["dt"], steps=result["steps"],
        epsilon=result["epsilon"], mu=result["mu"],
        cfl=result["cfl"], source_name=source_name,
        boundary_condition="PEC",
        gauss_residual_rms=result["gauss_residual_rms"],
        gauss_residual_max=result["gauss_residual_max"],
    )
    return filename


def main(output_dir=None):
    """Run the experiment and export PNG/GIF and optional final-time NPZ.

    Returns (result, paths) where paths has 'png', 'gif', and optionally 'data'.
    This implementation has reflecting PEC walls; it does not implement CPML.
    """
    if PLOT_FIELD not in ("E", "H"):
        raise ValueError('PLOT_FIELD must be "E" or "H".')
    frames = []

    def record_frame(time, electric, centers, magnetic):
        field = electric if PLOT_FIELD == "E" else magnetic
        frames.append(sample_fields(time, field, centers, PLOT_FIELD))

    if USE_CUSTOM_CURRENT:
        source = custom_current
        source_name = "compact_chirp"
    else:
        def source(x, y, z, t):
            return current_density(
                x, y, z, t, dc=INCLUDE_DC_WIRE, sym=RADIAL_PULSE
            )
        source_name = "gaussian_pulse" + ("_wire" if INCLUDE_DC_WIRE else "")

    result = solve(
        bounds=(X_RANGE, Y_RANGE, Z_RANGE),
        cells=(NX, NY, NZ),
        end_time=T_END_NS * 1e-9,
        cfl=CFL,
        current_density=source,
        on_frame=record_frame,
        frame_every=FRAME_EVERY,
    )
    output_dir = Path(output_dir) if output_dir is not None else default_output_dir()
    paths = save_results(result, frames, output_dir, fps=GIF_FPS, kind=PLOT_FIELD)
    if SAVE_NUMERICAL_DATA:
        paths["data"] = save_field_data(
            result, output_dir / "fdtd_final_fields.npz", source_name
        )
    print(f"Grid: {NX} x {NY} x {NZ}; steps: {result['steps']}")
    print(f"dx,dy,dz [m]: {result['spacing']}; dt [ns]: {result['dt'] * 1e9:.6g}")
    print(f"Gauss residual RMS [C/m^3]: {result['gauss_residual_rms']:.3e}")
    print(f"Updated output files in: {output_dir}")
    return result, paths


if __name__ == "__main__":
    main()
