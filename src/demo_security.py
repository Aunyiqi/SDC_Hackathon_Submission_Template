"""Access guards for a synthetic, single-owner demo, not a user-account system."""

from __future__ import annotations

import hashlib
import hmac
import math
import secrets
import threading
import time
from collections import deque
from typing import Callable

from flask import current_app, session


MIN_SIGNING_KEY_LENGTH = 32
MIN_OWNER_CODE_LENGTH = 24
OWNER_SESSION_SECONDS = 30 * 60


def constant_time_match(provided: object, expected: object) -> bool:
    if not isinstance(provided, str) or not isinstance(expected, str):
        return False
    return hmac.compare_digest(provided.encode("utf-8"), expected.encode("utf-8"))


def owner_access_configured() -> bool:
    code = current_app.config.get("OWNER_ACCESS_CODE", "")
    key = current_app.secret_key
    return (
        bool(current_app.config.get("OWNER_SIGNING_KEY_CONFIGURED"))
        and isinstance(key, str)
        and len(key) >= MIN_SIGNING_KEY_LENGTH
        and isinstance(code, str)
        and len(code) >= MIN_OWNER_CODE_LENGTH
        and bool(code.strip())
    )


def owner_session_marker() -> str:
    """Invalidate existing owner sessions when either configured secret rotates."""
    return hmac.new(
        current_app.secret_key.encode("utf-8"),
        b"orderguard-owner-session:" + current_app.config["OWNER_ACCESS_CODE"].encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def owner_unlocked() -> bool:
    expires_at = session.get("owner_expires_at")
    return (
        owner_access_configured()
        and isinstance(expires_at, (int, float))
        and math.isfinite(expires_at)
        and expires_at > time.time()
        and constant_time_match(session.get("owner_session"), owner_session_marker())
    )


def csrf_token() -> str:
    token = session.get("csrf_token")
    if not isinstance(token, str) or not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def valid_csrf_token(provided: object) -> bool:
    expected = session.get("csrf_token")
    return bool(expected) and constant_time_match(provided, expected)


class AttemptLimiter:
    """A bounded, thread-safe rolling window shared by this demo process.

    This is deliberately not advertised as a distributed or persistent quota.
    """

    def __init__(
        self, limit: int, window_seconds: int, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self._attempts: deque[float] = deque()
        self._lock = threading.Lock()

    def consume(self) -> int:
        """Return zero when allowed, otherwise seconds until a slot is available."""
        with self._lock:
            now = self.clock()
            while self._attempts and self._attempts[0] <= now - self.window_seconds:
                self._attempts.popleft()
            if len(self._attempts) >= self.limit:
                return max(1, math.ceil(self._attempts[0] + self.window_seconds - now))
            self._attempts.append(now)
            return 0
