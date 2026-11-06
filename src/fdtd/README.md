# 3D Yee FDTD

A small function-based solver for a prescribed current in a uniform medium,
with zero initial fields and six reflecting PEC walls.

- **[Function API and calling guide](docs/API.md)**: inputs, outputs, array shapes,
  units, side effects, and runnable examples for people and AI assistants.
- [Mathematics](docs/MATHEMATICS.md): discretization and boundary conditions.
- [Pseudocode](docs/PSEUDOCODE.md): execution order.

## Files

| File | Responsibility |
| --- | --- |
| [src/yee_solver.py](src/yee_solver.py) | Reusable solver; takes all problem settings as arguments; NumPy only |
| [src/plot_fields.py](src/plot_fields.py) | Sample E/H, draw frames, save PNG/GIF |
| [src/fdtd_3d.py](src/fdtd_3d.py) | Editable wire/pulse example and run entry point |
| [src/tests](src/tests) | Numerical and calling-contract checks |

The core workflow is `solve(...) -> result`. Add an `on_frame` callback using
`sample_fields(...)` and then call `save_results(...)` when plots are wanted.
Importing any module does not run a simulation or write result files.

## Run the example

Use a Python environment with NumPy, Matplotlib, and Pillow. From this directory:

```bash
python src/fdtd_3d.py
```

The current example uses a 40 x 40 x 40 grid on [-1,1] metres in each direction,
ends at 12 ns, and plots H. It enables a 100 A Gaussian wire along z, smoothly
turned on over 1 ns. The Gaussian pulse is disabled (`J_AMPLITUDE=0`).
These values describe the editable example; they are not solver requirements.

Each successful example run replaces `outputs/fdtd_3d_current.png` and
`outputs/fdtd_3d_current.gif`. Both show the selected `PLOT_FIELD` and use the
same color/arrow scale. Rendering finishes before either existing file is
replaced. The solver by itself never writes files.

## Example parameters

| Parameter | Meaning |
| --- | --- |
| `X_RANGE`, `Y_RANGE`, `Z_RANGE` | Absolute box bounds [m] |
| `NX`, `NY`, `NZ` | Cell counts |
| `T_END_NS`, `CFL` | Final time [ns] and stability fraction |
| `PLOT_FIELD` | `"E"` or `"H"` |
| `FRAME_EVERY`, `GIF_FPS` | Recording stride and playback speed |
| `USE_CUSTOM_CURRENT` | `True`: use only `custom_current`; `False`: use pulse + wire |
| `DC_CURRENT_A`, `DC_WIRE_XY` | Wire current coefficient [A] and axis position [m] |
| `DC_WIRE_WIDTH`, `DC_RAMP_NS` | Wire Gaussian width [m] and turn-on duration [ns] |
| `J_AMPLITUDE` | Pulse current-density coefficient [A/m²]; 0 disables it |
| `SOURCE_CENTER`, `SOURCE_WIDTH` | Pulse center and Gaussian standard deviation [m] |
| `SOURCE_RADIUS` | Pulse cutoff radius [m]; `None` means no hard cutoff |
| `FREQUENCY_GHZ` | Frequency parameter in `sin(phase)*cos(phase)` [GHz] |
| `PEAK_TIME_NS`, `PULSE_WIDTH_NS` | Gaussian time-envelope center and width parameter [ns] |

The example functions receive coordinates in metres and time in seconds.
They return current densities in A/m². Box bounds and source position are
independent. The wire's continuous Gaussian normalization is over the infinite
xy plane; truncation and grid sampling can change the represented total current.
If the pulse is enabled, `sin(phase)*cos(phase)=sin(2*phase)/2`: its oscillation
frequency is twice `FREQUENCY_GHZ`. Resolve the full source bandwidth and
spatial profile; CFL stability is not an accuracy check.

## Build your own current

In `src/fdtd_3d.py`, set `USE_CUSTOM_CURRENT = True` and edit only
`custom_current(x,y,z,t)`. Its equation is written directly in the docstring:

```text
J = amplitude * spatial_shape * time_waveform * (direction / |direction|)
```

The supplied DIY example is confined to a sphere and lasts for one finite
pulse. Change its local amplitude [A/m²], center [m], radius [m], duration [ns],
and direction weights. Direction is normalized automatically: `(1,1,0)` and
`(10,10,0)` give the same current. Supply three finite numbers and a nonzero
vector; use `amplitude=0` to disable the source. Change `spatial` or `waveform` to try other shapes,
or write separate formulas for Jx, Jy, Jz. Use NumPy functions for array
coordinates; ordinary `if` is suitable for the scalar time. Return all three
components. The solver handles their grid sampling and charge update.

The default remains the original wire/pulse combination. The source functions
now include their mathematical expressions, units, and support conditions.

## Supported scope

The solver accepts arbitrary rectangular boxes, unequal axis cell counts, any
prescribed three-component current, and constant scalar epsilon/mu. Defaults
are vacuum. It uses zero initial E/H/rho and PEC reflecting walls. It does not
implement nonzero initial fields, PML, nonuniform meshes, material maps, loss,
or exterior reconstruction. All calculations remain fully three-dimensional;
the three slices are only display views.

## Checks

```bash
python -m unittest discover -s src/tests -p 'test_*.py' -v
```

Checks include manufactured-solution convergence, charge continuity, PEC walls,
source locations, medium scaling, callback timing, and plotting formats.
