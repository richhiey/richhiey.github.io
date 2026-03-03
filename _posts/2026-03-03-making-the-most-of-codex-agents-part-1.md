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

### In the OpenClaw UI

1. Open provider settings and select **OpenAI-compatible** mode.
2. Use the **OpenAI web URL login** option if OpenClaw exposes a browser-based login flow.
3. Set your API base URL to the OpenAI-compatible endpoint (for example: `https://api.openai.com/v1` for OpenAI, or your self-hosted gateway URL).
4. Save, reload model list, and pick the model you want for agent tasks.

### Verify from terminal first (recommended)

Before running agent automations in OpenClaw, verify auth and endpoint behavior from terminal:

```bash
export OPENAI_API_KEY="<your_api_key>"
export OPENAI_BASE_URL="https://api.openai.com/v1"   # or your OpenAI-compatible URL

curl -s "$OPENAI_BASE_URL/models"   -H "Authorization: Bearer $OPENAI_API_KEY"   -H "Content-Type: application/json" | jq '.data[0:5]'
```

Then test a minimal chat request:

```bash
curl -s "$OPENAI_BASE_URL/chat/completions"   -H "Authorization: Bearer $OPENAI_API_KEY"   -H "Content-Type: application/json"   -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Reply with: OpenClaw connectivity OK"}],
    "temperature": 0
  }' | jq '.choices[0].message.content'
```

If both calls work, OpenClaw usually works as long as its provider URL/model name match exactly.

### Common failure checks

- 401/403 -> bad API key, missing org/project scope, or wrong auth header.
- 404 -> wrong base URL path (missing `/v1` is common).
- model-not-found -> model name mismatch between terminal test and OpenClaw config.
- timeout -> proxy/firewall/VPN issue; test with `curl -v` to inspect connection behavior.

Practical tip: keep a small "hello task" (for example, edit a markdown file) to validate auth, permissions, and repository write access before running bigger automations.

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
