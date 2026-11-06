# Repository setup and connection checks

## Team setup

Run the script without arguments:

```bash
python3 scripts/setup_codex.py
```

It uses Python 3.10 or later with no extra packages. Install the skills plugin
first using the [root README](../README.md).

### Agent copying

`install_agents()` copies runtime TOMLs from
`skills/<skill>/agent-definitions/` into `CODEX_HOME/agents`, or `~/.codex/agents`
by default.
Files are identified by filename, not parsed. Each filename must be unique and
should match the agent's declared name. The skill-local `agents/` directory is
reserved for host metadata such as `openai.yaml`; setup does not copy it.

Every run replaces matching agent files with the team versions. Personal agent
files with other names remain untouched. There is no update switch or backup
mechanism. Add future runtime agents to the relevant skill's
`agent-definitions/`; no script change is needed.

### MCP setup

`setup_mcps()` prints every guide at `config/<service>/README.md`, its TOML
configuration templates, and the destination configuration. It then runs the
provider-specific setup function. Follow the service guides under
[config/](../config/README.md).

GitHub-specific setup lives in `setup_github()`: it prints the prefilled 365-day
token form named **MSG - github actions** and prompts for the shared personal
token. It passes the token through standard input to
[credentials.py](../config/github/credentials.py), which stores it with Git
credential-store. Setup then applies the GitHub template with the resolved
Codex header-helper command.
Pressing Enter reuses an existing token. See the [storage documentation](../config/github/README.md#store-the-token-with-git)
for its plaintext storage, location, retrieval, and rotation. To add a
new service, add its guide and templates under `config/<service>/`. For extra
service-specific help, add a dedicated function and register it in the handlers
mapping in `main()`.

GitHub setup ends by running `config/github/check_access.py` with the saved
credential file. It reports the authenticated login, tests PR metadata/files/
reviews through the official GitHub MCP server, and checks the local Codex
entry. A failed check stops setup; a valid token is not reported as successful
configuration until the local entry has also been installed and checked. Setup also creates or updates a timestamped test comment; details follow below.

### Local adjustments and checks

There are no command-line options. `main()` derives the repository from the
script's location and collects source paths, the Codex destination, and MCP
handlers. Adjust those values there if necessary. Errors propagate normally
with their Python traceback.

GitHub configuration is installed in a marked `MSG GitHub MCP` block. Reruns
replace only that block, preserving unrelated settings. A changed configuration
is backed up to `config.toml.bak`. Setup always checks outside its marked block
for conflicting GitHub sections. If any exist, it leaves the file untouched and
prints the proposed block. Back up the configuration, then remove or reconcile
the conflicting settings before rerunning setup.

Run the offline setup tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## GitHub access checks during setup

[config/github/check_access.py](../config/github/check_access.py) is an internal
part of setup, not a helper used by the `pr-review` skill. Run
`python3 scripts/setup_codex.py`; setup saves or reuses your token, applies the
configuration, and runs these checks automatically. No JS adapter is needed.

| Check | What it establishes |
| --- | --- |
| Saved-token account | Reads the GitHub username using the stored token. |
| Official MCP connection | Initializes a connection to GitHub's hosted server. |
| Tool catalog | Reads all catalog pages and requires identity, PR-read, pending-review and pending-comment tools. Availability alone does not prove write permission. |
| MCP account | Confirms MCP uses the same account as the saved-token identity check. |
| PR access | Reads PR metadata, verifies a head commit exists, and reads the first files/reviews pages. |
| Comment write | Creates or updates the signed-in user’s marked conversation comment on the permanent test PR and verifies the saved timestamp. |
| Local Codex entry | Confirms `github_review` is enabled with the official URL and a header helper. |

Each successful check prints `PASS`. Failures stop setup with a nonzero exit
status. The default target is `GeoMop/msg_common`, PR #2 (`PERMANENT_TEST_PR`),
defined at the bottom of `check_access.py`. Maintainers can change these values there. An optional
expected username detects an unintended account. With no PR number, the check
can discover a unique PR on `PERMANENT_TEST_PR`; ambiguous results fail rather than selecting one.

These checks contact the server directly. They cannot prove that an existing
Codex session has loaded the new configuration or which tools its host permits.
Restart Codex and inspect `/mcp` for connection status and exposed tools.
Every successful setup creates or refreshes one conversation comment per user
on [the permanent test PR](https://github.com/GeoMop/msg_common/pull/2). The
comment carries `<!-- msg-github-access-check -->` and the current UTC date/time.
Only a comment with that marker authored by the signed-in user is updated;
other comments are left alone. All comment pages are searched before creating
one. The checker verifies the branch is `PERMANENT_TEST_PR` in `GeoMop/msg_common`
before writing, then reads the comment back and prints its URL.

This proves conversation-comment writes, not pending-review or submission
permissions. Setup calls the official MCP server directly; its test comment
does not go through Codex's interactive tool-approval prompts.

### Optional pending-comment diagnostic (maintainers)

The Python checker also retains the old JS probe's optional write test. Enable
it only for an explicitly requested test on a suitable PR. At the entry point
in `check_access.py`, set `expected_login` and an `inline` dictionary with
`expectedHead`, `body`, `path`, positive `line`, and `side` (`LEFT` or `RIGHT`).
Keep an explicit repository and PR number, then run the normal setup command.
Restore `inline = None` afterwards. Normal setup runs the conversation-comment
test above; the additional inline review test remains opt-in. There is no fallback to a submitting tool.

This diagnostic requires Node.js for the existing
`review_data.js validate-location` helper. It checks all existing review/file
pages, refuses an existing pending review by the same account, validates the
line against the real patch, and rechecks the head before writing. It creates
one pending review with general test text and one inline comment. It verifies
the author, commit, comment location/text, review association, pending state,
and unchanged head. It never submits, deletes, or retries a write.

Write attempts and the created review ID are printed. If a write or its
verification fails, inspect the PR in GitHub before rerunning; the request may
have succeeded. Leave the test review unsubmitted for user inspection.

## Offline script checks

These tests use temporary files and simulated GitHub responses. They require
no real token or network access and create no GitHub comments:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
node tests/review_data.test.cjs
node tests/github_pending_review.test.cjs
```

The Python checks cover setup, token storage, MCP responses/catalogs, identity,
PR data, timestamped comment creation/update, and the optional pending-comment
diagnostic's failure safeguards.
The JS checks cover the [production PR helpers](../skills/pr-review/README.md),
including patch locations, comment limits, duplicate prevention, and uploads.
Offline checks do not prove that your live GitHub connection works.
