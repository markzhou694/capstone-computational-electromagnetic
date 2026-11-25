# Shared project status

Last reviewed: **2026-11-25**. Humans: **Xiaodi Zhou and Guanlin Wang**.

## Near-to-far-field publication — 2026-11-25

Owner: Xiaodi; actor: Codex. This change set adds the direct retarded
latitude/longitude surface integrator, its exterior plotting function,
eight numerical tests and run instructions. It records E/H histories from
the existing Yee solver and reconstructs an exterior point without FFT
or an unknown-current solve. Source/settings remain in fdtd_3d.py.

Publication scope: src/fdtd/near-to-far-field.py, the save_exterior_fields
addition in src/fdtd/plot_fields.py, src/tests/test_near_to_far_field.py,
the relevant src/README.md section, and project status/timeline records.
Other local spectrum, analysis, viewer and parameter edits are excluded.
Generated PNG/NPZ outputs stay local. The current script observer is
(2,5,10); the recorded November 24 production validation used (2,0,0).
The published fdtd_3d settings stay at the existing repository values;
the local 50^3/CFL=.9 edits are preserved without publication.

The integrator requires a homogeneous exterior and sufficient time history.
The November 24 analytic convergence and 150^3 validation are recorded in
TIMELINE.md. All eight numerical tests passed again on the isolated, exact
publication tree on November 25. Geometry/material preflight also passed
with the existing repository defaults. This is not a new full-size run.

## Bunny field overlays — 2026-11-20

E/H exports now show a translucent bunny in 3D and gold mesh cross-section
outlines on slices through its bounding-box center. Bunny views focus on the
physical domain. These are continuous mesh overlays; Yee material remains
staircase sampled. Verified a 40^3, 40-step run and E/H PNG/GIF exports in a
temporary directory; rerun the bunny entry point to refresh full-size outputs.

## Optional dielectric bunny — 2026-11-20

fdtd_3d_complex_geometric.py reuses shared grid/PML/source settings and the
unchanged solver, replacing the medium with a closed bunny (epsilon=4) in
background epsilon=mu=1. Native E-grid inside/outside masks; no smoothing.
One-cell clearance and external-source placement checks are enforced.
plot_fields.py exports a mesh/source preview; E/H outputs use a separate bunny
folder. Dependencies trimesh 5.2.1 and rtree 1.4.1 installed in sci.
Verified box classification, 40^3 eight-step E/H run and four image exports,
PML placement rejection, and four existing material tests. Not a convergence
study; full configured 90^3 simulation has not been run.

## Both E and H visualization — 2026-11-20

The ordinary fdtd_3d.py run now solves once and exports separate E/H PNGs
and GIFs through plot_fields.py, using the same time-aligned snapshots.
Output names are fdtd_3d_E.png/.gif and fdtd_3d_H.png/.gif in src/outputs.
A 12^3 two-step test produced four readable artifacts, including two
three-frame GIFs. Current large-run parameters and old outputs were preserved.

## Spatial material functions and custom source only — 2026-11-20

fdtd_3d.py now defines epsilon(x,y,z) and mu(x,y,z), both returning 1 by
default, and retains only custom_current as a source model. The solver samples
epsilon on E edges and mu on H faces once, uses local materials in PEC/PML
updates and H output alignment, and bounds CFL using separate material minima.
PML layers/interfaces must be homogeneous. Returned epsilon/mu retain the input
scalars/callables; epsilon_fields/mu_fields hold the sampled arrays.
The existing reflection-time analysis reads these functions but explicitly
rejects nonuniform media because its timing model is homogeneous-only.
Four material tests passed, including local update, Gauss laws, scalar/callable
equivalence and validation. Small ordinary export and analysis runs passed.
No bunny, integral representation, or full configured run was added.

## Sphere field extraction — 2026-11-20

For Xiaodi, field_extraction.py now generates a source-centered sphere strictly
inside the physical domain and samples each native Yee component using trilinear
interpolation. Default 16x32 rings plus two poles give 514 unique samples.
extract_sphere(result) returns one time-aligned E/H snapshot and geometry;
running the file only saves a geometry preview via plot_fields.py.
Analytic multilinear interpolation and a small PML-solver integration check passed.
Time histories and surface quadrature are not yet implemented.

