# Beyond Computational Boundaries

**Electromagnetic Field Reconstruction via FDTD and Boundary Integrals**

**Group members:** Xiaodi Zhou and Guanlin Wang

This repository is our shared project notebook and collaboration space.
We use separate personal AI accounts, so the files here carry the project
context between sessions. GitHub does not synchronize our private chats.

Shared documents are grouped in **`docs/`**. **`src/` is the home for all
new project code**, including Python and MATLAB files. It currently contains
an explanatory README only; no existing local solver code, results, or old
code history have been imported. Code implementation and publication still
follow the humans' task instructions.

## Repository layout

```text
README.md                 Start here
AGENTS.md                 AI entry point pointing to the shared rules
CLAUDE.md                 Claude entry point pointing to the same rules
docs/
  PROJECT_RULES.md         Human-maintained rules
  COLLABORATION.md         Session and review procedure
  PROJECT_STATUS.md        Current progress, owners, and next steps
  TIMELINE.md              AI-maintained change history
  LITERATURE.md            Reference map
  proposal/
    Proposal_xiaodi_guanlin.pdf
src/
  README.md                Code placement instructions; no solver yet
.github/                   GitHub review ownership and PR template
```

The README and small AI entry points stay at the root for discoverability.
The full collaboration documents live together in `docs/`. GitHub's own
configuration stays in its conventional `.github/` folder.

## What each file does

| File | What to use it for | Who maintains it |
| --- | --- | --- |
| [Project rules](docs/PROJECT_RULES.md) | The shared rules every AI must read and follow | Humans; AI edits only on explicit human instruction |
| [AI entry point](AGENTS.md) | Directs AI tools to the shared rules in `docs/` | Humans; AI edits only on explicit human instruction |
| [Timeline](docs/TIMELINE.md) | What changed, who changed it, why, and what was checked | **AI**, including recording observed human changes |
| [Project status](docs/PROJECT_STATUS.md) | Current scope, task owners, progress, blockers, and next steps | AI updates from verified work and human decisions |
| [Collaboration guide](docs/COLLABORATION.md) | The detailed start/work/handoff procedure for both accounts | AI maintains explanations without changing the rules |
| [Literature](docs/LITERATURE.md) | Relevant papers, their roles, and what has actually been verified | AI updates with checked sources; humans review |
| [Project proposal](docs/proposal/Proposal_xiaodi_guanlin.pdf) | The supplied project scope and four references | Humans approve revisions |
| [Source directory](src/README.md) | Where AI and humans place newly created project code | AI/humans working on authorized coding tasks |
| [CLAUDE.md](CLAUDE.md) | A short pointer directing Claude sessions to the same rules | Humans; AI edits only on explicit human instruction |
| [.github/CODEOWNERS](.github/CODEOWNERS) | Identifies owners and optional reviewers for rules and governance files | Humans; owner approval is not required for merging |
| [PR template](.github/pull_request_template.md) | A checklist for explaining and reviewing a proposed change | AI fills it when preparing a PR |
| [.gitignore](.gitignore) | Allows the shared documents and `src/`; excludes local caches and outputs | Humans approve changes to the publication scope |

`docs/PROJECT_STATUS.md` answers **“Where are we now?”**;
`docs/TIMELINE.md` answers **“How did we get here?”**. Git commits preserve the
exact saved differences. `docs/PROJECT_RULES.md` answers **“What rules must the AI follow?”**

## What Xiaodi and Guanlin need to do

1. Use your own GitHub and AI accounts. Clone this repository and open its
   root folder in your AI tool, or give the AI access through its GitHub
   connector. Read the rules once and review proposed changes.
2. At the start of a session, give the AI the prompt below and your task.
   The AI should inspect the latest shared work, identify the human owner,
   and check for overlaps before editing.
3. Let the AI maintain the timeline and status. You do **not** need to write
   routine timeline entries. If you edit a file yourself, the AI records the
   observed change at its next inspection. Tell it about intent or offline
   work that Git cannot reveal.
4. Review the AI's diff and evidence. You may authorize a direct update to
   `main` or use a task branch and PR. You can merge your own PR without the
   other person's approval; peer review is optional. Local changes are
   invisible to your collaborator until pushed.

## Copy this prompt into either AI account

> I am [Xiaodi / Guanlin]. Read AGENTS.md, docs/PROJECT_RULES.md,
> docs/PROJECT_STATUS.md, docs/COLLABORATION.md, and the recent
> docs/TIMELINE.md entries before working.
> Inspect Git status, diffs, recent commits, and accessible remote branches
> and pull requests. Reconcile any unlogged changes, including human edits,
> without guessing their authorship. Follow the shared rules. Maintain the
> timeline and project status yourself, verify your work, and give me a
> clear handoff. Store all newly created project code under src/. Do not
> edit the human-owned rules or import existing local prototypes unless
> explicitly instructed. My task is: [describe the task].

Codex loads repository `AGENTS.md` instructions when opened in the project;
other tools may need the explicit prompt. Merely pasting the repository URL
does not give an AI access to a private clone or unseen local changes.

## How AI manages the timeline

The AI checks it **at task start, after meaningful changes, before a commit
or PR, and at handoff**. It appends a record containing the person/AI that
made the change, the AI recording it, relevant commit or PR, exact paths,
purpose, verification, remaining limitations, and next step.

Human edits remain attributed to the human when supported by evidence.
Unknown authorship is recorded as unknown. Corrections are new entries;
earlier entries are retained. The AI checks the final Git diff against its
new entries so no changed tracked or nonignored untracked file is omitted.

This is AI responsibility during active sessions, **not a background
service**. It cannot observe unsaved editor buffers or a collaborator's
unpushed files. There is no checker script or CI workflow in this
repository.

## Human control and remaining setup

The two humans own the rules. AI may suggest changes, but may edit a rule
only when a human explicitly directs that specific change. The responsible
human controls publication and merging; a second person's approval is not
required. Direct updates to `main` are allowed when authorized. Force pushes
and deletion of `main` remain blocked. GitHub cannot distinguish a human
from AI using that human's credentials.

See [project status](docs/PROJECT_STATUS.md) for the verified repository setup
state, including Guanlin's collaborator access and review settings.
