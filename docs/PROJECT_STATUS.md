# Shared project status

Last reviewed: **2026-11-14**. Humans: **Xiaodi Zhou and Guanlin Wang**.

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
`src/outputs/normalized_verification/` directory. The existing five-times
plot scale is retained; the final weak E field is nearly dark on that scale.
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