## Error/reference norm plot — 2026-11-19

Added a separate dark-background logarithmic figure, pml_error_norms.png,
with E/H panels showing absolute discrete L2 differences and reference norms.
err_analysis.main saves it automatically alongside the existing error plot/CSV.
Rendered and visually checked using the existing 356-sample CSV; no solver rerun.
Current saved analysis uses safety=50*dt; the older three-step entry below is historical.

## PML norm CSV columns — 2026-11-19

Analysis now appends pml_L2_E and pml_L2_H, the PML field norms over the
shared physical region, alongside the reference norms. Peak-normalized errors
are unchanged. Small-run CSV checks passed; existing full-run CSV is preserved
and receives the new columns on the next analysis run.

## Safety reserve — 2026-11-19

At Xiaodi's request, analysis now requires T_end + 3*dt < t_return.
The total three-step margin includes the forward H half-step. Timing-only
checks passed; existing plots have not been regenerated for this change.

## Timing and progress — 2026-11-18

For Xiaodi, run_metrics.py provides editable timing, progress and core FLOP
estimation functions. Both entry points now report each solve; GIF export has
separate frame progress/timing and analysis reports the paired total. Counts
are formula-based core arithmetic estimates, not hardware measurements.
Small PEC/PML runs retained bitwise-identical E/H with instrumentation;
hand-count FLOP checks and a real two-frame PNG/GIF export passed.
Full current-grid timing was not run; no performance speedup is claimed.

## Peak-normalized errors — 2026-11-18

At Xiaodi's request, E/H differences are now divided by the maximum respective
reference norm over the sampled observation interval. Equations are beside
the calculation in err_analysis.py. CSV retains absolute and reference norms;
plot_fields.py labels the curve Peak-normalized L2 error. An entirely zero
reference gives NaN. Small nonzero/zero-source checks passed. Replotted the
previously measured 80^3/160^3 diagnostic data (no full rerun): peak normalized
E/H errors are 6.04379e-6 / 6.52354e-6. Earlier instantaneous-relative plots
and their metrics are superseded by this definition.

## Relative error over time — 2026-11-18

For Xiaodi, err_analysis.py now runs both domains from t=0 and computes
relative discrete L2 errors for E/H at every step in the observation interval.
Native Yee components are cropped to the shared physical domain without
averaging. Temporary PML samples are deleted as reference samples are compared.
Zero reference norms give NaN (undefined), not an invented denominator.
main saves pml_error_history.png and .csv in src/outputs; plotting remains in
plot_fields.py. It no longer calls the final-field comparison plot.
The configured 50^3/76^3 run completed over observation [0.436477,2.08539],
with actual PML thickness 0.32, B=1.52 and b=0.68. This is boundary sensitivity
relative to one reference, not a convergence or strict no-contamination proof.

## Separate analysis entry point — 2026-11-18

Xiaodi requested English comments and a simpler run workflow. run_simulations
now has English annotations. Set shared parameters and REFERENCE_HALF_WIDTH
in fdtd_3d.py, then run src/fdtd/err_analysis.py directly. Its main derives dt
from CFL and runs only the PML/reference pair, with no ordinary run or GIF
export. It now saves one final native-Ez comparison PNG through plot_fields.py. Analysis T_end remains reference-bound-driven, not fdtd_3d.T_END.
Final fields are returned; time histories and errors are still pending.
The script entry point passed a small 12^3/18^3 custom-current check.

## Length-based PML paired runs — 2026-11-18

For Xiaodi, err_analysis.py now recomputes PML cells from fdtd_3d.PML_length.
run_simulations(B, dt) runs PML and reference to a common safe final time,
returning both results and the observation interval. Actual rounded PML
thickness determines the physical region. Small custom-current and zero-source
checks passed; full configured runs were not performed. This step stores only
final fields; time-history sampling and relative E/H errors are the next step.

## Dark slice style — 2026-11-14

Restored black zero-field slice backgrounds, with blue negative and orange
positive values. Titles, axes and colorbar labels are shorter; fixed symlog
colors and scaled arrows are retained. Spatial axes use meters under the
user's convention; time remains in solver units (1 m / vacuum light speed).
Rendered and visually inspected cached 50^3 frames in
`src/outputs/dark_preview/`; no new simulation or standard output regeneration.
The current independent 100^3/PML-15 source settings are preserved. The older
visibility verification below describes the previous style and run.

