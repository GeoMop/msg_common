---
name: make-pr
description: Prepare and create a focused pull request from the current repository changes. Use when the user asks to validate changes, create or update a branch and commit, push it, and open a PR with a clear description. Do not include unrelated changes, silently repair substantive failures, or merge the PR.
---

# Make PR

Turn an existing, intended change into a reviewable pull request.

## Inputs

- **Change target:** Current working tree, selected commits, or explicit files.
- **Destination:** Base branch and repository; infer from repository configuration
  only when unambiguous.
- **Optional guidance:** Issue link, title, reviewers, labels, draft status, and
  required validation.

## Workflow

1. Verify repository identity, Git status, current branch, remotes, and
   authentication. Preserve unrelated and untracked user work.
2. Read applicable `AGENTS.md` and inspect the complete intended diff.
3. Confirm that the change is coherent and does not contain secrets, generated
   debris, debug output, or unrelated edits.
4. Run project-required formatting, linting, tests, and other relevant checks.
   If a substantive check fails, report it and stop unless the user separately
   authorizes a fix.
5. Create or select a descriptive non-protected branch when needed.
6. Stage only intended files and create a concise commit. Do not rewrite shared
   history without explicit authorization.
7. Push the branch and create the PR using the repository's configured provider
   and template.
8. Write a PR description containing purpose, approach, validation, risks,
   compatibility or migration notes, and unresolved items.
9. Verify the returned PR URL and remote head/base.

## Boundaries

- The invocation authorizes creating the branch, commit, push, and PR for the
  resolved intended change; ask if scope or destination is ambiguous.
- Do not merge, approve, or enable auto-merge.
- Do not include unrelated changes merely to obtain a clean status.
- Do not claim checks passed unless they were run successfully.

## Output

Return:

1. PR title and URL
2. Head and base branches
3. Commits and files included
4. Checks run and results
5. Risks, skipped checks, or follow-up work
