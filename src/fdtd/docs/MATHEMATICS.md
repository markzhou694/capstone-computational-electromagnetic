# Mathematics of the 3D Yee FDTD solver

This document describes the implemented equations in [yee_solver.py](../src/yee_solver.py),
not a future PML or boundary-integral method. See [PSEUDOCODE.md](PSEUDOCODE.md)
for the execution order and [README.md](../README.md) for parameter editing.

## 1. Physical problem and units

The rectangular computational domain is

$$
\Omega=[x_{\min},x_{\max}]\times[y_{\min},y_{\max}]\times[z_{\min},z_{\max}].
$$

The default medium is vacuum. The code defines

$$
c_0=299792458\ \mathrm{m/s},\qquad
\mu_0=4\pi\times10^{-7}\ \mathrm{H/m},\qquad
\epsilon_0=\frac{1}{\mu_0c_0^2}.
$$

The value of permeability above is the conventional numerical value used by
this implementation. The solver also accepts constant positive scalar
permittivity epsilon and permeability mu; vacuum is the default. Maxwell's
evolution equations are

$$
\boxed{\epsilon\frac{\partial\mathbf E}{\partial t}
=\nabla\times\mathbf H-\mathbf J},\qquad
\boxed{\mu\frac{\partial\mathbf H}{\partial t}
=-\nabla\times\mathbf E}.
$$

Here E is in V/m, H in A/m, prescribed J in A/m², and time in seconds.
The initial physical fields and interior charge are zero. The constraints are

$$
\nabla\cdot(\epsilon\mathbf E)=\rho,\qquad
\nabla\cdot(\mu\mathbf H)=0,\qquad
\frac{\partial\rho}{\partial t}=-\nabla\cdot\mathbf J.
$$

A general prescribed current need not be divergence-free: it can build charge.

## 2. Coordinates and Yee staggering

For Nx, Ny, Nz cells, define

$$
\Delta x=\frac{x_{\max}-x_{\min}}{N_x},\quad
x_i=x_{\min}+i\Delta x,\quad
x_{i+1/2}=x_{\min}+(i+1/2)\Delta x,
$$

and similarly for y and z. Indices start at zero. A node coordinate has
N+1 entries, while a half-index coordinate has N entries.

| Array | Physical location | NumPy shape | Time during the loop |
| --- | --- | --- | --- |
| Ex | (x[i+1/2], y[j], z[k]) | (Nx, Ny+1, Nz+1) | n dt |
| Ey | (x[i], y[j+1/2], z[k]) | (Nx+1, Ny, Nz+1) | n dt |
| Ez | (x[i], y[j], z[k+1/2]) | (Nx+1, Ny+1, Nz) | n dt |
| Hx | (x[i], y[j+1/2], z[k+1/2]) | (Nx+1, Ny, Nz) | (n−1/2) dt before update |
| Hy | (x[i+1/2], y[j], z[k+1/2]) | (Nx, Ny+1, Nz) | (n−1/2) dt before update |
| Hz | (x[i+1/2], y[j+1/2], z[k]) | (Nx, Ny, Nz+1) | (n−1/2) dt before update |
| rho | Interior nodes (x[i+1], y[j+1], z[k+1]) | (Nx−1, Ny−1, Nz−1) | n dt |

Array axes are ordered (x,y,z). The complete calling formats are in [API.md](API.md).

Each current component is evaluated at the location of the corresponding E
component. Thus Jx, Jy and Jz use different coordinate arrays. This is why the
solver calls `current_density` separately for each component.

## 3. Time step and stability

Let T be the solver argument `end_time` in seconds and S be `cfl`, with
0 < S <= 1. The example converts `T_END_NS * 1e-9` before calling the solver.
For the chosen medium, c = 1/sqrt(epsilon*mu). The solver computes

$$
\Delta t_{\max}=\frac{1}{c\sqrt{\Delta x^{-2}+\Delta y^{-2}+\Delta z^{-2}}},
\qquad N_t=\left\lceil\frac{T}{S\Delta t_{\max}}\right\rceil,
\qquad \Delta t=\frac{T}{N_t}.
$$

This reaches T exactly and ensures dt <= S dt_max. CFL stability does not
ensure spatial or temporal resolution of a particular source frequency.

