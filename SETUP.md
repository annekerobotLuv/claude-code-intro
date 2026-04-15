# Teacher Setup

Everything you need before, during, and after the workshop.

## Timeline at a glance

| When | What |
|---|---|
| ~1 week before | Anthropic workspace + prepaid credits + API key |
| ~1 week before | Push repo, add Codespaces secret, dry run |
| **Right after dry run** | **Delete the Codespaces secret** (safety window) |
| ~3 days before | Ask students to create GitHub accounts |
| Morning of workshop | Re-add the Codespaces secret, re-test |
| During workshop | Share launch link, monitor usage |
| **Immediately after workshop** | **Delete secret + revoke API key + delete codespaces** |

---

## Pre-workshop (one-time, ~15 min)

### 1. Set up the Anthropic workspace

1. Go to [console.anthropic.com](https://console.anthropic.com), sign in.
2. Create a **Workspace** (e.g., "HS Workshop") to isolate this billing.
3. Add **prepaid credits** — $200 is a safe start. Prepaid means it can literally never overspend.
4. Turn on **Auto Reload** (e.g., "top up $100 when balance drops under $50").
5. Set a **monthly spend limit** on the workspace as a second safety net.
6. **Check for model allowlist** in the workspace settings — if available, restrict to Sonnet 4.6 (+ Haiku if you want). If the UI doesn't expose this, skip it; the prepaid cap is your real safety net.
7. Generate an **API key** scoped to the workspace. Copy it.

### 2. Add the key to GitHub Codespaces

1. Go to `github.com/diganelin/claude-code-intro/settings/secrets/codespaces`
2. **New repository secret** → Name: `ANTHROPIC_API_KEY`, Value: paste the key
3. Save. GitHub encrypts at rest; you can't view it back, only overwrite or delete.

### 3. Dry run

Open the launch link yourself: `https://codespaces.new/diganelin/claude-code-intro?quickstart=1`

- Wait ~60s for the container to build
- Open the terminal, type `claude`
- At the "Do you want to use this API key?" prompt → pick **Yes (option 1)**. Default is No.
- Build a small Streamlit app end-to-end. Confirm the browser tab pops up when the port is forwarded.
- Type `/cost` and note the token usage for your later teaching demo.

### 4. After dry run: delete the Codespaces secret

Go back to `github.com/diganelin/claude-code-intro/settings/secrets/codespaces` and **delete** `ANTHROPIC_API_KEY`. Until workshop day, anyone who finds the repo and launches a Codespace just gets a Claude Code that can't authenticate — harmless.

### 5. Student pre-work (email them ~3 days before)

Ask students to:
1. Create a GitHub account at `github.com/signup` (free, ~2 min)
2. Reply with their GitHub username (in case you want to switch to private/collaborators later)

## Morning of workshop

1. **Re-add** the `ANTHROPIC_API_KEY` Codespaces secret at the URL above.
2. **Re-test** by opening the launch link yourself and typing `claude`. Confirm the API key prompt appears (proves the env var is injecting).
3. Check the Anthropic dashboard — balance should match what you set up.

## During workshop

- Share the launch link directly in your session chat/doc (not publicly):
  `https://codespaces.new/diganelin/claude-code-intro?quickstart=1`
- Remind students: **at the API key prompt, pick Yes (option 1)** — it defaults to No.
- Peek at console.anthropic.com once or twice to confirm spending is on track.
- If credits run low: Plans & Billing → Add Credits (~1 min via saved card).

## Immediately after workshop (shutdown checklist)

The repo is public, so rotate fast to minimize exposure:

- [ ] Delete the `ANTHROPIC_API_KEY` Codespaces secret
- [ ] Revoke the API key at console.anthropic.com → Workspace → API Keys
- [ ] Bulk-delete student codespaces at `github.com/codespaces` (stops any storage fees)
- [ ] Optionally disable Auto Reload on the Anthropic workspace
- [ ] Leave any remaining prepaid credits for your own use (they're yours, don't expire quickly)

## GitHub billing — do I need it?

**No.** Each student's Codespace bills against their own GitHub free tier (120 core-hours/month for free accounts, 180 for Pro). Your workshop uses ~4 core-hours per student — 2-3% of their monthly allowance. Your own dry runs also come out of your free tier. Set `Spending limits: $0` at `github.com/settings/codespaces` as a belt-and-suspenders zero-cost sanity check.

## Cost expectations (20 students × ~1 hour)

- **Codespaces compute**: $0 to you (student free tier)
- **Anthropic API**: ~$60–150 on Sonnet (the default)
- **Total**: ~$60–150

Opus instead of Sonnet: 2–3x the API cost. Students can try it mid-workshop with `/model`.

## Teaching cheat sheet

A few things we decided are worth demoing early:

### Commands to show in the first 5 minutes
- `/clear` — the "things got weird, reset the conversation" command. Teach this first.
- `/help` — discover everything else.
- `/cost` — shows tokens + dollars used. Great anchor for a 2-min lesson on tokens/context.
- `/model` — switch models. Useful if you want to demo Sonnet vs Opus on the same prompt.

### Non-slash tricks worth mentioning
- `@filename` — reference files by name instead of pasting contents
- `#` at start of a message — adds a rule to `CLAUDE.md` (project memory)
- `!` at start of a message — runs that line as bash directly, no Claude round-trip
- **Esc** — interrupt Claude mid-response if it's going the wrong way
- **Up arrow** — cycles through past prompts (like bash history)
- **Drag-and-drop** files or images into the terminal — attaches to next prompt

### Mental models to seed
- **Context = Claude's desk.** Everything visible to Claude sits on the same desk. Desk gets crowded → slow + pricey + confused. `/clear` = clean the desk.
- **Tokens = chunks of text** (~3/4 of a word). Input cheap, output expensive. Thinking counts as output.
- **Different models = different trade-offs.** Sonnet for most things, Opus for hard problems, Haiku for fast/cheap.

### Live demo idea (90 seconds)
1. Trivial prompt → `/cost` ("basically nothing")
2. "Read this whole folder and summarize every file" → `/cost` again
3. Point at the delta: *that's* context cost.

## Switching default model

`.devcontainer/devcontainer.json` has:
```json
"ANTHROPIC_MODEL": "claude-sonnet-4-6"
```

Change to `claude-opus-4-6` if you want Opus as default — budget 2–3x. Note: this is the *default* only. Students can switch with `/model` unless you restrict at the API key level.
