# Project timeline

**Maintained by AI.** The AI records its own changes and reconciles observed
human changes; collaborators do not need to write routine entries.
Append only. Times are observation times with an explicit timezone.

This timeline begins with the shared documentation repository. Earlier local
prototype preparation remains in the separate local repository and was never
published. Its source files, results, and commits are not part of this history.
See COLLABORATION.md for the recording and correction procedure.

## 2026-11-04T23:34:45+00:00 | docs-bootstrap-20261104

- Changed by: Codex file edits, following Xiaodi Zhou's explicit documentation-only publication decision and AI-managed timeline requirement.
- Recorded by: Codex, working for Xiaodi Zhou (@markzhou694).
- Context: Initial main branch in an empty remote repository; new history with no parents from the local solver repository.
- Files: `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `COLLABORATION.md`, `LITERATURE.md`, `PROJECT_STATUS.md`, `README.md`, `TIMELINE.md`, `proposal/Proposal_xiaodi_guanlin.pdf`.
- Change and reason: Created collaborator README, shared human-owned rules, AI-maintained timeline/status procedure, literature notes, rule-review ownership, PR template, and a documentation allowlist. Copied the supplied proposal unchanged. Excluded all solver code, scripts, tests, workflows, notebooks, results and earlier local code commits. Replaced the earlier unpushed helper-script plan with AI responsibility during active sessions.
- Verification: Both GitHub account names verified. Guanlin write-access invitation sent (ID 341598819) after explicit human approval; acceptance is still required. File/history/link checks will be recorded before publication.
- Limitations: No background watcher or executable timeline checker is deployed. AI cannot inspect unsaved, inaccessible, or unpushed changes. Remote branch protection is applied after documentation publication; the settings link is in PROJECT_STATUS.md.
- Next: Audit the exact documentation manifest and fresh history, publish the approved documents, then apply and verify the review policy. Guanlin accepts the invitation.

## 2026-11-04T23:35:22+00:00 | docs-audit-20261104

- Changed by: Codex; validation record only.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Prepublication audit of the initial documentation-only main branch.
- Files: `TIMELINE.md`.
- Change and reason: Recorded the completed audit before the approved initial upload.
- Verification: Exactly 11 allowlisted documents/configuration/PDF files found and staged; all relative Markdown links resolve; the timeline names every published path; staged whitespace check passed. Proposal SHA-256 is 0403a164adc2dd67bdbe766813917b0f31de37b78f554a241ff3bcb1fa9885bd and matches the supplied PDF byte for byte. Ignore rules reject example Python, MATLAB, shell, notebook, workflow and result paths. The repository was cloned empty and contains no imported prototype history.
- Limitations: No numerical tests were run for this documentation-only change; no code is being published. Remote tree and branch settings still require post-upload verification.
- Next: Publish the approved initial commit, verify the remote manifest/history, then apply the human review policy.

## 2026-11-04T23:36:04+00:00 | docs-publication-20261104

- Changed by: Codex, completing the authorized documentation-only publication.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Initial published commit 92999bb4ef74d80630643ec0a86e614f2e769bfb; final documentation handoff on main.
- Files: `PROJECT_STATUS.md`, `TIMELINE.md`.
- Change and reason: Updated shared status to reflect successful documentation publication and recorded remote verification. The README explains every shared file, both-account onboarding, AI-owned timeline maintenance, human reviews, and visibility limits.
- Verification: Initial git push succeeded. GitHub's recursive main tree returned exactly the 11 approved documentation/configuration/PDF paths with no truncation. The root commit has no prototype ancestors. Local links and staged whitespace passed earlier checks. GitHub still lists Lim-miL-Lim's write invitation as pending. Existing local prototype code/results remain separate and unpublished, with their public remote removed.
- Limitations: Guanlin must accept the invitation before write access and owner reviews work. No background AI service or CI has been installed. The final administrative step applies and reads back the main-branch protection policy; its live state is available through the settings link rather than inferred from this file.
- Next: Apply the agreed branch protection after this final setup commit. Guanlin accepts the invitation; both collaborators start future sessions with the README prompt and review each other's PRs.

## 2026-11-04T23:48:25+00:00 | organize-docs-src-20261104

- Changed by: Codex, implementing Xiaodi Zhou's explicit request to group shared files, add src, and direct AI code there.
- Recorded by: Codex, working for Xiaodi Zhou (@markzhou694).
- Context: xiaodi/organize-docs-src, based on f61b79033325148a5336573e95399c46d8ad4b6a; governance path and source-location edits are directly human-requested and still require the other human's review.
- Files: `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `COLLABORATION.md`, `LITERATURE.md`, `PROJECT_STATUS.md`, `README.md`, `TIMELINE.md`, `docs/COLLABORATION.md`, `docs/LITERATURE.md`, `docs/PROJECT_RULES.md`, `docs/PROJECT_STATUS.md`, `docs/TIMELINE.md`, `docs/proposal/Proposal_xiaodi_guanlin.pdf`, `proposal/Proposal_xiaodi_guanlin.pdf`, `src/README.md`.
- Change and reason: Moved the full shared rules to docs/PROJECT_RULES.md and grouped collaboration, literature, status, timeline, and proposal under docs/. Kept root README and minimal AGENTS/CLAUDE entry points for discovery. Added src/README.md and instructions that all new project code belongs under src/. Updated links, ignore rules, ownership patterns, status, and PR checklist. Existing local prototype code and its history were not imported. Old paths listed here document the moves; earlier timeline entries retain their original paths and wording.
- Verification: All relative Markdown links resolve. The previous timeline is retained byte for byte as a prefix; the literature file and proposal PDF are unchanged. Ignore-rule checks allow future Python, MATLAB, tests, scripts, and notebooks under src, while rejecting code at root/docs and ignoring credentials, caches, and generated results. No implementation files were introduced. Both humans remain owners of the moved canonical rules. git diff HEAD --check passed.
- Limitations: This is an organization/documentation change; src currently contains explanatory Markdown only, so no numerical tests were needed. Main requires the other human's approving review. Guanlin's collaborator permission was still read at the start of this task; write access depends on accepting the invitation.
- Next: Publish this task branch and open a PR; the other human reviews and approves it before merge. Future coding tasks place source files under src and AI records changes in docs/TIMELINE.md.

## 2026-11-04T23:49:08+00:00 | organize-docs-src-pr-20261104

- Changed by: Codex; PR handoff metadata.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: xiaodi/organize-docs-src at 4445e0602da687542b237874a628525c2a51857b; PR https://github.com/markzhou694/capstone-computational-electromagnetic/pull/1.
- Files: `docs/PROJECT_STATUS.md`, `docs/TIMELINE.md`.
- Change and reason: Linked the published reorganization PR from the shared task status so both AI accounts and humans can find the work awaiting review.
- Verification: Task branch push succeeded; GitHub returned PR #1 open and unmerged with the expected base and head. Earlier timeline content remains unchanged; only status/link and this appended record change in this handoff.
- Limitations: Protected main still requires the other human's approval; no merge or protection bypass has been performed.
- Next: Guanlin reviews PR #1 and approves it before merge. Continue to store newly created source code under src/ after this organization is adopted.

## 2026-11-05T00:06:37+00:00 | direct-main-authorization-20261104

- Changed by: Codex, implementing Xiaodi Zhou's explicit instruction to change main directly after he rejected mandatory second-person approval.
- Recorded by: Codex, working for Xiaodi Zhou (@markzhou694).
- Context: Main was fast-forwarded locally from f61b79033325148a5336573e95399c46d8ad4b6a to the prepared organization history ending at 34fe886f1234a9b4fd21651fa5194623e1150a90. This includes the paths already recorded in organize-docs-src-20261104 and organize-docs-src-pr-20261104. PR #1 had been closed and its branch deleted; at Xiaodi's request, Codex restored that exact branch head and reopened the PR, without changing file content.
- Files: `.github/pull_request_template.md`, `README.md`, `docs/COLLABORATION.md`, `docs/PROJECT_RULES.md`, `docs/PROJECT_STATUS.md`, `docs/TIMELINE.md`.
- Change and reason: Replaced mandatory two-person review with optional peer review and human-authorized direct main updates. A human may explicitly instruct a specific rule change; AI still cannot change governance on its own. Updated the README, procedure, checklist, and status consistently. The responsible human retains publication/merge authority. Earlier timeline entries remain unchanged; their mandatory-review next steps are superseded by this decision.
- GitHub setting: Removed main's required-pull-request-review requirement at Xiaodi's explicit direction. Readback confirmed required_pull_request_reviews is null; admin enforcement and conversation resolution remain enabled, and force pushes and branch deletion remain disabled.
- Verification: All local relative Markdown links resolve. Existing timeline content is retained byte for byte as a prefix. Literature and supplied proposal bytes are unchanged. All existing commits contain documentation/configuration/PDF files only; the current tree has 13 tracked files, src contains only README.md, and no nonignored untracked files are present. Whitespace checks passed for the policy edits. No solver code, scripts, workflows, outputs, or old prototype history are imported.
- Limitations: No numerical tests were run because this change contains no implementation. GitHub settings authenticate accounts, not human versus AI actions. Remote publication of this final record still requires the authorized push and readback.
- Next: Commit and push these prepared changes directly to main, then verify the remote commit/tree and PR state. Future work follows the updated human-controlled workflow; AI continues timeline maintenance.


## 2026-11-06T01:23:58-05:00 | fdtd-three-file-layout-20261106

- Changed by: Codex following Xiaodi's explicit request for exactly `src/fdtd/fdtd_3d.py`, `src/fdtd/plot_fields.py`, and `src/fdtd/yee_solver.py`, confirmed twice with the target tree.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context and reconciliation: `main` starts at `266b983`; Xiaodi supplied terminal output showing his successful commit/push of the nine-file FDTD project. Remote fetch matched HEAD and no open PRs were returned. Five pre-existing unstaged documentation changes were observed: `README.md`, `docs/PROJECT_RULES.md`, `docs/PROJECT_STATUS.md`, `docs/TIMELINE.md`, `src/README.md`. Earlier timeline records explain much of that local work; authorship of any unrecorded edits is not inferred. The rule file remains untouched; prior status/timeline edits are preserved locally but excluded from this commit. README updates now reflect the requested active code location.
- Files: moved `src/fdtd/src/fdtd_3d.py`, `src/fdtd/src/plot_fields.py`, `src/fdtd/src/yee_solver.py` to `src/fdtd/fdtd_3d.py`, `src/fdtd/plot_fields.py`, `src/fdtd/yee_solver.py`. Removed `src/fdtd/README.md`, `src/fdtd/docs/API.md`, `src/fdtd/docs/MATHEMATICS.md`, `src/fdtd/docs/PSEUDOCODE.md`, `src/fdtd/src/tests/test_api.py`, `src/fdtd/src/tests/test_fdtd_3d.py` from the active subtree. Updated `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and this timeline.
- Change and reason: removed nested source/docs/tests structure so the FDTD folder has only three Python files. Replaced references to removed API documents with function docstrings. Adjusted default output location to repository-root `outputs/` after moving the entry point. Original settings/current equations and solver/plot calculations were retained.
- Preservation: the complete previous FDTD folder, original local documentation and unstaged patch were saved and checked under `/Users/mark/Desktop/course_note/computational_elemag/capstone_fdtd_backup_20261106_012149` outside the repository. The original sibling `capstone_code/` and shared proposal/literature/governance files remain separate.
- Verification: all 14 existing tests loaded from the backup passed against the relocated imports; driven-mode convergence orders were 2.00116225 and 2.00029525, relative Gauss residual 5.503167e-16. Solver/plot executable ASTs were unchanged after excluding docstrings. A small 8 x 10 x 12, 0.2 ns entry-point run exported PNG/GIF files, both verified with Pillow; a mocked export confirmed the root default output directory. Exact three-file active directory checked. Smoke artifacts: `/var/folders/lc/yc10msgn6xbb6r677rsnmyhm0000gn/T/capstone-flat-smoke-f67c6t9w`.
- Limitations: inherited MU0 has `+0.1`, so it is not the vacuum constant; inherited DIY waveform has a step and its original smooth-pulse description is stale. This organization task does not change those settings or establish physical accuracy of the editable example. Tests/docs remain available in history/backup, but are no longer part of this FDTD subtree.
- Next: publish this cleanup on the existing main branch and verify the remote FDTD tree has exactly the three requested files; Xiaodi should edit this repository copy for future uploads.

## 2026-11-13T15:46:57-05:00 | reference-planning-start-20261113

- Changed by: Authorship of inherited code/output changes is unknown; Codex records them and starts Xiaodi's authorized conversion task.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`. Xiaodi requested planning discussion first, then explicitly authorized coding domain/time conversions in `error_analysis.py` and asked how to handle E/H time staggering.
- Files: Observed `src/fdtd/fdtd_3d.py`, `src/fdtd/yee_solver.py`, `src/fdtd/plot_fields.py`, `src/outputs/fdtd_3d_current.gif`; updated `docs/PROJECT_STATUS.md` and `docs/TIMELINE.md`.
- Reconciliation: Commits `512710e`, `86a1b9b`, and `dca455d` contain PML solver/driver, plotting, and output work since the last log. Current unstaged changes set 90 cells per axis, E plotting, a changed custom waveform, MU0 to `4*pi*1e-9`, and a changed GIF. EPSILON0 preserves wave speed C0. No authorship is inferred from commits. These changes are preserved.
- Verification: Inspected required project records, current files, status, staged/unstaged diffs and recent commits. Staging is empty. Git fetch failed with DNS resolution of github.com; connected GitHub search returned no open PRs. Confirmed `magnetic_at_e_time` already synchronizes callback/returned H with E using an output-only prediction and average.
- Limitations: No current field-accuracy claim. Geometric travel-time planning cannot prove exactly zero discrete FDTD boundary influence; later comparisons with a still larger reference are required.
- Next: Implement and check conservative conversions locally, retaining all plotting in `plot_fields.py` and preserving the existing source and solver.

