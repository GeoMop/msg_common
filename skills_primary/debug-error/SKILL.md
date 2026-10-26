---
name: debug-error
description: Investigate a current error, failed execution, or incorrect result and report evidence plus the causal chain leading to it. Use for root-cause analysis when the user does not want a fix or a new reproduction test. Do not modify implementation code, propose a patch as the deliverable, or create tests.
---

# Debug Error

Explain why the observed error occurs. Stop at diagnosis.

## Inputs

- **Observed failure:** Error message, failed command, log, incorrect output, or
  affected artifact. If omitted, resolve it from the active task only when
  unambiguous.
- **Expected behavior:** What should have happened and under which conditions.
- **Optional context:** Environment, inputs, first observed occurrence, and
  previous investigation.

## Workflow

1. Record the exact symptom, environment, input, and execution path.
2. Re-run existing commands or tests when safe and useful. Do not create a new
   reproduction test.
3. Preserve relevant error text, stack frames, values, logs, and configuration
   as evidence. Redact secrets.
4. Trace the failing value or state backward across component boundaries.
5. Distinguish the immediate failure from contributing conditions and the
   originating cause.
6. Challenge the leading explanation against alternatives and counter-evidence.
7. Stop when the causal chain is supported, or report precisely what missing
   evidence prevents a conclusion.

## Boundaries

- Keep the repository read-only. Do not edit source code or tests.
- Do not implement or recommend a concrete patch as the main result.
- Do not create a regression or reproduction test; use `test-reproduce` later.
- Do not call correlation a cause without a mechanism connecting the events.

## Output

Return a diagnostic report containing:

1. Observed failure and expected behavior
2. Evidence collected, with commands and locations
3. Causal chain: originating cause → intermediate states → visible error
4. Contributing conditions that are not the root cause
5. Ruled-out explanations
6. Confidence and missing evidence

Make the report directly usable as input to `test-reproduce`.
