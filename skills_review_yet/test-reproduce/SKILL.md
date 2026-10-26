---
name: test-reproduce
description: Create the smallest durable automated test that reproduces a known error or regression. Use after diagnosis, ideally with a debug-error or debug-regression report, to turn the observed failure into a reliably failing test. Do not fix production code or weaken an existing assertion to make the reproduction pass.
---

# Test Reproduce

Encode one diagnosed failure as a stable failing test.

## Inputs

- **Failure target:** Error, regression, or incorrect behavior to reproduce.
- **Preferred evidence:** Output from `debug-error` or `debug-regression`,
  including causal chain, inputs, environment, and known-good/bad behavior.
- **Optional constraints:** Required test layer, framework, fixture policy, and
  runtime budget.

## Workflow

1. Read applicable `AGENTS.md` and inspect the existing test organization.
2. Confirm the intended behavior and the exact observable failure. Ask if the
   expected result is ambiguous.
3. Choose the lowest test layer that reproduces the real defect without mocking
   away its cause.
4. Minimize inputs, fixtures, and environment while preserving the failure
   mechanism.
5. Add one focused test with a name explaining the behavior, not the bug ID
   alone.
6. Run the new test and show that it fails for the expected reason.
7. Run a relevant nearby test subset to detect accidental fixture or collection
   damage.

## Boundaries

- Modify tests and test fixtures only. Do not change production code.
- Do not change expected values merely to match current broken output.
- Do not use flaky timing, external state, or an oversized fixture when a stable
  alternative preserves the cause.
- If the failure cannot be reproduced, stop with evidence and missing
  conditions instead of adding a speculative test.

## Output

Return:

1. Test file and test name
2. Behavior encoded and its relation to the diagnostic evidence
3. Exact command used
4. Expected failing assertion or exception and observed result
5. Any limitations or environment requirements
