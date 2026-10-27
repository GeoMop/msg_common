# Team code-review policy

## Review priorities

Inspect these areas in order. Rank findings by severity and practical impact,
not by their position in this list.

1. Behavioral correctness and preservation of documented invariants.
2. Error handling, partial failure, cleanup, and recoverability.
3. Tests that exercise meaningful behavior and failure paths.
4. Security, privacy, permissions, and secret handling.
5. Backward compatibility. An intentional break must follow the stated
   requirements, document affected users/formats/APIs and any migration, and
   have suitable validation; documentation alone does not justify a break.
6. Performance, memory, I/O, parallelism, and scaling regressions.
7. Deduplication. Keep one authoritative implementation of each nontrivial
   rule, algorithm, or workflow. Consolidate repeated logic into shared
   functions, components, or data-driven definitions. Duplication itself is a
   maintainability finding: every copy adds development, testing, and
   synchronization costs, even before behavior diverges. Identify the repeated
   responsibility and representative locations; do not require an existing
   runtime bug. Exceptions need a concrete reason, such as independently
   evolving contracts or a demonstrated performance constraint, and must keep
   the duplicated behavior and its maintenance obligations explicit. Use the
   smallest useful abstraction and keep the requested change within scope.
8. Convoluted state flow, hidden mutation, and unnecessary coupling. Prefer
   stateless transformations where they simplify reasoning; do not require
   removal of state that the behavior needs.
9. Maintainability when it materially affects safe future changes.
10. Broad renaming or formatting mixed with behavioral changes when it obscures
    the change and prevents meaningful review. Prefer separate mechanical
    changes where practical; necessary local cleanup is acceptable. Verify
    compatibility and behavior even for a rename-only or formatting-only diff.
11. Minimize dependencies. Both between own components but especialy on extenal libraries.
    New dependecies must be backed up by research and justification.
    
## Language agonstic patterns
- Resource Acquisition by Initiation
- replace polymorphism by parametrization of a generic code

## Language agnostic anti patterns
- more then three nested blocks
- modeling different behavior by conditions (instead of e.g. polymorphism)
- functional programming style; state-less or "low-state" classes 
    
## Shared language rules

Read the bundled rules for each changed language:

- [Python rules](python.md)
- [C++ rules](cpp.md)

These requirements apply both when writing code and when reviewing it. Use
these files as the team language-rule sources and `AGENTS.md` for applicable
project instructions. Do not search for or require additional project-specific
coding-rule files. Report material conflicts rather than silently inventing
exceptions.

## Evidence standard

A finding must identify:

- the smallest useful file and line range;
- a concise description;
- the input, state, or execution condition that triggers the problem;
- the expected behavior or invariant;
- the contradicting observed or logically necessary result;
- the practical impact, including the concrete maintenance cost for a
  maintainability finding.

Prefer a command result, existing test, minimal trace, or explicit code path.
Label incomplete but important concerns as questions rather than defects.
For a directly checkable team rule, identify the rule and specific violation;
do not invent a runtime trigger for a build, static-check, or deduplication
requirement. For duplication, the repeated implementation and the need to
maintain its copies are sufficient evidence of maintenance cost.

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
when it follows this policy, the bundled language rules, and applicable
`AGENTS.md` instructions. Required deduplication is not a personal style
preference. Do not request unrelated refactoring.
