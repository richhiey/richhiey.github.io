---
layout: document
title: ERC-8004 Registration is Not Just "Log In"
eyebrow: Publication
subtitle: A full write-up on ERC-8004 login and registration flows.
date: 2026-05-19 00:00:00 +0100
summary: A detailed breakdown of ERC-8004 registration, wallet auth, and agent onboarding flows.
---

ERC-8004 registration is not just "log in and submit a form." The user is effectively proving wallet ownership, creating or updating an on-chain agent identity, and publishing a registration file that others will use for discovery and trust. ERC-8004 defines agent identity through an ERC-721-style Identity Registry, where each agent has an `agentId` and an `agentURI` pointing to its registration file. That file can include name, description, image, services, endpoints such as A2A or MCP, registrations, and supported trust models.

## Recommended login flow

### 1. Entry state: "Register an AI Agent"

Instead of starting with a generic Log In modal, frame the intent:

Title: Register an AI Agent

Subtitle: Connect a wallet to create, manage, or verify an ERC-8004 agent identity on Base.

Primary CTA:

Continue with Base wallet

Secondary CTA:

Connect another wallet

Small helper text:

"Your wallet will own the agent identity. You can transfer ownership or delegate management later."

This matters because ERC-8004 treats the ERC-721 token owner as the agent owner, and the owner can update the registration URI or delegate management through supported ERC-721 mechanisms.

### 2. Perfected auth sequence

#### Step 1 - Connect wallet

User clicks:

Sign in with Base

System checks:

- Wallet is installed or embedded wallet is available.
- Connected address exists.
- Network is Base/Mainnet or supported ERC-8004 network.
- User has not connected with a watch-only or unsupported wallet.
- Chain ID matches the selected registration target.

UX states:

- No wallet: "Install Coinbase Wallet, MetaMask, or use embedded Base sign-in."
- Wrong network: "Switch to Base to continue."
- Already connected: Skip to signing.
- Wallet rejected: "Connection cancelled. No changes were made."

#### Step 2 - Sign message, not transaction

After connection, ask for an off-chain signature:

Sign in to 8004scan

Use SIWE-style auth with EIP-712 or EIP-191. ERC-8004 already references EIP-712 and EIP-1271, and agent wallet changes specifically rely on wallet-control proofs for EOAs or smart contract wallets.

The signed payload should include:

- domain: 8004scan.io
- address: 0x...
- chainId: 8453
- nonce: random server nonce
- issuedAt: timestamp
- expirationTime: short window
- statement: Sign in to manage ERC-8004 agent registrations.

Do not ask for a blockchain transaction just to log in.

Success result:

- Create session.
- Bind session to wallet address.
- Store wallet type: EOA, smart contract wallet, embedded wallet.
- Detect whether address already owns ERC-8004 agents.

### Post-login routing

After successful sign-in, route users based on wallet state.

#### Case A - Wallet owns no agents

Show:

Create your first agent identity

Options:

- Register new agent
- Import existing agent
- Explore ERC-8004 first

Primary CTA:

Start registration

#### Case B - Wallet owns agents

Show dashboard:

Your agents

Each card:

- Agent name
- Agent ID
- Registry
- Chain
- Status: Active / Incomplete / Needs verification
- Endpoint verification status
- Reputation summary
- Last updated
- CTA: Manage

#### Case C - Wallet is delegated operator

Show:

Agents you can manage

Make it explicit that they are not the owner:

"You can update metadata for this agent, but ownership remains with 0x..."

### Agent registration flow

#### Step 1 - Agent basics

Fields:

- Agent name
- Description
- Image/logo
- Category/domain
- Public website
- Contact email
- Active status

Validation:

- Name length limit
- Description quality check
- Image size and format
- No duplicate name warning, but do not block unless your product requires uniqueness

The ERC-8004 registration file expects top-level fields like type, name, description, image, services, active, registrations, and optional supportedTrust.

#### Step 2 - Services and endpoints

Ask what the agent exposes:

- Web endpoint
- A2A agent card
- MCP endpoint
- OASF profile
- ENS
- DID
- Email
- API endpoint
- Custom service

For each endpoint:

- Validate URL format.
- Check HTTPS.
- Test reachability.
- Show response status.
- Detect `.well-known` files where relevant.
- Warn if endpoint is not verifiable.

ERC-8004 allows agents to advertise endpoints such as A2A, MCP, OASF, ENS, DID, email, and web services.

#### Step 3 - Domain verification

This should be optional but strongly encouraged.

For HTTPS endpoints, generate a verification file:

```json
{
  "registrations": [
    {
      "agentRegistry": "eip155:8453:0x...",
      "agentId": "pending-or-existing"
    }
  ]
}
```

Ask the user to publish it at:

`https://their-domain.com/.well-known/agent-registration.json`

Then your portal checks:

- File exists.
- HTTPS is valid.
- agentRegistry matches.
- agentId matches after minting.
- Domain matches endpoint domain.

ERC-8004 specifically describes optional endpoint-domain verification through `.well-known/agent-registration.json`.

#### Step 4 - Trust profile

Ask which trust modes the agent supports:

- Reputation
- Crypto-economic validation
- TEE attestation
- zkML proof
- Human/auditor validation
- Discovery only

Recommended UX copy:

"ERC-8004 makes trust signals public, but it does not guarantee that an agent is safe or capable. Choose the trust mechanisms your agent can actually support."

That warning is important: the standard makes identity, reputation, and validation signals discoverable, but advertised capabilities still need verification; the ERC notes that Sybil attacks and malicious capability claims remain implementation-level concerns.

#### Step 5 - Generate registration file

Before minting, generate the registration JSON and show a preview.

Example:

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "ResearchAgent",
  "description": "An AI research agent that summarizes technical papers and exposes an MCP endpoint.",
  "image": "ipfs://...",
  "services": [
    {
      "name": "web",
      "endpoint": "https://research-agent.example.com"
    },
    {
      "name": "MCP",
      "endpoint": "https://research-agent.example.com/mcp",
      "version": "2025-06-18"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [],
  "supportedTrust": ["reputation", "tee-attestation"]
}
```

Storage options:

- IPFS recommended
- HTTPS-hosted JSON
- Fully on-chain base64 data: URI for advanced users

ERC-8004 allows `agentURI` to resolve through IPFS, HTTPS, or base64-encoded data URIs.

#### Step 6 - Transaction preview

Before asking for a transaction, show:

- Network
- Registry contract
- Connected wallet
- Estimated gas
- Agent URI
- Whether metadata will be included
- Whether agentWallet defaults to owner wallet
- What will happen after mint