## Field animation visibility — 2026-11-14

Xiaodi requested clearer oscillations and vector lengths. Codex updated
only plotting behavior in src/fdtd/plot_fields.py: signed component slices
(default z), fixed symmetric-log colors, and explicitly labeled per-frame
square-root arrow lengths. Actual field amplitudes remain visible on the
colorbars and peak readout. Known-field E/H checks passed for signs, zero,
weak fields, direction reversal and arrow scaling. Full GIF export and
visual inspection passed. Source edits (50^3, phase 3*pi*CUSTOM_FREQUENCY*t) are preserved;
the amplitude changed from 10 to 100 during this task, with unknown authorship.
The final regeneration uses the amplitude-100 snapshot: 619 solver steps
to T=10, 620 GIF frames at 900x720, and a final PNG at 1500x1200. Standard
src/outputs/fdtd_3d_current.png/.gif now contain the improved views. Signed
early/late frames and the final PNG were inspected; finite E/H were checked.
Solver and analysis files are unchanged. Plotting/docs are saved locally;
source edits and generated GIF changes remain outside that commit.

## Normalized FDTD — 2026-11-14

Xiaodi authorized normalized units and a local Git commit. Codex updated
the four FDTD modules and their documentation on local main: epsilon=mu=1,
c=1/sqrt(mu*epsilon), T=10, custom-source duration 6, frequency 0.5 and
amplitude 1. All times, coordinates, sources and plot labels use consistent
normalized units. This is a new normalized example, not an equivalent
rescaling of the previous SI run. No push requested.
Historical numerical checks below used the units/settings stated there.

Verification passed: equivalent SI/normalized 12^3 PEC and PML runs agree
within 8e-16 relative error in E/H/charge; a nonunit medium (epsilon=4, mu=9)
uses c=1/6. Small PML/reference runs retain common spacing, time and the
physical region, agreeing within 3e-15 at early time. The 60^3 default
physics setup completed 743 steps to T=10 with finite fields and a physical
interior Gauss residual below 4.3e-15. E and H PNG/GIF exports were checked.
The full-grid verification animation samples every 20 steps (39 frames);
the saved code retains FRAME_EVERY=1. Verification plots are in the ignored
`src/outputs/normalized_verification/` directory. That earlier verification
retained the five-times plot scale; the visibility change above replaces it.
These checks validate consistent units and execution, not convergence or a
full-duration reference-error bound. Existing tracked GIF changes/deletions
remain outside the source/documentation commit.

## Physical domain convention — 2026-11-14

Xiaodi defines the physical domain as the interior enclosed by the inner
PML interfaces, excluding the absorbing PML cells. This is the region of
interest. Compare the small PML run and larger reference over this same
physical region, using matching native Yee positions, grid spacing and
physical time. Do not include PML cells in the error norm.

For a centered computational cube [-A,A]^3, spacing h and p PML cells per
side, the physical domain is [-b,b]^3 with b=A-p*h. Derive these bounds
from the current setup each time. The larger reference extends outside
this region while the comparison region stays fixed. The solver already
reports physical_bounds; fdtd_with_pml returns full-grid E/H, so
comparison cropping remains a future step.

## Minimal timing and PML run — 2026-11-14

At Xiaodi's request, `src/fdtd/err_analysis.py` has three simple functions.
`simulation_time(a,b,B,c,dt)` returns a grid-aligned stopping time with one
safety step plus the forward H half-step before the reflection-arrival bound.
`fdtd_with_pml(T,dt)` uses fdtd_3d's grid and PML parameters, always passes its
custom_current and returns the solver result dictionary with native E/H
tuples at T, physical bounds, grid/timing/material/PML information, and
physical_lengths=(Lx,Ly,Lz) in normalized length units excluding the PML.
It fixes the number of steps to preserve dt; the solver checks CFL and
already centers H in time.
T must be a positive integer multiple of dt, and PML_CELLS must be positive.
There are no plots, additional helper modules or automatic runs on import.
Previously verified a 50^3 run with the then-current PML-8 setting for 229 steps at
T=14.0923076923 ns and dt=0.0615384615385 ns. All six returned arrays are
finite and nonzero, with the expected native Yee shapes. The custom source
and PML are used even when both example selector flags are false. A separate
zero-current PML run preserves exactly zero E/H; invalid timing, disabled
PML and unstable CFL inputs are rejected. These checks validate this run
interface, not a new accuracy or reflection study.
The renamed function's returned information was checked on a 10x12x14
rectangular PML run: physical side lengths [1.2,2,3] m matched the inner
PML interfaces; grid/time information and full-grid E/H shapes were verified.

