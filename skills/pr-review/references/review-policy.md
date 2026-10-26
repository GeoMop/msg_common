# Team pull-request review policy

Edit this file as the team's review practice evolves. Keep project-specific
commands and domain conventions in each project's `AGENTS.md`.

## Review priorities

Apply these priorities in order:

1. Behavioral correctness and preservation of documented invariants
2. Data integrity, provenance, schema, units, and transformations
3. Compatibility of public APIs, persistent formats, and supported environments
4. Error handling, partial failure, cleanup, and recoverability
5. Tests that exercise meaningful behavior and failure paths
6. Security, privacy, permissions, and secret handling
7. Performance, memory, I/O, parallelism, and scaling regressions
8. Maintainability when it materially affects safe future changes

## Evidence standard

A finding must identify:

- the smallest useful file and line range;
- the input, state, or execution condition that triggers the problem;
- the expected behavior or invariant;
- the observed or logically necessary result;
- the practical impact.

Prefer a command result, existing test, minimal trace, or explicit code path.
Label incomplete but important concerns as questions rather than defects.

## Severity

- **Critical:** Likely data loss, security breach, unsafe external action, or
  broadly unusable release. Must block merge.
- **High:** Concrete correctness or compatibility defect affecting realistic
  use. Should block merge.
- **Medium:** Real but limited defect, important missing failure handling, or
  material test gap. Normally fix before merge or explicitly accept.
- **Low:** Localized maintainability or robustness problem with credible future
  cost. Do not use for cosmetic preferences.

## Tests

Check that tests:

- verify externally meaningful behavior rather than only implementation detail;
- cover new branches, boundaries, invalid input, and error propagation;
- avoid unjustified tolerance widening or golden-output replacement;
- remain deterministic and independent of ambient state;
- use representative data without making the suite impractically expensive.

## Data and research software

When applicable, additionally check:

- dimensions, units, coordinates, indexing, ordering, masks, and missing data;
- dtype, precision, tolerances, seeds, and platform dependence;
- preservation of metadata and provenance;
- separation between scientific assumptions and software defaults;
- behavior on empty, degenerate, small, and large inputs;
- whether numerical or statistical changes are justified and validated rather
  than merely made to satisfy an existing fixture.

## Exclusions

Do not block a PR for personal naming, formatting, or architectural preference
when it follows project policy and has no demonstrated adverse effect. Do not
request unrelated refactoring.