## 4. The six component updates

Let Dq denote the centered difference between the two adjacent staggered
samples surrounding the target location, divided by the grid spacing in q.
For example, at the Hx location,

$$
(D_y E_z)_{i,j+1/2,k+1/2}
=\frac{E_{z,i,j+1,k+1/2}-E_{z,i,j,k+1/2}}{\Delta y}.
$$

At the Ex location,

$$
(D_y H_z)_{i+1/2,j,k}
=\frac{H_{z,i+1/2,j+1/2,k}-H_{z,i+1/2,j-1/2,k}}{\Delta y}.
$$

For each n = 0, ..., Nt−1, first update all magnetic components:

$$
\begin{aligned}
H_x^{n+1/2}&=H_x^{n-1/2}-\frac{\Delta t}{\mu}(D_yE_z^n-D_zE_y^n),\\
H_y^{n+1/2}&=H_y^{n-1/2}-\frac{\Delta t}{\mu}(D_zE_x^n-D_xE_z^n),\\
H_z^{n+1/2}&=H_z^{n-1/2}-\frac{\Delta t}{\mu}(D_xE_y^n-D_yE_x^n).
\end{aligned}
$$

Evaluate J at t = (n+1/2) dt. Then update the electric components:

$$
\begin{aligned}
E_x^{n+1}&=E_x^n+\frac{\Delta t}{\epsilon}
(D_yH_z^{n+1/2}-D_zH_y^{n+1/2}-J_x^{n+1/2}),\\
E_y^{n+1}&=E_y^n+\frac{\Delta t}{\epsilon}
(D_zH_x^{n+1/2}-D_xH_z^{n+1/2}-J_y^{n+1/2}),\\
E_z^{n+1}&=E_z^n+\frac{\Delta t}{\epsilon}
(D_xH_y^{n+1/2}-D_yH_x^{n+1/2}-J_z^{n+1/2}).
\end{aligned}
$$

All spatial positions are as in the table. `curl_e` produces differences on
H faces; `curl_h` produces differences on E edges. Tangential boundary E
entries are overwritten by the PEC condition below.

The implementation initializes E^0 = 0 and H^(−1/2) = 0. For the zero initial
E/H data, the first-order backward half-step correction to H is zero because
curl(E^0) = 0. This initialization must be reconsidered if nonzero initial
fields are later introduced.

## 5. PEC walls and interior charge

On each wall, the tangential electric field vanishes:

$$
\mathbf n\times\mathbf E=0.
$$

Consequently, set Ey=Ez=0 at the two x walls, Ex=Ez=0 at the two y walls,
and Ex=Ey=0 at the two z walls after every E update. Normal E is not forced
to zero. These are reflecting walls, not absorbing or open boundaries.

At interior nodes, update

$$
\rho^{n+1}=\rho^n-\Delta t
(D_xJ_x^{n+1/2}+D_yJ_y^{n+1/2}+D_zJ_z^{n+1/2}).
$$

For example,

$$
(D_xJ_x)_{i,j,k}=\frac{J_{x,i+1/2,j,k}-J_{x,i-1/2,j,k}}{\Delta x}.
$$

The compatible discrete identity div_h(curl_h H)=0 preserves
`epsilon * divergence_e(E) = rho` at interior nodes up to roundoff, given
consistent initial data. Charge is a diagnostic here; it does not feed a
separate Poisson solve. Metal-wall surface charge is not stored separately.

## 6. Example source; independent of the reusable solver

The solver accepts any real prescribed vector current through the callable
`current_density(x,y,z,t)`. The example in `fdtd_3d.py` uses

$$
J_x=J_y=0,\qquad J_z=J_{\mathrm{pulse}}+J_{\mathrm{wire}}.
$$

With r0=`SOURCE_CENTER`, sigma=`SOURCE_WIDTH`, J0=`J_AMPLITUDE`,
f=`FREQUENCY_GHZ * 1e9`, tc=`PEAK_TIME_NS * 1e-9`, and
w=`PULSE_WIDTH_NS * 1e-9`, the pulse is

$$
J_{\mathrm{pulse}}(\mathbf r,t)=J_0
\exp\!\left(-\frac{\lVert\mathbf r-\mathbf r_0\rVert^2}{2\sigma^2}\right)
\exp\!\left(-\frac{(t-t_c)^2}{w^2}\right)
\sin(2\pi ft)\cos(2\pi ft)\,\mathbf{1}_D(\mathbf r).
$$

