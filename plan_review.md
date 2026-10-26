# Plan: local code review and PR review orchestration

Status: proposed implementation plan. This change creates the plan only; skill
and agent changes follow in a separate implementation step.

## Intended result

Maintain two review skills:

- `code-review`: review locally available changes against a shared team policy,
  returning findings and optionally saving findings and/or input context.
- `pr-review`: collect a pull request and its context, delegate analysis to the
  code-review agent, and produce a report or stage GitHub review comments.

Do not introduce a third GitHub publishing skill. Keep analysis in the local
reviewer and remote operations in the PR orchestrator.

## 1. Refactor `skills/review` into `skills/code-review`

- Use the existing workflow and evidence requirements as the starting point.
  Rename its directory, frontmatter name, UI metadata, and invocation examples.
- Move `skills/pr-review/references/review-policy.md` to
  `skills/code-review/references/review-policy.md`. Adapt PR-specific wording to
  general change review while retaining priorities, severity definitions,
  evidence standards, test expectations, and scientific/data checks.
- Require the reviewer to read this policy and applicable repository
  `AGENTS.md` instructions. Keep one authoritative team-policy file; the PR
  skill consumes it through the reviewer rather than duplicating it.
- Preserve repository-specific requirements and identify material conflicts
  with the shared policy instead of silently ignoring them.

### Input contract

- Repository path; default to the current local repository.
- Default target: staged and unstaged changes relative to `HEAD`, plus relevant
  non-ignored untracked source files. Describe the exact scope and avoid
  reviewing generated review reports as source changes.
- Optional explicit target: staged changes, selected paths, or two commits.
  Resolve commit identifiers to immutable SHAs. For two commits, compare their
  trees directly; do not silently replace the first commit with a merge base.
- Optional context: supplied text or local files containing intent,
  requirements, discussion, CI results, constraints, and review focus.
- Only local Git objects and supplied context are required. Do not fetch,
  browse, query hosting APIs, or resolve linked issues remotely. Report missing
  commits or unavailable context to the caller. However search for explicit documentation 
  if in doubts concerning external library use. 
- Inspect the reviewed revision's surrounding code rather than assuming the
  current working tree matches it. 
- Preserve the user's branch, index, and
  existing edits. !! Absolutely read-only for any existing files, the skill can only create temporary files 
  if necessary. !! 
- Use any near history review results `REVIEW_RESULTS.md`  

### Output 

- Always write down findings to the file: ordered by severity, followed by test gaps,
  overall assessment, and review limitations. Distinguish questions from
  evidenced defects.
- Each finding records a stable identifier, severity, title, file and smallest
  useful line range, revision/side where applicable, expected behavior,
  evidence, trigger, impact, and recommended direction.
- No gueses, express doubts if not sure, be technical and short. 
- Avoid comment duplicities for single issue spread ofer the codebase. 
  Describe at one place with an issue name, refer to thet on other places.
- When saving is requested without a path, use `REVIEW_RESULTS-*.md` in the
  repository root. Support a caller-supplied path. 
- If called for a similar review (e. g. same diff sources or modified local state) use 
  the last output file as the input and then update it. 
- Otherwise, do not overwrite any existing file.
- Define read-only precisely: no source edits, commits, pushes, or remote
  writes. Explicitly requested report files and temporary validation artifacts
  are allowed. Run only suitable local checks with available dependencies.
- Create the file at the beginning to make sure to have write permissions.


## 2. Configure a dedicated code-review agent

- Keep `skills/code-review/agents/openai.yaml` for skill discovery/UI metadata.
  It is not the runtime model or sandbox configuration.
- Inspect the installed Codex version and supported agent schema before
  implementing runtime configuration. Add a reusable agent definition and
  document how the plugin/project installs or registers it in consuming repos.
  Do not assume installing a skill automatically registers a custom agent.
- Configure an explicit review-specific model and reasoning default after
  checking available models; keep the choice editable and document it. The
  user has not specified an exact model yet.
- Give the agent a bounded task with the local repository, resolved target,
  context, team policy, and report options. Load `code-review` and delegate
  once; avoid recursively spawning the same reviewer.
- Define its environment as local repository access, existing local test
  tools, and permitted report/temp output. Keep GitHub operations in the
  parent PR agent. Disable remote capabilities where the runtime supports it
  without disabling access to the required skill. However access to possible online 
  documentation must be preserved. 
- Distinguish behavioral restrictions from enforced permissions. Current
  official documentation says custom agents inherit parent permissions and
  MCP servers; model/instructions and supported capability reductions are
  configurable, but a custom agent cannot override the parent's sandbox.
  Verify actual runtime support and do not claim isolation that is not enforced.
