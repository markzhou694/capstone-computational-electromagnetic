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
```

Run `python src/fdtd/fdtd_3d.py` from the repository root with NumPy,
Matplotlib and Pillow installed. Outputs go to root `outputs/` (ignored).
Calling formats and mathematical expressions are in the Python docstrings.
Xiaodi requested this three-file layout; duplicated FDTD documentation and
tests were removed from this subtree. Their prior versions remain in Git
history and in a local backup outside the repository. The original sibling
`capstone_code/` is separate and does not automatically synchronize here.
