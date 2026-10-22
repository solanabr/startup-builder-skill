#!/usr/bin/env python3
"""Repo checks for startup-builder-skill (#26). Standard library only.

    python3 .github/scripts/validate.py              # every blocking check
    python3 .github/scripts/validate.py --external   # report dead external links (never fails)

Each check prints its failures as `path: message` and the script exits 1 if any fail.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# A routing line, not documentation. The longest today is 295 characters.
DESCRIPTION_MAX = 300

# Files that may exist besides Markdown, HTML and LICENSE. Each entry needs a reason,
# so adding a script or config is a visible decision in review (#1's hazard rules).
ALLOWED_OTHER_FILES = {
    "skills/pitch-review/references/anonymize.sh": "user-run anonymizer, no network; reviewed in #38",
    ".github/scripts/validate.py": "this check",
    ".github/workflows/validate.yml": "runs this check",
}

# #1 and #15: what a pack must never carry.
FORBIDDEN_NAMES = {".mcp.json", "settings.json", "settings.local.json", "package.json"}
HAZARDS = [
    (re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba|z)?sh\b"), "pipes curl into a shell"),
    (re.compile(r"\bwget\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba|z)?sh\b"), "pipes wget into a shell"),
    (re.compile(r"superstack", re.I), "telemetry marker (superstack)"),
    (re.compile(r"convex\.cloud", re.I), "telemetry endpoint (convex.cloud)"),
]

MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*\)")
HTML_REF = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
GH_PINNED = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/(?:blob|tree)/([^/\s)\"'#>]+)")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
CONTEXT_FILE = re.compile(r"\.claude/context/([a-z0-9-]+\.md)")
ADAPTED = re.compile(r"adapted from\s+\[?([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\]?(?:@([0-9a-f]{7,40}))?", re.I)

failures: list[str] = []


def fail(path: Path | str, msg: str) -> None:
    failures.append(f"{path if isinstance(path, str) else path.relative_to(ROOT)}: {msg}")


def tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    return [ROOT / p for p in out.stdout.decode().split("\0") if p]


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def strip_code(text: str) -> str:
    """Drop fenced blocks and inline code: links there are examples, not links."""
    text = re.sub(r"^(```|~~~).*?^\1", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def slug(heading: str) -> str:
    """GitHub's anchor for a heading: lower case, punctuation dropped, spaces to hyphens."""
    h = re.sub(r"<[^>]+>", "", heading).replace("`", "").strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


_anchor_cache: dict[Path, set[str]] = {}


def anchors(path: Path) -> set[str]:
    if path not in _anchor_cache:
        seen: dict[str, int] = {}
        found: set[str] = set()
        text = re.sub(r"^(```|~~~).*?^\1", "", path.read_text(encoding="utf-8"), flags=re.S | re.M)
        for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
            s = slug(h)
            n = seen.get(s, 0)
            found.add(s if n == 0 else f"{s}-{n}")
            seen[s] = n + 1
        found.update(re.findall(r"""\bid\s*=\s*["']([^"']+)["']""", text))
        _anchor_cache[path] = found
    return _anchor_cache[path]


