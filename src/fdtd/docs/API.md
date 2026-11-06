# Function API and calling guide

This is the calling contract for people and AI assistants using this project.
The reusable solver is `src/yee_solver.py`; `src/fdtd_3d.py` is one example.
The solver never imports example settings, plots, or writes files.

## Supported problem

Solve the time-domain Maxwell equations in a rectangular box:

```text
epsilon * dE/dt = curl(H) - J
mu      * dH/dt = -curl(E)
drho/dt         = -div(J)
```

- Arbitrary box position, side lengths, and cell counts in x, y, z.
- Constant spacing along each axis; dx, dy, dz may differ.
- Any prescribed real three-component current J(x,y,z,t).
- Constant, positive scalar epsilon [F/m] and mu [H/m]; defaults are vacuum.
- Zero initial E, H, and interior charge; six reflecting PEC walls.

“Reusable” applies within this model. Spatially varying or anisotropic media,
conductivity, nonzero initial fields, periodic/open boundaries, and PML are not
implemented. Do not pass arrays for epsilon or mu. Stable time stepping alone
does not establish accuracy: resolve the source and check grid refinement.

## 1. Main solver

```python
solve(
    bounds,
    cells,
    end_time,
    cfl=0.8,
    current_density=None,
    on_frame=None,
    frame_every=1,
    *,
    epsilon=EPSILON0,
    mu=MU0,
)
```

### Inputs

| Name | Required format | Meaning |
| --- | --- | --- |
| `bounds` | Sequence or float array, shape `(3, 2)` | `((xmin,xmax),(ymin,ymax),(zmin,zmax))` in metres; each finite min < max |
| `cells` | Three integers, each >= 2 | `(Nx,Ny,Nz)` cell counts, not node counts |
| `end_time` | Positive finite scalar | Final time in **seconds**, e.g. `3e-9` for 3 ns |
| `cfl` | Scalar in `(0,1]` | Requested fraction of the CFL time-step limit |
| `current_density` | Callable or `None` | Source contract below; `None` gives zero current |
| `on_frame` | Callable or `None` | Optional observation callback; no plotting is required |
| `frame_every` | Positive integer | Callback stride, independent of the physics time step |
| `epsilon` | Positive finite scalar | Uniform permittivity [F/m], keyword-only |
| `mu` | Positive finite scalar | Uniform permeability [H/m], keyword-only |

Time stepping uses

```text
wave_speed = 1 / sqrt(epsilon * mu)
dt_limit   = 1 / (wave_speed * sqrt(1/dx^2 + 1/dy^2 + 1/dz^2))
steps      = ceil(end_time / (cfl * dt_limit))
dt         = end_time / steps
```

### Current function format

```python
def current_density(x, y, z, t):
    # x,y,z: sparse broadcastable NumPy arrays [m]
    # t: scalar time [s]
    Jx = ...  # real scalar or broadcastable NumPy array [A/m^2]
    Jy = ...
    Jz = ...
    return Jx, Jy, Jz
```

Use NumPy operations (`np.exp`, `np.sin`, `np.where`) on coordinates. A Python
`if` on an array is not a pointwise condition. The solver calls this function
three times per time step at `t=(n+0.5)*dt`, using these sparse grid shapes:

| Call | x shape | y shape | z shape | Component used |
| --- | --- | --- | --- | --- |
| Ex grid | `(Nx,1,1)` | `(1,Ny+1,1)` | `(1,1,Nz+1)` | `Jx` |
| Ey grid | `(Nx+1,1,1)` | `(1,Ny,1)` | `(1,1,Nz+1)` | `Jy` |
| Ez grid | `(Nx+1,1,1)` | `(1,Ny+1,1)` | `(1,1,Nz)` | `Jz` |

Return all three components on every call. Each selected component must be
finite, real, and broadcastable to that call's full grid. For example, a
constant current component may be returned as `0.1`. Avoid side effects or
random draws inside this function: the three calls refer to the same time.
A tuple or list of three components is preferred; a length-three NumPy array
is also accepted when its entries have suitable shapes.

