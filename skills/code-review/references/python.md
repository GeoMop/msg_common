# Python coding rules

Apply these requirements when writing and reviewing Python. Read applicable
`AGENTS.md` instructions; use the supported versions and dependencies declared
by the build/package configuration. Apply rules to the changed behavior and
interfaces, without demanding unrelated rewrites.

- **Reuse implementation.** Follow the review policy's deduplication rule.
  Put repeated validation, transformations, and workflow logic in shared
  functions or components. Represent repeated variants as data or parameters
  rather than copying implementations. Keep abstractions explicit and small.
- **Make contracts explicit.** Add accurate type annotations to new or changed
  public interfaces. Document non-obvious units, array shapes, accepted missing
  values, mutation, and failure behavior. 
- **Extranal inputs validation.** Validate external inputs at boundaries;
  do not rely on annotations or `assert` for runtime input validation.   
- **Control mutation.** Avoid mutable argument defaults and unintended shared
  class state; allocate per-call/per-instance mutable values separately. Make
  intentional shared state explicit. Do not mutate caller-owned inputs unless
  the interface documents it; keep transformations free of hidden global state.
- **Handle errors deliberately.** Catch only treatable exceptions or if 
  more specific error report is needed. Do not catch without clear and explicit 
  falback bahavior that restores the invariants.  Do not silently discard exceptions or turn failure into plausible
  success. 
  Broad catches are exceptional and for explicit boundaries with deliberate handling
  or cleanup followed by re-raising, not ordinary control flow.
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
- **Test observable behavior.** Cover changed contracts, boundaries, invalid
  inputs, and failure cleanup. Use parameterized cases or shared fixtures for
  repeated scenarios; expected results must be independent of the logic under test.
- ** Vectorize.** Use SIMD approach for critical code, e.g. vectorization with Numpy arrays, xarrays or other compiled libraries.  
  
Language-semantics references (not additional team rule files):
[default argument evaluation](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values),
[exceptions and cleanup](https://docs.python.org/3/tutorial/errors.html).
