---
name: review
description: Perform a generic, read-only code review of selected files, a working tree, a diff, branch, or commit range. Use when the user asks for code review without requiring pull-request metadata or the team's PR-specific policy. Prioritize concrete correctness and maintainability findings; do not edit code or submit a review.
---

# Review

Find consequential defects and risks in a code change or selected code.

## Inputs

- **Target:** Explicit files, working tree, staged diff, commit range, or branch.
  If omitted, use the current uncommitted change when unambiguous; otherwise
  ask.
- **Optional baseline:** Base branch or commit.
- **Optional focus:** Correctness, data integrity, API compatibility, security,
  performance, concurrency, tests, or maintainability.
- **Requirements:** Issue, plan, specification, or stated intended behavior.

## Workflow

1. Resolve the exact review boundary and preserve the user's working state.
2. Read applicable `AGENTS.md`, requirements, the full diff, and enough
   surrounding code to understand behavior.
3. Trace affected inputs, state changes, outputs, errors, and callers.
4. Inspect relevant tests and run safe targeted checks when they materially
   confirm or reject a finding.
5. Report only actionable findings supported by code or test evidence.
6. Rank findings by impact and likelihood. Keep stylistic suggestions separate
   and omit them unless they affect correctness or maintainability.

## Boundaries

- Keep the review read-only. Do not apply fixes, commit, push, or submit a
  remote review.
- Do not review unchanged code unless needed to establish the effect of the
  target change.
- Do not inflate uncertain concerns into defects. Mark assumptions and missing
  evidence.
- Use `pr-review` when PR metadata, discussion, CI, or team PR policy matters.

## Output

List findings first, ordered by severity. Each finding must include:

- severity;
- concise title;
- file and line or smallest useful location;
- violated behavior or risk;
- evidence and triggering conditions;
- recommended direction, without implementing it.

Then provide testing gaps and a brief overall assessment. If no findings are
supported, say so and note residual review limits.
