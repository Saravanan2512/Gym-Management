from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.package import Package

packages_bp = Blueprint('packages', __name__, url_prefix='/packages')

# -----------------------------
# List all packages
# -----------------------------
@packages_bp.route('/')
def package_list():
    packages = Package.query.all()
    return render_template('packages.html', packages=packages)

# -----------------------------
# Add a new package
# -----------------------------
@packages_bp.route('/add', methods=['POST'])
def add_package():
    name = request.form.get('name')
    amount = request.form.get('amount')
    description = request.form.get('description')
    plan_duration = request.form.get('plan_duration')  # dynamic months input

    if name and amount and plan_duration:
        try:
            new_package = Package(
                name=name,
                amount=float(amount),
                description=description,
                plan_duration=f"{plan_duration} month"  # save as string
            )
            db.session.add(new_package)
            db.session.commit()
            flash('Package added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding package: {str(e)}', 'danger')
    else:
        flash('All fields are required!', 'warning')

    return redirect(url_for('packages.package_list'))

# -----------------------------
# View a single package
# -----------------------------
@packages_bp.route('/<int:id>')
def view_package(id):
    package = Package.query.get_or_404(id)
    return render_template('view_package.html', package=package)

# -----------------------------
# Delete a package
# -----------------------------
@packages_bp.route('/delete/<int:id>', methods=['POST'])
def delete_package(id):
    package = Package.query.get_or_404(id)
    try:
        db.session.delete(package)
        db.session.commit()
        flash('Package deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting package: {str(e)}', 'danger')
    return redirect(url_for('packages.package_list'))
