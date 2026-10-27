# MSG group - common tools

- `skills` - reviewed team shared codex skills
- `skills-*` - various stages of yet unreviewed skills
- `project_templates` - templates for AI and other stup of projects/repositories
- `gdsync` - Google drive and S3 bucket automounting script - based on rclone.




## Skills - overview

This repository provides shared skills for small software and research teams,
plus a reusable Codex code-review agent definition. The active review workflows
are:

| Skill | Purpose |
| --- | --- |
| `code-review` | Review local changes or two local commits using the [team policy](skills/code-review/references/review-policy.md); always save findings. |
| `pr-review` | Collect PR context, delegate to the code-review agent, optionally save the full context bundle and upload pending GitHub comments through MCP. |

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
For example, shared team review rules belong in:

```text
skills/code-review/references/review-policy.md
```

Then validate and inspect the changes:

```bash
skills-ref validate ./skills/code-review
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
agent performs a task but does not become a separate agent. Custom agent TOML
definitions can set task-specific model defaults and instructions;
`agents/openai.yaml` within a skill supplies UI metadata instead.

**Subagent**

An additional agent thread delegated a bounded part of a larger task. Subagents
have separate context and return their findings to the coordinating agent.

**Plugin**

An installable distribution package containing one or more skills and,
optionally, MCP servers, hooks, apps, or UI resources. This repository is a
skills plugin with a separately registered review-agent definition.

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

The normal PR review delegates once to the dedicated reviewer:

```text
Use $pr-review on the current pull request. Collect the full context and use
the code-review agent to write the report. Focus on data integrity and API
compatibility. Save the complete input context for debugging.
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

## 7. Configure and use the review workflows

`code-review` owns the shared [team policy](skills/code-review/references/review-policy.md).
Its bundled [Python](skills/code-review/references/python.md) and
[C++](skills/code-review/references/cpp.md) rules apply to both coding and review,
alongside applicable `AGENTS.md` instructions.
It reviews staged/unstaged changes and relevant untracked files by default, or
compares two locally available commits with supplied context. It can run in
the active agent without a custom-agent installation. It preserves existing
source files and writes `REVIEW_RESULTS-<name>-<num>.md` at the repository root,
or a requested path. Follow-ups after code changes or comment resolutions get
a new report describing previously unreported issues, with a fresh issue limit.
Unresolved earlier issues are referenced only by ID, grouped by their original
report filename, and do not count toward that limit. Resolved issues are omitted.
An unchanged completed review reuses its report without adding issues.
Unrelated files are never overwritten. See the [report contract](skills/code-review/references/reporting.md).
Reports contain at most ten topically distinct issues by default, grouping
similar problems with representative code locations. Request an explicit higher
issue limit for a broader report. The skill returns only the report path.
`pr-review` can optionally save the complete context bundle passed to the reviewer
in the same report. It writes only the report and necessary temporary files;
missing Git objects are obtained in a temporary repository, leaving the original
repository and its `.git` unchanged.

```text
$code-review Review the local changes and write findings.

$code-review Compare commits abc123 and def456 using requirements.md as
context. Write a fresh report to /tmp/review-output.md.

$pr-review Review PR 142 with GitHub upload and save the full context bundle.
Leave the comments pending for me to inspect and submit.

$pr-review Review PR 142 and submit the findings as a COMMENT review.
```

`pr-review` delegates to the dedicated `code-review` agent. The
[runtime definition](skills/code-review/agents/code-review.toml)
defaults to `gpt-6.1-sol` with `high` reasoning. Copy it to
`~/.codex/agents/code-review.toml` or the consuming project's
`.codex/agents/code-review.toml`, preserving existing custom definitions, then
start a new session. Skill/plugin installation does not register this agent
automatically. Hosts exposing only generic explicit-model spawning can use the
definition as task defaults; the workflow discloses that mode and its lack of
runtime feature controls. See [agent setup and inherited permissions](skills/code-review/references/agent-setup.md).

The reviewer permits online primary documentation lookups for uncertain library
behavior; PR/repository collection stays in the orchestrator. Reports must be
writable: failure to create or update one stops the review before analysis.
The custom agent inherits the parent's sandbox. Its instructions preserve
source files; they do not enforce a separate read-only filesystem environment.

GitHub upload needs an MCP connection supporting pending review creation,
inline draft comments, body updates where needed, and state inspection.
Generic comments go in the pending review body. A tool that only submits a
review is insufficient. When draft capability is unavailable, the workflow
records that limitation in the local report and uploads nothing. Upload uses
MCP's existing permissions without an extra confirmation. Submission requires
an explicit request. Return values are limited to the report path or a count of
new GitHub comments/issues. The usual limit is 10, with an absolute maximum of
30 unless the user requests more. See the
[GitHub lifecycle and comment limits](skills/pr-review/references/github-review.md).

### Development checks

Run the script checks with Node.js and validate both skill directories:

```bash
node tests/check_github_review_mcp.test.cjs
skills-ref validate skills/code-review
skills-ref validate skills/pr-review
git diff --check
```

`scripts/check_github_review_mcp.js` is a development probe outside the skills.
It defines the function `checkGithubReviewMcp` in its evaluation context and
expects an MCP host's `catalog` and `call(name, args)` adapter. In a Codex
`functions.exec` host, it can be run with:

```javascript
const source = await tools.exec_command({cmd: "cat scripts/check_github_review_mcp.js"});
const probe = new Function(source.output + "\nreturn checkGithubReviewMcp;")();
text(await probe({catalog: ALL_TOOLS, call: (name, args) => tools[name](args)}));
```

By default it tests identity/repository access and reads PR metadata when a
unique target is available. To test one actual pending inline comment, supply
`prNumber`, `expectedLogin`, and
`inline: {expectedHead, path, line, side, body}` only for an explicitly
authorized test target. It leaves the test draft for user inspection and never
submits/deletes it. Existing pending reviews and changed heads block writes.
Its creation adapter targets the official GitHub MCP server's documented
pending-review tools; other transports require a verified adapter.