`fdtd_reference(pml_result,B)` runs on a larger centered cube without PML,
with PEC outer walls. It rounds the requested half-width B outward by whole
cells, contains the entire original computational cube, and preserves h,
dt, final time, material constants and custom_current. It rejects a box
too small for the existing safe-time condition. Returned physical_bounds
and physical_lengths retain the original region of interest; padding_cells
records the enlargement. Fields still cover the full reference grid.
Small 20^3/24^3 and 21^3/25^3 runs verified matching native Yee coordinates
and early physical-domain E/H agreement within 3e-15 relative difference.
This is an early-time consistency check, not a full-duration accuracy study.

## FDTD cleanup — 2026-11-14

Xiaodi requested removal of the error-analysis feature and all its project
files. Its script, tests, generated results and dedicated plot function
have been removed. The source/current settings, Yee solver and standard
PNG/GIF plotting remain. Earlier experiment records are historical in
TIMELINE.md; their deleted outputs are no longer available in this project.

The current solver includes PML and time-centered H. Older no-PML and
material statements below describe their historical observation dates.
No publication was requested.

## Current FDTD layout — 2026-11-06

This section supersedes earlier documentation-only/local-only FDTD statements
below. Xiaodi uploaded the FDTD project to `main` in commit `266b983` and then
explicitly requested exactly three files under `src/fdtd/`:
`fdtd_3d.py`, `plot_fields.py`, and `yee_solver.py`.
Codex flattened the nested source directory and removed its duplicated README,
math/API/pseudocode documents and tests from the active subtree. The proposal,
literature and shared collaboration documents remain in their existing places.
Run `python src/fdtd/fdtd_3d.py`; generated PNG/GIF files go to root `outputs/`.

Verification: the 14 existing tests were loaded from the external backup and
passed against the relocated modules. A separate 8 x 10 x 12, 0.2 ns entry-point
run exported readable PNG/GIF files to a temporary directory; a mocked export
checked the default root output path. Solver and plotting executable ASTs
were unchanged. These checks validate relocation and existing test problems,
not the physical accuracy of the currently edited DIY example.

Known inherited settings remain: MU0 includes `+0.1` and is not the vacuum
value; the DIY waveform includes a step and differs from its original smooth
pulse description. No PML, material map or exterior reconstruction was added.
Human owner: Xiaodi; Codex assisting; branch `main`. Earlier unrelated local
documentation edits remain outside this change's staged content.

## Current scope

**Beyond Computational Boundaries: Electromagnetic Field Reconstruction via
FDTD and Boundary Integrals**

[The supplied proposal](proposal/Proposal_xiaodi_guanlin.pdf) defines the
project: Maxwell equations in `[-1,1]^3` with a prescribed current; FDTD with
appropriate initial/boundary conditions; extraction of enclosing-surface
field data; and exterior reconstruction through a space-time Green identity.
Use larger-domain FDTD reference fields to measure accuracy, convergence,
reflection effects, stability over the test window, and computational cost.
Two-way FDTD–time-domain BIE coupling is further investigation.

The proposal contains the required title, members, background, computational
approach, success/failure measures, and four literature references.
Earlier local draft proposals are not included or substituted for this PDF.

## Publication decision

- On 2026-11-04, Xiaodi authorized publication **without any code files**.
- The latest organization request groups collaboration documents under
  `docs/` and reserves `src/` for all newly created project code. The source
  directory currently contains explanatory Markdown only.
  Local solver code, tests, scripts, notebooks, result files, and their Git
  history remain unpublished. Existing local work is preserved separately.
- The AI maintains `docs/TIMELINE.md`, including recording observed human edits.
  Humans review work and own the rules; they have no routine logging duty.
