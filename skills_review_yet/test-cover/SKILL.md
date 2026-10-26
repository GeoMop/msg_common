---
name: test-cover
description: Design and implement substantial behavior-focused tests for a function, class, or coherent component. Use when tests should cover general functionality, equivalence classes, boundaries, invariants, state transitions, and representative failures rather than reproduce one known bug. Do not refactor or fix production code unless separately requested.
---

# Test Cover

Create a maintainable test model for the target behavior, not merely additional
line coverage.

## Inputs

- **Target:** Function, class, module, or coherent behavior boundary.
- **Contract:** Documented behavior, types, invariants, error semantics, and
  compatibility requirements. Infer only what the code and project establish.
- **Optional focus:** Risks, platforms, data characteristics, test level, and
  runtime budget.

## Workflow

1. Read applicable `AGENTS.md`, the implementation, callers, documentation, and
   existing tests.
2. Write a compact behavior model: normal cases, equivalence classes,
   boundaries, invariants, state transitions, and invalid inputs.
3. Identify gaps in the existing suite and prioritize failures with meaningful
   impact over raw coverage percentage.
4. Choose an economical combination of examples, parameterization,
   property-based tests, and integration tests.
5. Use public behavior where possible. Test internal details only when they are
   intentional contracts or the only practical observation point.
6. Implement focused tests with reusable fixtures and clear failure messages.
7. Run the target suite, then the relevant broader suite. Report unexpected
   production failures without silently changing the implementation.

## Boundaries

- Do not duplicate equivalent existing tests.
- Do not over-mock interactions that are central to the behavior.
- Avoid tests coupled to incidental ordering, formatting, random seeds, or
  implementation structure unless those are contractual.
- Do not modify production code solely to make a test pass. Report discovered
  defects separately.

## Output

Return:

1. Behavior and risk model
2. Existing gaps addressed
3. Tests added, grouped by behavior
4. Commands and results
5. Remaining untested risks and why they remain
