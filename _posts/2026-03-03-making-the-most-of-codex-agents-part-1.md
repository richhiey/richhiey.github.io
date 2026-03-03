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

The correct setup I use here is based on **OpenClaw docs -> Providers -> OpenAI -> Option B: OpenAI Code (Codex Subscription)**:

- https://docs.openclaw.ai/providers/openai#option-b-openai-code-codex-subscription

### What Option B means

Option B is the path for people using a **Codex subscription login flow** (web login), instead of directly wiring a standard API-key-only provider flow.

### Exact OpenClaw flow for Option B (UI + CLI combined)

1. Start with the OpenClaw onboarding wizard and pick Codex OAuth:

```bash
# Run Codex OAuth in the wizard
openclaw onboard --auth-choice openai-codex
```

2. If you skip the wizard or need to re-authenticate later, run OAuth directly:

```bash
# Or run OAuth directly
openclaw models auth login --provider openai-codex
```

3. Open the OpenClaw TUI and confirm the provider/model selection is available:

```bash
# Open the OpenClaw TUI
openclaw tui
```

4. In the UI path (**Providers -> OpenAI**), select **Option B: OpenAI Code (Codex Subscription)** if prompted and confirm web-login status.
5. Choose the Codex-capable model exposed by that login path.
6. Restart the OpenClaw gateway to reload provider/auth state:

```bash
# Restart OpenClaw gateway after provider/login updates
openclaw gateway restart
```

7. Run a tiny task (for example: "edit one markdown line") to verify end-to-end read/write workflow.

### Practical checks for Option B

- If login succeeds but models are empty, re-open Providers and refresh/reselect Option B.
- If agent replies but cannot commit/edit, check workspace mount + repo permissions in your OpenClaw runtime.
- If session seems stale, restart OpenClaw and repeat Option B web login once.

This keeps the integration aligned with OpenClaw's Codex-subscription flow instead of generic OpenAI API-key wiring.

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
