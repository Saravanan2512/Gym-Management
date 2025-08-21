from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.client import Client
from app.models.package import Package
from app.models.trainer import Trainer
from app import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

clients_bp = Blueprint("clients", __name__)

# ------------------------
# Helpers
# ------------------------
def update_all_client_statuses():
    today = datetime.utcnow().date()
    clients = Client.query.all()
    for c in clients:
        c.status = "Inactive" if c.end_date and c.end_date < today else "Active"
    db.session.commit()

def get_recent_clients(limit=1):
    return Client.query.order_by(Client.id.desc()).limit(limit).all()

# ------------------------
# Routes
# ------------------------

@clients_bp.route("/")
def list_clients():
    update_all_client_statuses()
    clients = Client.query.all()
    recent_clients = get_recent_clients(1)
    return render_template("all_clients.html", clients=clients, recent_clients=recent_clients)

@clients_bp.route("/active")
def active_clients():
    update_all_client_statuses()
    clients = Client.query.filter_by(status="Active").all()
    recent_clients = get_recent_clients(1)
    return render_template("active_clients.html", clients=clients, recent_clients=recent_clients)

@clients_bp.route("/inactive")
def inactive_clients():
    update_all_client_statuses()
    clients = Client.query.filter_by(status="Inactive").all()
    recent_clients = get_recent_clients(1)
    return render_template("inactive_clients.html", clients=clients, recent_clients=recent_clients)

@clients_bp.route("/<int:client_id>")
def view_client(client_id):
    client = Client.query.get_or_404(client_id)
    recent_clients = get_recent_clients(1)
    return render_template("view_client.html", client=client, recent_clients=recent_clients)

@clients_bp.route('/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.first_name = request.form['first_name']
        client.last_name = request.form['last_name']
        client.email = request.form['email']
        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('clients.view_client', client_id=client.id))
    return render_template('edit_client.html', client=client)


@clients_bp.route('/delete/<int:client_id>', methods=['POST', 'GET'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('clients.list_clients'))


@clients_bp.route("/new", methods=["GET", "POST"])
def new_client():
    packages = Package.query.all()
    trainers = Trainer.query.all()

    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            middle_name = request.form.get("middle_name")
            last_name = request.form["last_name"]
            email = request.form.get("email")
            contact = request.form["contact"]
            gender = request.form.get("gender")
            address = request.form["address"]
            duration = request.form["plan"]
            package_id = request.form["package"]
            trainer_id = request.form.get("trainer") or None

            # Dates
            start_date = datetime.utcnow().date()
            if duration.startswith("3"):
                end_date = start_date + relativedelta(months=3)
            elif duration.startswith("6"):
                end_date = start_date + relativedelta(months=6)
            elif duration.startswith("12"):
                end_date = start_date + relativedelta(months=12)
            else:
                end_date = None

            status = "Active" if end_date is None or end_date >= start_date else "Inactive"

            # Create Client
            client = Client(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                contact=contact,
                gender=gender,
                address=address,
                status=status,
                start_date=start_date,
                end_date=end_date,
                billing_date=start_date,
                duration=duration,
                package_id=int(package_id),
                trainer_id=int(trainer_id) if trainer_id else None,
            )
            db.session.add(client)
            db.session.commit()

            flash("Client added successfully!", "success")
            return redirect(url_for("clients.list_clients"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding client: {str(e)}", "danger")

    recent_clients = get_recent_clients(1)
    return render_template("new_member.html", packages=packages, trainers=trainers, recent_clients=recent_clients)
