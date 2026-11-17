# MzansiConnect_CapstoneProject-

A collaboration project between five individuals from Shaper's Data Science Program.

## Phase 3: Version Control with Git and GitHub

The project is maintained in the public [MzansiConnect_CapstoneProject- repository](https://github.com/Renitaparumal/MzansiConnect_CapstoneProject-). Work uses focused feature branches and small commits. Pull requests should explain changes and provide a place for review and automated checks before merging. The repository's `.gitignore` excludes Python virtual environments, Jupyter checkpoints, and common trained-model artifacts; data should only be committed when it is permitted to share.

### Git checkpoint questions

- **What is the difference between `git merge` and `git rebase`?** `git merge` joins histories by creating a merge commit (when needed), preserving the branches' original commits. `git rebase` replays commits onto a new base, creating new commit IDs and a linear history. Avoid rebasing commits that others already depend on.
- **Why do teams use pull requests instead of pushing directly to the main branch?** Pull requests provide a place to review changes, discuss tradeoffs, run automated checks, and catch issues before integration. They also document why a change was made and help protect the shared main branch.

### Merge conflict practice

Two practice branches changed the same README sentence differently. Merging them produced a conflict in that line. I resolved it by comparing both versions, keeping the final wording that accurately describes the repository workflow, removing Git's conflict markers, and completing the merge commit. The resulting README retains the checkpoint answers and this resolution note.