### Output format

The return value is a Python dictionary containing NumPy arrays, **not JSON**:

```text
{
    "electric": (Ex, Ey, Ez),       # [V/m], all at end_time
    "magnetic": (Hx, Hy, Hz),       # [A/m], all at end_time
    "charge": rho,                 # [C/m^3], interior nodes only
    "bounds": array shape (3,2),    # [m]
    "cells": (Nx, Ny, Nz),
    "nodes": (x, y, z),             # 1D arrays [m], lengths Nx+1,Ny+1,Nz+1
    "centers": (xc, yc, zc),        # 1D arrays [m], lengths Nx,Ny,Nz
    "spacing": array([dx,dy,dz]),   # [m]
    "time": end_time,              # [s]
    "dt": time_step,               # [s]
    "steps": number_of_steps,      # integer
    "cfl": dt / dt_limit,          # actual fraction, <= requested cfl
    "epsilon": permittivity,       # [F/m]
    "mu": permeability,            # [H/m]
}
```

All array axes are ordered `(x,y,z)`, with zero-based indexing.

| Array | Shape | Coordinate location |
| --- | --- | --- |
| `Ex` | `(Nx,Ny+1,Nz+1)` | `(xc[i],y[j],z[k])` |
| `Ey` | `(Nx+1,Ny,Nz+1)` | `(x[i],yc[j],z[k])` |
| `Ez` | `(Nx+1,Ny+1,Nz)` | `(x[i],y[j],zc[k])` |
| `Hx` | `(Nx+1,Ny,Nz)` | `(x[i],yc[j],zc[k])` |
| `Hy` | `(Nx,Ny+1,Nz)` | `(xc[i],y[j],zc[k])` |
| `Hz` | `(Nx,Ny,Nz+1)` | `(xc[i],yc[j],z[k])` |
| `rho` | `(Nx-1,Ny-1,Nz-1)` | `(x[i+1],y[j+1],z[k+1])` |

The six field arrays do **not** have one common shape. Use `cell_center_fields`
for display on a common `(Nx,Ny,Nz)` grid. Charge is diagnostic; metal-wall
surface charge is not stored. It satisfies `epsilon * divergence_e(E) = rho`
at interior nodes to floating-point roundoff for resolved finite calculations.

### Observation callback

```python
def on_frame(time, electric, centers, magnetic):
    # time: scalar [s]
    # electric: (Ex,Ey,Ez), as in the table above
    # centers: (xc,yc,zc), 1D arrays [m]
    # magnetic: (Hx,Hy,Hz), aligned to the same time as electric
    # Return None. Copy arrays you want to retain; do not modify inputs.
    ...
```

Calls occur at time zero, every `frame_every` steps, and the final step (once).
The solver's internal H is staggered by half a step. Output H is aligned by
`H_out = H - dt/(2*mu)*curl(E)`. This operation never modifies internal H.
Changing the callback or its stride does not change the solution, provided
that the callback respects the no-mutation contract. Exceptions propagate.

### Minimal complete example

Run this Python code from the `capstone_code` directory. It requires NumPy.

```python
import sys
import numpy as np
sys.path.insert(0, "src")
from yee_solver import solve, EPSILON0, MU0


def source(x, y, z, t):
    spatial = np.exp(-(x**2 + y**2 + z**2) / 0.1)
    pulse = 0.01 * spatial * np.sin(2 * np.pi * 0.3e9 * t)
    return pulse, -0.3 * pulse, 0.7 * pulse


result = solve(
    bounds=((-1, 1), (-0.8, 0.8), (-0.6, 0.6)),
    cells=(12, 14, 16),
    end_time=1e-9,
    current_density=source,
    epsilon=2 * EPSILON0,
    mu=MU0,
)
Ex, Ey, Ez = result["electric"]
Hx, Hy, Hz = result["magnetic"]
rho = result["charge"]
print(Ex.shape, Hx.shape, rho.shape)
# (12, 15, 17) (13, 14, 16) (11, 13, 15)
```

