#!/usr/bin/env python3
"""Validate every manifest in this repository against its published schema or documented rules."""

import json
import re
import sys
import urllib.request
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SERVER_URL = "https://neverapply.co/mcp"
PLUGIN_NAME = "neverapply"

SCHEMAS = {
    "agent-plugin": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "agent-mcp": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
    "claude-plugin": "https://www.schemastore.org/claude-code-plugin-manifest.json",
    "claude-marketplace": "https://www.schemastore.org/claude-code-marketplace.json",
    "gemini-settings": "https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json",
}

errors: list[str] = []


def fail(path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def fetch_schema(key: str) -> dict:
    request = urllib.request.Request(SCHEMAS[key], headers={"User-Agent": "neverapply-mcp-ci"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def load(path: str):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(path, "file is missing")
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON: {exc}")
    return None


def validate_schema(path: str, data, schema: dict) -> None:
    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema, format_checker=validator_cls.FORMAT_CHECKER)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        location = "/".join(str(p) for p in error.path) or "<root>"
        fail(path, f"schema error at {location}: {error.message}")


def require_https(path: str, field: str, value) -> None:
    if not isinstance(value, str) or not value.startswith("https://"):
        fail(path, f"{field} must be an https URL")


def require_asset(path: str, field: str, value) -> None:
    if not isinstance(value, str) or not (ROOT / value).is_file():
        fail(path, f"{field} points to a missing file: {value}")


def check_openai_interface(path: str, interface: dict) -> None:
    # Limits from https://developers.openai.com/plugins/deploy/submission (Listing metadata).
    limits = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
    for field, limit in limits.items():
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(path, f"interface.{field} is required")
        elif len(value) > limit:
            fail(path, f"interface.{field} is longer than {limit} characters")
    if not isinstance(interface.get("category"), str):
        fail(path, "interface.category is required")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        require_https(path, f"interface.{field}", interface.get(field))
    prompts = interface.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if len(prompts) > 3 or len(set(prompts)) != len(prompts) or any(len(p) > 128 for p in prompts):
        fail(path, "interface.defaultPrompt allows up to three unique prompts of at most 128 characters")
    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.startswith("./"):
            fail(path, f"interface.{field} must be a ./-prefixed path")
        else:
            require_asset(path, f"interface.{field}", value)


def server_urls(path: str, servers: dict, key: str = "url") -> None:
    if not isinstance(servers, dict) or set(servers) != {PLUGIN_NAME}:
        fail(path, f"mcpServers must contain exactly one server named {PLUGIN_NAME}")
        return
    if servers[PLUGIN_NAME].get(key) != SERVER_URL:
        fail(path, f"mcpServers.{PLUGIN_NAME}.{key} must be {SERVER_URL}")
    if servers[PLUGIN_NAME].get("headers"):
        fail(path, "server headers must stay empty; authentication is OAuth")


def check_skills() -> None:
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        rel = str(skill.relative_to(ROOT))
        if not match:
            fail(rel, "missing YAML frontmatter")
            continue
        frontmatter = dict(
            line.split(":", 1) for line in match.group(1).splitlines() if ":" in line
        )
        if frontmatter.get("name", "").strip() != skill.parent.name:
            fail(rel, "frontmatter name must match the skill directory")
        if not frontmatter.get("description", "").strip():
            fail(rel, "frontmatter description is required")


def main() -> int:
    schemas = {key: fetch_schema(key) for key in SCHEMAS}
    versions: dict[str, str] = {}

    # Agent Plugins package: Kiro powers, OpenAI Codex and ChatGPT, Cursor.
    plugin = load("plugin.json")
    if plugin is not None:
        validate_schema("plugin.json", plugin, schemas["agent-plugin"])
        versions["plugin.json"] = plugin.get("version")
        author = plugin.get("author", {})
        if not author.get("name"):
            fail("plugin.json", "author.name is required by Kiro and Codex")
        if not plugin.get("keywords"):
            fail("plugin.json", "keywords are required by Kiro")
        check_openai_interface("plugin.json", plugin.get("extensions", {}).get("com.openai", {}).get("interface", {}))

    mcp = load("mcp.json")
    if mcp is not None:
        validate_schema("mcp.json", mcp, schemas["agent-mcp"])
        server_urls("mcp.json", mcp.get("mcpServers"))

    # Claude, Claude Code and Grok Build.
    claude_mcp = load(".mcp.json")
    if claude_mcp is not None:
        server_urls(".mcp.json", claude_mcp.get("mcpServers"))
        if claude_mcp.get("mcpServers", {}).get(PLUGIN_NAME, {}).get("type") != "http":
            fail(".mcp.json", "server type must be http")

    claude_plugin = load(".claude-plugin/plugin.json")
    if claude_plugin is not None:
        validate_schema(".claude-plugin/plugin.json", claude_plugin, schemas["claude-plugin"])
        versions[".claude-plugin/plugin.json"] = claude_plugin.get("version")

    marketplace = load(".claude-plugin/marketplace.json")
    if marketplace is not None:
        validate_schema(".claude-plugin/marketplace.json", marketplace, schemas["claude-marketplace"])
        entries = marketplace.get("plugins", [])
        if [e.get("name") for e in entries] != [PLUGIN_NAME] or entries[0].get("source") != "./":
            fail(".claude-plugin/marketplace.json", f"must list only {PLUGIN_NAME} with source ./")

    # OpenAI Codex repo marketplace.
    codex_marketplace = load(".agents/plugins/marketplace.json")
    if codex_marketplace is not None:
        path = ".agents/plugins/marketplace.json"
        if not codex_marketplace.get("name"):
            fail(path, "name is required")
        for entry in codex_marketplace.get("plugins", []):
            source = entry.get("source", {})
            source_path = source if isinstance(source, str) else source.get("path", "")
            if not source_path.startswith("./") or ".." in source_path.split("/"):
                fail(path, "source.path must be ./-prefixed and stay inside the repository")
            elif not (ROOT / source_path / "plugin.json").is_file():
                fail(path, f"no plugin.json at {source_path}")
            policy = entry.get("policy", {})
            if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
                fail(path, "policy.installation is missing or invalid")
            if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
                fail(path, "policy.authentication is missing or invalid")
            if not entry.get("category"):
                fail(path, "category is required")
            if entry.get("name") != PLUGIN_NAME:
                fail(path, f"plugin name must be {PLUGIN_NAME}")

    # Gemini CLI extension.
    gemini = load("gemini-extension.json")
    if gemini is not None:
        path = "gemini-extension.json"
        versions[path] = gemini.get("version")
        if gemini.get("name") != PLUGIN_NAME or not re.fullmatch(r"[a-z0-9-]+", gemini.get("name", "")):
            fail(path, f"name must be {PLUGIN_NAME} (lowercase letters, numbers and dashes)")
        for field in ("version", "description"):
            if not gemini.get(field):
                fail(path, f"{field} is required")
        server_schema = dict(schemas["gemini-settings"]["$defs"]["MCPServerConfig"])
        server_schema["$defs"] = schemas["gemini-settings"]["$defs"]
        for name, server in gemini.get("mcpServers", {}).items():
            validate_schema(f"{path} mcpServers.{name}", server, server_schema)
            if "trust" in server:
                fail(path, "extensions may not set trust")
        server_urls(path, gemini.get("mcpServers"), key="httpUrl")

    # LobeHub MCP marketplace.
    lobehub = load("lhm.plugin.json")
    if lobehub is not None:
        path = "lhm.plugin.json"
        versions[path] = lobehub.get("version")
        if not re.fullmatch(r"[\da-z][\d_a-z-]*", lobehub.get("identifier", "")):
            fail(path, "identifier is required and must match ^[\\da-z][\\d_a-z-]*$")
        for field in ("name", "version"):
            if not lobehub.get(field):
                fail(path, f"{field} is required")
        for field in ("authorUrl", "homepage", "cloudEndpoint", "icon"):
            if field in lobehub:
                require_https(path, field, lobehub[field])
        if lobehub.get("cloudEndpoint") != SERVER_URL:
            fail(path, f"cloudEndpoint must be {SERVER_URL}")

    # Cursor and Grok Build manifests.
    for path in (".cursor-plugin/plugin.json", ".grok-plugin/plugin.json"):
        manifest = load(path)
        if manifest is None:
            continue
        versions[path] = manifest.get("version")
        if manifest.get("name") != PLUGIN_NAME:
            fail(path, f"name must be {PLUGIN_NAME}")
        if "logo" in manifest:
            require_asset(path, "logo", manifest["logo"])

    for path, manifest in (("plugin.json", plugin), (".claude-plugin/plugin.json", claude_plugin)):
        if manifest is not None and manifest.get("name") != PLUGIN_NAME:
            fail(path, f"name must be {PLUGIN_NAME}")

    if len(set(versions.values())) != 1:
        fail("versions", f"all manifests must share one version: {versions}")

    check_skills()

    if errors:
        print("\n".join(errors))
        return 1
    print(f"All manifests are valid (version {next(iter(versions.values()))}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
