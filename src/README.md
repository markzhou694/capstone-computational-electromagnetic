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
