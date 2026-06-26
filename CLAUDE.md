# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo packages the [OpenSSF Secure Coding Guide for Python](https://github.com/ossf/wg-best-practices-os-developers/tree/main/docs/Secure-Coding-Guide-for-Python)
as a **Claude Skill** (`skills/python-secure-coding/`). It contains almost no
executable code — it is curated security guidance adapted from upstream. The
content's job is to make Claude *write* secure Python proactively; it is the
generative complement to the `security-guidance` plugin's reactive diff review.

There is no build/lint/test toolchain. "Correctness" here means: the Skill loads,
its `description` triggers on the right prompts, and each reference file is a
faithful, accurate adaptation of its upstream rule.

## Skill anatomy

- `skills/python-secure-coding/SKILL.md` — the entry point. YAML frontmatter
  (`name`, `description`) drives skill selection; the `description` is a precise
  trigger surface (and a deliberate *anti*-trigger for non-security cases, e.g.
  "NOT random test data"). The body is a lean **index** of all 9 domains / rules
  (do-this · trigger · primary CWE) plus fast heuristics. It must stay short and
  point to reference files — depth lives in `references/`, loaded on demand
  (progressive disclosure). Keep `description` under ~1024 chars.
- `skills/python-secure-coding/references/<NN_domain>/pyscg-XXXX-<slug>.md` — one
  file per rule, named by its upstream `pyscg-XXXX` number. Domains mirror
  upstream (`01_introduction` … `09_cryptography`).
- `skills/python-secure-coding/ATTRIBUTION.md` — licensing (see below).
- `skills/python-secure-coding/scripts/sync-from-upstream.sh` — caches upstream
  READMEs for diffing; does **not** overwrite `references/`.

## Reference-file format contract

Every `references/.../pyscg-XXXX-*.md` follows the same shape (the pilot files
`pyscg-0001/0038` are the gold standard):

1. `# pyscg-XXXX: <Title>`
2. An attribution blockquote: `> Adapted from … (CC-BY-4.0 / MIT).` plus the
   rule's **CWE mapping**, copied from upstream's "Related Guidelines" table.
3. `## Rule` (BLUF), `## Why`, then trimmed `## Non-compliant` / `## Compliant`
   code (~15–20 lines, showing the essential contrast).

Hard rules when authoring/editing:
- **Never invent** CWEs, CVEs, APIs, or behaviors not in the upstream README.
- The compliant snippet must be a genuinely safe fix faithful to upstream's
  solution — and **self-contained** (no undefined names).
- If a rule maps to the `security-guidance` plugin's coverage (the † rules:
  `pyscg-0008/0009/0010/0023`), add the italic overlap note and cross-reference
  the plugin rather than duplicating it.
- If upstream has no code example for a rule, any illustrative snippet must be
  flagged with an *"illustrative, not a verbatim port"* note.

When you add or rename a reference file, update the matching row in `SKILL.md`'s
index — the index and `references/` must stay 1:1.

## Upstream provenance & licensing

Source is dual-licensed **CC-BY-4.0** (docs) / **MIT** (code). Adaptation is
permitted with attribution to OpenSSF; preserve `ATTRIBUTION.md` and the per-file
attribution blockquote. Files are adaptations, not verbatim copies — trim
examples but keep rule numbers and CWE mappings intact.

## Workflows (commands actually used here)

Fetch an upstream rule README (`gh` must be authenticated):

```bash
gh api "repos/ossf/wg-best-practices-os-developers/contents/docs/Secure-Coding-Guide-for-Python/<NN_domain>/pyscg-XXXX/README.md" --jq '.content' | base64 -d
```

> Sandbox gotcha: this environment runs shell **for-loop bodies under `eval` with
> a stripped PATH**, so `gh`/`base64`/`wc` are "command not found" inside loops.
> Use absolute paths in loops (`/opt/homebrew/bin/gh`, `/usr/bin/base64`) or run
> commands individually.

Verify the index and reference set stay consistent:

```bash
cd skills/python-secure-coding
# every indexed rule number maps to exactly one file, and no orphan files
grep -oE '^\| 0[0-9]{3}' SKILL.md | grep -oE '0[0-9]{3}' | sort -u   # indexed rules
find references -name 'pyscg-*.md' | wc -l                            # file count
```

Sanity-check changed code snippets (extract to a `.py` and run `py_compile`); for
behavioral claims, actually run the snippet and confirm the stated output.

Validate `SKILL.md` frontmatter: `python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"`.

## Change process

Work is tracked as numbered tasks in `docs/tasks/NNNN-*.md`; the resulting
decision/record goes in `docs/plans/NNNN-*.md` (e.g. `0001` = viability,
`0002` = porting all domains). Follow this numbering for new units of work.

Two quality gates are expected before relying on edits:
1. **Trigger test** — give a fresh agent only the `SKILL.md` `description` plus a
   battery of should-fire / should-not-fire prompts; tighten the `description`
   until both under- and over-firing are gone.
2. **Fidelity review** — for ported rules, diff each reference file against its
   upstream README (CWE mapping correct, compliant code genuinely safe, nothing
   fabricated). Fix SERIOUS findings before commit.
