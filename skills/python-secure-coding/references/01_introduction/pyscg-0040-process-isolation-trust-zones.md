# pyscg-0040: Use Process Isolation for Trust Zones

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-664 (pillar), CWE-501 (Trust Boundary Violation), CWE-306 (Missing Authentication for Critical Function), CWE-269 (Improper Privilege Management).

## Rule

Run each trust zone in a **separate Python runtime under a distinct POSIX/OS user** with least-privilege access rights. Python has no built-in in-process access manager (unlike Java's Oracle Access Management), so process-level isolation is the only reliable enforcement mechanism.

## Why

When all Python scripts share the same OS user, a single perimeter breach gives an attacker the same privileges as the entire system. Layering security via separate OS users creates defense-in-depth: crossing trust-zone boundaries requires explicit authentication and authorization, so a compromise in one zone cannot automatically escalate into another.

## Non-compliant

All components (front-end, business logic, data layer) run as the same OS user. A breach anywhere gives full access everywhere.

```
[STRIDE diagram — all Python processes share one POSIX user]

front-end  ──►  business-logic  ──►  data-layer
     \_____________same OS user______________/
```

Breaking the outer perimeter allows the attacker to run commands with the same privileges as every other component.

## Compliant

Each trust zone runs as a separate OS user; crossing dotted red borders requires authentication and authorization.

```
[STRIDE diagram — separate POSIX users per zone]

front-end (user: www)
    │  [auth required]
    ▼
business-logic (user: app)
    │  [auth required]
    ▼
data-layer (user: db-svc)
```

Assign file-system and network permissions per user in accordance with the minimum access needed for that zone.

## Guidance

- Map trust boundaries during design using a threat model (e.g., STRIDE).
- Assign a dedicated OS user per zone with only the permissions it needs.
- Require authentication and authorization for every cross-zone call.
- Apply the same principle to containers and serverless functions (one identity per service).

See also: OWASP Top 10:2021 A04 Insecure Design.
