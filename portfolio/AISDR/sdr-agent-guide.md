# AI SDR Agent Swarm with Claude Code
## Architecture Overview

```
Port Data API → [Agent 1: Extractor] → imports.csv
                                            ↓
                               [Agent 2: Enricher] ← Claude API
                                            ↓
                             [Agent 3: Contact Finder] ← Seamless/Apollo
                                            ↓
                               [Agent 4: Data Cleaner]
                                            ↓
                               [Agent 5: Uploader] → Apollo Sequences
                                            ↓
                          [Agent 6: Reply Listener] → CRM/Sheets
```

---

## Phase 1: Project Scaffold & CLAUDE.md

### Folder Structure
```
/sdr-agent
  CLAUDE.md                  ← Master instructions for Claude Code
  .env                       ← All API keys
  /src
    /agents
      extractor.js           ← Agent 1
      enricher.js            ← Agent 2
      contact-finder.js      ← Agent 3
      cleaner.js             ← Agent 4
      uploader.js            ← Agent 5
      reply-listener.js      ← Agent 6
    /skills
      portApi.js             ← Port data skill
      claudeEnrich.js        ← LLM enrichment skill
      seamlessApi.js         ← Contact discovery skill
      apolloApi.js           ← Apollo fallback skill
      csvHandler.js          ← CSV read/write skill
      webhookServer.js       ← Webhook skill
    /data
      imports.csv
      enriched.csv
      contacts.csv
      cleaned.csv
  orchestrator.js            ← Runs all agents in sequence
  package.json
```

---

## Phase 2: CLAUDE.md — The Brain of Your Swarm

This file tells Claude Code exactly how to behave across every agent. Place it in the project root.

```markdown
# CLAUDE.md — SDR Agent Swarm

## Project Purpose
This is a high-volume outbound AI SDR pipeline. It moves raw shipping
port data through enrichment, contact discovery, cleaning, and upload
into Apollo.io email sequences.

## Agent Responsibilities
- **extractor**: Fetches Long Beach → China shipping data, deduplicates
  company names, writes to /data/imports.csv
- **enricher**: Takes each company name, uses Claude API to find the
  primary domain. Writes to /data/enriched.csv
- **contact-finder**: Uses Seamless.ai as primary. Falls back to Apollo
  /organizations/search if Seamless returns no results
- **cleaner**: Normalizes all data to Apollo's CSV import schema
- **uploader**: Pushes cleaned.csv to Apollo via their API or CSV import
- **reply-listener**: Express webhook server that receives Apollo reply
  webhooks, classifies intent, updates CRM

## Coding Rules
- All API keys come from process.env — never hardcode
- Every agent must log its progress to console with timestamps
- All agents write to /data — never read from a previous agent's raw output
  without the csvHandler skill
- Handle rate limits with exponential backoff (max 3 retries)
- Deduplication happens at the extractor stage — do not re-deduplicate

## Skills Available
Import skills from /src/skills — do not rewrite API logic inside agents.
Each agent should be thin: call a skill, transform data, write output.

## Error Handling
If an agent fails on a single record, log the error and continue.
Write failed records to /data/errors.csv with the reason.

## Running the Pipeline
node orchestrator.js          ← Full pipeline
node src/agents/extractor.js  ← Single agent for testing
```

---

## Phase 3: The Skills Layer

Skills are reusable functions that agents call. Build these first.

### skill: csvHandler.js
```javascript
const fs = require('fs');
const { parse } = require('csv-parse/sync');
const { stringify } = require('csv-stringify/sync');

const read = (path) => parse(fs.readFileSync(path), { columns: true, skip_empty_lines: true });
const write = (path, data) => fs.writeFileSync(path, stringify(data, { header: true }));

module.exports = { read, write };
```

### skill: claudeEnrich.js
```javascript
const Anthropic = require('@anthropic-ai/sdk');
const client = new Anthropic();

async function findDomain(companyName) {
  const msg = await client.messages.create({
    model: 'claude-opus-4-5',
    max_tokens: 256,
    messages: [{
      role: 'user',
      content: `Find the official primary domain for this company: "${companyName}".
Return ONLY the domain (e.g., acmecorp.com). If uncertain, return "unknown".
Do not include http:// or www.`
    }]
  });
  return msg.content[0].text.trim().toLowerCase();
}

module.exports = { findDomain };
```

### skill: seamlessApi.js
```javascript
const axios = require('axios');

async function getContacts(domain) {
  const res = await axios.get('https://api.seamless.ai/v1/contacts', {
    headers: { Authorization: `Bearer ${process.env.SEAMLESS_API_KEY}` },
    params: { domain, titles: 'VP,Director,Manager,Owner', limit: 5 }
  });
  return res.data.contacts || [];
}

