# MSG group - common tools

- `skills` - reviewed team shared codex skills
- `skills-*` - various stages of yet unreviewed skills
- `project_templates` - templates for AI and other stup of projects/repositories
- `gdsync` - Google drive and S3 bucket automounting script - based on rclone.




## Skills - overview

This repository is a first iteration of a shared, skills-only plugin for small
software and research teams. It contains ten focused workflows:

| Skill | Purpose |
| --- | --- |
| `code-review` | Perform a team specific code review of a local changes, diff, branch, commit range, or PR with context. Follows: `skills/code-review/references/review-policy.md`|
| `pr-review` | Extract PR context, call `code-review` in specialized agent, optionaly create unsubmitted comments on github. |

| `debug-regression` | Identify the particular historical change that caused previously working behavior to regress. |
| `test-reproduce` | Add the smallest durable test that reproduces a known error; do not fix the implementation. |
| `test-cover` | Design broader tests for a function, class, or coherent component using behavior, boundaries, invariants, and representative cases. |
| `make-pr` | Prepare, validate, push, and open a focused pull request. |
| `fix-ci` | Diagnose CI and repair only small failures with an obvious solution; report design or algorithmic failures without changing them. |
| `literature` | Find and organize literature for a topic; optionally create a Zotero collection through an available Zotero MCP connection. |
| `plan-work` | Turn a request, issue, or research task into an executable plan without implementing it. |
| `debug-error` | Collect evidence and report the causal chain behind a current error, without fixing it or writing a reproduction test. |

The repository includes both the portable root `plugin.json` manifest and the
Codex compatibility manifest at `.codex-plugin/plugin.json`.

## 1. Register the plugin and use it in projects

### Local development installation

Clone the repository once, outside individual projects:

```bash
git clone <team-repository-url> ~/work/team-workflow-plugin
```

The checkout already contains a local marketplace descriptor at
`.agents/plugins/marketplace.json`. In Codex CLI:

1. Start Codex and enter `/plugins`.
2. Add `~/work/team-workflow-plugin` as a local marketplace source. If the
   browser does not expose an add-source action, invoke `$plugin-creator` and
   ask it to add that absolute directory as a personal local marketplace.
3. Install **Team Workflows** from that marketplace.
4. Start a new Codex session in any project where you want to use the skills.

The project does not need to contain the plugin or know its filesystem path.
The plugin is installed in the developer's Codex environment and its skills are
then available in all projects. Repository-specific commands, conventions, and
constraints should remain in that project's `AGENTS.md`.

If you intentionally want only selected skills in one local CLI project, Codex
also discovers repository skills from `.agents/skills/`. You can copy or
symlink selected skill directories there, but that is a project-scoped fallback,
not the recommended team distribution mechanism.

### Team and cloud installation

A local path is available only on the machine that owns the checkout. For
ChatGPT on the web, Codex cloud, or other team members, publish the repository
as a GitHub-backed workspace marketplace/plugin and install it from the
**Plugins** tab. The same plugin can then supply its skills to new ChatGPT and
Codex conversations.

Current OpenAI documentation:

- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Use plugins](https://learn.chatgpt.com/docs/plugins)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)

## 2. Introduce changes through your own local copy

Use the local checkout as the editable development version:

```bash
cd ~/work/team-workflow-plugin
git switch -c improve-pr-review
```

Edit the appropriate `SKILL.md`, its directly referenced files, and its
`agents/openai.yaml` if the name, short description, or default prompt changed.
For example, team-specific pull-request rules belong in:

```text
skills/pr-review/references/review-policy.md
```

Then validate and inspect the changes:

```bash
skills-ref validate ./skills/pr-review
git diff --check
git diff
```

Refresh or reinstall the local plugin if needed and test representative prompts
in a new conversation. Commit the result and open a pull request to the team
repository. Once merged, other developers update their one local checkout:

```bash
git switch main
git pull --ff-only
```

Important operating rules:

- Treat `main` as the stable team version.
- Use a branch in the same checkout to test changes locally.
- Avoid simultaneously installing stable and development copies with identical
  skill names; the agent may see both and they are not merged.
- Keep project-specific facts in `AGENTS.md`. Promote only reusable workflow
  knowledge into this repository.
- Increment the manifest version when publishing a team release.

## 3. Use the skills from ChatGPT

After the plugin is installed, start a new Chat or Work conversation. ChatGPT
can select a skill implicitly from the request, or you can select it explicitly
with `@` in ChatGPT. Examples:

```text
@plan-work Plan the implementation of versioned IceChunk inputs in this project.

@debug-regression This workflow worked last week. Determine which change caused
the incorrect output, but do not fix it.

@pr-review Review PR 142, concentrating on data integrity and compatibility.
```

In Codex CLI or the IDE, use `/skills` to browse skills or mention one using
`$`, for example:

```text
$test-reproduce Add a failing test for the error described in debug-report.md.
```

Local source code and a local plugin checkout are directly available only to a
local Codex environment. ChatGPT web and hosted Codex need the repository and
plugin to be available through the configured workspace/GitHub distribution.

## 4. Skill, agent, plugin, and MCP terminology

**Prompt or request**

The task supplied by the user. It normally identifies the target and supplies
task-specific goals or constraints.

**Skill**

A reusable package of instructions for one recognizable job. A skill is a
directory containing `SKILL.md` and, when useful, scripts, references, assets,
or interface metadata. A skill is not a running process and has no formal
function signature. Its instructions define how to resolve inputs, handle
ambiguity, use tools, and format outputs.

**Agent**

The active model process that reads the request, project instructions, and any
selected skills; uses tools; and produces the result. A skill changes how an
agent performs a task but does not become a separate agent.

**Subagent**

An additional agent thread delegated a bounded part of a larger task. Subagents
have separate context and return their findings to the coordinating agent.

**Plugin**

An installable distribution package containing one or more skills and,
optionally, MCP servers, hooks, apps, or UI resources. This repository is a
skills-only plugin.

**MCP server**

A service exposing structured tools or data to the agent. The `literature`
skill can search and report literature without Zotero, but creating Zotero
collections or records requires an independently configured Zotero MCP server.
This repository deliberately does not embed Zotero credentials or assume a
particular third-party server implementation.

## 5. Write and improve skills

A minimal skill is:

```text
skills/my-skill/
├── SKILL.md
└── agents/
    └── openai.yaml
```

Start `SKILL.md` with only the required frontmatter:

```yaml
---
name: my-skill
description: State what the skill does, when it should trigger, and important exclusions.
---
```

Use the body to define:

1. **Inputs and resolution order** — explicit user value, unambiguous working
   context, project default, then clarification.
2. **Boundaries** — especially whether the skill may edit code, write tests,
   push branches, or call external services.
3. **Workflow** — imperative steps with evidence and decision gates.
4. **Output contract** — the exact result another person or skill can consume.
5. **Failure behavior** — when to stop, ask, or report uncertainty.

Keep stable project policy in `AGENTS.md`; keep reusable workflow policy in a
skill. Prefer instructions over scripts until a repeated operation has stable,
deterministic inputs and behavior. Put long policy or tool documentation in a
directly linked `references/` file. Add a script only when deterministic
execution is materially safer or when the same code is repeatedly recreated.

Descriptions are the routing surface. Test at least:

- a prompt that must trigger the skill;
- a similar prompt that must not trigger it;
- a prompt with an explicit target;
- a prompt where the target can be inferred;
- an ambiguous prompt that should cause a clarification request.

Validate every skill and test changed behavior in a fresh conversation. The
format is based on the [Agent Skills specification](https://agentskills.io/specification).

## 6. Use skills with parallel agents in Codex CLI

Parallel agents are most useful when tasks are independent and read-heavy:
review dimensions, repository exploration, test execution, log analysis, or
literature searches. Ask for delegation explicitly and specify:

- how the task should be divided;
- which skill each subagent should follow;
- whether the coordinator must wait for every result;
- the result format returned by each subagent;
- how duplicate or conflicting findings should be reconciled.

Example PR review:

```text
Use $pr-review on the current pull request. Spawn four parallel subagents:
one for behavioral correctness, one for tests, one for API/data compatibility,
and one for performance and resource use. All agents must read the same team
review policy. Keep the work read-only, wait for all agents, deduplicate their
findings, and return one severity-ordered review with file and line references.
```

Example regression investigation:

```text
Use $debug-regression. Spawn one agent to inspect history and candidate diffs,
one to analyze logs and failing outputs, and one to trace the affected data
flow. Do not edit code or tests. Wait for all three and synthesize one causal
chain, marking disagreements and confidence.
```

Use `/agent` in Codex CLI to inspect active and completed agent threads. Prefer
one coordinating agent for all final decisions. Avoid parallel edits to the
same files; if write-heavy work must be parallelized, divide ownership by
disjoint files or use isolated worktrees and integrate changes deliberately.
Subagents inherit the parent sandbox and approval policy and consume additional
tokens.

See [OpenAI's subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
