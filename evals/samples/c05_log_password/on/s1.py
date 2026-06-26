import logging

logger = logging.getLogger(__name__)


def log_failed_login(username, password):
    # Log only the username; never include the password in log output.
    # Logging credentials violates pyscg-0019 (CWE-532) and privacy regulations.
    logger.warning("Failed login attempt for user: %s", username)
