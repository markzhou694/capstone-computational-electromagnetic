# Session and handoff procedure

Read the [root README](../README.md) for the file map and starting prompt.
[PROJECT_RULES.md](PROJECT_RULES.md) is authoritative; root
[AGENTS.md](../AGENTS.md) points AI tools to it. Paths in the procedure below
are relative to the repository root.

## Separate clones and coordinated work

Both contributors use their own GitHub and AI accounts. Start the AI in this
repository's root. It must inspect the shared files and actual Git state.
The following are commands for the **AI** to execute when it has shell access;
the human does not need to perform the routine checks or timeline bookkeeping.

```bash
git status --short --branch --untracked-files=all
git log -8 --date=iso-strict --format='%h %ad %an: %s'
git diff
git diff --cached
git ls-files --others --exclude-standard
git fetch origin
```

Inspect before switching or pulling. If the tree is clean, update `main`
with a fast-forward. Use `xiaodi/<topic>` or `guanlin/<topic>` for parallel
tasks, or work directly on `main` when the human authorizes it. If the tree is
dirty or diverged, preserve the changes and resolve the specific issue;
do not reset/clean/stash automatically. With connector-only access, inspect
the corresponding branch, commits, PRs, and full file contents. Say explicitly
that local edits cannot be inspected from that connection.

Claim the task in `docs/PROJECT_STATUS.md` with human owner, branch, files or
interfaces, progress, and next step. Shared ownership is only visible after
an authorized push. Check open PRs before overlapping edits. Avoid two AI
sessions writing to the same local clone simultaneously.

## Record human and AI work accurately

The AI is the routine timeline editor. Humans can edit project documents
normally and ask the AI to reconcile them. The AI examines differences since
the last recorded point and appends a reconciliation entry before its own
work. It uses evidence for authorship; a commit account by itself does not
say whether a person typed the change or used an AI.

Use this entry structure (replace all placeholders before saving):

```markdown
## YYYY-MM-DDTHH:MM:SS±HH:MM | unique-entry-id

- Changed by: Human or AI; identify known person/tool and any uncertainty.
- Recorded by: AI tool; working for Xiaodi or Guanlin.
- Context: Branch, starting commit, and relevant PR or decision.
- Files: `exact/path`, `another/path`, `docs/TIMELINE.md`.
- Change and reason: What actually changed and why.
- Verification: Commands/checks actually performed and their outcomes.
- Limitations: Missing access, skipped checks, or unresolved issues.
- Next: Concrete next step and owner if agreed.
```

The observation time is not necessarily the original edit time. Local-only
code work must be clearly labeled and recorded in its local workspace;
do not imply its diffs or results are available in this shared repository.
Unsaved or unpushed work cannot be reconstructed without access. If a human
supplies a correction, the AI appends a correction referencing the old entry.

## Finish and share

The AI updates status, appends its own entry, and compares all changed paths
against the new entries. It verifies Markdown links, checks for conflicting
claims, inspects the diff, and runs `git diff --check`. It stages only the
approved files, reviews the staged diff, and commits the records with
the changes. Store newly created source files in `src/`, supporting scripts
in `src/scripts/`, tests in `src/tests/`, and notebooks in `src/notebooks/`
when needed. Shared prose and the timeline belong in `docs/`. There is no
executable timeline checker or CI workflow; do not add one without a task
request to do so.

Before an authorized push, inspect the complete history being sent as well
as the latest files. Never push a branch descended from the earlier local
solver repository: its history contains code even if the current tree does
not. The published documentation repository has its own clean history.

Publish directly to `main` when the human authorizes that action, or open a
PR and use its template. The human may merge their own PR; peer review is
optional. Before a direct push, fetch and integrate any new remote commits
without overwriting work. After main changes, reconcile task branches without
dropping either contributor's entries. Keep the main timeline intact and
append unique task entries with their original IDs/times. At handoff, report
the branch/commit, changes, verification, remaining issues, and next action.

## Rules and GitHub settings

The humans maintain `docs/PROJECT_RULES.md`, root `AGENTS.md`, `CLAUDE.md`,
`.github/CODEOWNERS`, and `.gitignore`.
AI may suggest changes in conversation; it must not apply them on its own.
A human may explicitly direct a specific governance change and have AI
implement it, with the authorization recorded in the timeline. Publication
and merge authority remain with humans; AI review is not permission to push.

Xiaodi explicitly replaced the initial mandatory peer-review policy with
human-authorized direct updates to `main` and optional PR review. No PR,
second-person approval, code-owner approval, or latest-push approval is
required. Main still blocks force pushes and deletion, and the remaining
protections apply to admins. PR conversations must be resolved when using
a PR. The live settings link is in `docs/PROJECT_STATUS.md`. No CI status
is currently required; no workflow has been installed.

The verified accounts are `@markzhou694` (Xiaodi) and `@Lim-miL-Lim` (Guanlin).
Both are listed on each CODEOWNERS line. Guanlin must accept the write-access
invitation before pushing. That invitation does not block Xiaodi's updates.
GitHub does not let a PR author submit an approving review of their own PR,
but the author can merge it because approving reviews are optional here.

Sources checked during initial setup:
[Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[GitHub code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners),
and [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
