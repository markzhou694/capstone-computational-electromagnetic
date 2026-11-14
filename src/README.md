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
