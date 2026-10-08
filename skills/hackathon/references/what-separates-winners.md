<!-- Written from an unpublished study of Colosseum pitch videos by this file's contributor (Sep–Oct 2026). Aggregates only: no transcript is reproduced. Quotes are under 25 words, taken from automatic transcripts of the public pitch videos, each linked to the project's Colosseum page (all opened 2026-10-08). -->

# What separated winners in Colosseum pitch videos

Read this before scripting the presentation video ([demo-video-script.md](demo-video-script.md)). It shows which things winners said more often than matched projects that won nothing. That is association, not cause, and it covers the pitch video only.

## The study, in five lines

1. **Winners:** 43 of the 61 companies Colosseum took into its accelerator (cohorts 1–5, from Renaissance 2024 to Frontier 2026) whose hackathon pitch video could still be played.
2. **Controls:** one project per accelerated company, drawn from the same hackathon and category, with no prize, honourable mention or accelerator place; 47 had a playable pitch video.
3. **Coding:** a closed codebook written before any transcript was read, applied blind to group; a second coder re-coded 21 projects, and variables with agreement below 0.6 were dropped. Numbers per minute, word rate and readability were computed by script.
4. **Tests:** two-sided Fisher exact per variable, 22 tests. "Robust" means it survives a Holm correction across all 22.
5. **Scope:** only the presentation (pitch) video was coded. The product demo video was not.

## What separated, robustly

| Said in the pitch video | Winners | Controls | p | Holm-adjusted p | Agreement |
|---|---|---|---|---|---|
| Any traction | 34/43 | 12/47 | < 0.001 | < 0.001 | 0.95 |
| Traction with a number, said out loud | 23/43 | 9/47 | 0.0009 | 0.019 | not measured |
| A team credential | 37/43 | 25/47 | 0.0012 | 0.024 | 1.0 |