## 2026-11-13T15:50:19-05:00 | reference-planning-implemented-20261113

- Changed by: Codex, implementing Xiaodi's authorized conversion functions.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; continuation of reference-planning-start-20261113. No commit or push performed.
- Files: Added `src/fdtd/error_analysis.py` and `src/tests/test_error_analysis.py`; updated `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and `docs/TIMELINE.md`.
- Change and reason: Added CFL/time-grid planning, source-face-sample round-trip bounds, strict downward rounding of sample times, and outward integer-cell padding independently on six faces. Default margin is one timestep plus dt/2 for the existing synchronized H output. Source support is an explicit enclosing box; the CLI requires a declared sphere radius. The CLI imports current example settings without changing them and prints a plan without solving or plotting. Existing `fdtd_3d.py`, `yee_solver.py`, `plot_fields.py`, and output files were not edited by this change.
- Verification: `python3 -B -m unittest discover -s src/tests -p test_error_analysis.py -v` passed all 10 tests. Checks include strict equality exclusion, off-center geometry, anisotropic grid alignment and minimal sufficient padding, invalid inputs, actual full-3D small/enlarged solves with matching times and matching central E/H fields, and second-order magnetic time centering for Ez=x*cos(t), Hy=sin(t), mu=1. `python3 -B src/fdtd/error_analysis.py --source-radius 0.25` used the current 90^3, 12 ns, CFL=0.8 settings: 351 steps, dt=0.034188034188 ns; 61 padding cells per side, 212^3 reference over [-2.35555556,2.35555556]^3; first reflected-arrival bound 12.1380267975 ns; reserve 0.0512820512821 ns; last permitted fixed-dt sample index 353 at 12.0683760684 ns. Requested simulation remains 12 ns.
- Limitations: The full 212^3 comparison has not run. Continuum travel time and rounding do not establish a discrete reflection tolerance. The default one-step margin is adjustable, not a measured numerical-contamination bound. Solver dt is recomputed if its requested end time changes; callers must check timing again. Remote fetch remains unavailable due to DNS; no open PRs were returned by the connector. Full-tree whitespace checking reports only the pre-existing trailing space in `src/fdtd/yee_solver.py:14`, which is preserved.
- Next: Discuss and implement the actual field-error comparison, verify agreement with a still larger reference, and keep every plotting function in `plot_fields.py`.
- Handoff checks: New Python files parse and contain no trailing whitespace; changed documentation links resolve and scoped `git diff --check` passes. Reconciliation clarification for reference-planning-start-20261113: 90 cells per axis was already committed; the observed unstaged edit to that assignment changes whitespace only.

## 2026-11-13T16:05:51-05:00 | shared-fdtd-setup-start-20261113

- Changed by: Codex, following Xiaodi's report of the required-radius CLI error and explicit instruction that fdtd_3d setup must be accessible to error_analysis.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`. The interrupted preceding turn only inspected files; no implementation changes were made there. Current pending source, solver, output, documentation and analysis changes match the preceding records; staging remains empty. Remote fetch was already unavailable due to DNS in this ongoing task.
- Files: Planned `src/fdtd/fdtd_3d.py`, `src/fdtd/error_analysis.py`, `src/tests/test_error_analysis.py`, `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`; appended this `docs/TIMELINE.md` record.
- Change and reason: Share the run settings and active source geometry from fdtd_3d, make no-argument analysis work, and avoid a second copy of the source setup. Preserve the existing source equations, numerical settings, solver and plots.
- Verification: Re-read current source/analysis/tests and project instructions; captured pre-change custom/pulse source arrays in `/private/tmp/fdtd-source-before-shared-20261113.npz` using Xiaodi's sci Python interpreter for a later exact comparison.
- Next: Implement shared setup access, run the user's no-argument command, and verify source behavior and numerical planning checks.

## 2026-11-13T16:07:53-05:00 | shared-fdtd-setup-complete-20261113

- Changed by: Codex, following Xiaodi's explicit shared-setup instruction.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; no commit, push, or output regeneration.
- Files: Updated `src/fdtd/fdtd_3d.py`, `src/fdtd/error_analysis.py`, `src/tests/test_error_analysis.py`, `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and `docs/TIMELINE.md`. Preserved the previously observed solver/material edit and GIF.
- Change and reason: Moved DIY source constants to the shared CUSTOM_* setup in fdtd_3d. Added get_simulation_settings() for both the normal driver and analysis, and get_source_bounds() for the selected source geometry. Analysis now works without arguments and returns the shared settings with its plan. Optional CLI geometry overrides affect the plan only; no duplicate source defaults are kept in analysis. The pulse branch uses SOURCE_CENTER/RADIUS and rejects infinite spatial support for travel-time planning. All plotting remains in plot_fields.py.
- Verification: Ran the no-argument analysis with `/Users/mark/miniconda3/envs/sci/bin/python -B` successfully; it read the current 0.25 m support and retained the previously calculated 212^3 plan. All 14 tests passed with that interpreter, including propagation of edited grid/time/PML/source settings, pulse selection, the no-argument entry point, and override isolation. Compared custom and pulse outputs at 8 times on 9x7x5 spatial samples with saved pre-change arrays: exact equality for both sources.
- Limitations: The full large-domain field-error experiment remains under discussion; this task only fixes shared setup and the planning entry point. A changed source spatial equation must retain correct support metadata. No numerical-accuracy claim is inferred from the source-preservation check. Remote access limits remain as recorded at task start.
- Next: Xiaodi can run error_analysis.py directly and edit the setup once in fdtd_3d.py. Continue discussing the actual reference-field comparison.

## 2026-11-13T16:12:37-05:00 | field-error-plots-start-20261113

- Changed by: Codex, following Xiaodi's explicit request for actual error plots and editable constants like fdtd_3d, with plotting functions in plot_fields.py.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; this authorizes the previously discussed field comparison. Existing shared-setup, source, solver/material, GIF and documentation edits are preserved; staging remains empty. Remote fetch was unavailable earlier in this ongoing task.
- Files: Planned `src/fdtd/error_analysis.py`, `src/fdtd/plot_fields.py`, `src/fdtd/yee_solver.py`, `src/tests/test_error_analysis.py`, `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`; appended `docs/TIMELINE.md`.
- Change and reason: Replace the planning-only default with full 3D small/reference simulations, optionally a further reference check, matched Yee/time samples, numerical error histories, and plots. Put analysis controls at the top of error_analysis, keep source/run setup shared, and put all plotting in plot_fields.
- Verification: Re-read current code and instructions, inspected current status/diffs and disk availability. Hardware sysctl reads were denied; no machine-memory assumption is made. Plan to stage cropped field snapshots on disk to avoid retaining full time histories in RAM.
- Next: Implement the numerical comparison and rendering, verify with small controlled cases, then run the actual configured example and inspect its plots.

## 2026-11-13T16:26:24-05:00 | field-error-plots-complete-20261113

- Changed by: Codex, implementing Xiaodi's full comparison/plotting request.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; no staging, commit, push, or external messages. The earlier source setup, material edit and original GIF remain preserved.
- Files: Updated `src/fdtd/error_analysis.py`, `src/fdtd/plot_fields.py`, `src/fdtd/yee_solver.py`, `src/tests/test_error_analysis.py`, `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and `docs/TIMELINE.md`. Generated local ignored `src/outputs/error_analysis/error_history.png`, `src/outputs/error_analysis/field_comparison.png`, `src/outputs/error_analysis/field_comparison.gif`, `src/outputs/error_analysis/error_data.npz`, and `src/outputs/error_analysis/error_metadata.json`.
- Implementation: Analysis now runs all simulations and exports plots by default. Top-level constants control time override, sample stride/interior margin, extra reference padding, further-reference check/tolerance, field/component, slice/probe, snapshot time, GIF and output location. Driver source/grid/material/PML setup is reused. Explicit solver `time_steps` enforces one dt across grids while retaining original automatic stepping by default. Original Yee components are cropped at matching locations; discrete E/H L2 differences are normalized separately by peak reference norms over sampled times. Cropped snapshots are staged on disk and cleaned up. Every spatial display average, plot and animation function is in plot_fields.py. PEC-only small-domain planning is also supported by excluding its outermost cells.
- Verification: All 18 tests passed with `/Users/mark/miniconda3/envs/sci/bin/python -B -m unittest discover -s src/tests -p test_error_analysis.py -v` and temporary MPLCONFIGDIR. Tests include signed norms, shared settings, geometric/temporal rounding, reference sampling, fixed-step/default bitwise equality, unstable-step rejection, manufactured H convergence, actual small/reference/check solves, PNG/GIF/NPZ/JSON export, and snapshot cleanup. After metadata reporting was extended, the full export test and then all 18 tests passed again.
- Full configured experiment: Ran the no-argument script with the same sci interpreter. Small 90^3 PML-8 grid, reference 228^3 PEC, and check 244^3 PEC; original h=2/90 m, T=12 ns, 351 shared updates, dt=0.034188034188 ns, 37 frames at stride 10 plus endpoints. Reference reflection-time lower bounds were 13.3240324693 and 14.5100381411 ns. Source equations, medium and source settings stayed as in fdtd_3d. Observed solve wall times: 21.2472 s small, 209.1779 s reference, 267.0256 s check.
- Measured results: Peak normalized E/H errors = 5.607674646854311e-5 / 9.527104987900361e-5. Peak reference changes = 1.6377009253045247e-13 / 1.9033807477211704e-13; reference-change/measured-error ratios = 2.920463522653212e-9 / 1.997858478665352e-9. Both reference changes pass the configured 1e-6 diagnostic tolerance. NPZ arrays are finite; independently recomputing normalization exactly matches saved errors. Source/analysis constants and actual plot positions were added to the completed run's JSON after a metadata-only reporting extension; no fields or error arrays were changed.
- Artifact review: Visually inspected the 1650x1050 error-history PNG and 1800x600 field-comparison PNG; labels/scales and small/reference/difference panels are readable. Pillow verified the 1080x360 GIF has 37 frames. No temporary Yee snapshot directory remains. Changed-file syntax/whitespace and documentation links were checked; the unrelated pre-existing solver constant trailing space is retained.
- Limitations: These are sampled boundary/domain sensitivity measurements, not total field accuracy. Shared spatial/time/source-resolution errors, including the existing custom waveform's resolution issues, are not tested by changing only the box. Very small reference differences do not mathematically prove zero discrete boundary influence. The reference threshold is adjustable and advisory. Remote access limits remain as recorded earlier.
- Next: Xiaodi edits the analysis constants and reruns error_analysis.py to regenerate these artifacts; further numerical studies can reuse this workflow.

