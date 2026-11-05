# Shared project status

Last reviewed: **2026-11-04**. Humans: **Xiaodi Zhou and Guanlin Wang**.

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
