---
name: fix-ci
description: Diagnose failing pull-request CI, summarize the failure, plan a repair, and implement only a small error with an obvious low-risk solution; then validate, push, and create or update the PR. Use for CI failures such as formatting, lint, simple imports, paths, metadata, or similarly mechanical defects. For design, algorithm, numerical, schema, API, security, concurrency, or ambiguous behavioral failures, report the diagnosis and stop without changing code.
---

# Fix CI

Repair only CI failures whose cause and correction are both small, local, and
obvious. Escalate substantive failures instead of disguising them as CI work.

## Inputs

- **PR target:** URL or number; otherwise resolve the current branch PR. If no
  PR exists but the current branch contains the intended change, it may become
  the head of a new PR.
- **Repository:** Current repository by default.
- **Optional scope:** Named workflow, job, or check.
- **Prerequisites:** Authenticated repository and CI access.

## Workflow

1. Resolve the PR, repository, base/head commits, and failing checks.
2. Fetch actionable logs for repository-native CI. Report external-provider
   checks with their details URL unless an available project tool explicitly
   supports them.
3. Summarize each failure: check, failing command, decisive log excerpt,
   affected code, and likely cause.
4. Classify the required change before editing.

   **Eligible for repair:** mechanical, local, behavior-preserving changes with
   one evident correction, such as formatting, lint, simple import mistakes,
   misspelled paths, or manifest metadata.

   **Report only:** changes involving algorithms, numerical or statistical
   behavior, data models or schemas, public APIs, architecture, concurrency,
   security, broad refactoring, ambiguous expected results, or altered test
   expectations without an established contract.

5. If any required repair is report-only, stop with evidence, likely ownership,
   and the decision needed. Do not mix an obvious cleanup with a substantive
   speculative change merely to turn CI green.
6. For an eligible repair, state the short plan, apply the smallest change, and
   run the failing check locally plus relevant nearby tests.
7. Inspect the final diff, commit only the repair, push the branch, and create a
   PR if none exists or update the existing PR otherwise.
8. Recheck or clearly report the remote CI state.

## Boundaries

- Never change an expected scientific, numerical, or algorithmic result merely
  because CI reports a mismatch.
- Never weaken assertions, tolerances, validation, security controls, or static
  checks without a separately reviewed requirement.
- Preserve unrelated user changes and shared history.
- Do not claim remote success while checks are pending.

## Output

Return:

1. Failure summary and decisive evidence
2. Classification: **fixed** or **report only**, with rationale
3. Plan and diff summary when fixed
4. Local validation results
5. Commit and PR URL when changed
6. Remote CI status or remaining failing checks