For `SOURCE_RADIUS=None`, D is the full box. For a positive radius R,
D is the intersection of the box and the ball of radius R centered at r0.
The spatial Gaussian width controls decay; the radius controls the cutoff.
The time Gaussian has no hard cutoff, and w is not its standard deviation.

With I=`DC_CURRENT_A`, a=`DC_WIRE_WIDTH`, (xw,yw)=`DC_WIRE_XY`, and
tau=`DC_RAMP_NS * 1e-9`, the wire current is independent of z:

$$
J_{\mathrm{wire}}(x,y,t)=\frac{I}{2\pi a^2}
\exp\!\left(-\frac{(x-x_w)^2+(y-y_w)^2}{2a^2}\right)R(t).
$$

For tau > 0 and t >= 0,

$$
R(t)=\begin{cases}
\sin^2(\pi t/(2\tau)), & 0\le t<\tau,\\
1, & t\ge\tau.
\end{cases}
$$

For tau <= 0, the code uses R=1 immediately. The continuous profile integrates
to I over the infinite xy plane after turn-on. Finite box truncation and grid
sampling change that integral. Its interior divergence is zero because only
Jz is nonzero and it is independent of z; wall surface charge is not stored.

The saved example currently has I=100 A and J0=0, so only the wire is active.
Source settings are independent of the box and of the general solver API.

## 7. Resolution checks

For an active oscillation frequency nu and wave speed c, compare

$$
\lambda=\frac{c}{\nu},\qquad
N_{\lambda,q}=\frac{\lambda}{\Delta q},\qquad
f_{\mathrm{Nyquist}}=\frac{1}{2\Delta t}.
$$

The example's pulse uses sin(2*pi*f*t)*cos(2*pi*f*t), equal to
sin(4*pi*f*t)/2. Thus its oscillation frequency is 2f. If enabled with the
saved f=0.5 GHz in vacuum, that oscillation has wavelength about 0.30 m,
or about six cells on the saved 0.05 m grid. The envelope adds bandwidth.
The saved wire width is 0.04 m, or 0.8 cells, so its spatial profile also
needs a refinement check. The pulse is currently disabled.

For the saved 12 ns duration and CFL=0.8, the vacuum 40^3 grid uses 156 steps,
dt approximately 0.0769231 ns. These are example values, not fixed solver
settings. Recalculate resolution for the requested medium and source.
Reducing dt alone does not repair insufficient spatial resolution.

## 8. Output times, pictures and energy

The final H stored by the loop is at T−dt/2. The returned H is time-aligned
with the final E using a half-step extrapolation, equivalently the average
of the neighboring leapfrog H values:

$$
\mathbf H_{\mathrm{out}}^N=\mathbf H^{N-1/2}
-\frac{\Delta t}{2\mu}\operatorname{curl}_h\mathbf E^N.
$$

The same alignment is used at every observation callback, so both callback
fields refer to the stated time. It does not modify the internal staggered H.

For display only, each E component is averaged from its four parallel edges
to the cell center. For example,

$$
\overline E_x{}_{i+1/2,j+1/2,k+1/2}
=\frac14\sum_{a=0}^{1}\sum_{b=0}^{1}E_{x,i+1/2,j+a,k+b}.
$$

For H, average the two opposite faces for each component instead.
Colors show the norm of the averaged vector, not the average of the original norms.
The three slices are from the same full 3D simulation. GIF frames share one
color scale and one arrow scale; the final PNG uses those same scales.
FRAME_EVERY selects stored frames and GIF_FPS changes playback, not dt.

For these PEC walls, the continuum energy balance is

$$
U=\frac12\int_\Omega(\epsilon|\mathbf E|^2+\mu|\mathbf H|^2)\,dV,
\qquad \frac{dU}{dt}=-\int_\Omega\mathbf J\cdot\mathbf E\,dV.
$$

A prescribed current can supply or remove energy. The active code does not
plot an energy-conservation curve, and it implements no PML, material objects,
or exterior field reconstruction. Uniform epsilon and mu are supported;
spatial material maps are not.
