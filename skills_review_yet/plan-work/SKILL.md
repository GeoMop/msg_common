---
name: plan-work
description: Create an executable implementation, maintenance, data-processing, or research work plan from a request, issue, or specification. Use when work should be scoped and decomposed before implementation. Inspect relevant context and define verification, but do not modify implementation files or execute the plan.
---

# Plan Work

Produce a decision-ready plan without implementing it.

## Inputs

- **Target:** User request, issue, specification, or research objective. Resolve
  linked or repository-local context when available; ask if the goal remains
  materially ambiguous.
- **Optional guidance:** Constraints, exclusions, priorities, deadline, desired
  granularity, and acceptance criteria.
- **Project context:** Read applicable `AGENTS.md`, relevant code, tests,
  documentation, configuration, and recent history.

## Workflow

1. Restate the intended outcome and explicit non-goals.
2. Inspect enough of the current system to ground the plan in actual files,
   interfaces, data flow, and existing conventions.
3. Identify unresolved decisions. Ask only about choices that materially change
   the plan; otherwise record a reasonable assumption.
4. Decompose the work into ordered, independently verifiable steps. Name likely
   files or components when known.
5. For every step, state its result and verification method.
6. Identify dependencies, migration or compatibility concerns, risks, and
   rollback needs.
7. Check that the plan satisfies the request without unrelated expansion.

## Boundaries

- Do not edit implementation or test files.
- Do not present invented file paths or APIs as facts.
- Do not hide important design choices inside implementation steps.
- A plan may recommend exploratory work when evidence is missing.

## Output

Return:

1. Goal and non-goals
2. Current-state observations
3. Assumptions and open decisions
4. Ordered work items with verification
5. Risks, compatibility, and rollback considerations
6. Completion criteria
