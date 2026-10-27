# Review reports

Write to the requested path or default to `REVIEW_RESULTS-<name>-<num>.md` at
the repository root. Use the PR or branch name (sanitized as a filename), or
`YYYYMMDD` when neither is available; increment `<num>` from 0 without collisions.

Read relevant earlier reports as context. Reuse an unchanged completed review's
report; create a new version for a follow-up round. Describe only new issues.
Add an `Unresolved prior issues` section with IDs grouped by original review
filename, one line per file, e.g. `REVIEW_RESULTS-branch-0.md: Missing validation`.
Do not repeat their descriptions or list resolved issues. These references do
not count toward the new-issue limit.

Create the report before analysis to check write access; stop on failure. Never
overwrite an unrelated file or follow a symlink destination. An interrupted
round may update its own report. Preserve sections supplied by `pr-review`.

Briefly identify the reviewed target and prior report, if any. Each issue needs:

- **Name/ID:** A human-readable name of at most three words, plus severity.
- **Locations:** A few representative file + line references.
- **Problem:** Concise evidence, triggering condition, expected behavior, and
  practical impact. Label an uncertain concern as a question, not a defect.
- **Direction:** (optional) A short recommended correction, without applying it.

If there are no new issues, say so. Include only limitations needed to interpret
the review; omit assessments, resolved-issue summaries, and boilerplate sections.
Full context-bundle output belongs to `pr-review`.
