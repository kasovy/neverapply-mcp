# NeverApply MCP plugin

Plugin for the hosted [NeverApply](https://neverapply.co) MCP server at `https://neverapply.co/mcp`, for Claude, Cursor and Grok Build. This repository holds only manifests, skills and an icon. The server runs on NeverApply; no server code, API key or token is here.

With the plugin, your AI assistant can search jobs, explain your matches, show your application history, update your profile, prepare resume and interview drafts, and apply to jobs you approve, all from your NeverApply account.

## Use it

Ask in plain words, for example:

- "Find remote product manager jobs in Germany that fit me."
- "Why is this job a good match?"
- "Apply to the Acme job with my tailored resume."
- "What applications are waiting for me?"

The plugin's skills teach Claude the steps: read your profile first, use only real job IDs, show salary only when the employer stated it, and ask for your approval of each named job before it applies.

## Files

| File | Used by |
| --- | --- |
| `.claude-plugin/plugin.json`, `.mcp.json` and `skills/` | Claude (claude.ai, desktop, Cowork and Claude Code) |
| `.cursor-plugin/plugin.json` and `mcp.json` | Cursor |
| `.grok-plugin/plugin.json` and `.mcp.json` | Grok Build |
| `assets/neverapply-96.png` | Cursor and Grok Build manifests |

The skills are `find-jobs`, `apply-to-jobs` and `track-applications`.

## Connect

1. Install the plugin in Claude, Cursor or Grok Build. In Claude, connect NeverApply on the plugin's Connectors tab.
2. Choose Connect. Your browser opens the NeverApply sign-in. Use Google, LinkedIn or your email, or create an account.
3. Sign in and choose which permissions to give: `mcp:read`, `mcp:write` or `mcp:apply`.

The server uses OAuth 2.1 with PKCE only. Never paste a bearer token into these files.

Grok chat does not use this plugin. Add a custom connector at [grok.com/connectors](https://grok.com/connectors) with the URL `https://neverapply.co/mcp`.

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

## License

[MIT](LICENSE). The license covers the files in this repository only, not the NeverApply service.
