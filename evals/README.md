# Skill-usefulness eval

Measures whether Claude writes **more secure Python with the
`python-secure-coding` skill loaded than without it** — at equal correctness and
without over-firing on irrelevant prompts. See
[`../docs/plans/0003-measure-skill-usefulness.md`](../docs/plans/0003-measure-skill-usefulness.md)
for the rationale.

## How it works

For each case in `dataset.json` we generate code **twice**:

- **OFF** — a coding agent answers from its own knowledge, no skill in context.
- **ON** — the same neutral coding request, but the matching `references/` file is
  in context (read first), mirroring how the skill delivers guidance via
  progressive disclosure.

Instructions are identical and *neutral* ("write Python for this request") — we
never tell the model "make it secure", so we measure the skill's silent effect.
Each generated file is scored by `detectors.py` (pure-Python `ast`/regex, one
detector per rule) for: **vulnerable?**, **parses + defines the expected symbol**
(correctness gate), and **cites the rule/CWE**.

**Headline metric:** vulnerability-rate reduction (OFF → ON) at equal correctness,
split by plugin-overlap vs non-overlap (non-overlap = the skill's marginal value
over the `security-guidance` plugin).

## Run it

```bash
cd evals
python3 detectors.py     # self-test: every detector must distinguish vuln vs safe
python3 run_eval.py      # scores samples/ -> results/scorecard.md
```

`run_eval.py` has no dependencies. Bandit can optionally cross-check the
high-confidence detectors (B311/B602/B608/B301/B101) but is not required.

## Regenerating samples

`samples/<case>/<off|on>/s*.py` are committed as evidence. To regenerate, delete
a cell's folder and have an agent (or any LLM) answer that case's `prompt` under
the OFF/ON conditions above, writing fresh `.py` files. Then re-run `run_eval.py`.

## Latest result (starter run, n=2)

| Slice | Vuln% OFF | Vuln% ON | Reduction |
|-------|-----------|----------|-----------|
| All security cases | 71% | 0% | 71 pts |
| Non-overlap (skill's marginal value) | 70% | 0% | 70 pts |
| Overlap with plugin | 75% | 0% | 75 pts |

Correctness held at 100% OFF and ON. Full table in `results/scorecard.md`.

## Caveats (read before trusting the number)

- **Small n.** Starter run is n=2 per cell — directional, not definitive. Raise to
  ≥5 and widen the prompt set for stable numbers.
- **ON injects the reference directly** rather than exercising live skill
  auto-selection. Trigger accuracy (does the skill *fire* on the right prompts) is
  a separate axis — measured by the prompt battery in `docs/plans/0001`/`0002`.
- **Some detectors are heuristic** (`float_money`, `thread_per_request`); the
  Bandit-backed ones (random/shell/sql/pickle/assert/logging) are high-confidence.
- **Noise signal:** the neutral cases catch over-firing. In the starter run, 50%
  of neutral ON samples added a security/CWE citation to trivial code (e.g. `None`
  guards + rule references on a string-reversal). The skill improves security
  dramatically but can be chatty on irrelevant tasks — a real cost to weigh.
