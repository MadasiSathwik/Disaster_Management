from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import Victim, Camp
from extensions import db
from routes.auth_routes import login_required
import uuid

victim_bp = Blueprint('victim', __name__, template_folder='../templates')

def generate_victim_id():
    """Generate unique victim ID."""
    return f"VID-{uuid.uuid4().hex[:8].upper()}"

@victim_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_victim():
    camps = Camp.query.all()
    auto_victim_id = None
    if request.method == 'GET':
        auto_victim_id = generate_victim_id()
    if request.method == 'POST':
        victim_id = request.form.get('victim_id')
        name = request.form.get('name')
        age = request.form.get('age', type=int)
        health_condition = request.form.get('health_condition')
        camp_id = request.form.get('assigned_camp')

        if not victim_id or not name or age is None or not health_condition:
            flash('All fields are required', 'danger')
            return redirect(url_for('victim.register_victim'))

        existing = Victim.query.filter_by(victim_id=victim_id).first()
        if existing:
            flash('Victim ID already exists', 'warning')
            return redirect(url_for('victim.register_victim'))

        victim = Victim(
            victim_id=victim_id,
            name=name,
            age=age,
            health_condition=health_condition
        )

        if camp_id:
            camp = Camp.query.filter_by(id=camp_id).first()
            if camp:
                if not camp.has_space():
                    flash('Selected camp is full', 'warning')
                    return redirect(url_for('victim.register_victim'))
                victim.assign_to_camp(camp)
            else:
                flash('Camp not found', 'danger')
                return redirect(url_for('victim.register_victim'))

        db.session.add(victim)
        db.session.commit()
        flash('Victim registered successfully', 'success')
        return redirect(url_for('victim.list_victims'))

    return render_template('register_victim.html', camps=camps, auto_victim_id=auto_victim_id)

@victim_bp.route('/list')
@login_required
def list_victims():
    victims = Victim.query.all()
    return render_template('dashboard.html', victims=victims)

# TODO: Add edit/delete victims
# TODO: Add pagination
