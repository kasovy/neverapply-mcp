# NeverApply MCP plugin

Plugin for the hosted [NeverApply](https://neverapply.co) MCP server at `https://neverapply.co/mcp`, for Claude, ChatGPT and Codex, Cursor, VS Code with GitHub Copilot, Gemini CLI, Kiro and Grok. This repository holds only manifests, skills and an icon. The server runs on NeverApply; no server code, API key or token is here.

With the plugin, your AI assistant can search jobs, explain your matches, show your application history, update your profile, prepare resume and interview drafts, and apply to jobs you approve, all from your NeverApply account.

## Server

| | |
| --- | --- |
| URL | `https://neverapply.co/mcp` |
| Transport | Streamable HTTP |
| Authentication | OAuth 2.1 with PKCE and dynamic client registration. No API key. |
| Docs | [neverapply.co/features/mcp](https://neverapply.co/features/mcp) |

The same URL works in every assistant. When you connect, your browser opens the NeverApply sign-in. Sign in, or create an account, and choose which permissions to give: `mcp:read`, `mcp:write` or `mcp:apply`. Never paste a bearer token into a config file.

## Install

### Claude (claude.ai, desktop and Cowork)

Open Customize → Connectors → Add custom connector and enter `https://neverapply.co/mcp`. On Team or Enterprise, an owner adds it in Organization settings first. Connect and sign in.

### Claude Code

Install the plugin, which adds the server and the skills:

    /plugin install neverapply --marketplace kasovy/neverapply-mcp

Or, from your shell:

    claude plugin marketplace add kasovy/neverapply-mcp
    claude plugin install neverapply@neverapply

To add only the server, run `claude mcp add --transport http neverapply https://neverapply.co/mcp`. Then run `/mcp` in Claude Code and sign in.

### ChatGPT

For a custom connection, enable Developer mode in Settings → Security and login. Open Plugins, select +, add `https://neverapply.co/mcp`, and complete OAuth sign-in.

### Codex

Add the server and sign in:

    codex mcp add neverapply --url https://neverapply.co/mcp
    codex mcp login neverapply

Or add it to `~/.codex/config.toml`, then run `codex mcp login neverapply`:

```toml
[mcp_servers.neverapply]
url = "https://neverapply.co/mcp"
```

To install the plugin with its skills instead, add this repository as a marketplace:

    codex plugin marketplace add kasovy/neverapply-mcp
    codex plugin add neverapply@neverapply
    codex mcp login neverapply

### Cursor

Install the NeverApply plugin, or add the server to `.cursor/mcp.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "neverapply": {
      "url": "https://neverapply.co/mcp"
    }
  }
}
```

Then use Cursor's Connect action to sign in with OAuth.

### VS Code and GitHub Copilot

Run:

    code --add-mcp '{"name":"neverapply","type":"http","url":"https://neverapply.co/mcp"}'

Or add the server to `.vscode/mcp.json`:

```json
{
  "servers": {
    "neverapply": {
      "type": "http",
      "url": "https://neverapply.co/mcp"
    }
  }
}
```

Start the server from the file or the MCP servers list, sign in when VS Code asks, and use it in Copilot Chat agent mode.

### Gemini CLI

Install the extension, which adds the server and the skills:

    gemini extensions install https://github.com/kasovy/neverapply-mcp

Then run `/mcp auth neverapply` in Gemini CLI and sign in. To add only the server, put this in `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "neverapply": {
      "httpUrl": "https://neverapply.co/mcp"
    }
  }
}
```

### Kiro

Open the Powers panel, choose Add Custom Power → Import power from GitHub, and enter `https://github.com/kasovy/neverapply-mcp`.

### Grok

Grok Build uses the plugin in this repository. In Grok chat, if your account offers custom connectors, open [grok.com/connectors](https://grok.com/connectors), choose New Connector then Custom, enter `https://neverapply.co/mcp`, and complete authentication.

## Use it

Ask in plain words, for example:

- "Find remote product manager jobs in Germany that fit me."
- "Why is this job a good match?"
- "Apply to the Acme job with my tailored resume."
- "What applications are waiting for me?"

The plugin's skills teach your assistant the steps: read your profile first, use only real job IDs, show salary only when the employer stated it, and ask for your approval of each named job before it applies.

## Tools

| Access | Tools |
| --- | --- |
| Read | `search_jobs`, `get_matches`, `get_job`, `get_profile`, `list_applications`, `get_application` |
| Edit | `update_profile`, `upload_resume`, `save_answer`, `tailor_resume`, `prepare_interview`, `send_feedback` |
| Apply | `apply_to_job`, `answer_screening_question`, `approve_application` |

## Files

| File | Used by |
| --- | --- |
| `.claude-plugin/plugin.json`, `.mcp.json` and `skills/` | Claude (claude.ai, desktop, Cowork and Claude Code) |
| `.claude-plugin/marketplace.json` | Claude Code plugin marketplace and marketplace indexes |
| `plugin.json`, `mcp.json`, `skills/` and `assets/` | Agent Plugins: Codex and ChatGPT, Kiro powers and Cursor |
| `.agents/plugins/marketplace.json` | Codex plugin marketplace |
| `.cursor-plugin/plugin.json`, `mcp.json` and `assets/` | Cursor |
| `gemini-extension.json` and `skills/` | Gemini CLI extension and gallery |
| `.grok-plugin/plugin.json`, `.mcp.json` and `assets/` | Grok Build |
| `lhm.plugin.json` | LobeHub MCP marketplace |

The skills are `find-jobs`, `apply-to-jobs` and `track-applications`. `scripts/validate.py` checks every manifest against its published schema in CI.

## Data

The plugin sends your requests and the tool arguments that your assistant chooses (for example a job search, a `listing_id`, profile answers or a pasted resume) to NeverApply at `https://neverapply.co/mcp`, over HTTPS with your OAuth token. It sends data nowhere else, runs no code on your computer, and stores nothing itself. NeverApply stores your account data as its [privacy policy](https://neverapply.co/privacy) describes. When you apply, NeverApply sends your application to the employer's own hiring site.

## Permissions and costs

- Searching, reading your matches and applications, and editing your profile are free within usage limits.
- Resume tailoring and interview preparation need paid feature access.
- Applying needs the `mcp:apply` scope, credits and your approval of each named job. Without a separate send permission for this client, the application waits for your approval and costs nothing.
- Disconnect a client at any time in NeverApply under Settings → Connected AI clients.

## Links

- [Connector guide](https://neverapply.co/features/mcp#connector-guide)
- [Authorization guide](https://neverapply.co/auth.md)
- [Privacy](https://neverapply.co/privacy) and [terms](https://neverapply.co/terms)
- Support: hello@neverapply.co

NeverApply is operated by Kasovy LLC, 30 N Gould St STE R, Sheridan, WY 82801, USA.

## License

[MIT](LICENSE). The license covers the files in this repository only, not the NeverApply service.
