#!/usr/bin/env python3
"""Copy all team agents and run setup for every bundled MCP."""

import json
import os
from pathlib import Path
import re
import shutil
import shlex
import subprocess
import sys


def install_agents(agent_files: list[Path], destination: Path) -> None:
    """Copy bundled agent definitions into the user's agents directory.

    Args:
        agent_files: Source TOML paths with unique filenames. Contents are copied
            without parsing; matching destination files are overwritten.
        destination: Agents directory to create if needed.

    Returns:
        None. Prints the destination of each copied file.

    Raises:
        AssertionError: Two source files have the same filename.
    """
    names = [path.name for path in agent_files]
    assert len(names) == len(set(names)), "Duplicate agent filenames"
    destination.mkdir(parents=True, exist_ok=True)
    for source in agent_files:
        target = destination / source.name
        shutil.copy2(source, target)
        print(f"Agent: {target}")


def format_command_for_toml(args: list[str]) -> str:
    """Compose a platform-specific command and encode it as a TOML string.

    Args:
        args: Executable followed by its arguments, each supplied unquoted.

    Returns:
        A string literal including its outer quotes and TOML escaping. Insert
        it directly after a TOML key's equals sign, without further quoting.
    """
    command = subprocess.list2cmdline(args) if os.name == "nt" else shlex.join(args)
    return json.dumps(command)


def apply_github_template(template: Path, config_file: Path, cmd_escaped: str) -> None:
    """Install or refresh the marked MSG GitHub block in Codex configuration.

    Args:
        template: GitHub TOML template containing an http_headers_helper setting.
        config_file: Personal config.toml to create or update. Other settings
            outside the marked block are preserved.
        cmd_escaped: Header-helper command as a complete quoted TOML string
            literal returned by format_command_for_toml(). Inserted verbatim.

    Returns:
        None. Writes only when the rendered configuration changes, first backing
        up an existing file to config.toml.bak. Prints paths of changed files.

    Raises:
        SystemExit: Block markers are malformed or unmarked GitHub sections
            would conflict with the template. The file is left untouched;
            conflicts print the proposed block for manual reconciliation.
    """
    begin, end = "# BEGIN MSG GitHub MCP\n", "# END MSG GitHub MCP\n"
    
    # Form the new MCP config block
    content = re.sub(
        r"(?m)^http_headers_helper =.*$",
        lambda _: f"http_headers_helper = {cmd_escaped}",
        template.read_text(),)
        
    proposed_block = begin + content.rstrip() + "\n" + end
    
    # Split the config.toml to MCP block and remaining "unmanaged" part.
    current = config_file.read_text() if config_file.exists() else ""
    parts = re.split(
        f"({re.escape(begin)}.*?{re.escape(end)})", current, maxsplit=1, flags=re.DOTALL,
    )
    before, block, after = parts if len(parts) == 3 else (current, "", "")
    unmanaged = before + after
    
    # Consistency check for no github config in the unmanaged part.
    if begin in unmanaged or end in unmanaged:
        raise SystemExit("Invalid MSG GitHub MCP block markers; fix config.toml before rerunning setup.")
    
    owned_tables = (
        r'(?m)^\s*\[(?:mcp_servers\.["\']?github_review["\']?(?:\.|\])'
        r'|apps\.["\']?connector_76869538009648d5b282a4bb21c3d157["\']?(?:\.|\]))'
    )
    if re.search(owned_tables, unmanaged):
        print("Proposed GitHub configuration block (file unchanged):")
        print(proposed_block, end="")
        raise SystemExit(
            "Unmanaged GitHub settings found. Remove them or reconcile them with "
            "the proposed block, then rerun setup."
        )
    
    

    updated = before + proposed_block + after
    if updated != current:
        if config_file.exists():
            backup = config_file.with_suffix(".toml.bak")
            shutil.copy2(config_file, backup)
            print(f"  Configuration backup: {backup}")
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text(updated)
        print(f"  Applied GitHub template: {config_file}")


