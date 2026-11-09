# Python coding rules

Apply these requirements when writing and reviewing Python. Read applicable
`AGENTS.md` instructions; use the supported versions and dependencies declared
by the build/package configuration. Apply rules to the changed behavior and
interfaces, without demanding unrelated rewrites.

- **Prefer the smallest clear implementation.** Implement the stated behavior
  with direct control flow and familiar standard-library operations. Minimize what the
  reader must understand, not just the line count; avoid compression obscuring readability.
- **Match complexity to the task.** A small internal tool usually needs fewer
  configuration options, compatibility paths, and recovery mechanisms than a
  public service or library. Add such machinery for concrete requirements or
  failure consequences, not by default. Preserve the protections the actual
  operations need.
- **Organize by responsibility.** Use straightforward functions for distinct
  tasks. Separate generic work from service-specific behavior. Collect paths,
  defaults, and service choices in `main()` or another clear composition point,
  then pass them explicitly. Prefer sensible defaults and few arguments; add
  command-line options only for choices users actually need. For internal tools,
  keep occasional local adjustments easy to make in that composition point.
- **Reuse implementation.** Follow the review policy's deduplication rule.
  Put repeated validation, transformations, and workflow logic in shared
  functions or components. Represent repeated variants as data or parameters
  rather than copying implementations. Keep abstractions explicit and small.
- **Make contracts explicit.** Add accurate type annotations to new or changed
  public interfaces. Document non-obvious units, array shapes, accepted missing
  values, mutation, and failure behavior.
- **Validate at boundaries.** Validate external inputs where they enter the
  program; do not repeatedly check established internal assumptions. Type
  annotations do not validate runtime input. Use `assert` for programmer
  invariants, not for required validation of external input.
- **Control mutation.** Avoid mutable argument defaults and unintended shared
  class state; allocate per-call/per-instance mutable values separately. Make
  intentional shared state explicit. Do not mutate caller-owned inputs unless
  the interface documents it; keep transformations free of hidden global state.
- **Let errors explain themselves.** Let exceptions propagate unless the caller
  can recover, add useful context, or meet an explicit interface contract. In
  internal tools, a traceback is usually more useful than a top-level catch
  that only prints an error and exits. Catch specific exceptions for a concrete
  handling action. Do not silently discard errors, turn failure into plausible
  success, or add fallback behavior without a requirement. Broad catches belong
  only at explicit error-handling boundaries or around cleanup with re-raising.
- **Release resources.** Use context managers or guaranteed cleanup for files,
  locks, connections, and other owned resources, including failure paths. Make
  ownership and closure responsibilities explicit when returning iterators or
  objects that retain resources.
- **Keep imports predictable.** Importing a module must not unexpectedly start
  work, access external services, or mutate application state. Put executable
  workflows behind explicit entry points. Do not change the process import path
  to hide packaging errors; declare runtime dependencies in package metadata.
- **Preserve numerical meaning.** Make dtype, shape, units, indexing, masks,
  missing-data handling, and copy/view ownership explicit where they affect
  results. Do not silently modify shared arrays or widen tolerances to hide a
  regression. Pass random generators or seeds explicitly for reproducible work.
- **Test observable behavior.** Choose tests for the changed behavior and its
  practical risks, including relevant boundaries and failure paths. Do not
  mirror the implementation or require a separate test for every helper. Use
  parameterized cases or shared fixtures for repeated scenarios; expected
  results must be independent of the logic under test.
- **Vectorize critical numerical work.** Prefer array operations in NumPy,
  xarray, or other compiled libraries for performance-critical numerical code.
  Preserve numerical meaning and avoid unnecessary temporary arrays.

When reviewing, identify concrete reading, modification, testing, or runtime
costs of unnecessary complexity. Suggest the smallest useful simplification;
do not replace a small implementation with another framework or request
unrelated rewrites to satisfy a stylistic preference.

Language-semantics references (not additional team rule files):
[default argument evaluation](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values),
[exceptions and cleanup](https://docs.python.org/3/tutorial/errors.html).
