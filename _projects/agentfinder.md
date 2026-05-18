---
layout: page
title: AgentFinder
eyebrow: Featured project
subtitle: Registry-first A2A platform for discovering, validating, submitting, and integrating live agents.
date: 2026-05-19 00:00:00 +0100
summary: Registry-first A2A platform with public catalog browsing, discovery search, trust signals, submission publishing, and a monetized public API.
link: https://agentfinder-web.vercel.app/agents
link_label: Live agents page
---

## Overview

AgentFinder is the public registry front door for `a2aproject`.

It currently centers the public registry, discovery, trust and compliance signals, automatic submission publishing, a monetized public API, and a lightweight enterprise inquiry path for private registry hosting.

## Current status

- The web app, API, worker, shared domain package, and SDK are all part of the platform shape.
- The public registry/catalog is live at the agents page.
- Public agent submissions auto-validate and auto-publish when they pass.
- Seeded demo data supports registry browsing and walkthroughs.
- The public API is monetized with x402 settlement.
- Enterprise and private registry hosting flow through a separate inquiry path.

## Platform shape

- `apps/api`: Fastify REST API for auth, public registry submission, discovery, trust, public monetized API, and enterprise inquiry
- `apps/web`: React/Vite registry UI with the public catalog, directory browse, agent detail views, discovery, and enterprise hosting inquiry
- `apps/worker`: polling worker with composable ingestion, freshness, and indexing job seams
- `packages/domain`: shared A2A schemas, canonical agent model, registry primitives, discovery models, trust helpers, and ingestion boundaries
- `packages/sdk`: typed client for registry, discovery, auth, and enterprise workflows

## Notes

- This page should stay aligned with the latest registry status as the project changes.
