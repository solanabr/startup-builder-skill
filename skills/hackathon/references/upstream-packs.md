# Upstream packs this skill draws on

The skill works standalone: every reference link in `SKILL.md` points at the upstream
repository over https, pinned to the commit the paths were verified against, so nothing
needs to be installed to follow them.

Install a pack locally when you want to grep across it or work offline.

## solana-new (sendaifun/solana-new)

Carries the submission guide, judging criteria, demo-video script, the Colosseum
winner history under `skills/data/colosseum/`, and the grant-shaped ideas dataset.

- Upstream: https://github.com/sendaifun/solana-new
- Pinned commit for the links in `SKILL.md`: `e81c261645035c0e902eaaa518ff58722d188bb7`
- Standalone: `git clone https://github.com/sendaifun/solana-new`
- With [solanabr/ai-kit](https://github.com/solanabr/ai-kit) installed: `bash .claude/bin/skills.sh add solana-new`
  (it lands at `.claude/skills/ext/solana-new/`)

## colosseum-copilot (ColosseumOrg/colosseum-copilot)

Queries 5,400+ past Colosseum submissions — used here for the live crowdedness check on
candidate tracks. Backed by a CLI, so it needs a one-time sign-in per machine regardless
of install route:

```
npx @colosseum-org/copilot-connect login
```

Node 20+ required.

- Upstream: https://github.com/ColosseumOrg/colosseum-copilot
- Pinned commit for the link in `SKILL.md`: `0453ffe26e8d245152619fcc949689a6adaab1c6`
- With [solanabr/ai-kit](https://github.com/solanabr/ai-kit) installed: `bash .claude/bin/skills.sh add colosseum` (installed by default there)