## 2026-11-13T21:51:29-05:00 | math-readable-analysis-start-20261113

- Changed by: Codex, following Xiaodi's request to make error_analysis.py simpler and put the mathematics ahead of software bookkeeping.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; prior pending changes and generated default outputs are preserved. No staged changes or new local commits. This is a readability refactor, not a new numerical method.
- Files: Planned `src/fdtd/error_analysis.py`, a supporting `src/fdtd/error_analysis_helpers.py`, `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and this `docs/TIMELINE.md`.
- Change and reason: Keep editable controls, sampling-domain/time formulas and the mathematical comparison sequence in the main file. Move validation, Yee indexing, temporary snapshots, progress reporting and output metadata into a plainly named helper module. Keep all plots in plot_fields.py and retain the shared fdtd_3d setup.
- Verification baseline: Saved the pre-refactor file and generated actual small PML and PEC comparison outputs on a rectangular 12x14x16 grid at 5 ns under `/private/tmp/capstone-error-readability-before/`. These provide numerical before/after evidence without overwriting the completed 90^3 experiment.
- Next: Refactor, compare every saved numerical array with these baselines, and rerun the existing tests.

## 2026-11-13T21:57:55-05:00 | math-readable-analysis-complete-20261113

- Changed by: Codex, implementing Xiaodi's request to make the mathematics easier to read.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local `main` at `dca455d`; no staging, commit, push, or external messages. Existing source/solver/material/plot edits and the saved full-size experiment remain preserved. Remote fetch failed due to DNS at task start; the GitHub connector returned no open PRs.
- Files: Refactored `src/fdtd/error_analysis.py`; added `src/fdtd/error_analysis_helpers.py`; updated `README.md`, `src/README.md`, `docs/PROJECT_STATUS.md`, and this `docs/TIMELINE.md`. No solver, source, plotting, or test changes in this readability task.
- Change and reason: Reduced the main analysis file from 487 to 253 lines. Its opening formulas identify A, a, b, B, the source-wall-sample travel time, time reserve and normalized error. The code exposes CFL time selection, b=A-trim*h, six-face return bounds, strict integer rounding and the discrete Yee norm, followed by a five-step run_analysis workflow. Validation, snapshot storage, indexing, progress and metadata export are in one helper module. Plotting remains in plot_fields.py; settings remain shared with fdtd_3d. The equivalent strict rounding expression ceil(limit/dt)-1 replaces floor(nextafter(limit/dt,-inf)).
- Verification: All 18 existing tests passed after the final computational changes with Xiaodi's sci Python interpreter and temporary MPLCONFIGDIR. Repeated the pre-refactor 12x14x16, 5 ns pulse-source experiment for both PML-2 and PEC-only small domains, each with reference and enlarged-check runs. Every one of the 14 NPZ arrays in each case exactly matched the pre-refactor result; all JSON metadata matched except measured runtimes. Evidence is in `/private/tmp/capstone-error-readability-before/` and `/private/tmp/capstone-error-readability-after/`. Parsed both Python files, checked their whitespace and updated documentation links, and ran scoped git diff --check successfully.
- Limitations: The earlier 90^3/228^3/244^3 experiment was not rerun or overwritten. The refactor preserves the tested numerical comparisons; these measure boundary/domain sensitivity, not common mesh/source discretization error. The travel-time calculation is a continuum bound supplemented by the numerical larger-reference check.
- Next: Read the formulas at the top of error_analysis.py and the numbered run_analysis workflow. Edit its existing constants and run the same entry point to regenerate comparisons.

## 2026-11-13T23:07:15-05:00 | analysis-driver-style-start-20261113

- Changed by: Codex, following Xiaodi's request that error_analysis.py look as clean as fdtd_3d.py.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d, staging empty; existing pending edits preserved. Fetch failed due to DNS; the GitHub connector returned no open PRs.
- Observed changes: The current fdtd_3d.py uses CUSTOM_DIRECTION=(1,1,1) and phase=2*pi*f0*t_ns*sin(2*pi*t_ns/duration_ns), unlike the earlier recorded custom-source experiment. Authorship and intent are not inferred. This task preserves that file and its source equations; earlier full-size results describe the earlier source, not this changed setup.
- Files: Planned src/fdtd/error_analysis.py, src/fdtd/error_analysis_helpers.py, README.md, src/README.md, docs/PROJECT_STATUS.md, and this docs/TIMELINE.md.
- Change and reason: Follow the example driver's Parameters / Equations / Run and export structure. Keep controls and a concise mathematical guide in the entry point; organize geometry, timing, field comparison and export in the existing helper, without adding modules.
- Verification baseline: Backed up both analysis modules and fdtd_3d.py; ran the current custom and pulse sources with PML-2 and PEC-only small boxes on 12x14x16 grids at 5 ns, each with larger references. Saved data under /private/tmp/capstone-analysis-driver-style/before/. Captured hashes of solver/source/plot files and the existing full-size output artifacts.
- Next: Refactor and verify exact numerical agreement, existing tests and preservation of the source and saved large-run artifacts.

## 2026-11-13T23:09:22-05:00 | analysis-driver-style-complete-20261113

- Changed by: Codex, implementing Xiaodi's request to match fdtd_3d.py's readable experiment-driver style.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; no staging, commit, push or external messages. Existing unrelated work preserved. Remote fetch remains unavailable due to DNS; connector search returned no open PRs.
- Files: Updated src/fdtd/error_analysis.py, src/fdtd/error_analysis_helpers.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md. No added modules or changes to source equations, solver, plotting, tests or existing full-size outputs.
- Change and reason: The 119-line entry point mirrors fdtd_3d.py with Parameters, Comparison equations, and Run and export sections. A short run_analysis calls prepare_comparison, compare_fields and save_analysis. The main mathematical guide states the sample cube, reference-size inequality, return time, strict rounding, half-step reserve and norm. The existing helper holds the implementation in geometry/time, field comparison, export, and input-check sections. Existing mathematical functions remain importable from the entry point; controls, outputs and shared setup behavior are retained.
- Verification: All 18 existing tests pass with the sci interpreter, including actual PNG/GIF/data generation. Before/after current custom and pulse source cases, each with PML-2 and PEC-only small domains on 12x14x16 grids at 5 ns plus enlarged references, exactly match all 14 NPZ arrays per case. Metadata matches except measured runtimes. Evidence is under /private/tmp/capstone-analysis-driver-style/before/ and after/. SHA-256 comparisons confirm fdtd_3d.py, yee_solver.py, plot_fields.py and the saved full-size error artifacts are unchanged. Both edited modules parse and pass whitespace checks; updated documentation links and scoped git diff --check pass.
- Limitations: This verifies refactoring equivalence for these cases, not a new accuracy study. The large experiment was not rerun. Status now distinguishes its older source from the currently observed source changes recorded at task start.
- Next: Xiaodi can edit the Parameters section and run error_analysis.py as before; the detailed formulas and calculations are available in the helper when needed.

## 2026-11-13T23:48:51-05:00 | simple-analysis-rewrite-start

- Changed by: Codex, following Xiaodi's explicit request to delete the existing error analysis and helper and replace them with straightforward code using fdtd_3d.custom_current.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; staging empty; source/solver/GIF and prior plot changes preserved. Fetch failed due to DNS; connector returned no open PRs.
- Files: Planned replacement src/fdtd/error_analysis.py, deletion src/fdtd/error_analysis_helpers.py, adaptation src/tests/test_error_analysis.py, small plot documentation update src/fdtd/plot_fields.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md.
- Change and reason: Use one explicit cubic-domain experiment with the custom current directly, recognizable domain/time formulas, raw Yee differences, and plots in plot_fields. Remove the generic case-planning/helper interfaces rather than hiding them behind a short wrapper.
- Verification baseline: Backed up the superseded analysis/helper/test modules under /private/tmp/capstone-simple-analysis-rewrite/. Generated custom-current 12^3, 5 ns PML-2 and PEC comparison baselines there, with extra reference/check padding 2 cells. Saved hashes of fdtd_3d.py, yee_solver.py, plot_fields.py and existing default artifacts. The current source matches the newer form recorded in the preceding task; no additional source change is inferred.
- Next: Write the single-file replacement, remove the helper, adapt numerical checks and compare with the recorded baselines.

## 2026-11-13T23:52:08-05:00 | simple-analysis-rewrite-complete

- Changed by: Codex, carrying out Xiaodi's explicit deletion/replacement request.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; no staging, commit, push or external messages. Prior unrelated edits remain preserved; remote fetch failed due to DNS and connector search returned no open PRs.
- Files: Replaced src/fdtd/error_analysis.py and src/tests/test_error_analysis.py; deleted src/fdtd/error_analysis_helpers.py. Updated the producer-name docstring in src/fdtd/plot_fields.py, plus README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md. Source and solver code were not changed.
- Change and reason: Replaced the old generic analysis/helper with one 202-line direct cubic experiment. It explicitly passes fdtd_3d.custom_current, reads the shared grid/material/PML setup, calculates h, b, B, dt and the strict last safe step, crops six Yee components with explicit slices, runs the three boxes in one loop and subtracts fields directly. It uses one small norm function and temporary snapshots to keep RAM bounded. All rendering remains in plot_fields.py. Constants remain editable; source selection, rectangular-box planning and generic helper APIs have been removed. A further reference check is always run, and its measured differences are printed/plotted.
- Verification: Eight adapted tests passed using the sci interpreter, including direct custom-current use when USE_CUSTOM_CURRENT=False, actual three-domain PNG/GIF/NPZ/JSON export, manufactured matching Yee coordinates, strict rounding equality, signed norms, solver fixed-step/CFL behavior and second-order magnetic time centering. For 12^3, 5 ns custom-current PML-2 and PEC cases with 2 extra cells at each reference stage, all 14 NPZ arrays per case exactly match pre-rewrite baseline arrays. Evidence: /private/tmp/capstone-simple-analysis-rewrite/before/ and after/. Measured PML E/H peak differences were approximately 0.02470744/0.02520338, with reference changes 3.33690394e-10/2.27266982e-10. PEC differences were approximately 0.04601378/0.04512760, with reference changes 8.55019641e-12/5.82160025e-12.
- Artifact and preservation checks: Inspected the generated small-run history and field-comparison PNGs; labels/panels are readable. The test verified GIF frame count and snapshot cleanup. SHA-256 checks confirm fdtd_3d.py, yee_solver.py and saved default artifacts are unchanged; plot_fields differs only by the documented producer name. Syntax, whitespace, documentation links, helper deletion and absence of imports from the removed module were checked.
- Limitations: The replacement intentionally supports centered cubic equal-spacing grids and the declared compact custom source. The travel-time estimate is a continuum bound checked numerically using the larger reference, not proof of zero discrete contamination. The 90^3 full-size run was not rerun or overwritten. These experiments do not measure common mesh/source discretization error.
- Next: Edit the current in fdtd_3d.py and the few analysis constants, then run error_analysis.py to regenerate its plots/data.

## 2026-11-14T00:24:39-05:00 | minimal-analysis-controls-start

- Changed by: Codex, following Xiaodi's request to keep only necessary analysis controls.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; existing edits preserved. No publication authorized.
- Files: Planned src/fdtd/error_analysis.py, src/fdtd/plot_fields.py, src/tests/test_error_analysis.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md.
- Change and reason: Retain sampling stride and one reference-padding increment. Reuse fdtd_3d stopping time/field/GIF speed, fix the existing 1.5 dt reserve, derive the sample interior from PML, and use fixed plotting defaults. Merge the two equal extra-padding settings to preserve default reference sizes; remove duplicate overrides and output switches.
- Verification baseline: Backed up edited modules and generated current custom-source 12^3 PML/PEC comparison artifacts with 5 ns and 2-cell reference increments under /private/tmp/capstone-analysis-minimal-controls/before/. Captured protected-file hashes.
- Next: Simplify controls, run numerical/export checks and compare the saved arrays.

## 2026-11-14T00:26:06-05:00 | minimal-analysis-controls-complete

- Changed by: Codex, implementing Xiaodi's request to retain only necessary controls.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; no staging, commit, push or external messages. Remote fetch failed due to DNS; connector returned no open PRs. The pre-existing fdtd_3d_current.gif is now 6883944 bytes, differing from the earlier observed working-file size; authorship is unknown and it was not edited in this task.
- Files: Updated src/fdtd/error_analysis.py, src/fdtd/plot_fields.py, src/tests/test_error_analysis.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md.
- Change and reason: The analysis parameter block contains only SAMPLE_EVERY=10 and REFERENCE_PADDING=8. The latter merges the previous equal extra-reference/check increments while retaining the default domain sizes. Stopping time follows fdtd_3d; reserve is fixed at 1.5 dt; trim follows PML width with one-cell minimum. Plot sampling defaults remain z/xy/0/(0.4,0,0), with the same PNG/GIF output and standard folder. Removed the time override, interior-margin setting, adjustable safety count, separate padding counts, separate plot constants, animation switch and output-directory constant. The plotting function now supplies its previous default sample arguments; no solver or source changes.
- Verification: Eight tests passed, including equality rounding under the fixed reserve and actual custom-current three-domain export. Current custom-source 12^3, 5 ns PML/PEC runs with 2-cell reference increments matched all 14 arrays exactly, and metadata, both PNGs and the GIF were byte-for-byte identical before/after. Evidence: /private/tmp/capstone-analysis-minimal-controls/before/ and after/. Protected-file hashes confirmed source, solver and saved default outputs were preserved. Syntax, whitespace, documentation links, exactly two top-level controls and removal of obsolete control references were checked; scoped git diff --check passed.
- Limitations: No new field-accuracy study or full 90^3 run was performed. The defaults preserve the tested calculations; centered-cube/custom-support assumptions remain.
- Next: Change SAMPLE_EVERY or REFERENCE_PADDING for the comparison; edit shared physics/time/E-H display settings in fdtd_3d.py.

## 2026-11-14T00:30:07-05:00 | final-time-comparison-start

- Changed by: Codex, following Xiaodi's request for substantially simpler code and readable saved plots; Xiaodi explicitly selected final-time field comparison instead of time histories.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; existing edits preserved; no publication authorized. Fetch failed due to DNS. The current fdtd_3d grid is 50^3, while existing error-analysis output metadata still describes 90^3. Authorship of the intervening grid edit is not inferred; the 50^3 setup will be preserved and used.
- Files: Planned src/fdtd/error_analysis.py, src/fdtd/plot_fields.py, src/tests/test_error_analysis.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md, plus new root-level src/outputs/error_analysis PNG/PDF/CSV artifacts.
- Change and reason: Remove the history/callback/snapshot machinery and generic result records. Calculate the reference geometry explicitly, run three domains, crop final Yee fields, calculate relative norms at T, and render a large final-time comparison in plot_fields.py. No new helper module.
- Verification baseline: Saved old modules and current custom-source 12^3 PML/PEC, 5 ns history outputs under /private/tmp/capstone-final-time-comparison/. Their final absolute difference/reference norms provide an independent baseline for the changed final-time normalization. Captured source/solver/GIF hashes.
- Next: Implement, verify the final comparisons, run the current 50^3 setup and visually inspect the actual saved PNG/PDF.

## 2026-11-14T00:35:23-05:00 | final-time-comparison-complete

- Changed by: Codex, implementing Xiaodi's explicit final-time selection and request for concise code and readable plots.
- Recorded by: Codex.
- Context: Local main at dca455d; no commit, push or publication. Existing source/grid/solver/GIF edits preserved.
- Files: Rewrote src/fdtd/error_analysis.py and the error plotting section of src/fdtd/plot_fields.py; adapted src/tests/test_error_analysis.py; updated README.md, src/README.md, docs/PROJECT_STATUS.md and this docs/TIMELINE.md. Generated ignored src/outputs/error_analysis.png, error_analysis.pdf and error_analysis.csv. The deleted helper remains absent; older history artifacts remain untouched.
- Change and reason: The 107-line analysis reads fdtd_3d constants directly, computes the sample/reference geometry and strict time limit, runs three solves, copies final native Yee samples and computes relative norms. One parameter remains: REFERENCE_PADDING=8. Removed history arrays, callback/snapshot machinery, generic records and configuration dictionaries. Errors now use the reference norm at T, rather than the peak norm over the time history. All plotting stays in plot_fields.py; the original fdtd plotting functions have identical ASTs to task-start backups.
- Verification: All seven tests passed in the sci environment after the final plot adjustment, including actual custom-current solves/export, strict boundary timing, matching Yee coordinates, signed relative errors, fixed-step CFL checks and second-order H time alignment. Independent 12^3 PML/PEC runs at 5 ns matched the earlier history's final raw difference/reference norms at relative tolerance 2e-14 after normalization conversion. Source, solver and existing fdtd GIF SHA-256 hashes match task-start values. Scoped git diff --check, Python AST parsing and local documentation links passed.
- Configured experiment: Current custom source, small 50^3 PML-8, reference 130^3 PEC and check 146^3 PEC; h=0.04 m, sample cube [-0.68,0.68]^3, reference half-widths 2.6 and 2.92 m, T=12 ns, 195 shared steps, dt=0.0615384615385 ns. Reference return bounds 14.243186865 and 16.3779970742 ns exceed T+0.0923076923077 ns. First-reference last safe step is 229. Total run/export time 45.944250416 s.
- Measured results: Relative final E error 7.978210341746784e-5; H error 0.7831477828834478. Reference/check changes E=6.428968497363356e-15 and H=2.8862405565568895e-11. The large final relative H discrepancy is retained as measured; its cause was not established by this task.
- Plot verification: Visually opened the final 3520x2420 PNG and rendered the one-page 1152x792-point PDF with pdftoppm. Both show legible axes/units, scientific color scales, aligned final Ez/Hz slices, signed differences and full 3D norm summaries. Corrected row spacing before the configured run. CSV agrees with the recorded final errors.
- Limitations: This is a centered-cube, compact-source, uniform-medium boundary/domain comparison. It does not detect common grid/source discretization error or prove exactly zero discrete reflection. Previous 90^3 history outputs are historical and use different source/grid settings and normalization.
- Next: Edit physics/grid/time in fdtd_3d.py and rerun error_analysis.py to refresh all three final-time outputs. The final relative H discrepancy is available for a separate numerical investigation.

## 2026-11-14T00:44:35-05:00 | remove-error-analysis-start

- Changed by: Codex, following Xiaodi's explicit instruction to delete all error-analysis files from this project.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; earlier local changes preserved. Remote fetch failed because github.com could not be resolved. No commit or publication requested.
- Files: Plan to delete src/fdtd/error_analysis.py, src/tests/test_error_analysis.py, analysis bytecode and src/outputs/error_analysis artifacts; remove the analysis-only function in src/fdtd/plot_fields.py and references in src/fdtd/fdtd_3d.py, README.md and src/README.md; update docs/PROJECT_STATUS.md and this timeline.
- Change and reason: Remove the analysis feature and generated results while preserving the FDTD solver, current settings and standard plotting. Existing timeline history remains as a record of earlier work.
- Next: Apply the requested deletion, inspect remaining files and verify the main modules still import.

## 2026-11-14T00:44:53-05:00 | remove-error-analysis-complete

- Changed by: Codex, at Xiaodi's explicit request to delete all error-analysis project files.
- Recorded by: Codex, working for Xiaodi Zhou.
- Context: Local main at dca455d; no commit, push or publication. Remote fetch was unavailable due to DNS.
- Deleted: src/fdtd/error_analysis.py; src/tests/test_error_analysis.py and its now-empty directory; src/fdtd/__pycache__/error_analysis.cpython-311.pyc; src/outputs/error_analysis.png, error_analysis.pdf and error_analysis.csv; src/outputs/error_analysis/field_comparison.png, field_comparison.gif, error_metadata.json, error_history.png and error_data.npz, followed by their empty directory. The old helper was already absent. Removed stale bytecode for modified fdtd_3d and plot_fields modules.
- Updated: Removed save_final_comparison from src/fdtd/plot_fields.py, analysis references in src/fdtd/fdtd_3d.py comments/docstring, and obsolete instructions from README.md and src/README.md. Updated docs/PROJECT_STATUS.md and appended this timeline. Previous timeline records are retained as history.
- Verification: fdtd_3d, yee_solver and plot_fields import successfully with the sci interpreter. Python syntax and README links pass. Searches find no analysis files or references in src or the READMEs. The source executable AST and retained plotting code are unchanged; solver and standard PNG/GIF hashes match task-start values. Scoped git diff --check passes. No new numerical experiment was needed for this removal.
- Limitations: This cleanup is confined to the selected project; external temporary verification folders and Git history were not altered.
- Next: The active FDTD folder contains fdtd_3d.py, yee_solver.py and plot_fields.py.

## 2026-11-14T00:47:49-05:00 | add-minimal-simulation-time

- Changed by: Codex, working for Xiaodi at the explicit request for a new err_analysis file containing only a time-returning function.
- Recorded by: Codex.
- Context: Local main at dca455d. Existing changes preserved; newly observed deletions of src/fdtd/fdtd_3d_H_pulse_current.gif and src/fdtd/fdtd_3d_current.gif were already present before this task, with unknown authorship. Remote fetch failed due to DNS. No publication requested.
- Files: Added src/fdtd/err_analysis.py; updated docs/PROJECT_STATUS.md, src/README.md and this timeline.
- Change and reason: One function simulation_time(a,b,B,c) returns ((B-a)+(B-b))/c in seconds. The docstring states centered geometry, source start at zero, uniform wave speed and the strict pre-reflection stopping requirement. This is the continuum arrival bound; timestep rounding is not included. No solver, plotting, simulation or extra helper added.
- Verification: Checked the explicit 1-second path-length example and the earlier reference geometry giving 14.243186864961096 ns; AST confirms exactly one function in the new file.
- Next: Await Xiaodi's next incremental instruction.

## 2026-11-14T01:00:08-05:00 | minimal-custom-pml-run-start

- Changed by: Codex, working for Xiaodi on the requested simple PML run returning E and H with fdtd_3d.custom_current.
- Recorded by: Codex.
- Context: Local main at dca455d; existing edits and GIF deletions preserved. Remote fetch failed due to DNS. The on-disk err_analysis timing function still lacks dt, while Xiaodi supplied the desired rounded version in chat; this task applies that supplied version with an accurate docstring.
- Files: Planned src/fdtd/err_analysis.py, src/README.md, docs/PROJECT_STATUS.md and this timeline.
- Change and reason: Add run_fdtd(T,dt) with explicit solver arguments, positive PML width, the custom current, fixed time-step count and final native E/H output. Existing solver already predicts the forward H half-step and averages to T, including PML.
- Next: Execute a PML custom-current run and check source selection, step size, output shapes and values; do not add plotting or helper modules.

## 2026-11-14T01:01:17-05:00 | minimal-custom-pml-run-complete

- Changed by: Codex, implementing Xiaodi's request for a simple PML run returning E and H with custom_current.
- Recorded by: Codex.
- Context: Local main at dca455d; no commit or publication. Remote fetch failed due to DNS; GitHub connector returned no open PRs. Existing source, solver, plot code, outputs and GIF deletions were preserved.
- Files: Updated src/fdtd/err_analysis.py, src/README.md, docs/PROJECT_STATUS.md and this timeline.
- Change and reason: Applied Xiaodi's supplied ceil-based safe-time function with a corrected docstring, then added run_fdtd(T,dt). The new function directly calls yee_solver.solve with fdtd_3d grid/PML values and fdtd_3d.custom_current, fixing the step count to retain dt. It returns electric/magnetic tuples already aligned to T by the existing PML-aware solver. No plotting, new helpers or test files added.
- Verification: Actual current 50^3, PML-8 custom-source run completed in 1.753 s, using 229 steps at T=14.0923076923 ns, dt=0.0615384615385 ns. The timing example used a=0.25, b=0.68, B=2.6 m and the current medium speed; T+1.5dt is below the reference arrival bound 14.243186865 ns. E shapes were (50,51,51), (51,50,51), (51,51,50); H shapes were (51,50,50), (50,51,50), (50,50,51). All components were finite and nonzero. Source callable identity, enabled PML metadata, time and dt were checked with USE_CUSTOM_CURRENT=False and USE_PML=False in memory, then restored. An 8^3 PML-2 zero-current run preserved E=H=0 exactly. Strict timing equality, invalid time/dt, noninteger step counts, unstable CFL and zero PML width checks passed. Syntax, exactly two functions, scoped whitespace and documentation links passed.
- Limitations: No reference-domain solve, error comparison or new numerical-accuracy claim. The caller supplies T and dt; simulation_time uses the stated continuum travel-time estimate and assumptions.
- Next: Use T=simulation_time(a,b,B,c,dt), then E,H=run_fdtd(T,dt). Continue only with Xiaodi's next requested increment.

## 2026-11-14T01:03:18-05:00 | restore-missing-pml-run-function

- Changed by: Codex, following Xiaodi's report that the file had not been updated.
- Recorded by: Codex, working for Xiaodi.
- Context: Inspected the exact project path and searched for duplicate analysis filenames. The sole src/fdtd/err_analysis.py contained Xiaodi's supplied timing function but no run_fdtd, unlike the earlier verified saved content. The intervening writer is unknown; no editor cause is assumed.
- Files: Updated src/fdtd/err_analysis.py and this timeline. Existing timing calculations and formatting were preserved; its stale docstring was corrected. No source, solver or plotting files changed.
- Change and reason: Added the requested run_fdtd(T,dt), using fdtd_3d grid/PML settings, explicit custom_current, fixed step count and final time-aligned E/H tuples.
- Verification: Read the saved file back, parsed both functions and executed a 50^3, PML-8 custom-current run at 12 ns with 195 steps. All six output arrays were finite and nonzero. SHA-256 before/after verification confirmed the saved file stayed unchanged during the check.
- Next: run_fdtd is present in the project file; no publication requested.

## 2026-11-14T01:09:37-05:00 | physical-domain-convention

- Changed by: Codex, recording Xiaodi's explicit request to remember the physical-domain definition for future larger-domain comparisons.
- Recorded by: Codex.
- Files: Updated docs/PROJECT_STATUS.md and this timeline; no computational code or output edits. Saved the requested convention as a separate Codex memory note.
- Decision: Physical domain means the interior inside the PML interfaces, excluding absorbing cells. Compare both runs on this same physical region with matching native Yee positions, spacing and time. The larger reference extends the computational domain without enlarging the comparison region.
- Observed changes: First read showed PML_CELLS=6 and NX=NY=NZ=50. A later source read showed NX=NY=NZ=100 with PML_CELLS=6. These edits were preserved; authorship is unknown. The final snapshot has h=0.02 m and physical half-width b=0.88 m for A=1 m. Stored definitions use b=A-p*h rather than a fixed numerical bound.
- Verification: Read current setup and solver physical_bounds calculation. An initial check assuming the first grid snapshot failed after the grid changed; a direct AST read verified the later 100^3 setting. No simulation was performed. run_fdtd still returns full-grid fields; comparison cropping is not implemented.
- Next: Use this convention for Xiaodi's next requested comparison step.

## 2026-11-14T01:13:22-05:00 | rename-pml-run-return-information

- Changed by: Codex, following Xiaodi's explicit request to rename run_fdtd to fdtd_with_pml and return physical-domain dimensions and information for later comparison.
- Recorded by: Codex.
- Context: Local main at dca455d. Existing source/solver/output edits and GIF deletions preserved; the output GIF size has changed since earlier inspections, with unknown authorship. Fetch failed due to DNS; no publication requested.
- Files: Updated src/fdtd/err_analysis.py, src/README.md, docs/PROJECT_STATUS.md and this timeline.
- Change and reason: Renamed the function without adding an alias. Return the existing solver result dictionary instead of only its E/H tuples, retaining physical_bounds, computational coordinates, spacing, cells, timing, material constants and PML settings. Add physical_lengths=physical_bounds[:,1]-physical_bounds[:,0], a three-component array [m] excluding PML. The simulation_time calculation and solver call are unchanged. No cropping or larger-domain comparison implemented.
- Verification: An actual custom-current 10x12x14 rectangular run with two PML cells per face returned physical bounds [-0.6,0.6] x [-1,1] x [-1.5,1.5] m and lengths [1.2,2,3] m, matching the inner PML interface nodes. Grid spacing [0.2,0.25,0.3] m, time 0.5 ns, dt 0.1 ns, five steps, native Yee shapes and finite nonzero E/H all checked. Both example selector flags were temporarily false during this check and restored. Read-back verified exactly simulation_time and fdtd_with_pml definitions; the saved-file hash stayed unchanged during validation.
- Next: Use result=fdtd_with_pml(T,dt), then read electric, magnetic and physical_lengths. Later comparisons must use the same physical region; fields currently cover the full computational grid.

## 2026-11-14T01:19:30-05:00 | fdtd-reference-start

- Changed by: Codex, working for Xiaodi on the requested larger-domain reference without PML.
- Recorded by: Codex.
- Context: Local main at dca455d; existing changes preserved. Current inspected fdtd_3d settings are 105^3, T_END_NS=10, PML_CELLS=10, CUSTOM_DIRECTION=(1,-0.5,1); these differ from earlier observations, with unknown authorship. No source edits planned. Remote fetch failed due to DNS.
- Files: Planned src/fdtd/err_analysis.py, src/README.md, docs/PROJECT_STATUS.md and this timeline.
- Change and reason: Add fdtd_reference(pml_result,B), using the completed PML run's grid, time and material data. Round requested reference half-width outward by whole cells to contain the original centered cube and align Yee samples. Disable PML explicitly, retain custom_current and the original physical comparison region, and reuse the safe-time condition.
- Next: Verify reference geometry, unchanged sampling/time/materials, no PML, safety validation and early-time field agreement on small real runs.

## 2026-11-14T01:20:43-05:00 | fdtd-reference-complete

- Changed by: Codex, implementing Xiaodi's requested larger-domain FDTD reference without PML.
- Recorded by: Codex.
- Context: Local main at dca455d; no commit or publication. Source/solver/plot code and generated outputs preserved.
- Files: Added fdtd_reference to src/fdtd/err_analysis.py; updated src/README.md, docs/PROJECT_STATUS.md and this timeline. No extra module or plotting added.
- Change and reason: fdtd_reference(pml_result,B) requires a centered cubic original grid and B>A, rounds the reference extent outward in whole original cells, and runs custom_current with pml_cells=0. It uses the PML result's final time, steps, CFL fraction and epsilon/mu; the common spacing and timestep are retained. simulation_time validates the reference return-time margin. physical_bounds and physical_lengths identify the unchanged original region of interest; padding_cells records the per-face enlargement. Full reference fields and existing solver metadata are returned.
- Verification: Real early-time custom-current PML/reference pairs on 20^3/24^3 and 21^3/25^3 grids, dt=0.05 ns and T=0.1 ns, verified containment, requested-B outward rounding, PML disabled, source callable identity, matching dt/time/steps/materials, and matching original node/cell-center coordinates within 1e-15 m. Requested B=1.17 m produced B=1.2 and B=1.19047619048 m, respectively. Relative E/H differences over the original physical region were 2.3824937276459202e-15/2.94101556307849e-15 and 1.7752001498541565e-15/2.3123584129683994e-15. Equal/smaller reference size, unsafe final time and noncubic original geometry were rejected before solving. Source settings patched for checks were restored. Saved-file hash/read-back, AST and documentation links checked.
- Limitations: No full-duration reference experiment or error plot generated. Reference walls remain PEC; the existing continuum safe-time estimate is a timing condition, not proof of exactly zero discrete boundary contamination. Custom-current settings must stay the same between runs.
- Next: Call pml_result=fdtd_with_pml(T,dt), then reference=fdtd_reference(pml_result,B). Physical-region extraction/comparison remains for the next requested step.

## 2026-11-14T12:21:53-05:00 | normalized-fdtd-start

- Changed by: Codex, working for Xiaodi on the explicitly authorized normalized-unit conversion and local Git commit.
- Recorded by: Codex.
- Context: Local main at dca455d; no staged changes. Remote fetch failed due to DNS. Local commit authorized; no push requested.
- Observed existing changes: README.md, src/README.md, docs/PROJECT_STATUS.md and this timeline contain prior workflow updates. src/fdtd/err_analysis.py is untracked and contains the three previously requested functions. src/fdtd/yee_solver.py includes fixed-step support and an edited SI permeability. src/fdtd/fdtd_3d.py currently uses 60^3 cells, T_END_NS=10, CFL=0.7, six PML cells, and a windowed sin(pi*t_ns) custom current; its old chirp parameters are unused. src/fdtd/plot_fields.py multiplies the displayed maximum by five. Authorship of intervening parameter/plot edits is unknown; preserve them except where normalization requires a change.
- Existing outputs: src/fdtd/fdtd_3d_H_pulse_current.gif and src/fdtd/fdtd_3d_current.gif are deleted, and src/outputs/fdtd_3d_current.gif is modified, all before this task. Preserve these states and leave generated artifacts outside the code commit.
- Planned files: src/fdtd/yee_solver.py, src/fdtd/fdtd_3d.py, src/fdtd/plot_fields.py, src/fdtd/err_analysis.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this timeline.
- Decision: Use a new normalized example with epsilon=mu=1, c=1/sqrt(mu*epsilon), T=10, custom-source duration 6, frequency 0.5 and amplitude 1. Remove ns/GHz conversions and SI plot labels; retain the Yee/PML algorithms, spacing and time-aligned output. This is not a rescaling chosen to reproduce the former SI experiment.
- Next: Implement the consistent units, verify numerical behavior and plots, and commit the source/documentation locally.

## 2026-11-14T12:25:29-05:00 | normalized-fdtd-verified

- Changed by: Codex, implementing Xiaodi's authorized normalized-unit conversion and local Git save.
- Recorded by: Codex; human owner Xiaodi.
- Context: Local main based on dca455d. GitHub connector returned no open PRs; shell fetch failed due to DNS. No push requested. The local code commit also saves the previously requested fixed-step solver support and three-function err_analysis.py workflow already present at task start.
- Files: Updated src/fdtd/yee_solver.py, src/fdtd/fdtd_3d.py, src/fdtd/plot_fields.py, src/fdtd/err_analysis.py, README.md, src/README.md, docs/PROJECT_STATUS.md and this timeline. Generated ignored verification PNG/GIF under src/outputs/normalized_verification/. Preexisting tracked GIF edits/deletions listed in normalized-fdtd-start remain untouched and excluded from the commit.
- Change and reason: MU0=EPSILON0=1 and C0=1/sqrt(MU0*EPSILON0); solver CFL continues to use the actual epsilon and mu. Source/run settings now use normalized time directly, with T_END=10, CUSTOM_DURATION=6, CUSTOM_FREQUENCY=0.5 and CUSTOM_AMPLITUDE=1. Removed ns/GHz conversions, unused chirp parameters and SI labels. The custom source retains the existing windowed sine form and direction. Optional pulse/wire currents also use normalized time. PML strength is automatically recalculated from normalized impedance and thickness. The analysis wrapper explicitly passes the common material constants; reference c uses their square root. No changes to Yee/PML updates, output time centering, comparison geometry, or the existing factor-five plot scale. Updated unit documentation and removed references to the previously deleted API document.
- Numerical verification: Using the sci Python interpreter, 12^3, T=1, 40-step PEC/PML-2 runs were bitwise equal to the pre-edit solver when both were given normalized constants. Equivalent SI runs with scaled sources/units agreed in E/H/rho with relative errors [3.19e-16,4.82e-16,1.67e-16] for PEC and [4.58e-16,7.37e-16,1.67e-16] for PML. PML conductivity scaling and the PEC Gauss residual passed. A 10^3 zero-source run with epsilon=4, mu=9 used c=1/6 and two steps to T=0.7, with exactly zero E/H and the expected PML strength.
- Wrapper verification: PML/reference 20^3/24^3 runs at T=0.02, dt=0.01 retained identical physical bounds, material/time data and grid spacing; early physical-domain E/H relative differences were 2.36e-15/2.91e-15. PML/custom current stayed enabled in the wrapper with example selector flags false. Strict timing rounding and rejection of an unsafe reference passed.
- Full run and plots: The current 60^3, PML-6 physics setup reached T=10 in 743 steps, dt=0.0134589502, with finite E/H and physical bounds [-0.8,0.8]^3. Maximum physical-interior Gauss residual was 4.29e-15. A temporary in-memory frame stride of 20 produced a 1500x1200 PNG and a 39-frame 900x720 GIF; saved FRAME_EVERY remains 1. A separate 12^3 H run at T=1.5 exported both formats. Inspected E/H PNGs and an active-source GIF frame; normalized titles/axes are correct. The final E image is nearly dark because its field is weak relative to the preserved global color scale. Output rendering is not evidence of field accuracy.
- Other checks: All four modules parse; README/status links and git diff --check pass. Reviewed executable AST differences against task-start backups; solver update formulas are unchanged. No new helper modules, test suite or analysis plots were added.
- Limitations: This is a new normalized experiment, not the original SI experiment with the same physical parameters. No convergence study or full-duration large-reference comparison was performed. Standard prior output GIFs were not regenerated; verification artifacts are separate.
- Next: Save these eight source/documentation paths in the requested local commit; future physical-domain extraction/error comparison remains a separate user-directed step.

## 2026-11-14T12:52:49-05:00 | clearer-field-animation-start

- Changed by: Codex, working for Xiaodi on the request to make oscillations, changes and vector lengths visible in the GIFs.
- Recorded by: Codex; human owner Xiaodi.
- Context: Local main at 4f8a15d. No staged changes; remote fetch failed due to DNS, and the GitHub connector returned no open PRs. No push requested.
- Observed existing changes: src/fdtd/fdtd_3d.py now uses 50^3 cells, CUSTOM_AMPLITUDE=10 and phase=3*pi*CUSTOM_FREQUENCY*t; authorship is unknown. Preserve these source/solver settings. The two old GIF deletions under src/fdtd/ remain, and src/outputs/fdtd_3d_current.gif is modified (620 frames, 900x720). Existing outputs and plot_fields.py were backed up under /private/tmp/fdtd-visual-before-20261114 before replacement.
- Files planned: src/fdtd/plot_fields.py, src/README.md, docs/PROJECT_STATUS.md, this timeline, and regenerated src/outputs/fdtd_3d_current.png/.gif. Solver, source and analysis calculations will remain unchanged.
- Findings and plan: Magnitude slices hide sign reversals; the factor-five maximum and global arrow cutoff suppress visible motion. Use a selectable signed component (default z) on a fixed symmetric-log color scale, remove the inflated maximum, and rescale thicker arrows per frame with an explicit label and actual peak-amplitude readout. Keep the existing four-panel layout and avoid extra helper modules.
- Next: Verify signed/zero/weak fields and unchanged field data, regenerate the actual run, and inspect early, late and opposite-sign frames.

## 2026-11-14T13:02:48-05:00 | clearer-field-animation-complete

- Changed by: Codex, implementing Xiaodi's visualization request; recorded by Codex for Xiaodi.
- Context: Local main based on 4f8a15d. Local plotting/documentation save only; no push. Source amplitude changed independently from 10 to 100 while the task was active; authorship is unknown. That change was preserved and the final export reran the amplitude-100 source. The earlier 50^3 grid and phase=3*pi*CUSTOM_FREQUENCY*t edits were also preserved.
- Files: Updated src/fdtd/plot_fields.py, src/README.md, docs/PROJECT_STATUS.md and this timeline. Regenerated src/outputs/fdtd_3d_current.png and src/outputs/fdtd_3d_current.gif. No AI edit to src/fdtd/fdtd_3d.py, src/fdtd/yee_solver.py or src/fdtd/err_analysis.py. The existing deletions of src/fdtd/fdtd_3d_H_pulse_current.gif and src/fdtd/fdtd_3d_current.gif remain untouched. Generated artifacts and independent source changes are excluded from the local plotting commit.
- Change and reason: Removed the factor-five display maximum. SLICE_COMPONENT selects x/y/z (default z); slice data now retain sign, with red positive, blue negative and white zero. All frames share one symmetric-log color scale and readable fixed ticks, preserving amplitude interpretation while revealing weaker fields. Three-dimensional vectors use denser samples, thicker arrows and length=ARROW_LENGTH*min(box_lengths)*sqrt(|F|/sample_peak) in each frame; their directions are unchanged. Labels identify this scaling and report the actual max|F|. Plotting remains in one module with the existing four-panel output, and the solver's field calculations/time alignment are unchanged.
- Verification: Known native-Yee E/H fields checked positive/negative signed slices, exactly zero fields, sign reversal of arrow directions, weak-vector visibility, immutable input fields and fixed color normalization. A quarter-strength vector has half the drawn length, as required by the square-root display scale. Both E and H exported short verification PNG/GIF files successfully. Syntax, documentation links and git diff --check passed. Source/solver/analysis hash checks detected only the independently changed source amplitude; the final source snapshot stayed unchanged during its run.
- Actual regeneration: /Users/mark/miniconda3/envs/sci/bin/python ran the current 50^3, PML-6, amplitude-100 source through fdtd_3d.main(), T=10, CFL=0.7, 619 steps, dt=0.01615508885298869. All E/H components were finite. The output GIF has 620 frames at 900x720 (39,237,776 bytes); PNG is 1500x1200 (184,524 bytes). Final E component absolute maxima were [0.2393556919001619, 0.161234331473353, 0.23935569190016132]. Total final run/export time was 204.44 seconds. Environment: NumPy 2.4.3, Matplotlib 3.10.8, Pillow 12.1.1.
- Visual verification: Inspected the original GIF, representative previews, saved GIF frames at t=1.002 and 3.328 showing opposite signs, and the final PNG at T=10. Weak late fields and vector directions are visible; colorbar labels do not overlap. Interim renders were stopped after review to refine arrows/ticks and incorporate the changed source amplitude; temporary rendering preserved the prior complete output until successful replacement. Original output backups remain under /private/tmp/fdtd-visual-before-20261114.
- Limitations: Arrow lengths intentionally use a nonlinear, per-frame display scale; compare fixed color values and the max|F| readout for absolute amplitudes over time. This is visualization validation, not a new convergence or physical-accuracy study.
- Next: Open the standard updated GIF or rerun fdtd_3d.py. Adjust only SLICE_COMPONENT and ARROW_LENGTH in plot_fields.py for the chosen component and displayed arrow size.

## 2026-11-14T14:04:34-05:00 | dark-slice-style

- Changed/recorded by: Codex for Xiaodi's request for black backgrounds and shorter plot labels.
- Files: src/fdtd/plot_fields.py, src/README.md, docs/PROJECT_STATUS.md and this timeline. Blue/black/orange signed colors replace blue/white/red. Short titles remove the peak readout; fixed symlog color values still show amplitudes. Spatial axes use meters under the user's stated unit convention.
- Verification: Rendered PNG/GIF previews using previously verified cached 50^3, amplitude-10 fields; checked zero maps to black and visually inspected active.png. Python syntax and git diff checks passed. No physics calculation or standard output regeneration was performed. Preview files are in src/outputs/dark_preview/.
- Preserved: Independent fdtd_3d.py edits (100^3, PML-15, amplitude 1), existing tracked GIF modifications and two old GIF deletions. No solver/source edits, no push.

## 2026-11-18T17:45:45-05:00 | length-based-pml-paired-runs

- Owner: Xiaodi; actor/recorder: Codex. Base main 28d7e1a. User requests adapting analysis to their length-based PML and adding the next function to run both domains.
- Observed: fdtd_3d.py contains pml_length_to_cells and PML_length; current independent edits set 50^3 and length 0.3. Existing two src/fdtd GIF deletions and src/outputs/fdtd_3d_current.gif modification are preserved. No attribution inferred beyond the user's stated PML change. Remote fetch failed (github.com DNS); remote state not verified.
- Changed: src/fdtd/err_analysis.py recomputes PML cells from current length/settings. Added run_simulations(B, dt), which derives the actual physical interior, rounds reference bounds outward, computes the safe time window and runs both wrappers. Returns final fields and interval metadata; history sampling/error calculation remains next. Updated docs/PROJECT_STATUS.md and this timeline. Solver, source and plotting code unchanged.
- Verification: sci Python, in-memory 12^3/PML-length 0.2 settings, requested B=1.4, dt=0.05; reference 18^3 with actual B=1.5. Window [0.45,2.0], continuum return bound 2.083333333333333. Verified matching spacing/nodes/time, finite custom-current E/H, strict safety inequality, and length conversion despite a deliberately stale PML_CELLS value. Zero-current E/H remained exactly zero in both runs. git diff --check passed. No full configured run or new convergence claim. No push.

## 2026-11-18T17:50:46-05:00 | restore-paired-run-edit

- Codex for Xiaodi: current src/fdtd/err_analysis.py and supplied attachment had reverted to the old PML_CELLS wrapper and lacked run_simulations; cause/actor unknown. Restored the previously verified length conversion and paired-run function while preserving all newly added comparison comments. Reimported saved file and verified a 12^3/18^3 zero-source run, stale-cell override, equal dt and strict time margin. No other source files changed.

## 2026-11-18T17:52:16-05:00 | annotate-paired-run-geometry

- Codex for Xiaodi: annotated run_simulations in src/fdtd/err_analysis.py line by line in Chinese. Named actual pml_length explicitly and documented B > b + pml_length = A; retained direct B > A comparison to avoid floating-point reconstruction. Preserved other working changes. Checked rejection of B=0.9 and B=1.0 for A=1, and a zero-source 12^3/18^3 paired run with equal final time. No full simulation or plot changes.

## 2026-11-18T17:59:20-05:00 | standalone-analysis-entry

- Owner Xiaodi; actor/recorder Codex. Translated run_simulations annotations in src/fdtd/err_analysis.py to English and added main/__main__ so analysis runs without the ordinary simulation/export. Added REFERENCE_HALF_WIDTH=1.5 to src/fdtd/fdtd_3d.py alongside shared parameters. dt follows CFL; T_end follows the reference safety bound. Updated docs/PROJECT_STATUS.md and this timeline.
- Preserved independent source edits and existing GIF modifications/deletions. Observed an additional PML-length print in fdtd_3d during verification; authorship unknown, preserved.
- Verified actual __main__ via runpy with in-memory 12^3, PML length 0.2, requested B=1.4: reference 18^3, dt=0.0673575, observation [0.471503,1.95337], finite E/H, equal spacing/time and strict safety margin. Guards confirmed ordinary fdtd_3d.main and plot export were not called. git diff --check passed. Full configured simulation not run; histories/errors not yet implemented. No push.

## 2026-11-18T18:07:34-05:00 | final-comparison-png

- Codex for Xiaodi: added save_final_comparison to src/fdtd/plot_fields.py and called it from src/fdtd/err_analysis.py main. Saves src/outputs/pml_reference_final.png: matching native Ez xy slices inside the physical region, common linear signed black-centered colors, short labels. No spatial averaging, error calculation or GIF. Updated docs/PROJECT_STATUS.md and this timeline; unrelated work preserved.
- Verification: executed main with temporary in-memory 12^3/PML-length 0.2, B=1.4 settings, reference 18^3. Checked shared node/center coordinates and visually inspected the generated PNG at T=1.95337, z=0.0833. This is a small-grid preview, not a full configured run. git diff --check passed.

## 2026-11-18T18:11:25-05:00 | print-actual-analysis-geometry

- Codex for Xiaodi: added three print statements in src/fdtd/err_analysis.py main for actual PML thickness, reference half-width B and physical half-width b, read directly from solver result metadata. Syntax and git diff --check passed; no simulation rerun for this display-only change. Preserved unrelated edits.

## 2026-11-18T18:15:46-05:00 | relative-error-time-history

- Codex for Xiaodi: updated src/fdtd/err_analysis.py with optional solver callbacks, relative_l2_error, temporary physical-domain PML snapshots and per-step E/H relative errors during the observation window. Both simulations still start at zero. main saves numerical CSV and calls new save_error_history in src/fdtd/plot_fields.py, replacing the final raw-field plot call. Existing final-plot helper/output retained; unrelated source/GIF changes preserved. Updated docs/PROJECT_STATUS.md and this timeline.
- Checks: known 10-percent field scaling gives 0.1, identical fields give zero, zero reference norm gives NaN. On 12^3/18^3 custom-current runs, sampling endpoints/stride matched and final history errors matched an independent final-field crop/norm calculation. No spatial averaging. Final-time E/H alignment remains the solver's responsibility.
- Actual configured run: 50^3 PML / 76^3 reference, actual thickness 0.32, B=1.52, b=0.68, dt=0.0161658; 103 finite samples over [0.43647680350735707, 2.085389172312928]. Final E/H relative errors [7.645353395887044e-06, 4.085793767609731e-05]; peak E/H [1.7532811821045003e-05, 4.085793767609731e-05]. Saved src/outputs/pml_error_history.png/.csv; visually inspected the black-background two-curve plot. No claim of total discretization accuracy or validation against a still larger reference. No push.

## 2026-11-18T18:47:21-05:00 | peak-normalization

- Codex for Xiaodi: src/fdtd/err_analysis.py now collects absolute differences and reference norms, then normalizes by separate E/H maxima over sampled observation times. Added explicit formulas and norm definition in English comments. CSV retains absolute/reference histories. src/fdtd/plot_fields.py uses the new label, preserving independently selected blue/red colors. Updated docs/PROJECT_STATUS.md and this timeline; unrelated source changes preserved.
- Verified small 12^3/18^3 nonzero-source histories against fixed-peak division, known 10-percent scaling and zero-source undefined-relative behavior. Reused the previous full-size diagnostic norms in /private/tmp/pml_norm_diagnostic.npz to regenerate src/outputs/pml_error_history.png/.csv and visually checked the plot. No full FDTD rerun. Peak E/H 6.043785576024414e-6 / 6.523538677579468e-6.
- Scoped diff checks passed. Full diff check reports preexisting trailing whitespace in independently edited src/fdtd/fdtd_3d.py; left untouched. No push.

## 2026-11-18T19:18:56-05:00 | timing-progress-flops

- Owner Xiaodi; actor/recorder Codex. Added src/fdtd/run_metrics.py with print_progress, timed_call, estimate_fdtd_flops and timed_solve. Updated src/fdtd/yee_solver.py with optional step progress hook; fdtd_3d.py and err_analysis.py now use timed solves, and plot_fields.py exposes GIF rendering progress. Updated src/README.md, docs/PROJECT_STATUS.md and this timeline. User's current 100^3/source edits, color changes and tracked GIF edits/deletions preserved; no push.
- Metrics: wall time includes setup/source/callback work; analytic FLOP count includes core update/curl/charge and H alignment arithmetic only, with explicit conventions/exclusions. Reports ordinary solve/export separately, PML/reference separately and paired total. No hardware-throughput claim.
- Verification: 8^3 PEC and PML-2, T=0.1, 4 steps gave bitwise-identical E/H before/after instrumentation; progress sequence was 0..4. Hand-count 2^3 one-step estimates matched 706 PEC / 1984 PML operations (one output). Paired 12^3/18^3, 40-step run completed with per-run metrics. Actual two-frame PNG/GIF export to /private/tmp/fdtd_metrics_preview passed; observed solve+callbacks about 0.001 s and export 0.929 s for this tiny test only. Initial ordinary test used a stale in-memory PML_CELLS after reducing grid size and was rejected correctly; setting the test cell count consistently resolved it. No full configured benchmark.

## 2026-11-19T00:15:32-05:00 | three-step-safety-reserve

- Codex for Xiaodi: changed total safety reserve in src/fdtd/err_analysis.py from 1.5*dt to 3*dt, including the forward H half-step; updated corresponding comments/docstring. Verified strict bound and maximal permissible step for an exact-grid case and the B=5, h=0.025 case. No FDTD rerun or plot regeneration; prior outputs remain from the previous reserve. Three steps are a chosen margin, not proof of absent numerical boundary contamination.

## 2026-11-19T00:24:12-05:00 | pml-field-norm-columns

- Codex for Xiaodi: added pml_L2_E and pml_L2_H to run_simulations results and appended CSV columns in src/fdtd/err_analysis.py. They are unweighted native-Yee PML field norms inside the shared physical region, using the same definition as reference norms. Peak-normalized error formulas unchanged.
- Verified main with in-memory 12^3/18^3 settings; output redirected to /private/tmp/pml_norm_columns_check to preserve existing full-run artifacts. Checked final PML norms against independent final-array sums, all nine CSV columns and existing peak-error formula. No full run or replacement of user's outputs. Scoped diff check passed.

## 2026-11-19T22:34:28-05:00 | log-error-reference-norm-plot

- Actor/recorder: Codex for Xiaodi; branch main, base 28d7e1a. User requested an additional log-scale error/reference norm figure.
- Reconciliation: existing changes in docs/PROJECT_STATUS.md, docs/TIMELINE.md, src/README.md, src/fdtd/err_analysis.py, src/fdtd/fdtd_3d.py, src/fdtd/plot_fields.py, src/fdtd/yee_solver.py, untracked src/fdtd/run_metrics.py, deleted src/fdtd/fdtd_3d_H_pulse_current.gif and src/fdtd/fdtd_3d_current.gif, and modified src/outputs/fdtd_3d_current.gif were preserved. Current analysis safety is 50*dt (user-described edit); other intervening authorship is not inferred.
- Changed src/fdtd/plot_fields.py: added save_error_norms with separate E/H log panels, error and reference norms, dark background, and gaps for zero/nonfinite values. Labels explicitly describe unweighted discrete L2 norms.
- Changed src/fdtd/err_analysis.py: main calls this function, reports its path and includes its time in plot_seconds. Existing error plot/CSV formulas unchanged. Updated docs/PROJECT_STATUS.md and this timeline.
- Verification: parsed both Python files; rendered src/outputs/pml_error_norms.png from the existing 356-row CSV (t=0.17512958165418652..4.957514311441587), and visually checked labels, curves and log axes. No FDTD rerun; no scientific validation of the existing CSV implied. Plot-module diff whitespace check passed.
- Limitations: git fetch failed because github.com could not resolve. No commit or push; next ordinary analysis run generates both figures automatically.

## 2026-11-20T00:03:58-05:00 | spherical-field-extraction

- Actor/recorder: Codex for Xiaodi; main at 28d7e1a. User authorized clean English-commented field extraction and plotting. Existing dirty paths recorded in the preceding entry remain preserved; no attribution of additional intervening edits is inferred.
- Added src/fdtd/field_extraction.py: sphere_points uses CUSTOM_CENTER/RADIUS, validates strict source enclosure and physical containment, generates latitude rings plus one sample per pole. trilinear samples each native Yee component without cell-center averaging or extrapolation; extract_sphere returns Cartesian E/H and geometry at the solver result time. main previews geometry only.
- Updated src/fdtd/plot_fields.py with save_sphere_samples; generated src/outputs/sphere_samples.png with 514 points, R=0.1875 and physical half-width 0.275 from current settings. English comments describe non-equal-area samples and single-snapshot scope. Updated docs/PROJECT_STATUS.md and this log.
- Verified all six staggered coordinate layouts reproduce a multilinear analytic field within 5e-15; unique points, poles, sphere radius, invalid radius rejection and extrapolation rejection passed. Extracted finite (514,3) E/H from an actual 12^3, two-step custom-current PML solve. Generated and visually inspected the configured geometry figure; scoped whitespace check passed. No full configured solve or time-history recording.
- Limitations: snapshot extraction requires unchanged source metadata; surface quadrature weights and history storage are not implemented. Remote access remains unavailable from prior DNS failure; no commit or push.

## 2026-11-20T01:26:51-05:00 | spatial-material-functions-custom-source

- Actor/recorder Codex for Xiaodi, main base 28d7e1a. User explicitly requested material functions in fdtd_3d and only custom_current. Preserved current grid, source formula/parameters, PML settings and unrelated plot/GIF edits. Removed alternative source definitions/settings as authorized.
- Files: src/fdtd/fdtd_3d.py, src/fdtd/yee_solver.py, src/fdtd/err_analysis.py, new src/tests/test_material_functions.py, src/README.md, docs/PROJECT_STATUS.md, docs/TIMELINE.md.
- epsilon/mu callables sampled once on native E/H grids; local division in both PEC/PML updates and H alignment. Positive-real validation, homogeneous PML checks, conservative CFL from material minima, material-array metadata. Default functions return 1. Existing scalar solve calls remain valid. Corrected the custom-current formula comment to match the unchanged implemented waveform.
- Analysis consumes the new material functions and rejects nonuniform material timing instead of using vacuum constants. Its existing 50*dt safety parameter was not changed. Whitespace cleaned in the two edited entry points.
- Verification: four unittest cases pass (six-grid material sampling, local E update/H alignment, div(epsilon E)=rho and div(mu H)=0, zero-loss PML equivalence, uniform scalar/callable equivalence, invalid material/PML/CFL rejection). Compared uniform PEC/PML solutions against pre-edit solver saved temporarily; agreement within 1e-14 relative/1e-15 absolute, new scalar versus callable bitwise equal.
- Integration: 12^3 ordinary PNG/GIF export to /private/tmp/material_function_check; 152-step uniform 12^3/36^3 analysis pair; 20-step heterogeneous nonzero-loss PML finite; sphere extraction compatible; nonuniform analysis guard verified. Scoped diff whitespace checks pass. No configured 90^3 rerun, no claim of dielectric-interface convergence.
- Remote still inaccessible from earlier DNS failure. No commit or push. Next: define/test an actual dielectric geometry if requested.

## 2026-11-20T01:50:22-05:00 | both-fields-single-solve

- Actor/recorder Codex for Xiaodi; branch main, base 28d7e1a. User requested E and H plots together. Preserved current material/source/grid settings and unrelated changes.
- Changed src/fdtd/fdtd_3d.py to record both fields in one solve and export separately; main returns paths keyed by E/H. Changed src/fdtd/plot_fields.py to use distinct fdtd_3d_E and fdtd_3d_H PNG/GIF names. Updated status and this timeline.
- Verified an in-memory 12^3, two-step uniform PML run in /private/tmp/fdtd_both_fields: four distinct readable artifacts, both GIFs three frames. Scoped whitespace check passed. No configured large simulation, no removal of previous outputs, no commit or push.

## 2026-11-20T03:18:14-05:00 | dielectric-bunny-example

- Actor/recorder Codex for Xiaodi; main base 28d7e1a. Added requested separate bunny entry point. Observed existing 90^3, T_END=2, PML length .4, sphere epsilon6 settings and deleted old output GIF; authorship of intervening edits unspecified, preserved all. Other dirty paths remain as previously logged.
- Added src/fdtd/fdtd_3d_complex_geometric.py, src/fdtd/assets/bunny.off and assets/README.md. Closed libigl tutorial mesh, native E-grid containment masks, epsilon4/mu1, source outside bunny, one-cell homogeneous collar. Reuses shared setup without mutating it or changing solver.
- Added save_dielectric_geometry to src/fdtd/plot_fields.py; generated src/outputs/bunny/bunny_geometry.png and visually checked. Updated src/README.md, docs/PROJECT_STATUS.md and this timeline. E/H exports are separate in bunny output directory.
- Installed trimesh5.2.1 and rtree1.4.1 in sci after sandbox networking failed; approved escalated download/install succeeded. Git fetch failed DNS; no commit/push.
- Validation: downloaded mesh has 3485 vertices/6966 faces, watertight positive volume. Known-box inside/outside epsilon check passed. In-memory 40^3, PML8, T=.15, source radius .08 test completed eight steps with finite nonzero E/H, both epsilon values and four readable PNG/GIF artifacts in /private/tmp/bunny_fdtd_check. PML placement rejection passed. Four existing material unittests passed. Scoped whitespace check passed.
- No full90^3 solve, interface convergence or scattering accuracy claim. The preview is a smooth mesh; numerical material remains staircase sampled.

## 2026-11-20T03:31:22-05:00 | bunny-field-overlays

- Codex for Xiaodi; main base 28d7e1a. User requested clearer bunny shape in E/H plots. Observed BUNNY_EPSILON now 2 (intervening authorship unspecified); preserved this and other settings.
- src/fdtd/plot_fields.py: optional slice_center sampling with recorded exact coordinates; translucent mesh in vector panel, gold true mesh-plane intersections in slices, physical-region limits for bunny, brighter bunny vectors and dark export style. src/fdtd/fdtd_3d_complex_geometric.py passes bunny-centered slices and mesh metadata for rendering only. Solver unchanged. Updated docs/PROJECT_STATUS.md and this timeline.
- Verified 40^3, PML8, T=.8, 40-step small run; four readable outputs, five frames per GIF in /private/tmp/bunny_overlay_check. Visually inspected E PNG. Constant-field and default/custom slice-coordinate checks passed; scoped diff check passed. Initial section-path method required unavailable networkx; replaced with direct mesh-plane segments, no added dependency.
- Full configured run and existing outputs not regenerated. Mesh outline is continuous input geometry, not the exact staircase material boundary. No commit/push.

## 2026-11-20T10:59:38-05:00 | publish-src-authorized

- Actor/recorder Codex for Xiaodi; main base 28d7e1a. User explicitly requested pushing src files to GitHub. Remote fetch succeeded with network permission; origin/main equals local base, no unpublished prior commits.
- Publishing current src/README.md, src/fdtd/err_analysis.py, fdtd_3d.py, plot_fields.py, yee_solver.py, field_extraction.py, run_metrics.py, fdtd_3d_complex_geometric.py, assets/README.md, assets/bunny.off and src/tests/test_material_functions.py, plus existing deletions of src/fdtd/fdtd_3d_H_pulse_current.gif, src/fdtd/fdtd_3d_current.gif and src/outputs/fdtd_3d_current.gif. Include accumulated docs/PROJECT_STATUS.md and docs/TIMELINE.md per project recording rules. Ignored generated outputs remain local.
- Observed current grid120^3, T_END1.5, reference half-width1.5, bunny epsilon2; preserved intervening edits without assigning authorship. All four material unittests pass, Python syntax parse passes, diff whitespace check passes. Prior smoke/plot checks remain documented above; no full current run. Analysis still homogeneous-only, safety50dt (older three-step docstring is stale).
- Source/mesh publication authorized by this request. No history rewriting or force push.

- Publication validation clarification: staged full-tree whitespace check flagged trailing spaces in the unchanged upstream bunny.off asset. Python/Markdown whitespace checks pass; retained the asset byte-for-byte to preserve its recorded SHA-256. Commit 09af488 contains the authorized source changes.

## 2026-11-24T17:23:19-05:00 | direct-retarded-integration-start

- Actor/recorder: Codex for Xiaodi; main, base 364f842. User requested a simple latitude/longitude, spacetime-Green-function implementation in near-to-far-field.py, with an explanation and numerical checks.
- Reconciled and preserved preexisting edits in docs/PROJECT_STATUS.md, docs/TIMELINE.md, src/README.md, src/fdtd/err_analysis.py, src/fdtd/fdtd_3d.py, src/fdtd/plot_fields.py, and untracked src/fdtd/freq.py and src/tests/test_nonuniform_analysis.py. Current saved grid is now 150 cells/axis (previous record: 90); T_END=1.5, uniform material defaults, source radius .05, PML length .4. Intervening authorship is unknown. Analysis safety/comment discrepancies remain unrelated and untouched.
- Read repository instructions/records, current native extraction, callback/time-alignment contracts and the local theory guide's explicit E/H kernels. Saved temporary pre-task copies. git fetch failed because github.com could not resolve; the GitHub connector returned no open PRs. No staged changes or publication.
- Updated docs/PROJECT_STATUS.md with the authorized local task. Plan: full surface histories with area weights, causal delayed sampling and explicit Maxwell kernels; PNG plotting in plot_fields.py; analytic dipole convergence and a small actual FDTD check. Current 150^3 production settings will not be reduced on disk.

## 2026-11-24T17:31:29-05:00 | direct-retarded-integration-implemented

- Actor/recorder: Codex for Xiaodi; main, base 364f842. Added src/fdtd/near-to-far-field.py and src/tests/test_near_to_far_field.py. Added only save_exterior_fields to src/fdtd/plot_fields.py; updated src/README.md, docs/PROJECT_STATUS.md and this timeline. Existing fdtd_3d.py, yee_solver.py, err_analysis.py and field_extraction.py match saved pre-task bytes; all preexisting plotting code is preserved.
- Implementation: reuse native Yee trilinear interpolation and already time-aligned H. Record every solver step, retaining sphere histories rather than full-volume histories. Latitude patch weights sum to 4*pi*R^2; extra north/south samples have zero integration weight. Use Js=n cross H, Ms=-n cross E and normal-trace equivalent charges in the full retarded E/H kernels. Time derivatives use second-order differences, delayed values use linear interpolation; zero prehistory and explicit rejection of unrecorded future data. Homogeneous exterior/collar checks precede the solve. No Fourier transform, spherical modes, unknown-current equation or two-way boundary coupling.
- Verification: eight unittest cases passed in 6.082 s with /Users/mark/miniconda3/envs/sci/bin/python. Analytic dipole at (.07,-.04,.03), p(t)=(1,-.4,.7)*sin(pi*t/4)^4 on 0<t<4, sphere R=.5, observers (1.2,.2,.3) at 3.1 and (2,-.7,.3) at 4.2, epsilon=mu=1: largest relative E/H error .0182369/.00443707/.00112565 for 8x16/16x32/32x64 at dt=.005. At 32x64, temporal refinement dt=.08/.04/.02 reduced maximum error .0111518/.00352044/.00167740. Nonunit epsilon=2.25, mu=4 check passed with appropriately scaled pulse/time.
- Independent FDTD comparison: same custom-current formula with source radius .12 in memory only, [-1,1]^3, T=1.4, CFL=.7, PML thickness .25, sphere R=.45 with 24x48 quadrature and probe (.62,.11,.07). Relative time-L2 E/H trace errors were (.0335697,.0453143) for 24^3 and (.0108018,.00986297) for 48^3. Tests also check areas/poles, causal zero output, invalid observation locations, missing future history, heterogeneous enclosure and actual callback recording independent of visualization stride.
- Actual configured entry point completed: 150^3, source radius .05, duration 1, frequency .5, direction (1,-1,1), epsilon=mu=1, PML length .4 and target 1e-10, T_END=1.5, 279 steps, dt=.005376344086021506. Recorded 280x514x3 arrays per field on R=.325 and reconstructed point (2,0,0) for t=[1.675,3.175]. Observed inclusive solver+callback time 147.580 s and integral .062 s; estimated core arithmetic 160,084,969,560 operations is not a hardware measurement.
- Generated local src/outputs/near_to_far_field/surface_history.npz (6,943,054 bytes), exterior_fields.npz, near_to_far_field.png and sphere_samples.png. All numeric arrays finite, weight sum agrees with sphere area, both PNGs opened and visually checked. Changed component line styles so overlapping Hy/Hz remain identifiable, then regenerated the field PNG from saved data without rerunning FDTD. Reloaded NPZ with allow_pickle=False and reproduced exterior arrays exactly. AST parsing and working-tree whitespace checks passed.
- Limits: this is a known-data exterior representation; numerical PML/extraction/time/quadrature errors remain. Material checks are sampled and cannot establish homogeneous continuation beyond the computational box. These tests do not certify a global error bound for the configured 150^3 run. Matplotlib used a writable temporary cache after sandbox cache warnings; both image exports completed. Remote fetch restriction remains as recorded at start; no staging, commit or push. Next: user review of the direct baseline and optional angular/time refinement using its reusable histories.

## 2026-11-24T17:32:45-05:00 | concurrent-parameter-edits-observed

- Recorded by Codex for Xiaodi; main, base 364f842. Final byte-preservation audit detected external edits made after the successful pre-export comparison. Authorship is unknown and is not inferred from timestamps.
- Observed src/fdtd/fdtd_3d.py: NX/NY/NZ changed from 150 to 180. Observed src/fdtd/err_analysis.py: safety changed from 15*dt to 20*dt. Codex did not make either edit and preserved both. Solver, sphere extraction and preexisting plotting functions still match pre-task copies. New/edited task Python files parse successfully; working-tree whitespace check passed.
- Clarification to direct-retarded-integration-implemented: reported full-run measurements and saved arrays belong to the completed 150^3 configuration (also stored in surface_history.npz), not the now-saved 180^3 configuration. The next near-to-far-field.py invocation reads the new settings; no 180^3 run has been performed. Updated docs/PROJECT_STATUS.md accordingly and informed the user. No additional numerical work or publication is needed for these unrelated parameter edits.

## 2026-11-25T13:03:49-05:00 | near-to-far-publication-start

- Actor/recorder: Codex for Xiaodi; main, base 364f842. User explicitly requested GitHub publication of the new near-to-far-field work; no additional approval is needed for this scoped upload.
- Read rules, current records, branch, recent commits, staged/unstaged changes and all nonignored untracked paths. GitHub connector confirms main still at 364f842 and no open PRs. Sandboxed git fetch failed DNS; approved network access refreshed origin successfully. No pull into the dirty tree.
- Reconciliation: current local grid is now 50^3 with CFL=.9; err_analysis safety remains 20*dt. The new script observer changed to (2,5,10). Intervening authorship is unknown. Preserve all current settings; include the current observer in the authorized new script.
- Preparing only src/fdtd/near-to-far-field.py, src/tests/test_near_to_far_field.py, save_exterior_fields in src/fdtd/plot_fields.py, the corresponding src/README.md section, docs/PROJECT_STATUS.md and docs/TIMELINE.md. Existing local changes to source settings, err_analysis, freq.py, test_nonuniform_analysis.py, other plotting functions and unrelated document sections remain unpublished. Outputs remain local.
- Built an isolated candidate from the current remote-equivalent base to test exactly what will be shared. Existing checked-in dependencies are reused. No files have been published at this point.

## 2026-11-25T13:04:48-05:00 | near-to-far-publication-validated

- Actor/recorder: Codex for Xiaodi; main, base 364f842. The user-authorized publication is limited to src/fdtd/near-to-far-field.py, src/tests/test_near_to_far_field.py, the save_exterior_fields addition in src/fdtd/plot_fields.py, the near-to-far section of src/README.md, docs/PROJECT_STATUS.md and docs/TIMELINE.md. The current script observer (2,5,10) is retained.
- Verification on an isolated tree built from the remote-equivalent base and only these selected changes: all eight near-to-far unittests passed in 3.674 s. Relative direct-FDTD time-L2 E/H errors decreased from (.0373800,.0529839) at 24^3 to (.0123637,.0110114) at 48^3 with existing checked-in source defaults. Analytic angular/time convergence, area, causality and material checks also passed. Existing 120^3/default-material geometry preflight passed; no new full-size simulation. Python parsing and selected-diff review passed.
- The published plotting change adds exactly one 32-line function; other local plot edits, current-spectrum/nonuniform-analysis work, source settings, assets and generated outputs are excluded. Local source hashes match the publication-start snapshot. Status and timeline distinguish past local results from this published source tree.
- Ready for the authorized commit and fast-forward push. Verify the GitHub main head and changed-file list after publication; no force push or history rewriting.
