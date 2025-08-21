from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.trainer import Trainer

trainers_bp = Blueprint('trainers', __name__, url_prefix='/trainers')

# List all trainers
@trainers_bp.route('/')
def list_trainers():
    trainers = Trainer.query.all()
    return render_template('trainer.html', trainers=trainers)

# Add trainer (existing)
@trainers_bp.route('/add', methods=['POST'])
def add_trainer():
    trainer_id = request.form.get('trainer_id')
    name = request.form.get('name')
    experience = request.form.get('experience')
    qualities = request.form.get('qualities')
    batch = request.form.get('batch')
    photo = request.files.get('photo')

    if trainer_id:  # edit existing
        trainer = Trainer.query.get(trainer_id)
        if trainer:
            trainer.name = name
            trainer.experience = experience
            trainer.qualities = qualities
            trainer.batch = batch
            if photo:
                filename = photo.filename
                photo.save(f"app/static/uploads/trainers/{filename}")
                trainer.photo = filename
            db.session.commit()
            flash('Trainer updated successfully!', 'success')
    else:  # new trainer
        filename = photo.filename
        photo.save(f"app/static/uploads/trainers/{filename}")
        new_trainer = Trainer(
            name=name,
            experience=experience,
            qualities=qualities,
            batch=batch,
            photo=filename
        )
        db.session.add(new_trainer)
        db.session.commit()
        flash('Trainer added successfully!', 'success')

    return redirect(url_for('trainers.list_trainers'))

# -----------------------------
# Delete trainer
# -----------------------------
@trainers_bp.route('/delete/<int:trainer_id>', methods=['POST'])
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    try:
        db.session.delete(trainer)
        db.session.commit()
        flash('Trainer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting trainer: {str(e)}', 'danger')
    return redirect(url_for('trainers.list_trainers'))
