# Upstream packs this skill draws on

The skill works standalone: every reference link in `SKILL.md` points at the upstream
repository over https, pinned to the commit the paths were verified against, so nothing
needs to be installed to follow them.

Install a pack locally when you want to grep across it or work offline.

## solana-new (sendaifun/solana-new)

Carries the audience guide, slide structures, storytelling frameworks, slide templates,
the deck design system, worked crypto deck examples, primary sources and the
common-mistakes list.

- Upstream: https://github.com/sendaifun/solana-new
- Pinned commit for the links in `SKILL.md`: `e81c261645035c0e902eaaa518ff58722d188bb7`
- Standalone: `git clone https://github.com/sendaifun/solana-new`
- With [solanabr/ai-kit](https://github.com/solanabr/ai-kit) installed: `bash .claude/bin/skills.sh add solana-new`
  (it lands at `.claude/skills/ext/solana-new/`)

## frontend-design (anthropics/skills)

Optional. Carries visual direction for the rendered HTML deck and for any graphic or
marketing asset it needs. Not required to produce the deck outline.

- Upstream: https://github.com/anthropics/skills/tree/main/frontend-design
- With [solanabr/ai-kit](https://github.com/solanabr/ai-kit) installed it is present by
  default as a top-level skill at `.claude/skills/frontend-design/`
- Standalone: copy the `frontend-design/` folder from `anthropics/skills` into your
  `.claude/skills/` directory