- It holds in both periods. Traction: 8/11 vs 3/17 in 2024, 26/32 vs 9/30 in 2025–26. Credential: 9/11 vs 9/17, then 28/32 vs 16/30.
- 35 of the 47 controls cited no traction of any kind. The winners' traction, by type (projects per type): users 19, partnerships 15, volume 9, revenue 7, grants or prizes 7, LOIs or pilots 5, waitlist 1.
- What it sounds like:
  - [CrowdBrain](https://colosseum.com/projects/explore/crowdbrain), Frontier Grand Champion: "We already have a live alpha node in Georgia, two deployment partners and an active government partnership."
  - [CargoBill](https://colosseum.com/projects/explore/cargobill): "our initial customers who have done $70,000 in payment volume"
  - [stablecorp](https://colosseum.com/projects/explore/stablecorp): "We have 13 paying users. We launched 1.5 months ago and we're doing 8k in MRR."
  - Credential tied to the problem: "In my 15 years of experience working in logistics" ([CargoBill](https://colosseum.com/projects/explore/cargobill)); "Previously, we founded and exited our computer vision company and scaled our gamified DeFi up to $4 billion and 100,000 monthly active users." ([CrowdBrain](https://colosseum.com/projects/explore/crowdbrain))

## Weak signals (do not survive correction)

- **Face on camera:** 35/41 vs 24/43, p 0.004, Holm-adjusted 0.077. A hand count suggests it only appears from 2025 on (29/31 vs 12/26; 2024: 6/10 vs 12/17), which no script regenerates.
- **Revenue as the traction:** 7/43 vs 1/47, p 0.026.
- **Numbers per minute:** median 5.1 vs 3.6, p 0.018 (Mann-Whitney, one of 14 language metrics, uncorrected). See [pitch-rhetoric.md](pitch-rhetoric.md).
- Not differences: total words 490 vs 413 (p 0.075); words per minute 170 vs 153 and crypto jargon 1.6 vs 2.0 per minute were not tested.

## What did not separate

| Said or shown in the pitch video | Winners | Controls | p |
|---|---|---|---|
| Product running on screen | 20/37 | 23/36 | 0.48 |
| Onchain proof on screen (explorer, transaction) | 4/33 | 10/35 | 0.13, fewer winners |
| Explicit "why Solana" | 21/43 | 16/47 | 0.20 |
| Market size with a number | 18/43 | 17/47 | 0.67 |
| Token mentioned | 8/42 | 9/46 | 1.0 |
| Problem stated with a number | 19/43 | 16/47 | 0.39 |
| A specific, named user | 21/42 | 19/45 | 0.52 |
| Revenue model stated | 25/43 | 22/47 | 0.30 |
| Competition mentioned | 31/43 | 26/47 | 0.13 |
| An ask or next steps | 31/43 | 30/47 | 0.50 |
| Opens with the problem or a story | 4/43 | 3/47 | 0.71 |

- Denominators below 43 and 47 leave out videos where the item couldn't be judged (no screen shown, for example).
- Same median length (177 s vs 176 s) and the same time to the problem (15.5 s vs 15 s). Style didn't separate either: sentence length 17 vs 14 words (p 0.40), Flesch 59 vs 65 (p 0.41), analogies a median of 0 in both groups.
- Dropped for low agreement, so unknown: the type of opening (0.57) and stated full-time commitment (0.5).

**What it means for the two videos.** The pitch video reads as evidence of a company: who uses it, who pays, why this team. That matches Colosseum's own framing that its hackathons "are startup competitions" ([FAQ](https://colosseum.com/hackathon)). Spend pitch-video seconds on traction and team. The product walkthrough and the explorer transaction belong in the demo video, which this study did not code, so the demo script in [demo-video-script.md](demo-video-script.md) is untouched by it.

## No traction yet: the other way in

9 of the 43 winners cited no traction (TapeDrive, Reflect, Urani, Archer, Rekt, Kormos, Banger, TypeX, WeLikeSports), mostly infrastructure or a new technical primitive. In its place they gave one of two things:

- **A technical artifact a judge can check:** "We've deployed the program to DevNet. There's a reference miner and an archive node" ([TapeDrive](https://colosseum.com/projects/explore/tapedrive), Breakout Grand Champion).
- **A team whose record carries the claim:** "core contributor to ethereum and led the development of solidity" ([WeLikeSports](https://colosseum.com/projects/explore/welikesports)).

Without traction, artifact or record, nothing in this data suggests what else wins.

## Category hype

From [colosseum-copilot](https://github.com/ColosseumOrg/colosseum-copilot/blob/0453ffe26e8d245152619fcc949689a6adaab1c6/skills/colosseum-copilot/SKILL.md)'s primary-category labels across 8,286 submissions and 180 winners in five hackathons (Renaissance to Frontier), pulled late September 2026. Counts only, no test.

- What builders crowd into is not what wins: agent-control-plane was 144 of Frontier's submissions (5%) and 0 of its 28 winners; token-launch was 244 submissions (2.9%) and 3 winners (1.7%); verifiable records (proofs, attestations, registries) were 175 submissions and 0 winners.
- Judges' taste moves by edition: DePIN took 17 of 119 wins across Renaissance, Radar and Breakout from about 3% of submissions, then 0 of 61 in Cypherpunk and Frontier; games were 10.6% of Renaissance and 4 of 34 winners, then 5.6% of Cypherpunk and 0 of 33.

Check the current edition's category in Copilot before treating a hot category as a tailwind.

## Demo Day: what changes after the hackathon

65 Demo Day pitches from accelerator cohorts 1–5 (cohort 5's teams are listed in [Cohort V Demo Day](https://blog.colosseum.com/cohort-v-demo-day-solana-microscope-alpenglow-migration/)), coded with the same codebook.

- **The same 43 companies, hackathon pitch vs Demo Day pitch** (paired, McNemar): median length 177 s → 133 s, and 33 of 43 got shorter; closing with an ask 31 → 39 (p 0.06), and 58 of all 65 Demo Day pitches close with one; opening with "Hi, I'm…" 9 → 2 (p 0.04); a named, specific user 21 → 13 (p 0.04). Traction with a number 23 → 30 and "why Solana" 21 → 15, neither significant. Word rate (170 → 167 a minute) and numbers per minute (5.1 → 5.2) didn't change.
- **Who raised afterwards vs the rest** (cohorts 1–4, 6 vs 38): mentioning a token, 5/6 vs 7/38 (p 0.004), the only strong signal, and it doesn't survive correction across ~30 tests. Traction with a number did not separate (3/6 vs 23/38). Cohort mattered more than pitch: 4 of 11 raised from cohort 1, 2 of 12 from cohort 2, none from cohorts 3 and 4, which had had less time.
- Outcome rules: a round led only by Colosseum doesn't count; a token sale counts as a token. 50 of 65 outcomes are unknown, meaning "not found in public sources", not "didn't raise".

## Limits

- **Association, not cause.** Traction and credentials may simply mark stronger companies. They are also what Colosseum's FAQ says judges look for, so the reading is consistent, not proven.
- **Pitch video only.** Nothing here speaks to the demo video, the written description or the interview round.
- **Top vs bottom.** Accelerated winners against projects that won nothing. It says nothing about the middle: track winners and honourable mentions who weren't accelerated are in neither group.
- **22 tests.** Three survive Holm. The weak signals can be noise.
- **Survivorship in both groups.** 18 of the 61 accelerated companies had no playable video, and about a third of the drawn controls were lost the same way. The remaining controls likely skew stronger, which would make the gaps conservative.
- **Partial blinding.** Coders didn't know the group, but company names stay in the transcripts. Agreement is simple percent agreement, which flatters lopsided variables; kappa was not computed.
- **Colosseum only.** Sponsor tracks and other organisers judge to their own criteria ([judging-criteria.md](judging-criteria.md#other-organisers)).
