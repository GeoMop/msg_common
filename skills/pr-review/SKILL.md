---
name: pr-review
description: Perform a read-only pull-request review using repository instructions and the team's bundled PR review policy. Use for a PR URL or number, the current branch PR, or an explicit request for the team's PR-review workflow. Inspect PR metadata, discussion, CI, full diff, tests, and surrounding code; do not edit code or submit remote review comments unless separately requested.
---

# PR Review

Review a pull request against its intended behavior and the team's explicit
policy.

## Inputs

- **PR target:** URL or number. If omitted, resolve the PR associated with the
  current branch. If none or multiple candidates exist, ask.
- **Optional focus:** Specific risks, components, requirements, or review depth.
- **Project context:** Applicable `AGENTS.md`, linked issue or plan, PR template,
  previous discussion, and required checks.

Before reviewing, read [the team review policy](references/review-policy.md).
Treat repository `AGENTS.md` as the authority for project-specific rules and the
bundled policy as the reusable review procedure. Report any conflict instead of
silently choosing one.

## Workflow

1. Verify repository and PR identity, base/head commits, author-stated purpose,
   linked requirements, and CI state.
2. Read the complete diff and sufficient unchanged context. Inspect generated,
   configuration, schema, migration, and dependency changes rather than
   dismissing them by file type.
3. Trace affected behavior from inputs through state and data transformations
   to outputs and side effects.
4. Evaluate the change against the team policy and project-specific rules.
5. Inspect tests for meaningful coverage and run safe targeted checks when they
   can establish a finding.
6. Consider existing review discussion without treating consensus as proof.
7. Deduplicate findings and rank them using the policy severity definitions.

For a large PR, parallel read-only subagents may review independent dimensions
such as correctness, tests, compatibility, and performance. Require every
subagent to read the same policy; wait for all results and reconcile duplicates
and disagreements before responding.

## Boundaries

Installation and configuration are prerequisites, not review steps. Do not
install agents, change Codex configuration, or request credentials while
reviewing. Report missing prerequisites and link to the
[user setup guide](../README.md#review-skills-setup).

- Keep the repository and remote PR read-only.
- Do not submit comments, approval, or change requests unless the user asks for
  that external action after seeing the findings.
- Do not report style preferences unless the policy or repository makes them a
  requirement with material effect.
- Do not infer correctness solely from passing CI.

## Output

Return findings first, ordered by severity. Each finding must include title,
location, violated expectation, evidence, triggering conditions, impact, and a
recommended direction. Distinguish verified defects from unresolved questions.

Then return:

- test and validation gaps;
- CI and requirement status;
- a concise overall assessment;
- explicit residual review limitations.

If no actionable finding is supported, state that directly.
