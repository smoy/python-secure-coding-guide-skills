import secrets


def make_reset_token() -> str:
    """Return a URL-safe, cryptographically random token for password-reset emails.

    Uses secrets.token_urlsafe() which draws from the OS CSPRNG (os.urandom),
    producing 32 bytes (256 bits) of entropy encoded as a URL-safe base64 string.
    This satisfies pyscg-0038: never use the random module for security-relevant values.
    """
    return secrets.token_urlsafe(32)
