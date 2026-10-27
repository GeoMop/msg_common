# Dedicated review agent

This is user-facing documentation for installing and configuring the review
agent, plus integration guidance for the calling orchestrator. Review behavior
is defined in `SKILL.md`, not here.

The runtime definition is [agents/code-review.toml](../agents/code-review.toml).
`agents/openai.yaml` supplies skill UI metadata only. The default review model
is `gpt-6.1-sol` with `high` reasoning; both are editable in the TOML file.

## Registration

On Codex versions supporting standalone custom agents, copy the definition to
`~/.codex/agents/code-review.toml` for personal use, or to
`<reviewed-project>/.codex/agents/code-review.toml` for project use. Create the
directory if needed and preserve an existing custom definition. Start a new
session after registration. Installing the skills plugin alone does not install
this runtime agent. The caller must also make `code-review` available through
the plugin/skill installation or supply its absolute `SKILL.md` path.

From this repository root, for a project without an existing definition:

```bash
mkdir -p /path/to/project/.codex/agents
cp -n skills/code-review/agents/code-review.toml /path/to/project/.codex/agents/code-review.toml
```

Check the installed Codex version and custom-agent support before registration.
The definition follows the standalone-agent schema documented for current
Codex and was developed with CLI 0.164.0. Older role/config-file schemas differ;
do not put model keys into `openai.yaml` or silently ignore an unsupported agent.

## Execution environment

Prefer registered agent type `code-review`. Spawn it once with the local
repository path, explicit target, context bundle, prior report references,
destination. The caller owns full-context output. Wait for its report. Do not
spawn the PR orchestration skill as the reviewer.

Some hosts expose only generic subagent spawning with explicit model/reasoning
arguments, rather than named agent types. In that environment, read the TOML
definition and use it as task defaults: pass its `model` and
`model_reasoning_effort` through the supported spawn arguments, give the child
its `developer_instructions` and absolute skill path, and start without the
parent conversation history. Supply the complete review bundle explicitly.
Record this adapter mode in the report: it applies task defaults and instructions, not
registered-agent feature controls. Do not claim the runtime registered the
custom type or enforced its `[features]` reductions. If neither named agents
nor explicit-model delegation is available, report the missing support and stop.

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