- If strict filesystem read-only execution prevents report creation, the review task will end prematurely with an error.
- If agent registration/delegation is unavailable, disclose the limitation;
  do not claim a configured review agent ran when it did not.

Reference: [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## 3. Refactor `skills/pr-review` into an orchestrator

1. Resolve the PR URL/number or current branch's PR and verify repository,
   author intent, base/head SHAs, and the authenticated GitHub identity.
2. Collect description, linked requirements where accessible, discussion,
   existing review threads, CI/check status, and the full change scope. Record
   missing or truncated information explicitly.
3. Ensure the required commits and code are available locally, fetching them
   in the orchestration layer if necessary without disturbing user changes.
   For GitHub PR semantics, resolve the merge base and pass that SHA plus the
   PR head SHA to `code-review`; also preserve the PR base SHA in context.
4. Build a bounded context package and invoke the configured review agent.
   Pass output options explicitly and wait for its findings.
5. Default to a local `REVIEW_RESULTS_*.md` report authored by the reviewer, with
   a concise user-facing result. Support custom paths and optional saved
   input context (whole bundle passed to 'code-review'. In GitHub-comment mode, local report saving remains optional.
6. When the user asks for GitHub comments, use GitHub MCP to stage the review
   as described below. Submission is a separate capability, enabled only by
   an explicit user request, including one given in the initial instruction.
7. Usualy no more then 10 comments per PR, 30 is an absolute limit (unless asked for more explicitely). 
   If more issues detected: sellect the most important, structural, design issues, spredding over the code base. 
   Also try to summarize into fewer more general comments. For more comments next review after resolution is necessary anyway. 

### GitHub comments and submission
- Make a script to check valid and vorking GitHub MCP, test getting a PR info and 
  creating code specific comments. Tast it on the current repository 'msg_common'.
  This is ot part of the skill, but part of the plan.
  
- Discover the available MCP tools and confirm their pending-review semantics;
  do not assume tool names or that every comment tool supports drafts.
- Use authentication under the user's account. Inspect existing pending
  reviews before creating another; preserve manually written comments and
  avoid duplicating findings on retries or after partial failures.
- Map code-specific findings to valid diff lines/sides at the reviewed head.
  Put general findings and the overall assessment into the pending review
  body. A normal PR conversation comment is published immediately and must
  not be used as a substitute for an unsubmitted generic comment.
- Recheck the PR head before staging or submitting. If it changed, refresh
  the relevant analysis and locations instead of posting stale findings.
- Create/update a pending review and its inline comments; verify the review
  remains pending and return its identifier and a useful GitHub link.
- Default: the user inspects, edits, and submits in GitHub. Do not approve,
  request changes, or submit a comment review automatically.
- If submission was explicitly requested, submit only the intended review and
  requested review action; resolve any ambiguity about the action or inclusion
  of existing user comments before submission. Do not ask for authorization
  again when the requested scope is already clear.
- If MCP cannot stage the required pending review, retain a complete local
  report and explain the missing capability. Do not silently publish comments
  or substitute a different transport for the requested MCP workflow.

Reference: [GitHub review creation and pending state](https://docs.github.com/en/rest/pulls/reviews#create-a-review-for-a-pull-request).

## 4. Integrate and validate

- Update README skill tables, policy paths, usage examples, and relevant
  packaging references. Remove the old active `review` entry so the result
  exposes exactly the two requested review skills.
- Inspect consumers before changing references. Leave archival/source copies
  in `skills_primary` and unrelated work untouched unless packaging actually
  depends on them. Do not regenerate packaged archives without a requirement.
- Validate skill frontmatter, UI metadata, reference resolution, and runtime
  agent configuration using the installed tooling.
- Exercise the workflow on isolated local fixtures: mixed staged/unstaged
  changes, two commits while another revision is checked out, missing commits,
  supplied context, no findings, and all report-saving combinations.
- Verify the configured agent is actually selected with the intended model
  and receives the required local context and policy.
- Validate GitHub mapping and lifecycle using mocked MCP responses: inline
  and general findings, existing pending review, changed head, retry after
  partial failure, unavailable draft capability, and explicit submission.
  Do not post to a real PR merely to test this refactor.

## Completion criteria

- Local review works without remote access and uses the shared team policy.
- Any two locally available commits plus supplied context are valid inputs.
- Findings/context file options work independently with the documented default.
- Review-agent model and environment behavior are configured and accurately
  documented, including inherited permission limits.
- PR review delegates analysis rather than duplicating the review procedure.
- Requested GitHub comments remain pending under the user's account unless
  submission was explicitly requested.
- Documentation and packaging references use the new names and policy location.
