---
name: debug-regression
description: Investigate behavior that worked in recent repository history but now fails or produces different results. Identify the specific change or smallest change set that introduced the regression and explain its causal chain. Do not fix code or create tests; use debug-error instead when no known-good historical state exists.
---

# Debug Regression

Locate the historical transition from working to broken behavior and explain
how the responsible change caused the regression.

## Inputs

- **Regression target:** Failing behavior, command, result, or artifact.
- **Known-good state:** Commit, tag, branch, date, release, or credible statement
  that the behavior worked recently. Ask for one when it cannot be derived.
- **Known-bad state:** Defaults to the current checkout unless specified.
- **Optional context:** Expected behavior, relevant datasets, environment
  changes, and earlier diagnostic reports.

## Workflow

1. Confirm that the good and bad states are comparable: inputs, environment,
   dependencies, configuration, and execution command.
2. Establish evidence that the chosen good state works and the bad state fails.
   If this cannot be established, explain why and do not falsely attribute a
   code regression.
3. Narrow the transition using history, diffs, existing tests, and, when safe,
   automated or manual bisection.
4. Inspect the smallest responsible change in surrounding code and data flow.
5. Explain the mechanism connecting that change to the observed failure.
6. Separate the introducing change from environmental drift, exposed latent
   bugs, and later changes that merely altered the symptom.
7. Stop after diagnosis.

## Boundaries

- Keep repository content read-only; temporary checkouts for historical
  execution are allowed when they do not disturb user work.
- Do not fix the regression or create a reproduction test.
- Do not identify a commit solely because it is adjacent in time; demonstrate
  behavioral transition and causal mechanism.
- Preserve uncommitted user changes and avoid destructive Git operations.

## Output

Return:

1. Good and bad states and their comparability
2. Commands and evidence establishing the transition
3. Introducing commit or smallest candidate change set
4. Causal chain from change to regression
5. Environmental or data qualifications
6. Confidence, remaining ambiguity, and suggested input for `test-reproduce`
