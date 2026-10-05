# startup-builder-skill

Agent skills for the non-program half of shipping a product on Solana — the things a small
team hits *around* the code.

## Charter

The all-in-one support skill pack for startups building on Solana. Program work — Anchor
patterns, CU optimisation, account layout — is covered well by
[solanabr/ai-kit](https://github.com/solanabr/ai-kit) and the packs it pins. This repo owns
the startup-operations layer: positioning and pricing, launch, fundraising, go-to-market and
growth, support and operations, and compliance-adjacent operations (pointing at
[solanabr/crypto-legal-skill](https://github.com/solanabr/crypto-legal-skill) for the legal
lane rather than restating it).

Full charter, the gap analysis behind it, and the design constraints: [issue #1](https://github.com/solanabr/startup-builder-skill/issues/1).

Two constraints from that charter shape everything here:

- **Skills stay off the always-on path.** A top-level skill's `description` is listed in
  every session *and every subagent*, so fan-outs of 100+ subagents multiply that cost. These
  load on demand, with detail behind links in `references/`.
- **One `SKILL.md` per skill directory**, routing-only descriptions, progressive disclosure.

## The skills

| Skill | Use it when |
|-------|-------------|
| [idea-sprint](skills/idea-sprint/SKILL.md) | Deciding *what* to build, or stress-testing an idea before any code. Interview → crypto-necessity gate → three candidates → score /15 → go/no-go. Output is a decision, not a brainstorm. |
| [pitch-deck](skills/pitch-deck/SKILL.md) | You need slides — demo day, a VC meeting, a grant application, an accelerator form, a hackathon final. Detects the audience, picks a narrative backbone, writes speaking notes, then drills the hostile questions. |
| [hackathon](skills/hackathon/SKILL.md) | A submission is due. Track choice by crowdedness, a description a judge can skim in 90 seconds, a sub-3-minute demo script, and the grant follow-on when the track doesn't land. |
| [build-status](skills/build-status/SKILL.md) | Before a deck, submission, grant or investor update. Records program IDs, upgrade authority, verified-build and audit state, what works today, and traction with the query behind each number into `.claude/context/build.md`. |
| [positioning](skills/positioning/SKILL.md) | Before the deck, site, docs intro or launch post. Writes the one-liner, ICP with disqualifiers, job to be done, three named alternatives with the dimension you beat each on, sourced proof points and words to avoid into `.claude/context/positioning.md`. |

They chain. `idea-sprint` writes `.claude/context/idea.md`, `build-status` writes
`.claude/context/build.md` and `positioning` writes `.claude/context/positioning.md`;
`pitch-deck` and `hackathon` read all three and pre-fill the problem, wedge, audience, what works
and traction instead of re-interviewing you. Run them in that order and the
later ones get shorter. `build.md`'s format is a contract other tools can write to as well:
[build-md-format.md](skills/build-status/references/build-md-format.md).

Rendered decks and any graphic or marketing asset come out as **HTML** — one file, your own
CSS. It renders anywhere, diffs in git, and the agent can design it directly.

## Install

Each skill is self-contained under `skills/<name>/`. Copy the ones you want into your
project's skills directory:

```
git clone https://github.com/solanabr/startup-builder-skill
cp -r startup-builder-skill/skills/idea-sprint .claude/skills/
```

Use `.agents/skills/` instead of `.claude/skills/` for Codex, Cursor, Copilot and other
Agent Skills clients.

The layout is `skills/<name>/SKILL.md` at the repository root, which is what an
upstream-folder fetch expects — so a kit can pin individual skills from here by name without
vendoring the whole repo as a submodule.

## Upstream dependencies

The interview, scoring and validation rubrics, the pitch structure, frameworks, templates and
deck shell, and the hackathon submission guide and video scripts are vendored under each
skill's `references/`, rewritten from [sendaifun/solana-new](https://github.com/sendaifun/solana-new)
with attribution. The hackathon judging criteria and winners index are written from
Colosseum's own FAQ and announcement posts, linked inline.

What remains upstream is small and optional: the Superteam ideas dataset (one pinned JSON
file, 240 entries), [ColosseumOrg/colosseum-copilot](https://github.com/ColosseumOrg/colosseum-copilot)
(5,400+ past submissions, for crowdedness checks) and Anthropic's
[frontend-design](https://github.com/anthropics/skills/tree/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/frontend-design). Links are
pinned or point at stable pages, so **nothing has to be installed** for the skills to work.
Each skill's `references/upstream-packs.md` gives the details.

Text adapted from solana-new keeps its MIT notice in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
