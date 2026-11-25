# Project source code

**AI assistants: store all newly created project code in this directory.**
Read the root [AGENTS.md](../AGENTS.md) and the shared
[project rules](../docs/PROJECT_RULES.md) before working.

- Put Python (`.py`) and MATLAB (`.m`) modules here. Start with simple files;
  introduce subdirectories only when useful.
- Put supporting executable scripts in `src/scripts/`, tests in `src/tests/`,
  and computational notebooks in `src/notebooks/` if those are needed. These
  are placement conventions, not folders or implementations already created.
- Keep collaboration notes, derivations, references, and progress records in
  `docs/`; do not use `docs/` or the repository root to store source code.
- Do not commit virtual environments, credentials, caches, generated results,
  or large datasets with the code. Record how to reproduce approved results.
- Record each change in [docs/TIMELINE.md](../docs/TIMELINE.md) and update
  [docs/PROJECT_STATUS.md](../docs/PROJECT_STATUS.md) as appropriate.

## 3D FDTD

The active FDTD folder contains only:

```text
fdtd/
  fdtd_3d.py      Editable parameters/current and run entry point
  plot_fields.py E/H sampling, plots and PNG/GIF export
  yee_solver.py  Reusable uniform-medium 3D Yee solver
  err_analysis.py Safe stopping time, PML run and larger PEC reference
```

Run `python src/fdtd/fdtd_3d.py` from the repository root with NumPy,
Matplotlib and Pillow installed. Outputs go to `src/outputs/`.
Calling formats and mathematical expressions are in the Python docstrings.

All example inputs and plots use normalized units. In `yee_solver.py`,
`MU0 = EPSILON0 = 1.0` and `C0 = 1/sqrt(MU0*EPSILON0)`; the solver also
calculates its wave speed from the supplied epsilon and mu for each run.
In `fdtd_3d.py`, `T_END=10`, `CUSTOM_DURATION=6`, `CUSTOM_FREQUENCY=0.5`
(cycles per time unit), and `CUSTOM_AMPLITUDE=1`. Geometry is unchanged
numerically. These are a new normalized test's parameters, not a conversion
preserving the former SI experiment. Source functions use t directly;
there are no ns/GHz conversions. PML strength is calculated in the same
units from the layer thickness, impedance and target reflection.

For clearer oscillations, `plot_fields.py` shows a signed field component
on each slice. Set `SLICE_COMPONENT` to `"x"`, `"y"`, or `"z"` there (default
`"z"`). Orange is positive, blue is negative, and black is zero. Colors use
one fixed symmetric-log scale across the GIF, with a linear region near
zero so weaker fields remain visible. The colorbar values are field values.
Arrows are thicker and rescaled in each frame. Length is proportional to the
square root of field magnitude, making weaker vectors visible; direction is
unchanged. `ARROW_LENGTH` controls their largest displayed length
as a fraction of the shortest box side. Compare the fixed colorbar values for amplitude changes between frames.
Labels are concise; spatial axes use meters. With vacuum speed set to 1,
one solver time unit corresponds to 1 m / c_vacuum (about 3.336 ns). This affects only
display, including the existing spatial averaging to cell centers.

In `err_analysis.py`, `simulation_time(a,b,B,c,dt)` returns the last safe
grid time with a 1.5 dt reserve. `result = fdtd_with_pml(T,dt)` uses the grid
and PML parameters from fdtd_3d and always passes its custom_current.
`result["electric"]` and `result["magnetic"]` contain three native Yee arrays,
both at T, over the full grid. The result also includes physical_bounds,
physical_lengths=(Lx,Ly,Lz), grid coordinates/spacing, timing,
material constants and PML settings. Physical dimensions exclude the PML
layers. No plots are generated.

`reference = fdtd_reference(result, B)` runs the same custom current on a
larger centered cube without PML (outer walls are PEC). It reuses the first
run's spacing, time, step count and material constants. Requested B is
rounded outward by whole cells; the actual bounds are returned in bounds.
physical_bounds/physical_lengths still identify the original comparison
region. padding_cells gives the number of added cells per side. A reference
too small for the final time is rejected using simulation_time.

Duplicated FDTD documentation and old tests were removed from this subtree
during the earlier layout change. Their prior versions remain in Git
history and in a local backup outside the repository. The original sibling
`capstone_code/` is separate and does not automatically synchronize here.

### Timing, progress and operation counts

`fdtd/run_metrics.py` contains editable `print_progress`, `timed_call`,
`estimate_fdtd_flops` and `timed_solve` functions. Both entry points report
solver wall time and estimated core arithmetic; ordinary PNG/GIF export is
timed separately, with GIF frame progress. Analysis reports each domain and
the combined pair; error plotting is timed separately. Solver result metadata
contains `performance.wall_seconds` and `performance.estimated_core_flops`.
Wall time includes initialization, source and frame callbacks (including
sampling, temporary I/O and error comparison); this is not pure kernel timing.
FLOPs count core array arithmetic and H output alignment only. They exclude
source evaluation, setup, plotting and I/O; the formula and conventions are
in the function docstring. These are estimates, not hardware counter readings.
Compare time/grid/step settings alongside these totals when comparing runs.

