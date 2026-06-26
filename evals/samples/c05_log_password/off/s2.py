import datetime


LOG_FILE = "failed_logins.log"


def log_failed_login(username, password):
    """Append a failed login record with timestamp, username, and password."""
    timestamp = datetime.datetime.utcnow().isoformat()
    entry = f"{timestamp} FAILED_LOGIN user={username!r} pass={password!r}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
