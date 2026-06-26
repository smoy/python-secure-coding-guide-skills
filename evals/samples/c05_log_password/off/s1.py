import logging

logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def log_failed_login(username, password):
    """Record a failed login attempt including credentials for investigation."""
    logger.warning(
        "Failed login attempt: username=%s password=%s", username, password
    )
