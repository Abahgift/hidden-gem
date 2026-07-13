import hmac
from hmac import compare_digest
from functools import wraps
from flask import session, redirect, url_for, current_app


def check_admin_credentials(email, password):
    correct_email = current_app.config.get('ADMIN_EMAIL')
    correct_password = current_app.config.get('ADMIN_PASS')
    if correct_email is None or correct_password is None:
        raise RuntimeError("ADMIN_EMAIL / ADMIN_PASS not set in config")
    return (
        hmac.compare_digest(email, correct_email) and
        hmac.compare_digest(password, correct_password)
    )


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated