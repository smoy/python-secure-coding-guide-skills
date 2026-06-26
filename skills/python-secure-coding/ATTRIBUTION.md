# Attribution & Licensing

The reference content in this skill is **adapted from the OpenSSF Secure Coding
Guide for Python**, a project of the OpenSSF Best Practices Working Group.

- Upstream: <https://github.com/ossf/wg-best-practices-os-developers/tree/main/docs/Secure-Coding-Guide-for-Python>
- Rules are identified by their upstream `pyscg-XXXX` numbers.

## Licenses (dual)

The upstream project is dual-licensed:

- **Documentation / prose** — Creative Commons Attribution 4.0 International
  (**CC-BY-4.0**). Adaptations here are provided under the same terms, with
  attribution to the OpenSSF project contributors.
- **Code snippets** — **MIT License**. Upstream snippets carry
  `SPDX-License-Identifier: MIT` and `SPDX-FileCopyrightText: OpenSSF project
  contributors`.

The content is provided **WITHOUT WARRANTY OF ANY KIND**, for educational use,
and is **not** a substitute for human review, SAST/DAST, dependency scanning, or
penetration testing.

## What was adapted

Examples have been trimmed and lightly edited for use as concise on-demand
reference material inside a Claude Skill. CWE/CVE mappings and the security
intent are preserved from upstream. For the authoritative, complete text and
runnable examples, consult the upstream rule directories linked in each file.

## Scope

This skill ships all 9 domains of the guide (42 `pyscg-XXXX` rules adapted as of
2026-06-25). Upstream may add rules over time; see Sync below.

## Sync

The repo-level `scripts/sync-from-upstream.sh` (a maintainer utility outside this
skill) pulls every upstream `pyscg-XXXX/README.md` into
`upstream-cache/<domain>/` so they can be diffed against the adapted
`references/` files. Re-adaptation (trimming examples to the essential contrast,
preserving rule numbers and CWE mappings) remains a manual judgment step — the
script intentionally does not overwrite `references/`.
