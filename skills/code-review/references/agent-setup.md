# Review agent execution

**Audience: the agent delegating or executing a code review.**
This reference describes invocation and runtime constraints. Installation and
configuration are user tasks documented in [skills/README.md](../../README.md#review-skills-setup).
Do not install agents, modify Codex configuration, or request credentials as
part of a review. Report missing prerequisites and point the user to that guide.

Review behavior is defined in [SKILL.md](../SKILL.md). Runtime defaults are in
[agent-definitions/code-review.toml](../agent-definitions/code-review.toml).

Prefer registered agent type `code-review`. Spawn it once with the local
repository path, explicit target, context bundle, prior report references,
destination. Use a fresh context without the parent's conversation history;
supply the full review input explicitly. The caller owns full-context output. Wait for its report. Do not
spawn the PR orchestration skill as the reviewer.

Some hosts expose only generic subagent spawning with explicit model/reasoning
arguments, rather than named agent types. In that environment, read the TOML
definition and use it as task defaults: pass its `model` and
`model_reasoning_effort` through the supported spawn arguments, give the child
its `developer_instructions` and absolute skill path, and start without the
parent conversation history. Supply the complete review bundle explicitly.
Record this adapter mode in the report: it applies task defaults and instructions, not
registered-agent feature controls. Do not claim the runtime registered the
custom type or enforced its `[features]` reductions. If delegation is unavailable
and the calling workflow permits it, run the `code-review` skill directly in
the current agent. Record this fallback without claiming a separate context.

When loaded as a runtime agent, the definition disables apps and memories. Shell and plugin/skill access remain
available, as does the parent's native web documentation tool. The reviewer
uses local code and existing dependencies; its instructions permit online
primary documentation lookups but prohibit remote repository operations.
Other inherited MCP tools may still exist: the no-GitHub rule is behavioral,
not a claim that every possible remote transport is technically removed.

Custom agents inherit the parent's filesystem permissions, approvals, provider,
and MCP configuration. They cannot impose a different sandbox. Choose a parent
environment that permits writing the report and temporary files. Source files
remain unchanged by instruction; for stronger enforcement, use an external
environment with source mounted read-only and a writable report destination.
If the destination is unwritable, stop before analysis; do not substitute a
chat-only report or silently have the parent write it.

Authoritative schema and permission behavior:
[OpenAI custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
