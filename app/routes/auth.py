# app/routes/auth.py
from flask import Blueprint, redirect, url_for, session, flash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("dashboard.login"))