- No executable timeline checker, CI workflow, or numerical environment is
  included. Do not claim a fresh clone can run the local prototypes.

## Scientific milestones

1. Agree the prescribed-current test problem, units, initial data, geometry,
   observation window, error norms, and measurable acceptance targets.
2. Review the reference sections needed for the method and derive surface
   representation, normal/sign conventions, and causal history requirements.
3. Validate FDTD and tangential E/H transfer on an enclosing surface,
   accounting for Yee spatial/time staggering and boundary placement.
4. Implement and validate one-way **time-domain exterior reconstruction**
   against a sufficiently large reference grid including the target points.
5. Study grid/time-step/quadrature/history refinement, finite-time stability,
   runtime, and memory including surface histories. Do not assume a speedup.
6. If feasible, investigate two-way nonreflecting FDTD–BIE coupling separately.

These are planned milestones, not claims of implementation. Local prototypes
exist outside this shared repository; audit their accessible evidence before
counting them toward a milestone. A harmonic BEM demonstration does not by
itself complete transient reconstruction or time-domain coupling.

No deadline, task division, or numerical tolerance has been invented. Agree
these together. Failure indicators include error that does not decrease under
appropriate refinement, unexplained field growth, causal/sign inconsistency,
or cost comparisons that omit history storage.

## Task ownership and handoff

| Task | Human owner | Branch / files | State and next step |
| --- | --- | --- | --- |
| Make field GIFs readable | Xiaodi; Codex assisting | `main`; `src/fdtd/plot_fields.py`, output plots, docs | Implemented and verified; standard PNG/GIF regenerated at amplitude 100 |
| Normalize FDTD and save locally | Xiaodi; Codex assisting | `main`; `src/fdtd/`, READMEs, status and timeline | Implemented and verified for local Git save; no push authorized |
| Documentation-only collaboration setup | Xiaodi; Codex assisting | `main`; documents and proposal | Published and remote manifest verified; Guanlin accepts invitation |
| Group documents and establish source directory | Xiaodi; Codex assisting | `main`; root entry points, `docs/`, `src/README.md`, review configuration | Applied directly to main under Xiaodi's explicit instruction; [PR #1](https://github.com/markzhou694/capstone-computational-electromagnetic/pull/1) contains the original organization history |
| Allow human-authorized main updates | Xiaodi; Codex assisting | `main`; rules, collaboration guide, README, PR template, timeline; GitHub branch protection | Mandatory peer review removed at Xiaodi's direction; humans retain control over publication and rule changes |
| Test-problem and success-target agreement | Unassigned | To be claimed | Next scientific planning task |
| Literature/formulation notes | Unassigned | To be claimed | Read needed equations before implementation |

AI: replace an unassigned row when a human takes the task. Include the exact
branch, files/interfaces, current state, and next step; record the update in
the timeline. Local claims are not shared until pushed.

## GitHub setup

- Repository: `markzhou694/capstone-computational-electromagnetic` (public).
- Publication uses a separate documentation-only clone and fresh Git history.
  The initial upload was verified against its exact 11-file allowlist; no
  source code, executable tooling, result files, or earlier code commits
  were included. This new organization request changes where files belong,
  not the decision to keep the earlier local prototypes unpublished.
- Only `markzhou694` was listed as a collaborator at the latest check.
- Guanlin's verified account is `Lim-miL-Lim`. The write-access invitation
  has been sent with Xiaodi's explicit approval; Guanlin must accept it.
  Both human accounts are listed in CODEOWNERS.
- Main-branch policy, updated at Xiaodi's explicit direction: direct pushes
  to main are allowed when human-authorized. PRs and peer reviews are
  optional; there is no required code-owner or latest-push approval.
  Force pushes and deletion remain blocked, the remaining protections apply
  to admins, and PR conversations must be resolved. No CI checks are required.
  This replaces the initial mandatory second-person review policy. Inspect
  [live branch settings](https://github.com/markzhou694/capstone-computational-electromagnetic/settings/branches)
  for the active configuration rather than assuming files activate it.
- The reorganization and review-policy correction follow Xiaodi's direct
  instructions. AI may implement explicitly requested rule changes and must
  log the authorization; it still cannot make autonomous governance edits.
