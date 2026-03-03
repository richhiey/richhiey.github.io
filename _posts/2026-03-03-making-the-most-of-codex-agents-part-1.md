---
layout: post
title: "Making the Most of Codex Agents - Part 1"
description: "How I got started with Codex agents for practical projects"
date: 2026-03-03 09:00:00 +0530
---

I have been wanting to document a practical Codex workflow for a while, so this is the beginning of a new series.

In this **Part 1**, I will cover:

- Why the **$20 plan** is a sweet spot for hobby projects
- How to get comfortable with the Codex interface
- A real first task: music transcription + pull requests
- Integrating Codex with **OpenClaw** via OpenAI web URL login
- What I am planning next in this journey

## Why I chose the $20 plan

If you're an independent builder, the $20 plan is a great cost saver.

For me, it balances:

- Enough usage for evenings/weekend hacking
- Room for multiple iterations on one task
- A predictable monthly budget

Unless you are running heavy daily automations or large team workflows, this tier is usually enough to get consistent progress without overcommitting.

## Getting into the interface quickly

My onboarding was simple:

1. Start with one repository that has clear structure.
2. Give Codex one scoped task at a time.
3. Ask it to explain changes before committing.
4. Review diffs like you would review a teammate's PR.

The key is to treat Codex as an engineering partner, not a magic black box.

## First task: building `transcribemusic` with iterative Codex development

By "transcribe music," I mean the project we built iteratively with Codex:

- Repo: [richhiey/transcribemusic](https://github.com/richhiey/transcribemusic)

The workflow was intentionally iterative:

1. Start from a very small goal (single-file transcription path).
2. Run the code and inspect outputs.
3. Ask Codex for focused improvements (error handling, CLI options, output formatting, docs).
4. Re-run and verify.
5. Repeat until the feature felt stable.

That iterative loop was the real unlock. Instead of trying to get everything perfect in one prompt, we used short feedback cycles and kept momentum.

### How the pull requests were created

For each iteration, we followed a repeatable PR workflow with Codex:

1. Ask Codex to summarize exactly what changed.
2. Stage only relevant files.
3. Commit with a scoped message.
4. Generate a PR title + body that includes:
   - problem/context
   - implementation details
   - validation steps
   - known limitations and next tasks

This process kept each change reviewable and made the project history easier to understand.

## Integrating Codex with OpenClaw using OpenAI web URL login

I also wanted Codex to work inside my OpenClaw setup. Here is the practical setup I now follow.

### In the OpenClaw UI (refined from OpenClaw provider docs)

I now keep this section focused on **OpenClaw-side setup** (not raw OpenAI API testing).

1. Open **Providers -> OpenAI** in OpenClaw.
2. Enable the **OpenAI web URL login** flow.
3. Paste the web URL exactly as shown in the OpenClaw docs page for your deployment.
4. Save provider settings and pick the Codex-capable model in OpenClaw.
5. Run a small agent task from OpenClaw to confirm repo access.

### Terminal steps I use around that UI flow

Use terminal for repeatable local operations around OpenClaw:

```bash
# 1) Start OpenClaw (from your OpenClaw project directory)
docker compose up -d

# 2) Follow logs while configuring provider settings in the UI
docker compose logs -f openclaw

# 3) Restart after provider/config changes
docker compose restart openclaw
```

If your OpenClaw deployment supports `.env` config, keep these values there and restart:

```bash
cat > .env <<'EOF'
OPENCLAW_PROVIDER=openai
OPENCLAW_OPENAI_LOGIN_MODE=web_url
OPENCLAW_OPENAI_WEB_URL=<use-the-url-from-openclaw-docs>
OPENCLAW_MODEL=<codex-capable-model-name>
EOF

docker compose up -d --force-recreate
```

### OpenClaw-specific troubleshooting (not OpenAI API checks)

- Login loop in UI -> clear browser session/cookies for the OpenClaw host and retry web login.
- Model does not appear -> confirm provider saved, then restart OpenClaw and refresh model list.
- Agent can answer but cannot edit repo -> check workspace mount and repository permissions in your OpenClaw runtime.
- Silent failures -> inspect `docker compose logs -f openclaw` during task execution.

Practical tip: keep a tiny "hello task" (for example, edit one markdown line in a branch) to validate end-to-end OpenClaw -> Codex -> repo workflow before larger automations.

## Jekyll + GitHub Actions publishing loop

For this blog itself, my loop is simple:

1. Draft/update post locally.
2. Commit and push to the website repo.
3. Let GitHub Pages deploy through Actions.
4. Verify the live page once the workflow completes.

As this series continues, I plan to automate more of this loop with Codex while keeping final human review before merge.

## Next steps in this series

In **Part 2**, I plan to cover:

- Prompt patterns that reduce rework
- Guardrails for safer autonomous edits
- CI-aware task planning
- Better review loops for agent-authored pull requests

If you're also experimenting with Codex agents, this is a good moment to start small, build confidence, and iterate fast.
