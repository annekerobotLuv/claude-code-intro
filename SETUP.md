# Teacher Setup

One-time setup before the workshop. ~10 minutes.

## 1. Get an API key with a spending cap

1. Go to [console.anthropic.com](https://console.anthropic.com) and create/sign into your account
2. Create a **Workspace** (e.g., "HS Workshop") so this billing is isolated from any other work
3. Add **prepaid credits** — $200 is a safe starting point for 20 students × 1 hour on Sonnet. Prepaid is safer than a card on file: it literally cannot overspend.
4. Turn on **Auto Reload** (e.g., "top up $100 when balance drops under $50") so you don't have to watch the dashboard mid-workshop.
5. Set a **monthly spend limit** on the workspace as a second safety net.
6. Generate an **API key** scoped to that workspace. Copy it.

## 2. Create the GitHub repo

1. Push this template to `github.com/diganelin/claude-code-intro` (public or private — either works).
2. Go to the repo's **Settings > Secrets and variables > Codespaces**.
3. Add a new secret:
   - Name: `ANTHROPIC_API_KEY`
   - Value: the key you copied above
4. That's it — the key is now injected into every student's Codespace as an env var, invisible to them.

## 3. Test it

Open the launch link yourself:
`https://codespaces.new/diganelin/claude-code-intro?quickstart=1`

Wait for the container to build. Open the terminal, type `claude`, confirm it starts (no API key prompt = env var is working). Try a quick Streamlit app end-to-end so you've seen the full flow students will see.

## 4. Day-of tips

- Share the launch link in a chat/doc at the start of the session.
- If credits run low mid-workshop, you can top up from console.anthropic.com in under a minute (Plans & Billing > Add Credits).
- After the workshop: delete the `ANTHROPIC_API_KEY` secret (and revoke the key in the Anthropic console) so no one keeps spending on leftover Codespaces.
- Bulk-delete student Codespaces from `github.com/codespaces` to stop any storage fees.

## Cost expectations (20 students × ~1 hour)

- **Codespaces compute**: ~$15 (2-core × ~2 hours with buffer, $0.18/hr)
- **Claude API**: ~$60–150 on Sonnet 4.6 (the default set in `devcontainer.json`)
- **Total**: ~$75–165

## Switching models

To have students try Opus for a prompt or two, they can type `/model` inside Claude Code and pick Opus. Or change the default in `.devcontainer/devcontainer.json`:

```json
"ANTHROPIC_MODEL": "claude-opus-4-6"
```

Opus roughly 2–3x the cost per student — budget accordingly.
