---
name: code-review
description: Review local changes or any two locally available commits against the shared team policy, using supplied requirements and context. Always write a review report. Use for local code review; use pr-review to collect remote PR context and optionally upload GitHub comments.
---

# Code Review

Find consequential defects in local changes. Read
[the team policy](references/review-policy.md) before reviewing. Apply repository
`AGENTS.md` instructions, the bundled Python/C++ rules linked from that policy,
and supplied requirements; report material conflicts.

## Inputs

- **Repository:** Local path; default to the current repository.
- **Target:** Default to the combined staged and unstaged change from `HEAD`,
  plus relevant non-ignored untracked files. Accept staged-only changes,
  selected paths, or two commits in the order **before, after**. Resolve both
  commits to SHAs and compare their trees directly, without substituting a
  merge base. A supplied diff must identify its baseline and available context;
  state limitations when its surrounding code cannot be established.
- **Context:** Optional text/local files with intent, requirements, discussion,
  CI results, constraints, or focus. Read relevant recent `REVIEW_RESULTS*.md`
  reports, including legacy `REVIEW_RESULTS.md`, as prior evidence to recheck.
- **Report:** Optional path; default to a unique
  `REVIEW_RESULTS-<name>-<num>.md` at the repository root, following
  [the report instructions](references/reporting.md). Findings are always saved.
- **Issue limit:** At most **10 topically distinct issues** by default. Use an
  explicitly requested limit instead, including an increase above ten.

Use only local repository objects and supplied context. Do not fetch, inspect
GitHub, or resolve remote requirements. If uncertain about external-library
behavior, consult primary documentation for the relevant version; record the
source or unresolved doubt. Documentation lookup is optional, so offline review
remains possible. Missing commits are an input error, not permission to fetch.

## Workflow
1. Before substantive analysis, select or create the report and verify it is
   writable using [the report contract](references/reporting.md). Stop with an
   explicit error if writing fails; do not finish with an unsaved chat review.

2. Resolve the repository and target; use `GIT_OPTIONAL_LOCKS=0` for local Git
   reads so status/diff operations do not refresh the index on disk.
   Use `git diff HEAD` for combined tracked changes, `git diff --cached`
   for staged changes, and `git ls-files --others --exclude-standard` for
   untracked candidates. Handle an unborn `HEAD` using the empty tree. Exclude
   review outputs, temporary files, and irrelevant untracked artifacts. For
   commit comparisons, use `git diff <before-sha> <after-sha> -- <paths>`.
3. Read the full diff, applicable instructions, requirements, tests, and enough
   surrounding code to trace inputs, state, outputs, errors, and callers.
   Inspect configuration, generated, migration, schema, and dependency changes
   too. Review unchanged code only as needed to establish the change's effect.
4. Read code from the correct snapshot: `git show <sha>:<path>` for a commit,
   `git show :<path>` for staged contents, and working files for local changes.
   Do not assume the current checkout matches a commit or staged snapshot.
5. Evaluate the change against the team policy. Run safe targeted local checks
   only when they are necessary to materially confirm or reject a finding. Any execution must
   leave existing files unchanged; redirect caches/results to temporary paths
   or run against a temporary copy of the reviewed snapshot. Otherwise skip the
   check and explain the limit. Do not install dependencies.
6. Check prior reports, current code, and supplied review discussion for earlier
   issues. Omit resolved issues. Carry still-unresolved issues only by their
   original IDs, grouped by source report filename as described below; do not
   repeat their descriptions or count them as new issues.
7. Select issues under the limit and grouping rules below. Rank by policy
   severity. Be technical, concise, and explicit about uncertainty; do not guess
   or inflate concerns.
8. Write the selected issues to the report and return only its path. If the
   report cannot be written, return a short error.

## Issue limit and grouping

Report at most the requested number of topically distinct issues, defaulting
to 10 **new issues**. Include new unresolved questions and actionable test gaps
in that limit; do not add overflow new issues under other headings. References
to unresolved issues from earlier reports do not consume this limit.

A follow-up after code changes or comment resolutions starts a new review
round with a fresh limit of ten (or the requested limit). Describe only new
issues. Under `Unresolved prior issues`, list earlier unresolved IDs on one
line per original report, for example:
`REVIEW_RESULTS-feature-0.md: Missing validation, Ambiguous units`.
Keep each reference tied to the report that originally described the issue,
rather than duplicating it through later summary reports. Do not list resolved
issues. If code and relevant review context are unchanged since a completed
review, reuse its report without adding more issues. A retry of an interrupted
review continues that same round and its existing limit.

Group similar problems with a shared violated expectation or corrective action
into one named issue. Give a short explanation and a few representative code
locations, rather than one finding per occurrence or an exhaustive location
list. For example: `Names obscure units — e.g. model.py:42 and export.py:18`,
with the concrete impact required by the team policy. Cosmetic preferences
remain excluded. Do not combine unrelated defects solely to fit the limit.

Use a human-readable name of **at most three words** as each issue's ID, such
as `Missing validation` or `Ambiguous units`. Use that name for references and
deduplication; choose distinct names for distinct topics within a report. A
prior issue is identified by its original report filename and ID together.
Preserve legacy IDs when referencing older reports. Do not assign new numbered
IDs such as `CR-001`.

Prioritize the highest-severity and most consequential distinct issues. Group
as you review; once a recurring issue has sufficient evidence, do not spend
resources cataloguing every instance. If more issues remain after grouping,
keep only the highest-priority ones and briefly note that the report is limited
to the selected issues. Do not enumerate the omitted issues. Increase the limit
only when explicitly requested.

## Boundaries

Do not recursively invoke `pr-review` skill.

Preserve existing files, branch, index, and user edits. Do not fix code, format,
commit, push, fetch, or write remote comments. The only existing file that may
be updated is the matching review report under the report contract. New report
files and necessary temporary files are allowed. Never use a source or context
file as the report destination.

This skill can run directly in the active agent. When delegated, use the
configured `code-review` agent described in [agent setup](references/agent-setup.md).
The reviewer does not delegate recursively. Remote collection and publication
belong to `pr-review`.
