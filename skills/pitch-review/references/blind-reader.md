# A reader with no context

An anonymized deck is only half of a blind read. The other half is a reader that starts without anything that says whose deck it is. An ordinary subagent doesn't qualify.

## Why an ordinary subagent is not blind

Per the subagent docs ([Claude Code, Create custom subagents § What loads at startup](https://code.claude.com/docs/en/sub-agents), read 2026-10-08), a non-fork subagent starts with:

- **Every level of `CLAUDE.md`** the main session loads, including the user's `~/.claude/CLAUDE.md`, project rules and `CLAUDE.local.md`. A founder's global instructions usually name the company.
- **A git status snapshot**: current branch, main branch, `git status` and recent commits. Run from the startup's repo, the commit subjects name the product.
- **Environment details** appended to its system prompt, including the working directory. `/home/jane/acme-pay` names the project.
- **Your skills**, when its tools include `Skill`: the docs say it can discover and invoke them, and a user's own skill descriptions often name the company.

Opening a second session doesn't help: it inherits the same files. The reader then fills the gaps in the deck from what it already knows, and the clarity score comes out higher than a stranger would give. This is the curse of knowledge: better-informed people can't ignore what they know even when they try ([Camerer, Loewenstein and Weber 1989](https://doi.org/10.1086/261651)).

## The fix

A custom agent, started from a neutral directory, that leaves out what it can:

- `omitClaudeMd: true` launches it without the user, project and local `CLAUDE.md` files; managed policy files still load. It needs v2.1.271 or later and is ignored when the agent runs as the main session through `--agent`, so run it as a subagent ([frontmatter fields](https://code.claude.com/docs/en/sub-agents), read 2026-10-08).
- `tools: Read, Glob` and nothing else. Without `Skill` the skill list doesn't reach it; without shell, web or write tools it can only read the folder you name.
- Start the reviewing session from a neutral directory outside the project repo (the folder from [anonymize.md](anonymize.md) works), or set `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` for that session, so the git snapshot is left out ([settings reference, `includeGitInstructions`](https://code.claude.com/docs/en/settings-reference), read 2026-10-08). This one comes from the docs; our own probe ran outside a repo and didn't exercise it.

The definition below is a reference to copy, not something this pack installs. Put it in `.claude/agents/blind-pitch-reader.md` (this project) or `~/.claude/agents/blind-pitch-reader.md` (every project), or pass the same fields as JSON with `--agents` for one session, which writes nothing to disk. If the `agents` directory didn't exist when the session started, restart once so it is picked up.

```markdown
---
name: blind-pitch-reader
description: Reads anonymized pitch material from the one folder named in the prompt, in the persona given, and returns only the JSON asked for. Also ranks the paired comparison and checks answers against an answer key. Use only with a prompt from pitch-review's reader-prompts.md, with no extra context.
tools: Read, Glob
omitClaudeMd: true
---

You are a reader with no prior context. You receive only a persona, a name for the leak check, a folder with the material and the questions. Follow the prompt exactly.

Answer the leak check before opening any file. Open only the files in the folder named, in the order asked. Do not open any other file, do not list other folders and do not search the web.

Return only the JSON asked for, with no markdown around it.
```

Without a custom agent, a clean session works too: a chat with no custom instructions, no memory and no project files, given only `deck.pdf` and the prompt.

## The probe: run it before the first round of each new session

Use a separate agent of the same type. It carries the real names, so it never reads the material afterwards.

```
Context test. Do not open any file and do not use any tool. Answer only from what is in your context right now:
(1) Is there a block of user instructions (CLAUDE.md) or of auto memory (MEMORY.md, a memory index)? For each, copy its first line literally, or write "none".
(2) Do you know anything about {REAL COMPANY}, {REAL PRODUCT} or {REAL FOUNDER NAMES} from your context (not from training)? Write what and where it came from, or "nothing".
(3) What working directory, git branch, commit subjects and account email appear in your context?
Answer only with JSON: {"instructions": "...", "memory": "...", "knows": "...", "cwd": "...", "git": "...", "email": "..."}
```

Pass: "none" for (1) twice, "nothing" for (2), and no project name in (3). The user's own name in the path or the email is the known residual below, and doesn't fail the probe on its own.

What we saw on 2026-10-08 (v2.1.295, unpublished): a control subagent without `omitClaudeMd` quoted the first line of the user's instructions file and of the auto-memory index. The agent above quoted neither and knew nothing about the company. The docs say auto memory doesn't reach a non-fork subagent; our control got it anyway. Run the probe on your version rather than trusting either.

## Known residual

Two things still reach the reader: the working-directory path and the account email. Both give the user's name. That is harmless when the name means nothing to the reader. It isn't when the founder is publicly tied to the company: run the reader from another OS account or a clean session. The reader prompt's leak check asks about both, so each round records what got through.

The publisher page behind the Camerer DOI link refuses scripted requests (403); the DOI and its abstract were confirmed through OpenAlex's record on 2026-10-08.