### Spatial materials

Edit `epsilon(x, y, z)` and `mu(x, y, z)` in `fdtd/fdtd_3d.py`; both default
to 1. They accept broadcastable coordinates and return positive real scalar
or broadcastable array values. The solver samples them once on the respective
E-edge and H-face grids. PML and its interfaces must stay homogeneous.
`custom_current` is now the only example source; pulse/wire alternatives and
`USE_CUSTOM_CURRENT` were removed. The existing `err_analysis.py` timing remains
homogeneous-only and rejects nonuniform materials.

Run material checks from the repository root:
`python -B -m unittest discover -s src/tests -p 'test_material_functions.py'`.

## Dielectric bunny example

Run `python src/fdtd/fdtd_3d_complex_geometric.py` from the repository root.
Install `trimesh` and `rtree` in the same Python environment first.
Grid/time/PML/custom current are read from fdtd_3d.py; its sphere material
is replaced only for this run. Edit BUNNY_CENTER, BUNNY_SIZE and BUNNY_EPSILON
in the new file. Background epsilon=mu=1; default bunny epsilon=4.
The included closed mesh is sampled directly at native electric locations,
using binary inside/outside masks (staircase geometry, no subpixel averaging).
The source stays outside the bunny and both remain inside the physical box.
Outputs go to src/outputs/bunny: geometry preview and separate E/H PNG/GIFs.
The smooth geometry preview shows the input mesh, not the discretized material.
The solver is unchanged; coarse-grid ears and interface fields require
resolution checks before quantitative scattering claims.

## Direct time-domain near-to-far field

Run `python src/fdtd/near-to-far-field.py`. It reads the saved grid, material,
custom current, PML and T_END from fdtd_3d.py, runs FDTD once, and records
only the sphere samples at every timestep. It does not run the ordinary
field animations. Edit RADIUS, N_THETA, N_PHI and OBSERVATION_POINT at the
top of the new file. None for RADIUS uses the existing source-centered
sphere rule. H is already aligned in time by the solver; each Cartesian
component is interpolated directly from its own native Yee locations.

The calculation follows four explicit steps:

1. Record `electric` and `magnetic`, each `(Nt,Ns,3)`, on the sphere.
2. Assign latitude-patch areas
   `w_ij = RADIUS**2 * dphi * (cos(i*dtheta)-cos((i+1)*dtheta))`.
   They sum to the sphere area. The two extra pole samples have zero
   integration weight because the patches already cover both caps.
3. Construct `Js=n cross H`, `Ms=-n cross E`, and the equivalent charge
   traces `rho=epsilon*n dot E`, `rho_m=mu*n dot H`.
4. For each sphere point y, interpolate these data and their time derivatives
   at `t-|x-y|/c`, where `c=1/sqrt(epsilon_background*mu_background)`.
   Sum the full Maxwell kernels displayed in `reconstruct_fields`.

The spacetime Green function is `delta(t-t'-r/c)/(4*pi*r)`. Its delta
function has already performed the time integral; do not multiply the
surface sum by dt. This is a direct integral of known fields, with no FFT,
modal expansion or integral-equation solve. It retains finite-distance
terms and can evaluate points outside the sphere, even beyond the FDTD box.

The source and every material contrast must be strictly inside the sphere.
The sphere and its interpolation stencils must stay in a homogeneous
physical region before PML. Native material samples are checked in a collar
one cell diagonal wide and throughout the grid exterior. The continuation
outside the FDTD box must also be that same homogeneous, nondispersive
background; grid checks cannot detect unresolved or external objects.
Zero initial fields and no incoming waves are assumed. Reconstructed
accuracy still depends on FDTD/PML, spatial interpolation, time sampling
and surface quadrature. Close-to-surface observers require more points.

The output folder is `src/outputs/near_to_far_field/`:

- `surface_history.npz`: times `(Nt,)`, E/H `(Nt,Ns,3)`, points/normals
  `(Ns,3)`, weights `(Ns,)`, geometry, exterior material constants and grid metadata.
- `exterior_fields.npz`: times `(No,)`, electric/magnetic `(No,3)`, point
  and background constants. The time is the observer's time, including travel.
- `near_to_far_field.png`: signed Ex/Ey/Ez and Hx/Hy/Hz time traces.
- `sphere_samples.png`: geometry and sampling locations.

With `times=None`, the observation window is the recorded time interval
shifted by `(distance(point,center)-RADIUS)/c`. Values before zero source
time are zero; unknown future data are rejected. T_END controls the recorded
history, so increase it for longer exterior waveforms. A saved surface
history can be reused in `reconstruct_fields(surface, point, times=None)`
for another exterior point without another FDTD simulation. The hyphenated
filename is a runnable script; use importlib to load it as in the tests.

Run the independent analytic dipole and small FDTD checks with
`python -B -m unittest discover -s src/tests -p 'test_near_to_far_field.py' -v`.
Tests cover area weights, angular/time refinement, nonunit backgrounds,
causality, missing history, material containment and a direct FDTD probe.
