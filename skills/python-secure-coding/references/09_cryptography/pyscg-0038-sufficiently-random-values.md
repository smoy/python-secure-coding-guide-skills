# pyscg-0038: Use Sufficiently Random Values

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-330 (Use of Insufficiently Random Values).

## Rule

For **any security-relevant random value** — tokens, session IDs, password-reset
codes, API keys, nonces, salts, IVs — use the **`secrets`** module (or
`os.urandom`), never the `random` module.

## Why

`random` is a Mersenne Twister (MT19937): a deterministic PRNG. Given the seed,
the entire sequence is reproducible, and observing enough outputs lets an attacker
recover internal state and predict future values. Two `Random` objects with the
same seed produce identical sequences. That predictability is fatal for secrets.
`secrets` draws from the OS CSPRNG via `os.urandom()`.

## Non-compliant

```py
import random

def generate_web_token():
    return random.randrange(int("1" + "0" * 31), int("9" * 32), 1)  # predictable
```

(Bandit flags this as **B311**; SonarQube as RSPEC-2245.)

## Compliant

```py
import secrets

def generate_web_token():
    return secrets.token_urlsafe()        # CSPRNG-backed, URL-safe token
```

Useful `secrets` helpers: `secrets.token_urlsafe(n)`, `secrets.token_hex(n)`,
`secrets.token_bytes(n)`, `secrets.choice(seq)`, `secrets.randbelow(n)`. The
`random` module remains fine for non-security uses (simulations, sampling, test
fixtures).
