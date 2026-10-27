# C++ coding rules

Apply these requirements when writing and reviewing C++. Read applicable
`AGENTS.md` instructions; use the language standard, platforms, and dependencies
declared by the build configuration. Apply rules to the changed behavior and
interfaces, without demanding unrelated rewrites.

- **Reuse implementation.** Follow the review policy's deduplication rule.
  Share repeated algorithms, validation, and resource-handling logic through
  functions, types, or templates as appropriate. Do not use copied branches or
  macros where an ordinary function or data-driven definition suffices. Keep
  generic interfaces limited to the variation actually required.
- **Express ownership.** Prefer values and RAII owners for resources. Use
  exclusive ownership when sharing is unnecessary; use shared ownership only
  when the lifetime contract requires it. Treat raw pointers/references as
  non-owning unless an external interface requires otherwise, and document
  nullability, ownership transfers, and cleanup at that boundary.
- **Protect lifetimes.** Do not return or retain references, pointers, views,
  iterators, or lambda captures beyond their referents' lifetimes. Account for
  container invalidation, reallocation, asynchronous execution, and moves.
  Make borrowing and lifetime requirements explicit in interfaces.
- **Initialize and constrain state.** Initialize objects before use and establish
  class invariants in constructors. Use `const` for read-only access and values
  that need not change. Keep mutation local and explicit; avoid hidden global
  dependencies and partially initialized externally visible objects.
- **Check numeric boundaries.** Do not rely on signed overflow or unchecked
  narrowing. Check ranges when converting sizes, indices, external values, or
  numeric representations. Preserve units and numerical accuracy; casts must
  express a justified conversion rather than silence a diagnostic.
- **Keep failure paths safe.** Release resources through ownership objects on
  every exit path. Handle error returns and exceptions according to the declared
  interface; do not ignore failures. Preserve required invariants after failure,
  do not let destructors propagate exceptions, and use `noexcept` only when its
  guarantee can be met.
- **Keep interfaces self-contained.** Include headers that declarations depend
  on rather than relying on transitive includes. Keep implementation details out
  of public interfaces and avoid namespace-wide `using` directives in headers.
  Document preconditions, ownership, and intentional compatibility changes.
- **Make concurrency explicit.** Protect shared mutable state and define the
  synchronization and lifetime contract. Do not assume `volatile` synchronizes
  threads. Manage worker completion before destroying resources they use.
- **Test observable behavior.** Cover boundaries, invalid inputs, ownership,
  lifetime-sensitive paths, and failure cleanup. Use configured compiler
  diagnostics or sanitizers when available and relevant; do not suppress a
  diagnostic without identifying why the operation is valid.

Language-design background (not an additional required rule set):
[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
