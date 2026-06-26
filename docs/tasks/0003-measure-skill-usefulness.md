Measure whether the `python-secure-coding` skill is actually useful: does Claude
write more secure Python with the skill loaded than without it, without hurting
correctness or firing on irrelevant prompts?

Build a reproducible offline eval harness that A/B-compares generated code with
the skill OFF vs ON, scores each output with automated vulnerability detectors,
and reports the vulnerability-rate reduction (the headline metric) broken out by
domain and by plugin-overlap. Run a starter pass and persist the scorecard.

Persist the plan/record on docs/plans/0003-measure-skill-usefulness.md.
