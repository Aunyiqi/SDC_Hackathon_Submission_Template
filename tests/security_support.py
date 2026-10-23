"""Isolated demo-owner setup for route tests; no production secrets are used."""

import secrets

from demo_security import AttemptLimiter


def configure_owner_access(test_case, app):
    values = {
        "TESTING": True,
        "SECRET_KEY": secrets.token_hex(32),
        "OWNER_SIGNING_KEY_CONFIGURED": True,
        "OWNER_ACCESS_CODE": secrets.token_urlsafe(32),
        "SESSION_COOKIE_SECURE": False,
    }
    previous = {key: app.config.get(key) for key in values}
    old_limiters = {
        name: app.extensions[name]
        for name in ("owner_login_limiter", "ai_extraction_limiter")
    }
    app.config.update(values)
    app.extensions["owner_login_limiter"] = AttemptLimiter(5, 60)
    app.extensions["ai_extraction_limiter"] = AttemptLimiter(10, 60)

    def restore():
        app.config.update(previous)
        app.extensions.update(old_limiters)

    test_case.addCleanup(restore)


def authenticate_owner(client, app, automatic_csrf=True):
    with client.get("/owner/login") as response:
        if response.status_code != 200:
            raise AssertionError("Owner login page did not load")
    with client.session_transaction() as session:
        old_csrf = session["csrf_token"]
    with client.post(
        "/owner/login",
        data={"csrf_token": old_csrf, "access_code": app.config["OWNER_ACCESS_CODE"]},
    ) as response:
        if response.status_code != 302:
            raise AssertionError("Test owner could not unlock demo controls")
    with client.session_transaction() as session:
        token = session["csrf_token"]
    if automatic_csrf:
        client.environ_base["HTTP_X_CSRF_TOKEN"] = token
    return token
