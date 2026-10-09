---
name: pitch-deck
description: Build a pitch deck for a crypto project. Use when the user says "pitch deck", "demo day", "investor presentation", "grant application slides", "accelerator application", "help me pitch", or needs slides for a hackathon final.
user-invocable: true
---

<!-- Adapted from sendaifun/solana-new (create-pitch-deck), MIT © 2026 SendAI and Superteam; full notice in THIRD_PARTY_NOTICES.md. Telemetry removed. -->

# Pitch Deck

Interview → detect audience → pick narrative → build slides with speaking notes → self-score → objection prep.

Detail lives in `references/`. The one optional upstream pack (visual direction for the rendered deck) is in [upstream-packs.md](references/upstream-packs.md).

## Context handoff

At start, read `.claude/context/idea.md` and `.claude/context/build.md` ([format](../build-status/references/build-md-format.md), written by [build-status](../build-status/SKILL.md)) if present — pre-fill problem, wedge, traction, and stack from them, and Q5 from build.md's What works today section; take traction only from its Traction table, with the source each row cites. Read `.claude/context/positioning.md` ([format](../positioning/references/positioning-md-format.md), written by [positioning](../positioning/SKILL.md)) if present too — use its Plain one-liner for Q1 and its Primary one-liner on the title slide, and its ICP, alternatives and proof points as written for Q2 and Q8, and its words-to-avoid list when drafting. Read `.claude/context/pricing.md` ([format](../pricing/references/pricing-format.md), written by [pricing](../pricing/SKILL.md)) if present too — take Q9 and the business-model slide from its Model and The number sections as written. Read `.claude/context/market.md` ([format](../market-sizing/references/market-md-format.md), written by [market-sizing](../market-sizing/SKILL.md)) if present too: take the market slide from its Market slide section as written. Only ask what's missing.

## Workflow

### 1. 12-question interview

Blunt, one at a time, skipping anything already answered by context files:

1. What does it do, in one sentence a non-crypto person understands?
2. Who exactly has the problem, and how painful is it (evidence)?
3. Why does this need a blockchain?
4. Why Solana specifically?
5. What works *today* (demo-able) vs. roadmap?
6. Traction numbers — users, volume, TVL, signups, waitlist?
7. Who is the team and what's the unfair edge?
8. Competitors and your moat?
9. Business model — who pays, when?
10. Who is the audience for this deck (judges, VCs, grant committee, accelerator)?
11. The ask — prize, check size, grant amount, admission?
12. Biggest weakness you're afraid they'll ask about?

### 2. Audience detection → slide set

Q10 decides the slide set — full breakdown and per-audience rubrics in [investor-audience-guide.md](references/investor-audience-guide.md):

| Audience | Emphasis | Length |
|----------|----------|--------|
| Hackathon judges | a startup pitch with a working product: team, insight, demo, traction | 5–7 slides |
| VC | market size, traction slope, team, moat, ask | 10–12 |
| Grant committee | ecosystem benefit, public-good angle, milestones, budget | 8–10 |
| Accelerator | team velocity, learning rate, wedge → expansion path | 8–10 |

Slide-by-slide order per audience, plus the optional Tokenomics and Regulatory readiness slides: [pitch-structure.md](references/pitch-structure.md).

### 3. Narrative framework

Pick one backbone and state why — PAS (obvious pain, hackathons), 6-Part Investor Arc (VC), BAB (before/after/bridge), Hero's Journey (founder-story-driven), Pixar (narrative momentum). Definitions, slide mappings and a chooser: [storytelling-frameworks.md](references/storytelling-frameworks.md).

### 4. Build slides + speaking notes

For each slide: headline (a claim, not a label), 3–5 supporting points, visual suggestion, and 30–60s speaking notes. Draw on [slide-templates.md](references/slide-templates.md) (per-slide content and markup) and [onchain-metrics.md](references/onchain-metrics.md) (traction numbers a skeptic can check). Every number on a slide needs a source; never invent one.

### 5. Self-score vs audience rubric

Score the draft against the audience's actual criteria (clarity, credibility, demo strength, ask specificity) and against [crypto-pitch-mistakes.md](references/crypto-pitch-mistakes.md) — flag every mistake the deck still commits, fix, re-score. Any token-return, yield or fee-share claim comes off the slide and goes to [crypto-legal-skill](https://github.com/solanabr/crypto-legal-skill) (Mistake 4). Don't present a deck you'd score below 8/10.

### 6. Objection-prep Q&A

From Q12 + the weakest scored dimension, draft the 8–10 hardest questions this audience will ask, each with a tight 30-second answer. Hostile-question drilling beats slide polish.

## Output

- Deck outline (markdown, one section per slide: headline / points / visual / speaking notes)
- Framework choice + one-line rationale
- Self-score with the fixes applied
- Objection Q&A sheet

Need a rendered deck? Build it as HTML — one self-contained file, one section per slide, with the no-JavaScript shell in [deck-design-system.md](references/deck-design-system.md). It renders anywhere, diffs in git, and Claude Code can design it directly, which a binary office file gives up. Anthropic's [frontend-design](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/frontend-design) skill carries the visual direction if you have it on disk ([upstream-packs.md](references/upstream-packs.md)), and the same route covers any graphic or marketing asset the deck needs.
