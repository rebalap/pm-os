---
name: tavily-search
description: >
  Searches the web using Tavily — a research-grade search API that returns
  AI-synthesised answers plus ranked source results. Use instead of WebSearch
  for any research task in the PM-OS context.

  Trigger on: "search for", "look up", "find research on", "what does the web say
  about", "search Tavily", "do a Tavily search", "research X online", "find sources
  on", "competitive research", "secondary research on", or any request to find
  external information to support PM work (market research, clinical evidence,
  regulatory context, competitor analysis, pricing benchmarks).

  Prefer this over built-in WebSearch — Tavily returns higher-quality sources with
  relevance scores and an AI-synthesised answer, making it better suited for
  evidence-based PM research.
---

# Tavily Search Skill

Use Tavily to search the web for any research needed in the PM-OS workflow. Tavily
returns an AI-synthesised answer summary AND ranked source results with relevance
scores — better signal-to-noise than raw web search for evidence-based work.

---

## How to Run a Search

The CLI tool lives at:
`/Users/prahladrebala/Documents/pm-os/tools/tavily-search.py`

The API key is stored in:
`/Users/prahladrebala/Documents/pm-os/.env`

Run searches using Bash:

```bash
cd /Users/prahladrebala/Documents/pm-os
python3 tools/tavily-search.py "your query here"
```

---

## Command Reference

### Basic search (fast, 5 results)
```bash
python3 tools/tavily-search.py "autism therapy India ABA market"
```

### Advanced search (thorough, better for research)
```bash
python3 tools/tavily-search.py "DPDPA 2023 health data consent minors" --depth advanced
```

### More results
```bash
python3 tools/tavily-search.py "ABA data collection software India" --max-results 10
```

### Restrict to specific domains (great for clinical/regulatory research)
```bash
python3 tools/tavily-search.py "autism prevalence India 2024" \
  --include-domains "pubmed.ncbi.nlm.nih.gov,pmc.ncbi.nlm.nih.gov,who.int"
```

### News / recent events
```bash
python3 tools/tavily-search.py "autism therapy India funding 2025" --topic news
```

### Get raw JSON (useful for piping into other tools)
```bash
python3 tools/tavily-search.py "RCI licensing special educators India" --raw
```

### Exclude noisy domains
```bash
python3 tools/tavily-search.py "ABA therapy software pricing" \
  --exclude-domains "reddit.com,quora.com"
```

---

## Search Strategy by Research Type

### Clinical / academic evidence
```bash
--depth advanced --include-domains "pubmed.ncbi.nlm.nih.gov,pmc.ncbi.nlm.nih.gov,researchgate.net,jamanetwork.com"
```

### Regulatory / policy (India)
```bash
--depth advanced --include-domains "indiacode.nic.in,dpdpa.com,rci.gov.in,disabilityrightsindia.com"
```

### Competitive analysis (software products)
```bash
--depth advanced --exclude-domains "reddit.com,quora.com,pinterest.com"
```

### Market sizing / pricing benchmarks
```bash
--depth advanced --topic general --max-results 10
```

### Recent news / funding / trends
```bash
--topic news --max-results 8
```

---

## Workflow — Research Session

When asked to do research on a topic for the Autism Therapy Platform:

1. **Break the topic into 2–4 focused queries.** Broad queries return noisy results.
   Good: `"DPDPA 2023 parental consent minors health data"`
   Bad: `"India data privacy law"`

2. **Run each query and capture the AI answer + top sources.**

3. **Synthesise across queries** — do not paste raw results. Extract the key finding
   from each search and combine into a structured response.

4. **Tag evidence level:**
   - ✅ Observed — peer-reviewed study, government source, official regulatory document
   - 🔵 Inferred — credible secondary source (news, industry report)
   - 🔶 [HYPOTHESIS] — blog, vendor marketing, or unverified claim

5. **Save findings to the appropriate research file** in:
   `/Users/prahladrebala/Documents/pm-os/products/autism-therapy-platform/research/secondary/`

---

## Output Format for Research Results

When presenting Tavily search results to the user, use this structure:

```
## Tavily Search Results: [Topic]
**Queries run:** [List the queries used]
**Date:** [Today's date]

### Key Finding
[AI answer synthesis across queries — 2–4 sentences]

### Sources
| Title | URL | Relevance | Evidence level |
|---|---|---|---|
| [Title] | [URL] | [score] | ✅/🔵/🔶 |

### Implications for [Product / Research area]
[What this means for the PM decision at hand]

### Gaps — What Tavily cannot answer
[What requires primary fieldwork or a deeper source]
```

---

## Limitations

- Tavily searches the public web — it cannot access paywalled journals, private databases, or internal documents.
- For PMC/PubMed full text, use `--include-domains "pmc.ncbi.nlm.nih.gov"` to maximise open-access results.
- Basic depth (~1s) is good for quick lookups. Advanced depth (~3–5s) is better for research synthesis.
- The `--topic news` mode prioritises recency over depth — use for trend monitoring, not clinical evidence.
- API key is stored in `/Users/prahladrebala/Documents/pm-os/.env`. Never commit this file.
