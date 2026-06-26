# pyscg-0047: Use Allow Lists Over Deny Lists

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-184 (Incomplete List of Disallowed Inputs).

## Rule

Validate input by checking against an **allow list** of known-safe values or patterns, not a deny list of known-dangerous ones. A deny list will always be incomplete — Unicode alone provides over 1 million code points that can disguise blocked tokens.

## Why

Deny lists enumerate what is forbidden; attackers only need one gap to bypass them. For example, a filter blocking `<script>` will miss `<script生>` because the non-ASCII character `生` causes a simple string match to fail. An allow list rejects everything not explicitly permitted, so unknown variants are blocked by default. This is especially critical for inputs that feed into HTML rendering (XSS), SQL, OS commands, or file paths.

## Non-compliant

```python
import re

def filter_string(input_string: str):
    for tag in re.findall("<[^>]*>", input_string):
        if tag in ["<script>", "<img", "<a href"]:   # deny list — easily bypassed
            raise ValueError("Invalid input tag")

# Bypasses the deny list — <script生> is not in the deny list:
filter_string("NOK <script生>")   # no exception raised; XSS succeeds
```

## Compliant

```python
import re

ALLOWED_TAGS = {"<b>", "<p>", "</p>"}   # allow list — everything else is rejected

def filter_string(input_string: str):
    for tag in re.findall("<[^>]*>", input_string):
        if tag not in ALLOWED_TAGS:              # reject anything not explicitly allowed
            raise ValueError("Invalid input tag")

# <script生> is not in ALLOWED_TAGS → ValueError raised immediately
filter_string("NOK <script生>")
```

Input containing `<script生>` now raises `ValueError` because the tag is absent from the allow list, regardless of its Unicode content.

> Note: canonicalize (normalize) input *before* validating — see pyscg-0044. An allow list applied to un-normalized Unicode may still be bypassed by homoglyph or normalization attacks.
