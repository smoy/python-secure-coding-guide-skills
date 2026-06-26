# python-secure-coding-guide-skills

A [Claude Code](https://claude.com/claude-code) **Skill** that brings the
[OpenSSF Secure Coding Guide for Python](https://github.com/ossf/wg-best-practices-os-developers/tree/main/docs/Secure-Coding-Guide-for-Python)
to Claude as proactive, on-demand guidance.

When you write, review, or refactor Python with Claude Code, this Skill loads
the relevant secure-coding rule — with a non-compliant/compliant example and its
CWE mapping — so insecure idioms get steered away *as the code is written*,
rather than caught afterward.

## Why this exists

The official `security-guidance` plugin is a **reactive/detective** layer: it
reviews diffs for a short list of dangerous patterns. This Skill is the
**proactive/generative** complement — broad, Python-specific guidance applied
while generating code, and an on-demand reference. The two are designed to work
together; where they overlap (command/SQL/format-string injection,
deserialization) this Skill defers to the plugin and cross-references it.

## What's inside

A single Skill, `skills/python-secure-coding/`, covering **42 rules across all 9
domains** of the upstream guide. Each rule keeps its upstream `pyscg-XXXX`
identifier and CWE mapping.

| Domain | Focus |
|--------|-------|
| `01_introduction` | trust zones, externalized secrets, operator precedence, server-side access control |
| `02_encoding_and_strings` | explicit locale, canonicalization, consistent encoding |
| `03_numbers` | float/`Decimal` precision, fixed-width overflow, bitwise vs arithmetic, loop counters |
| `04_neutralization` | format-string / OS-command / SQL injection, type confusion, archive extraction, search paths, deserialization, allow-lists |
| `05_exception_handling` | specific exceptions, error handling, context preservation, numeric validation, `finally`/cleanup |
| `06_logging` | sensitive-data exposure, event logging, dev-tool stripping, log injection, error disclosure |
| `07_concurrency` | interruptible pool tasks, bounded pools, deadlock avoidance |
| `08_coding_standards` | iterable mutation, shadowing builtins, value comparison, `None` checks, resource cleanup, return-value checks, assertions |
| `09_cryptography` | cryptographically secure randomness |

- `SKILL.md` — entry point: a lean index of every rule (do-this · trigger · CWE)
  plus heuristics. Detail lives in per-rule files, loaded only when relevant.
- `references/<domain>/pyscg-XXXX-*.md` — one adapted rule each.
- `scripts/sync-from-upstream.sh` — caches the upstream READMEs for re-diffing.

## Using it with Claude Code

Clone this repo and make the Skill available to Claude Code, either personally or
per-project:

```bash
git clone https://github.com/smoy/python-secure-coding-guide-skills.git

# Personal (available in every project):
mkdir -p ~/.claude/skills
cp -r python-secure-coding-guide-skills/skills/python-secure-coding ~/.claude/skills/

# — or — project-scoped (commit it with your repo):
mkdir -p .claude/skills
cp -r python-secure-coding-guide-skills/skills/python-secure-coding .claude/skills/
```

Claude Code loads the Skill automatically when a task involves the kinds of
Python work it covers; there is no command to invoke. You can confirm it's
detected by checking your available skills in a Claude Code session.

## Provenance & license

Rule content is **adapted from the OpenSSF Secure Coding Guide for Python**,
which is dual-licensed **CC-BY-4.0** (documentation) and **MIT** (code snippets).
Adaptations here preserve that attribution — see
[`skills/python-secure-coding/ATTRIBUTION.md`](skills/python-secure-coding/ATTRIBUTION.md).
The content is provided for educational use, **without warranty**, and is not a
substitute for human review, SAST/DAST, dependency scanning, or penetration
testing.

Repository tooling and packaging are licensed under [Apache-2.0](LICENSE).

This project is **not affiliated with or endorsed by** the OpenSSF or Anthropic.
