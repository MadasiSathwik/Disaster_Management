from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Camp
from extensions import db
from routes.auth_routes import login_required

camp_bp = Blueprint('camp', __name__, template_folder='../templates')

@camp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_camp():
    if request.method == 'POST':
        camp_id = request.form.get('camp_id')
        location = request.form.get('location')
        max_capacity = request.form.get('max_capacity', type=int)
        food = request.form.get('available_food_packets', type=int, default=0)
        medical = request.form.get('available_medical_kits', type=int, default=0)
        volunteers = request.form.get('volunteers', type=int, default=0)

        if not camp_id or not location or max_capacity is None:
            flash('Camp ID, location and capacity are required', 'danger')
            return redirect(url_for('camp.add_camp'))

        existing = Camp.query.filter_by(camp_id=camp_id).first()
        if existing:
            flash('Camp ID already exists', 'warning')
            return redirect(url_for('camp.add_camp'))

        camp = Camp(
            camp_id=camp_id,
            location=location,
            max_capacity=max_capacity,
            current_occupancy=0,
            available_food_packets=food,
            available_medical_kits=medical,
            volunteers=volunteers
        )
        db.session.add(camp)
        db.session.commit()
        flash('Camp added successfully', 'success')
        return redirect(url_for('camp.view_camps'))

    return render_template('add_camp.html')

@camp_bp.route('/list')
@login_required
def view_camps():
    camps = Camp.query.all()
    return render_template('dashboard.html', camps=camps)

# TODO: Add edit and delete endpoints
