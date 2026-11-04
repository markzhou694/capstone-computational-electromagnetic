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
