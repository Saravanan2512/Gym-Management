from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, date, timedelta
from calendar import monthrange
from app.models.client import Client
from app import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="")

# Dummy admin (replace with DB later)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# --- Helper decorator ---
def login_required(view_func):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please login first!", "warning")
            return redirect(url_for("dashboard.login"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def update_all_client_statuses():
    """Keeps each client's status in sync with end_date."""
    today = datetime.utcnow().date()
    changed = False
    for c in Client.query.all():
        new_status = "Inactive" if (c.end_date and c.end_date < today) else "Active"
        if c.status != new_status:
            c.status = new_status
            changed = True
    if changed:
        db.session.commit()


# --- Routes ---
@dashboard_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.home"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@dashboard_bp.route("/dashboard")
@login_required
def home():
    # 1. Update client statuses
    update_all_client_statuses()

    # 2. Get month/year from query params (default = current month)
    today = datetime.utcnow().date()
    year = int(request.args.get("year", today.year))
    month = int(request.args.get("month", today.month))

    # 3. Summary counts
    total_clients = Client.query.count()
    active_clients = Client.query.filter_by(status="Active").count()
    inactive_clients = Client.query.filter_by(status="Inactive").count()

    def pct(part, whole):
        return round((part / whole) * 100, 2) if whole else 0.0

    active_pct = pct(active_clients, total_clients)
    inactive_pct = pct(inactive_clients, total_clients)

    # 4. Business Growth → net active clients day by day
    num_days = monthrange(year, month)[1]
    first_day = date(year, month, 1)

    growth_dates, growth_counts = [], []
    active_count = 0

    for d in range(num_days):
        day = first_day + timedelta(days=d)

        joined_today = Client.query.filter(Client.start_date == day).count()
        expired_today = Client.query.filter(Client.end_date == day).count()

        active_count += joined_today - expired_today

        growth_dates.append(day.strftime("%Y-%m-%d"))
        growth_counts.append(active_count)

    # 5. Recent clients
    recent_clients = Client.query.order_by(Client.created_at.desc()).limit(10).all()

    return render_template(
        "dashboard.html",
        total_clients=total_clients,
        active_clients=active_clients,
        inactive_clients=inactive_clients,
        active_pct=active_pct,
        inactive_pct=inactive_pct,
        growth_dates=growth_dates,
        growth_counts=growth_counts,
        recent_clients=recent_clients,
        year=year,
        month=month,
    )
