---
layout: page
title: AgentFinder
eyebrow: Featured project
subtitle: Blockchain-backed discovery layer for ERC-8004 and A2A agents.
date: 2026-05-19 00:00:00 +0100
summary: Registry-first platform for discovering, evaluating, and publishing AI agents with provenance-aware ingestion and trust signals.
link: https://agentfinder-web.vercel.app/agents
link_label: Live agents page
---

## Overview

**WebApp:** [agentfinder-web.vercel.app/agents](https://agentfinder-web.vercel.app/agents).

AgentFinder is a registry-first platform I built to make AI agents easier to discover, evaluate, and publish. The product includes a React/Vite frontend, a Fastify API, background worker jobs, a typed SDK, and a monetized public API. 

The project grew out of the need for a clearer, more trustworthy way to browse live agents instead of treating them like isolated demos. It centers on a canonical agent record with provenance-aware ingestion, trust and compliance signals, and a public directory experience that helps people compare agents with more confidence.


## Current status

- The web app is live at the agents page and lists agents after validation.
- On-chain ingestion pulls the latest registration and reputation signals.
- ERC-8004 and A2A consistency checks run before agents are surfaced.
- Wallet-based publishing works through browser wallets such as MetaMask.
- Seeded demo data supports registry browsing and walkthroughs.

## Platform shape

- `apps/api`: Fastify REST API for auth, public registry submission, discovery, trust, public monetized API, and enterprise inquiry
- `apps/web`: React/Vite registry UI with the public catalog, directory browse, agent detail views, discovery, and enterprise hosting inquiry
- `apps/worker`: polling worker with composable ingestion, freshness, and indexing job seams
- `packages/domain`: shared A2A schemas, canonical agent model, registry primitives, discovery models, trust helpers, and ingestion boundaries
- `packages/sdk`: typed client for registry, discovery, auth, and enterprise workflows
