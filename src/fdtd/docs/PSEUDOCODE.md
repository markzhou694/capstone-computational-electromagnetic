# Pseudocode: reusable 3D Yee FDTD

For exact input/output formats, see [API.md](API.md). For component equations,
see [MATHEMATICS.md](MATHEMATICS.md).

## Solve

```text
INPUT box bounds [m], cell counts, final time T [s], CFL fraction
INPUT prescribed current J(x,y,z,t), or no current
INPUT constant epsilon [F/m] and mu [H/m] (default: vacuum)
INPUT optional observation callback and recording stride

VALIDATE parameters
BUILD node coordinates, cell-center coordinates, and dx,dy,dz
BUILD the three sparse coordinate grids for Ex, Ey, Ez
ALLOCATE zero E on edges, zero H on faces, zero rho at interior nodes

COMPUTE wave_speed = 1 / sqrt(epsilon * mu)
COMPUTE dt_limit = 1 / (wave_speed * sqrt(1/dx^2 + 1/dy^2 + 1/dz^2))
SET steps = ceil(T / (CFL * dt_limit)), dt = T / steps
CALL observation callback at time zero, if supplied

FOR n = 0, ..., steps - 1:
    # E is at n*dt; internal H is at (n-1/2)*dt.
    UPDATE all three H components:
        H = H - dt/mu * curl_e(E)

    FOR each of the three E grids:
        EVALUATE J(x,y,z,(n+1/2)*dt) on that grid (or use zero)
        SELECT the corresponding J component
        BROADCAST to the grid shape and check real, finite values

    UPDATE all three E components:
        E = E + dt/epsilon * (curl_h(H) - J)
    APPLY PEC: set tangential E to zero on every wall
        x walls: Ey=Ez=0; y walls: Ex=Ez=0; z walls: Ex=Ey=0
    UPDATE rho = rho - dt * divergence_e(J) at interior nodes

    IF callback supplied AND (recording step OR final step):
        COMPUTE H_output = H - dt/(2*mu) * curl_e(E)
        CALL callback((n+1)*dt, E, centers, H_output)
        # E and H_output refer to the same time; internal H is unchanged.

COMPUTE final H_output with the same half-step alignment
RETURN E, H_output, rho, grid metadata, time-step data, epsilon, mu
```

The solver does not retain a full field history, plot, or write files.
A callback must copy any data it retains and must not mutate solver inputs.

## Sample a frame

```text
INPUT time [s], selected field (E or H), cell-center coordinates
IF E: average the four parallel edges of each cell for each component
IF H: average the two opposite faces of each cell for each component
COMPUTE magnitude = sqrt(Fx_center^2 + Fy_center^2 + Fz_center^2)
COPY xy, xz, yz magnitude slices through the middle cell layer
COPY sparse vectors with stride max(1, N//8) on each axis
RETURN a frame dict: time, kind, maximum, vectors, planes
```

## Export plots

```text
INPUT solver result, chronological frame list, directory, fps, E/H selection
CHECK nonempty frames, matching field kind, positive fps, and time order
FIND one fixed color/arrow scale over all frames
CREATE a view dict with a figure and plotting artists
CREATE a temporary rendering directory
DRAW each frame using draw_frame(frame, view) and save a GIF
DRAW the last frame with the same scale and save a PNG
AFTER both files finish rendering, replace the two named output files
CLOSE the figure and remove the temporary directory
RETURN a dict of PNG and GIF paths
```

The two final file replacements are separate operations. Rendering errors
preserve previous output files. Plots show the selected E or H from the full
3D calculation; slices do not reduce the solver to a two-dimensional model.
