---
layout: page
title: AgentFinder
eyebrow: Featured project
subtitle: Blockchain-backed discovery layer for ERC-8004 and A2A agents.
date: 2026-05-19 00:00:00 +0100
summary: Blockchain-backed agent discovery layer that ingests the latest registration and reputation data, runs ERC-8004 and A2A consistency checks, and publishes verified agents.
link: https://agentfinder-web.vercel.app/agents
link_label: Live agents page
---

## Overview

AgentFinder is the public registry front door for `a2aproject`.

It ingests the latest agent registration and reputation data from the blockchain, runs consistency checks for ERC-8004 and A2A, and exposes a discovery layer for browsing verified agents. Agents can be published through wallet-based flows such as MetaMask.

## Current status

- The web app is live at the agents page and acts as the discovery layer.
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

## Notes

- This page should stay aligned with the latest registry status as the project changes.
