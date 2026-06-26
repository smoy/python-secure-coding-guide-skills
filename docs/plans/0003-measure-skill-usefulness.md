# 0003 — Measure skill usefulness (A/B eval harness)

**Status:** Implemented + starter run · **Date:** 2026-06-25 · Follows [0002](0002-port-all-domains.md)

## Context

The skill ships (0002) and its content was fidelity-reviewed. Open question: does
it actually change Claude's output for the better? "Useful" = a testable causal
claim — **with the skill loaded, Claude writes more secure Python than without
it, at equal correctness and without firing on irrelevant prompts.** This task
builds the measurement and runs a first pass.

## Approach

An offline **A/B generation eval**, entirely reproducible from the repo:

1. **Dataset** (`evals/dataset.json`) — coding prompts, each tagged with the
   `pyscg-XXXX` rule it should invoke, a `detector` key, the `expected_symbol`
   the solution must define, whether it overlaps the `security-guidance` plugin,
   and a `neutral` flag for decoy prompts (reverse a string, average a list)
   that should produce no security noise.
2. **Two cells per prompt** — generate code with the skill **OFF** (no guidance
   in context) and **ON** (the matching `references/` file present in context,
   read by the agent — mirroring progressive disclosure). Instructions are
   otherwise identical and *neutral* ("write Python for this request") so we
   measure the skill's silent effect, not a "make it secure" command.
3. **Automated scoring** (`evals/detectors.py`) — pure-Python `ast`/regex
   detectors, one per rule, returning `{vuln, reason}`. No external deps; Bandit
   can optionally cross-check (B311/B602/B608/B301/B101). Each output is also
   checked for: parses, defines the expected symbol (light correctness gate),
   and cites the rule/CWE.
4. **Scorecard** (`evals/run_eval.py` → `evals/results/scorecard.md`) — per-case
   and aggregate **vulnerability rate OFF vs ON**, split by plugin-overlap vs
   non-overlap (the latter is the skill's *marginal* value over the plugin), plus
   correctness and a neutral-prompt noise check.

**Headline metric:** vulnerability-rate reduction (OFF→ON) at equal correctness.

## Layout

```
evals/
  dataset.json          # cases (prompt, rule, detector, expected_symbol, overlap, neutral)
  detectors.py          # ast/regex vuln detectors keyed by detector name
  run_eval.py           # scores samples/ -> results/scorecard.md
  samples/<case>/<off|on>/s*.py   # generated code (committed as evidence)
  results/scorecard.md  # output
  README.md             # methodology + how to run / regenerate
```

## Scope of the starter run

~9 cases (5 non-overlap domains: crypto 0038, concurrency 0025, numbers 0001,
coding-standards 0037, logging 0019; 2 overlap: 0009, 0023; 2 neutral), n=2
samples per cell. Enough to validate the harness and get a first signal; `n`
should be raised (≥5) and the prompt set widened for statistically stable numbers.

## Verification

- Detectors self-test on known vulnerable/safe snippets before scoring real
  samples (a detector that can't tell secure from insecure invalidates the eval).
- `run_eval.py` runs to completion and emits `results/scorecard.md`.
- Generated samples parse; expected symbols present.

## Known limitations (documented, not hidden)

- ON injects the reference file directly rather than exercising live skill
  auto-selection; trigger accuracy is measured separately (the 0001/0002 battery).
- `float_money` (0001) and a few others are heuristic detectors — labeled as such;
  Bandit-backed detectors (0038/0009/0023/0037) are high-confidence.
- Small `n` → wide error bars; the starter pass is directional, not definitive.