def links_in(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        return HTML_REF.findall(text)
    body = strip_code(text)
    return MD_LINK.findall(body) + MD_IMAGE.findall(body) + HTML_REF.findall(body)


def check_frontmatter(skills: list[Path]) -> None:
    for d in skills:
        f = d / "SKILL.md"
        if not f.exists():
            fail(d, "skill directory has no SKILL.md")
            continue
        m = re.match(r"---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
        if not m:
            fail(f, "no frontmatter block")
            continue
        fm: dict[str, str] = {}
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
        if fm.get("name") != d.name:
            fail(f, f"name is {fm.get('name')!r}, expected the directory name {d.name!r}")
        desc = fm.get("description", "").strip().strip("\"'")
        if not desc:
            fail(f, "no description")
        elif len(desc) > DESCRIPTION_MAX:
            fail(f, f"description is {len(desc)} characters (max {DESCRIPTION_MAX}); keep it a routing line")
        if fm.get("user-invocable") != "true":
            fail(f, "user-invocable must be true")


def check_links(files: list[Path]) -> None:
    for f in files:
        for url in links_in(f):
            if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("//") or "{{" in url:
                continue  # external, or a template placeholder the user fills in
            path, _, frag = url.partition("#")
            target = (f.parent / path).resolve() if path else f
            if not str(target).startswith(str(ROOT)) or not target.exists():
                fail(f, f"broken link {url}")
                continue
            if frag and target.is_file() and target.suffix in (".md", ".html") and frag not in anchors(target):
                fail(f, f"no anchor #{frag} in {rel(target)}")


def check_pinned(files: list[Path]) -> None:
    for f in files:
        for ref in GH_PINNED.findall(f.read_text(encoding="utf-8")):
            ref = ref.rstrip(".,;:")  # sentence punctuation after a bare URL
            if not SHA40.match(ref):
                fail(f, f"GitHub blob/tree link points at {ref!r}; pin it to a full 40-character commit SHA")


def check_hazards(all_files: list[Path]) -> None:
    for f in all_files:
        r = rel(f)
        if f.name in FORBIDDEN_NAMES:
            fail(r, f"{f.name} is not allowed in this pack (#1)")
        if not (f.suffix in (".md", ".html") or r == "LICENSE" or r in ALLOWED_OTHER_FILES):
            fail(r, "only .md, .html and LICENSE belong here; add a reviewed entry to ALLOWED_OTHER_FILES if this one must")
        if r == ".github/scripts/validate.py":
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(r, "binary file")
            continue
        for rx, what in HAZARDS:
            if rx.search(text):
                fail(r, what)


def notice_sources() -> dict[str, tuple[str, set[str]]]:
    """repo -> (commit, skills it lists), from each block of THIRD_PARTY_NOTICES.md."""
    text = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    out: dict[str, tuple[str, set[str]]] = {}
    for block in re.split(r"\n(?=## )|\n\n(?=Parts of )", text):
        m = re.search(r"\[([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\]\(https://github\.com/[^)]+\)\s+at\s+commit\s+`([0-9a-f]{40})`", block)
        if m:
            lead = block[: m.start()]
            out[m.group(1)] = (m.group(2), set(re.findall(r"`skills/([a-z0-9-]+)`", lead)))
    return out


def check_attribution(md_files: list[Path], skills: list[Path]) -> None:
    sources = notice_sources()
    if not sources:
        fail("THIRD_PARTY_NOTICES.md", "found no source blocks ([owner/repo](url) at commit `sha`)")
        return
    credited: dict[str, set[str]] = {}
    for f in md_files:
        for repo, sha in ADAPTED.findall(f.read_text(encoding="utf-8")):
            if repo not in sources:
                fail(f, f"adapted from {repo}, which has no block in THIRD_PARTY_NOTICES.md")
                continue
            if sha and not sources[repo][0].startswith(sha):
                fail(f, f"adapted from {repo}@{sha}, but THIRD_PARTY_NOTICES.md pins {sources[repo][0][:12]}")
            parts = f.relative_to(ROOT).parts
            if parts[0] == "skills":
                credited.setdefault(repo, set()).add(parts[1])
    names = {d.name for d in skills}
    for repo, (_, listed) in sources.items():
        for s in sorted(listed - names):
            fail("THIRD_PARTY_NOTICES.md", f"{repo} lists skills/{s}, which does not exist")
        for s in sorted((listed & names) - credited.get(repo, set())):
            fail(f"skills/{s}", f"THIRD_PARTY_NOTICES.md says it adapts {repo}, but no file in it says \"adapted from {repo}\"")
        for s in sorted(credited.get(repo, set()) - listed):
            fail("THIRD_PARTY_NOTICES.md", f"skills/{s} says it is adapted from {repo}; add it to that block's list")


def check_readme(skills: list[Path], md_files: list[Path]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rows = set(re.findall(r"^\|\s*\[[^\]]+\]\(skills/([a-z0-9-]+)/SKILL\.md\)", readme, re.M))
    for d in skills:
        if d.name not in rows:
            fail("README.md", f"no row in the skills table for skills/{d.name}")
    table = set(re.findall(r"^\|\s*`([a-z0-9-]+\.md)`\s*\|", readme, re.M))
    used: dict[str, str] = {}
    for f in md_files:
        if f.parts[len(ROOT.parts)] == "skills":
            for name in CONTEXT_FILE.findall(f.read_text(encoding="utf-8")):
                used.setdefault(name, rel(f))
    for name, where in sorted(used.items()):
        if name not in table:
            fail("README.md", f"context file {name} (named in {where}) has no row in the context-file table")


def check_external(files: list[Path]) -> int:
    urls: dict[str, str] = {}
    for f in files:
        for u in links_in(f):
            if u.startswith(("http://", "https://")):
                urls.setdefault(u.split("#")[0], rel(f))
    headers = {"User-Agent": "Mozilla/5.0 (link check; startup-builder-skill)"}

    def status(u: str) -> int | str:
        code: int | str = "error"
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(u, method=method, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as r:
                    return r.status
            except urllib.error.HTTPError as e:
                code = e.code
                if method == "HEAD" and e.code in (403, 405, 429, 501):
                    continue
                return code
            except Exception:  # noqa: BLE001 - a network error is a report line, not a crash
                return "error"
        return code

    with ThreadPoolExecutor(max_workers=16) as pool:
        codes = dict(zip(urls, pool.map(status, urls)))
    dead = [f"{codes[u]} {u} (in {where})" for u, where in sorted(urls.items()) if codes[u] in (404, 410)]
    print(f"{len(urls)} external links checked, {len(dead)} dead (404/410).")
    for line in dead:
        print("  " + line)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as s:
            s.write(f"### External links\n\n{len(urls)} checked, {len(dead)} dead.\n\n")
            s.writelines(f"- {line}\n" for line in dead)
    return 0


def main() -> int:
    all_files = tracked()
    content = [f for f in all_files if f.suffix in (".md", ".html")]
    skill_files = [f for f in content if rel(f).startswith("skills/") or rel(f) == "README.md"]
    md_files = [f for f in content if f.suffix == ".md"]
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if "--external" in sys.argv:
        return check_external(skill_files + [ROOT / "THIRD_PARTY_NOTICES.md"])
    checks = [
        ("frontmatter", lambda: check_frontmatter(skills)),
        ("relative links", lambda: check_links(content)),
        ("pinned GitHub links", lambda: check_pinned(content)),
        ("hazards (#1)", lambda: check_hazards(all_files)),
        ("attribution", lambda: check_attribution(md_files, skills)),
        ("README coverage", lambda: check_readme(skills, md_files)),
    ]
    for name, run in checks:
        before = len(failures)
        run()
        new = failures[before:]
        print(f"{'FAIL' if new else 'ok  '} {name}")
        for line in new:
            print(f"     {line}")
    print(f"\n{len(failures)} problem(s)." if failures else "\nAll checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
