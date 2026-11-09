# Skills shared by MSG group

**Audience: users and maintainers.**
This document explains skill installation and configuration. It is not an
instruction for an agent to perform setup during a review.

## Review skills setup

Follow the [repository installation guide](../README.md#set-up-the-msg-workflows-plugin)
to install the plugin. From the repository root, run:

```bash
python3 scripts/setup_codex.py
```

The setup script performs these steps:

1. Copies `skills/*/agent-definitions/*.toml` into `CODEX_HOME/agents`, or
   `~/.codex/agents` when `CODEX_HOME` is unset. Filenames must be unique.
   Matching installed files are replaced; personal files with other names
   remain untouched. Skill metadata in `agents/openai.yaml` is not copied.
2. Runs setup for the MCP services documented under `config/`. GitHub setup
   asks for a personal token or reuses the saved one, stores it through Git
   credential-store, and applies the GitHub configuration template. It
   preserves unrelated settings and backs up changed configuration. Conflicting
   unmanaged GitHub settings stop setup and print the proposed block for
   manual reconciliation.
3. Checks the saved token's account, official GitHub MCP tools and PR access,
   creates or refreshes your timestamped comment on the permanent test PR,
   and verifies the local Codex MCP entry. Failed checks stop setup.

Restart Codex after successful setup. Installing the skills plugin alone does
not register runtime agents. Rerunning setup refreshes the bundled definitions;
keep personal variants under different filenames.

The reviewer definition is
[code-review/agent-definitions/code-review.toml](code-review/agent-definitions/code-review.toml).
Edit its model and reasoning settings if needed. Local `code-review` needs no
GitHub connection; `pr-review` uses the configured GitHub MCP. For token
permissions and storage, see [GitHub setup](../config/github/README.md).
Other service guides are listed in [config/README.md](../config/README.md);
[script usage](../scripts/README.md#team-setup) describes the setup functions.

Invocation and inherited runtime constraints are documented separately in
[the agent execution reference](code-review/references/agent-setup.md).

## Structure of one skill

Each directory under `skills/` describes one capability. Only `SKILL.md` is
required; the other files and directories are added when needed:

```text
skill-name/
├── SKILL.md                 Agent instructions and skill discovery metadata
├── README.md                Optional human documentation for this skill and its helpers
├── agents/                  Reserved for host-specific skill metadata
│   └── openai.yaml          Codex skill display and invocation settings
├── agent-definitions/       Optional runtime agents associated with this skill
│   └── agent-name.toml      Model, instructions, and runtime settings
├── references/              Supporting instructions and specifications for AI
├── scripts/                 Executable helpers used by the skill
└── assets/                  Templates and other files used in generated output
```

Keep at most one `README.md` per skill, at its root. Put skill-specific user
instructions and helper-script documentation there, rather than adding READMEs
inside subdirectories. Agent instructions belong in `SKILL.md` and relevant
`references/` files. Shared skill installation instructions belong in this
README. MCP configuration instructions belong in
[config/README.md](../config/README.md) and its linked service guides.

**Inside a skill, `agents/` is reserved for host-specific skill metadata.**
Codex expects [the metadata file at `agents/openai.yaml`](https://developers.openai.com/plugins/deploy/submission-errors#skill-agent-metadata-errors).
It describes the skill's display name, short description, suggested prompt,
and invocation policy. It is read by the host application, not supplied as the
reviewer's task instructions. It neither defines a runtime agent nor selects
its model. Keep this file at the documented location; moving it to the skill
root would not follow Codex's supported metadata layout.

**`agent-definitions/` contains runtime agents associated with the skill.**
This directory is our repository convention. Each TOML file defines an agent's
name, model, reasoning effort, instructions, and feature settings.
`scripts/setup_codex.py` copies `skills/*/agent-definitions/*.toml` into the
user's Codex agents directory. It does not copy the skill's `agents/` metadata.
Registration makes a runtime agent available; it does not automatically spawn it.

### Runtime agent TOML format

The file format is defined by Codex; only our `agent-definitions/` source
directory is a team convention. Each file defines one agent. For example,
with shortened instructions:

```toml
name = "code-review"
description = "Review local changes using the code-review skill."
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
developer_instructions = """
Follow the code-review skill and its team policy.
"""

[features]
apps = false
memories = false
```

- `name`: required identity used to select the agent; match the filename to it.
- `description`: required explanation of when to use the agent.
- `developer_instructions`: required behavioral instructions; triple quotes
  allow multiple lines. Our reviewer refers to its skill instead of repeating
  the review policy.
- `model` and `model_reasoning_effort`: optional model and reasoning settings
  for this agent.
- `[features]`: a table of capability settings. Here `false` disables apps and
  memories for the reviewer. It does not create a separate filesystem sandbox.

Permissions and MCP configuration are inherited from the parent session.
See the [official custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema)
for supported fields and settings.


## Work with AAS
[AAS](https://github.com/sickn33/agentic-awesome-skills) is a catalogue of over 2000 skills.

### Install MCP to search and install skills from codex

> npm exec --yes --ignore-scripts --package=agentic-awesome-skills@18.10.0 -- \
  aas mcp configure \
  --host codex \
  --scope user \
  --config "$HOME/.codex/config.toml" \
  --cache-root "$HOME/.cache/aas"

That outputs something like:
{"action":"mcp.configure","approvalDigest":"APPROVAL_DIGEST_HASH", ...

Make sure "$HOME/.cache" is not writable by group:
> chmod g-w "$HOME/.cache"


Then you call the same command with appended --approve ...:
> npm exec --yes --ignore-scripts --package=agentic-awesome-skills@18.10.0 -- \
  aas mcp configure \
  --host codex \
  --scope user \
  --config "$HOME/.codex/config.toml" \
  --cache-root "$HOME/.cache/aas" \
  --backup-dir "$HOME/.codex/aas-backups" \
  --approve <APPROVAL_DIGEST_HASH>

This installs AAS MCP user wide and for the Codex CLI. 
So verify that by:
> codex mcp list

## Search and install skills into given directory (msg_common/skills)
