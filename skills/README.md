# Skills shared by MSG group.

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
