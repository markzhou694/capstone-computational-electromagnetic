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
