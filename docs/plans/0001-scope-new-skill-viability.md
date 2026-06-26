# 0001 — Viability: A Claude Skill from the OpenSSF Secure Coding Guide for Python

**Status:** Decision recorded · **Date:** 2026-06-25 · **Decision:** GO (build it)

## TL;DR (the answer)

**Yes — it makes sense to build a Claude Skill from the OpenSSF "Secure Coding Guide for
Python," and it is _complementary_ to `security-guidance@claude-plugins-official`, not a
duplicate.** The plugin is a reactive reviewer over a short list of dangerous patterns;
the guide is a broad, prescriptive, Python-deep body of secure-coding knowledge. A Skill
turns that knowledge into proactive guidance Claude applies _while writing_ Python and an
on-demand reference — a different control at a different point in the lifecycle.

## What was compared

- **OpenSSF Secure Coding Guide for Python** (`ossf/wg-best-practices-os-developers`,
  `docs/Secure-Coding-Guide-for-Python`): 55+ numbered rules (`pyscg-XXXX`) across 9
  domains, each a BLUF-style `README.md` with paired `noncompliantNN.py` / `compliantNN.py`
  (~20 lines) and CWE/CVE mappings. Targets CPython ≥ 3.9.
- **`security-guidance@claude-plugins-official`**: auto-installed hooks that review code
  for ~8 known-dangerous categories (per-edit pattern match, end-of-turn model review,
  deeper review on commit/push). Best-effort assistive detection.

## Why it's complementary, not duplicative

| | `security-guidance` plugin | Proposed Skill |
|---|---|---|
| Control type | Reactive / detective — reviews diffs after the fact | Proactive / generative — shapes code as it's written, plus on-demand reference |
| Trigger | Automatic hooks (per-edit, end-of-turn, commit/push) | Loaded by `description` when doing Python security-relevant work |
| Coverage | ~8 narrow categories (eval, pickle, `os.system`, XSS, GHA injection, `child_process`, …) | 55+ Python-specific rules across 9 domains |
| Depth | Largely language-agnostic pattern + model review | Python-idiom-deep (CPython ≥ 3.9), CWE/CVE-mapped, compliant/noncompliant pairs |

The plugin catches a short list of dangerous patterns *after* they're written. The guide
encodes broad Python security idioms the plugin never addresses: numeric
precision/overflow, encoding & locale, exception handling, secure logging,
concurrency/thread-safety, and cryptography. Overlap is confined to a thin zone (pickle
deserialization, command injection) — there the Skill should *cross-reference* the plugin
rather than compete, leaving the plugin as the detective layer.

The 9 domains in the guide:

1. `01_introduction` · 2. `02_encoding_and_strings` · 3. `03_numbers` · 4. `04_neutralization`
5. `05_exception_handling` · 6. `06_logging` · 7. `07_concurrency` · 8. `08_coding_standards`
9. `09_cryptography`

## Why the content is genuinely "Skill-shaped"

Every rule already follows a rigid contribution template — BLUF README, numerically
paired compliant/noncompliant ~20-line examples, CWE/CVE references. That maps almost 1:1
onto Skill reference material under progressive disclosure: a lean index in `SKILL.md`
plus one reference file per rule.

## Licensing — no blocker

Upstream is dual-licensed: **CC-BY-4.0** for documentation and **MIT** for code snippets.
Adapting and bundling the material is permitted **with attribution**. We carry an
`ATTRIBUTION.md` crediting OpenSSF and linking sources.

## Risks / caveats

- **Size:** 55+ rules will not fit one `SKILL.md`. Use progressive disclosure (lean index
  + per-rule reference files), never a monolith.
- **Overlap dedup:** pickle / command-injection rules overlap the plugin — cross-reference,
  don't fight it.
- **Triggering:** the `description` must fire on Python *security* work without over-firing
  on all Python edits.
- **Maintenance / drift:** upstream evolves. Keep an attribution note and a sync strategy
  so the Skill doesn't silently fall behind.

## Recommended architecture

- **One skill, `python-secure-coding`.** A lean `SKILL.md` that (a) states triggers,
  (b) indexes the 9 domains and the rules as a BLUF cheat-sheet, and (c) points to bundled
  `references/<domain>/<rule>.md` files carrying detail + adapted examples.
- **Progressive disclosure:** `SKILL.md` stays short; depth lives in reference files loaded
  only when relevant.
- **Attribution + sync:** `ATTRIBUTION.md` (CC-BY-4.0 / MIT) plus, later, a small script to
  re-sync from upstream.

## Pilot (validate before porting all 55)

Build two domains chosen for being clearly **outside the plugin's coverage**, to prove the
Skill's distinct value and shake out triggering:

- **`09_cryptography`** — high-value, plugin-weak.
- **`03_numbers`** — distinctly Python (int/float/Decimal semantics), plugin-blind.

Port ~3–5 rules per domain into `references/`, wire them into `SKILL.md`'s index, and
verify the Skill loads and triggers. Remaining 7 domains / ~45 rules are explicit
follow-up work (`0002+`).

## Verification

- This memo answers the go/no-go question up front and renders as valid Markdown.
- Pilot skill: `skills/python-secure-coding/SKILL.md` has valid frontmatter and a
  triggering `description`; every reference it indexes exists; `ATTRIBUTION.md` credits
  OpenSSF per the licenses; the Skill is detected as loadable.
