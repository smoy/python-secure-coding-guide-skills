import logging
import hashlib

logger = logging.getLogger(__name__)


def log_failed_login(username, password):
    # The password must never appear in logs (pyscg-0019 / CWE-532).
    # Anonymize the username with a one-way hash for privacy compliance,
    # while still producing a stable, correlatable identifier for investigation.
    username_hash = hashlib.sha256(username.encode()).hexdigest()[:12]
    logger.warning(
        "Failed login attempt",
        extra={"username_hash": username_hash, "event": "auth.login_failed"},
    )
