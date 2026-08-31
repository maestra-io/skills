<a href="https://maestra.io"><img src="assets/maestra-green.svg" alt="Maestra" width="220"></a>

# Agent skills

Skills that let Claude work in your [Maestra.io](https://maestra.io) account: set up once, then just chat. The setup is two steps: connect Maestra to Claude, then install the skills.

## What's inside

| Skills | What they do |
|---|---|
| **Emails** | Create and edit emails in the visual editor from a text description: layout, images, preview, saving into your campaign as a draft. Sending stays in Maestra. |
| **Filters** | Build a filter from a request in plain words and get a link to the list in your account; explain a filter your account already stores. It can't change anything. |

The skills see only what you can see in Maestra.

## Setup

Stuck at any point? Paste the link to this page into Claude and ask it to walk you through, or write to us in the Maestra support chat.

### Step 1. Connect Maestra to Claude

1. In Maestra, open **Integrations → MCP server** and copy your account's connector link.
2. In Claude, go to **Settings → Connectors → Add custom connector** and paste the link ([step-by-step guide](https://help.maestra.io/api-integrations/connect-an-ai-assistant-to-maestra-via-mcp)).

**On a Team or Enterprise plan** — only the workspace Owner can add connectors: send them the connector link.

### Step 2. Install the skills

1. In Claude, open **Settings → Plugins**.
2. Click **Add → Add marketplace**, paste `https://github.com/maestra-io/maestra-plugins`, and click **Sync**.
3. The **Maestra** plugin appears — click **+** to install it.

Using a different AI tool? See [Other AI tools](#other-ai-tools).

## Try it

First, check the connection:

- "What Maestra tools do you have?"

Phrases like "create an email" or "build a filter" wake the right skill:

- "Create an email in Maestra: a spring-sale promo with a hero image, two product cards, and a discount code. Show me a preview before saving."
- "Build a filter: customers with a confirmed email who bought Nike in the last 90 days."

## Other AI tools

**ChatGPT** — this repository works there as a plugin too: in the ChatGPT app, open **Plugins → Add → Add a marketplace** and paste `https://github.com/maestra-io/maestra-plugins`.

For developers — the skills follow the open [Agent Skills](https://skills.sh) standard, so Codex, Cursor, and other compatible agents can use them:

```
npx skills add maestra-io/maestra-plugins
```

## License

[Apache-2.0](LICENSE)
