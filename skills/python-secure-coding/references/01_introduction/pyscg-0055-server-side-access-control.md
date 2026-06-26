# pyscg-0055: Determine Access on Server Side

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-693 (pillar), CWE-472 (External Control of Assumed-Immutable Web Parameter).

> *Upstream illustrates this rule with a single vulnerable example and no compliant
> code file; the compliant snippet below is an illustrative safe fix, not a verbatim
> port.*

## Rule

**Never derive a user's identity or role from client-submitted data** (form fields, query parameters, cookies set by the client, JWT claims without signature verification). Session state and role lookups must live entirely on the server side.

## Why

An attacker can tamper with any client-supplied value using browser DevTools, an intercepting proxy (e.g., Burp Suite), or a custom script. Trusting `session_user` from a POST body is equivalent to trusting the attacker's word for who they are.

## Non-compliant

```py
def post(self, form_data: Dict[str, str] = {"session_user": "", "action": ""}) \
        -> tuple[Dict[str, str], str]:
    action       = form_data.get("action", "")
    session_user = form_data.get("session_user", "")  # attacker-controlled!
    if session_user not in self.users:
        return form_data, "401: Please login"
    action_data = self._submit(session_user, action)
    return form_data, action_data
```

An attacker submitting `{"action": "write", "session_user": "admin"}` is immediately granted admin write access.

## Compliant

```py
# Server resolves the authenticated user from a server-managed session token,
# signed JWT (validated server-side), or OIDC IdP — never from form_data.

def post(self, session_token: str, form_data: Dict[str, str]) \
        -> tuple[Dict[str, str], str]:
    session_user = self._resolve_user_from_token(session_token)  # server-side
    if session_user is None:
        return form_data, "401: Please login"
    action = form_data.get("action", "")
    return form_data, self._submit(session_user, action)
```

The identity comes from a server-managed session token or a cryptographically verified mechanism (session cookie, signed JWT, OIDC). The client cannot influence `session_user`.

## Guidance

- Use server-side session stores, signed JWTs with proper validation, or an IdAM solution (e.g., OpenID Connect).
- Treat all fields in `form_data`, query strings, and HTTP headers as untrusted input.
- Perform role/permission lookups against a server-side store, not against client-submitted role claims.