def setup_github(guide: Path, codex_home: Path) -> None:
    """Prompt for the shared token, configure GitHub MCP, and check PR access.

    Args:
        guide: GitHub README path used to locate the provider directory, which
            also contains credentials.py, github-review.toml, and check_access.py.
        codex_home: User's Codex directory; receives github-credentials and the
            managed block in config.toml.

    Returns:
        None after setup and network/comment checks succeed. Prompts for a
        token or reuse of the saved token, and prints progress and check results.

    Raises:
        SystemExit: Access checks fail; preserves the check process's exit code.
            Token storage and configuration changes are not rolled back.
    """
    helper = guide.parent / "credentials.py"
    # JB note: Once we add other MCPs we should abstract the configuration setup so that
    # MCP specific script like 'credentials.py' will be used both as module for MPC specific setup part
    # (e.g. this setup_github function) as well as the helper script as here for credentials extraction.
    credential_file = codex_home / "github-credentials"
    token_form = (
        "https://github.com/settings/personal-access-tokens/new?"
        "name=MSG%20-%20github%20actions&target_name=GeoMop&expires_in=365"
        "&contents=read&issues=read&actions=read&pull_requests=write"
    )
    print(f"  MSG - github actions token form: {token_form}")
    print("  One personal token is reused by all MSG skills accessing GitHub.")
    print("  Git stores this token as plaintext with private file permissions, outside the repository.")
    token = input("MSG - github actions token (Enter to reuse the stored token): ")
    if token:
        subprocess.run(
            [sys.executable, str(helper), "store", str(credential_file)],
            input=token, text=True, check=True,
        )
        print(f"GitHub token saved through Git: {credential_file}")
    else:
        print(f"Using the saved GitHub token: {credential_file}")
    args = [sys.executable, str(helper), "headers", str(credential_file)]
    cmd_escaped = format_command_for_toml(args)
    apply_github_template(guide.parent / "github-review.toml", codex_home / "config.toml", cmd_escaped)
    print("  Testing saved-token PR access and the Codex entry...", flush=True)
    result = subprocess.run(
        [sys.executable, str(guide.parent / "check_access.py"), str(credential_file)],
    )
    if result.returncode:
        sys.exit(result.returncode)


def setup_mcps(guides: list[Path], config_file: Path, handlers: dict) -> None:
    """List MCP resources and invoke each available provider setup function.

    Args:
        guides: Provider README paths. Each parent directory's name identifies
            the provider; sibling TOML templates are listed for reference.
        config_file: Personal Codex config.toml. Its parent is passed to handlers
            as the Codex home directory.
        handlers: Mapping of provider names to functions accepting
            (guide_path, codex_home) and returning None. Providers without a
            handler have their resources listed only.

    Returns:
        None after all matching handlers finish. Handler failures propagate.
    """
    for guide in guides:
        name = guide.parent.name
        print(f"MCP {name}: setup")
        print(f"  Guide: {guide}")
        for template in sorted(guide.parent.glob("*.toml")):
            print(f"  Configuration template: {template}")
        print(f"  Codex configuration: {config_file}")
        handler = handlers.get(name)
        if handler:
            handler(guide, config_file.parent)


def main() -> None:
    """Run team setup with paths and provider choices defined here.

    Takes no arguments. Locates msg_common relative to this script and uses
    CODEX_HOME, or ~/.codex when unset, as the destination. Discovers all bundled
    agents and MCP guides, then copies agents and invokes provider setup.

    Returns:
        None after all setup steps succeed. Prints the completion message only
        on success; failures propagate to the invoking process.
    """
    # Keep paths and service choices here so local adjustments are straightforward.
    repository = Path(__file__).resolve().parents[1]
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()
    agent_files = sorted(repository.glob("skills/*/agent-definitions/*.toml"))
    guides = sorted((repository / "config").glob("*/README.md"))
    handlers = {"github": setup_github}

    install_agents(agent_files, codex_home / "agents")
    setup_mcps(guides, codex_home / "config.toml", handlers)
    print("Setup complete. Restart Codex to load the configured MCP tools.")


if __name__ == "__main__":
    main()
