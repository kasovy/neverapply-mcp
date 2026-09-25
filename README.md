# NeverApply MCP plugin

Plugin manifests for the hosted [NeverApply](https://neverapply.co) MCP server at `https://neverapply.co/mcp`. This repository holds only manifests and an icon. The server runs on NeverApply; no server code, API key or token is here.

With the plugin, your AI assistant can search jobs, explain your matches, show your application history, update your profile, and prepare resume and interview drafts from your NeverApply account.

## Files

| File | Used by |
| --- | --- |
| `.cursor-plugin/plugin.json` and `mcp.json` | Cursor |
| `.grok-plugin/plugin.json` and `.mcp.json` | Grok Build |
| `assets/neverapply-96.png` | Both manifests |

## Connect

1. Install the plugin in Cursor or Grok Build.
2. Choose Connect. Your browser opens the NeverApply sign-in.
3. Sign in and choose which permissions to give: `mcp:read`, `mcp:write` or `mcp:apply`.

The server uses OAuth 2.1 with PKCE only. Never paste a bearer token into these files.

Grok chat does not use this plugin. Add a custom connector at [grok.com/connectors](https://grok.com/connectors) with the URL `https://neverapply.co/mcp`.

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