## 2. Sampling and plotting

The normal workflow uses just two functions:

```python
frame = sample_fields(time, field, centers, kind="E")
paths = save_results(result, frames, output_dir, fps=12, kind="E")
```

### `sample_fields`

Purpose: average staggered data to cell centers, then copy sparse vectors and
three magnitude slices. Inputs use the solver's SI units and Yee shapes.
`kind="E"` selects edge averaging; `kind="H"` selects face averaging.

Output frame dictionary:

| Key | Format |
| --- | --- |
| `time` | Float [s], supplied by the caller |
| `kind` | `"E"` or `"H"` |
| `maximum` | Maximum norm of the cell-centered vector field |
| `vectors` | Tuple `(Fx_sample,Fy_sample,Fz_sample)`; each shape `(Sx,Sy,Sz)` |
| `planes` | Tuple `(xy,xz,yz)` magnitude arrays with shapes `(Nx,Ny)`, `(Nx,Nz)`, `(Ny,Nz)` |

For each axis, `stride=max(1,N//8)` and `S=len(range(0,N,stride))`.
Slices use the fixed indices `Nz//2`, `Ny//2`, `Nx//2`, respectively.
All magnitude and vector values are in V/m for E or A/m for H.
Returned arrays are copies, so retaining frames is safe. Colors represent
the norm of the averaged vector, not the average of the original norms.

### `save_results`

Inputs:

- `result`: solver result supplying grid metadata.
- `frames`: nonempty chronological list from `sample_fields`, all from that
  same grid and using the same `kind`.
- `output_dir`: string or `pathlib.Path`.
- `fps`: positive finite playback rate; `kind`: `"E"` or `"H"`.

Output: `{"png": Path(...), "gif": Path(...)}`. Files are named
`fdtd_3d_current.png` and `fdtd_3d_current.gif`. PNG shows the last supplied
frame; GIF contains the supplied sequence. Both use one shared scale.

This function creates the output directory and replaces these named files.
It finishes rendering both files in a temporary directory before replacing
them. Rendering failure preserves existing outputs. The final two replacements
are separate filesystem operations, not an atomic pair. Matplotlib and Pillow
are required. No other result files are written.

### Complete example with animation

Run from `capstone_code`. This writes to `outputs/api_example/`.

```python
import sys
import numpy as np
sys.path.insert(0, "src")
from yee_solver import solve
from plot_fields import sample_fields, save_results

frames = []


def source(x, y, z, t):
    Jz = 0.01 * np.exp(-(x**2 + y**2 + z**2) / 0.1) * np.sin(1e9 * t)
    return 0.0, 0.0, Jz


def record(time, electric, centers, magnetic):
    frames.append(sample_fields(time, magnetic, centers, kind="H"))


result = solve(
    bounds=((-1, 1), (-1, 1), (-1, 1)),
    cells=(8, 10, 12),
    end_time=1e-9,
    current_density=source,
    on_frame=record,
    frame_every=2,
)
paths = save_results(result, frames, "outputs/api_example", kind="H")
print(paths["png"], paths["gif"])
```

## 3. Supporting function descriptions

These functions are useful for inspection and custom workflows. Normal callers
can use `solve`, `sample_fields`, and `save_results` alone. Every function also
has a local docstring describing its inputs, outputs, and side effects.