module.exports = { getContacts };
```

### skill: apolloApi.js (fallback domain finder + uploader)
```javascript
const axios = require('axios');

async function findDomainByName(companyName) {
  const res = await axios.post('https://api.apollo.io/v1/organizations/search', {
    api_key: process.env.APOLLO_API_KEY,
    q_organization_name: companyName,
    page: 1, per_page: 1
  });
  return res.data.organizations?.[0]?.primary_domain || null;
}

module.exports = { findDomainByName };
```

---

## Phase 4: The Agents

### Agent 1 — extractor.js
**Claude Code prompt:**
> "Write extractor.js. Use the portApi skill to fetch Long Beach to China shipping records for December 2025. Extract unique company names only. Write to /data/imports.csv with columns: company_name. Log how many records were found and how many duplicates were dropped."

### Agent 2 — enricher.js
**Claude Code prompt:**
> "Write enricher.js. Read /data/imports.csv. For each company_name, call the claudeEnrich skill to get its domain. If domain is 'unknown', also try apolloApi.findDomainByName as a fallback. Write results to /data/enriched.csv with columns: company_name, domain. Rate limit to 10 requests per second."

### Agent 3 — contact-finder.js
**Claude Code prompt:**
> "Write contact-finder.js. Read /data/enriched.csv. Skip rows where domain is 'unknown'. For each domain, call seamlessApi.getContacts. If it returns empty, call apolloApi as fallback. Write all contacts to /data/contacts.csv with columns: first_name, last_name, email, company, domain, title, linkedin_url."

### Agent 4 — cleaner.js
**Claude Code prompt:**
> "Write cleaner.js. Read /data/contacts.csv. Normalize: lowercase all emails, remove emojis and special characters from company names, remove any rows missing first_name or email. Map to Apollo's import schema exactly. Write to /data/cleaned.csv."

### Agent 5 — uploader.js
**Claude Code prompt:**
> "Write uploader.js. Read /data/cleaned.csv. Use Apollo's People API to add contacts to sequence ID stored in process.env.APOLLO_SEQUENCE_ID. Batch in groups of 25. Log success/failure per batch."

### Agent 6 — reply-listener.js
**Claude Code prompt:**
> "Write reply-listener.js as an Express server on port 3000. Accept POST /webhook from Apollo. When a reply comes in, send the reply body to Claude API with this prompt: 'Classify this sales reply as: INTERESTED, NOT_NOW, WRONG_PERSON, or UNSUBSCRIBE. Return only the label.' Based on the label, update a Google Sheet or CRM via the appropriate skill."

---

## Phase 5: The Orchestrator

```javascript
// orchestrator.js
const { execSync } = require('child_process');

const agents = [
  'src/agents/extractor.js',
  'src/agents/enricher.js',
  'src/agents/contact-finder.js',
  'src/agents/cleaner.js',
  'src/agents/uploader.js'
];

(async () => {
  for (const agent of agents) {
    console.log(`\n▶ Running ${agent}...`);
    try {
      execSync(`node ${agent}`, { stdio: 'inherit' });
      console.log(`✓ ${agent} complete`);
    } catch (e) {
      console.error(`✗ ${agent} failed — stopping pipeline`);
      process.exit(1);
    }
  }
  console.log('\n✅ Pipeline complete. Launch reply-listener separately: node src/agents/reply-listener.js');
})();
```

---

## Phase 6: Environment Variables (.env)

```
PORT_API_KEY=
PORT_API_URL=https://api.importyeti.com/v1   # or Panjiva

ANTHROPIC_API_KEY=

SEAMLESS_API_KEY=
APOLLO_API_KEY=
APOLLO_SEQUENCE_ID=

WEBHOOK_SECRET=
CRM_WEBHOOK_URL=   # or Google Sheets endpoint
```

---

## Swarm Launch Sequence

```bash
# 1. Install dependencies
npm install axios dotenv @anthropic-ai/sdk csv-parse csv-stringify express

# 2. Run the full pipeline
node orchestrator.js

# 3. In a separate terminal, start the reply listener
node src/agents/reply-listener.js

# 4. Test a single agent
node src/agents/extractor.js
```

---

## Key Design Decisions

| Decision | Why |
|---|---|
| Skills separate from agents | Agents stay thin; skills are reusable and testable |
| CLAUDE.md at root | Claude Code reads this automatically — it governs all agent behavior |
| Errors go to errors.csv | Pipeline never halts on a single bad record |
| Claude API for enrichment | Replaces the "Custom GPT" — more reliable domain inference than regex |
| Apollo as primary uploader AND fallback enricher | Maximizes data coverage without extra vendors |
