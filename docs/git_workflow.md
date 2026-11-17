# Git Workflow

Use the public project repository as the shared source of truth. Keep changes attributable and reviewable; do not create empty commits or claim milestones that have not been completed.

## Branches and commits

- Start each distinct piece of work from the current `main` and use a descriptive branch such as `feature/cleaning`, `feature/sql`, `feature/model`, or `feature/app`.
- Keep commits small and focused. Use an imperative subject that describes the change, for example, `Add outlier handling for age column`.
- Do not commit credentials, private customer data, virtual environments, notebook checkpoints, or large model artifacts. Check `.gitignore` and review staged files before committing.

## Pull requests

- Open a pull request from each feature branch to `main`.
- Explain the problem, the change, and how it was validated. Link relevant project context and call out data, privacy, or model limitations.
- Review the diff, run relevant checks, and resolve discussion before merging. Prefer pull requests over direct pushes to the shared branch so changes can be reviewed and checked.

## Integrating and releasing

- Use `git merge` to preserve branch history when integrating a feature. Rebase is useful for cleaning up a private branch before review, but rewrites commit IDs; do not rebase commits others may already use.
- Tag `v1.0` only after the project scope is complete, the final changes are integrated, and required validation is recorded. Do not tag an interim documentation change as the final release.

Project branch, pull-request, commit, and release targets are cumulative across the project. Meet them through substantive project work rather than empty branches, duplicate pull requests, or artificial commits.