| Function | What it does | Input format | Output format / mutation |
| --- | --- | --- | --- |
| `curl_e(electric, spacing)` | Edge-to-face discrete curl | E tuple; `(dx,dy,dz)` | H-shaped tuple, E units per metre; no mutation |
| `curl_h(magnetic, spacing)` | Face-to-edge discrete curl | H tuple; `(dx,dy,dz)` | E-shaped tuple, H units per metre; tangential boundary placeholders are zero |
| `divergence_e(fields, spacing)` | Discrete divergence at interior nodes | E-shaped tuple, e.g. E or J; spacing | Array `(Nx-1,Ny-1,Nz-1)`, field units per metre |
| `sample_current(source, coordinates, time)` | Sample J at three edge grids | Source callable/None; three `(x,y,z)` sparse grids; time [s] | Three E-shaped real arrays [A/m²], treated as read-only |
| `apply_pec(electric)` | Zero wall-tangential E | Writable E tuple | `None`; mutates E in place |
| `magnetic_at_e_time(E, H, spacing, dt, mu=MU0)` | Align output H with E | E at t, H at t-dt/2; spacing [m], dt [s], mu [H/m] | New H tuple at t; no mutation |
| `cell_center_fields(field, kind="E")` | Spatial averaging for display | Yee field tuple, kind | Three new `(Nx,Ny,Nz)` arrays in original field units |
| `field_view(result, maximum, kind="E")` | Create plotting panels | Solver result; nonnegative finite field scale; kind | View dictionary; caller must close its `figure` |
| `draw_frame(frame, view)` | Draw/update one frame | Frame from `sample_fields`; view from `field_view`, same grid/kind | `None`; updates view artists |

The `view` dictionary contains `figure`, `vector_ax`, `positions`, `arrow_scale`,
`maximum`, `arrows`, `images`, `title`, and `kind`. `positions` holds the three
sparse-vector coordinate grids; `images` holds three slice artists. Example:

```python
from plot_fields import field_view, draw_frame
import matplotlib.pyplot as plt

frame = frames[-1]
view = field_view(result, frame["maximum"], kind=frame["kind"])
try:
    draw_frame(frame, view)
    view["figure"].savefig("outputs/api_example/custom.png")
finally:
    plt.close(view["figure"])
```

The example module has five top-level functions:

| Function | Inputs | Output / behavior |
| --- | --- | --- |
| `current_density(x,y,z,t)` | Scalar/broadcastable xyz [m], scalar t [s] | `(Jx,Jy,Jz)` [A/m²]; DIY if `USE_CUSTOM_CURRENT=True`, otherwise `(0,0,pulse+wire)` |
| `custom_current(x,y,z,t)` | Same | DIY `(Jx,Jy,Jz)` [A/m²]; local shape, waveform, amplitude and direction settings |
| `pulse_current(x,y,z,t)` | Same | Scalar/array Jz with broadcast xyz shape |
| `dc_wire_current(x,y,t)` | Scalar/broadcastable xy [m], scalar t [s] | Scalar/array Jz with broadcast xy shape, or `0.0` if disabled |
| `main(output_dir=None)` | Optional string/Path; default project outputs | `(result,paths)`; runs example, writes PNG/GIF, prints summary |

For DIY sources, set `USE_CUSTOM_CURRENT=True` and edit `custom_current`.
The supplied expression is `J0 * max(1-r²/R²,0)² * sin²(pi*t/T) * unit_direction`
for `0<t<T`, zero otherwise. The current is confined to a sphere of radius R;
J0 is in A/m², R in metres, and T is the local `duration_ns` converted to seconds.
The function normalizes `direction` to unit length, so its scale does not
change the peak magnitude `abs(J0)`. A zero vector, wrong component count,
or non-finite component raises `ValueError`; use `J0=0` to disable the source.
Each source function in `fdtd_3d.py` contains its exact equation and parameter
definitions. A spatially varying current can accumulate charge; the solver
already evolves that charge through the discrete continuity equation.

## 4. Validation and compatibility

Run `python -m unittest discover -s src/tests -p 'test_*.py' -v` using an
environment with NumPy, Matplotlib, and Pillow.

The original first seven positional arguments of `solve` are retained. The
additional medium arguments are keyword-only. Result metadata now also includes
`cells`, `nodes`, `epsilon`, and `mu`. Existing E/H shapes are unchanged.

The callback now receives H aligned to its stated time, matching returned H.
Earlier code passed half-step-lagged H to the callback. `field_view` now returns
a view dictionary; call `draw_frame(frame, view)` instead of an enclosed drawing
function. New sampled frames include `kind`, which plotting checks explicitly.
`save_results` now returns output paths instead of `None`.
