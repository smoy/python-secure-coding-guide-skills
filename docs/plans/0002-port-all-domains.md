# 0002 — Port all OpenSSF domains into the python-secure-coding skill

**Status:** Done · **Date:** 2026-06-25 · Follows [0001](0001-scope-new-skill-viability.md)

## Context

0001 validated the skill (GO) and shipped a 3-domain pilot (`03_numbers`,
`07_concurrency`, `09_cryptography`) plus a trigger-tested `SKILL.md`. This task
ported the remaining 6 domains so the skill covers the whole guide.

## What was done

- Inventoried the 6 remaining domains: **34 rules** (01: 4, 02: 3, 04: 8, 05: 6,
  06: 5, 08: 8). Combined with the 8 pilot rules → **42 `pyscg-XXXX` rules total**.
- Ported each domain with a dedicated subagent (fetch upstream `README.md` →
  adapt to the established `references/<domain>/pyscg-XXXX-<slug>.md` format:
  BLUF rule, Why, trimmed non-compliant/compliant snippets, preserved CWE map).
- Marked the plugin-overlap rules (`pyscg-0008/0009/0010/0023`) with † and a note
  to defer to `security-guidance` and cross-reference, not duplicate.
- Rewrote `SKILL.md` to index all 9 domains / 42 rules (per-domain tables:
  rule · do-this · trigger · primary CWE) and broadened the `description`.
- Added `scripts/sync-from-upstream.sh` (caches upstream READMEs into
  `upstream-cache/` for diffing) and updated `ATTRIBUTION.md` scope.

## Verification (passed)

- 42 reference files on disk; none empty; all contain `## Rule`.
- Every rule number in the `SKILL.md` index maps to exactly one reference file;
  no orphan reference files. `bash -n` on the sync script passes.
- `SKILL.md` frontmatter parses; `description` = 983 chars (< ~1024 limit).

## Follow-up (not done here)

- Manual fidelity pass over the agent-ported files (spot-checked 0009 + 0037 —
  faithful; a fuller review is advisable before relying on every example).
- Decide whether to commit `upstream-cache/` as a baseline or gitignore it.
- Optional: re-run the trigger battery against the broadened description.
