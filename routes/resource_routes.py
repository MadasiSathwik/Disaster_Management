from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Camp, Victim
from extensions import db
from routes.auth_routes import login_required

resource_bp = Blueprint('resource', __name__, template_folder='../templates')

@resource_bp.route('/distribute', methods=['GET', 'POST'])
@login_required
def distribute_resources():
    camps = Camp.query.all()
    victims = Victim.query.all()
    if request.method == 'POST':
        victim_id = request.form.get('victim_id')
        victim = Victim.query.filter_by(victim_id=victim_id).first()
        if not victim:
            flash('Victim not found', 'danger')
            return redirect(url_for('resource.distribute_resources'))

        camp = victim.camp
        if not camp:
            flash('Victim has not been assigned to a camp', 'warning')
            return redirect(url_for('resource.distribute_resources'))

        # allocate resources based on health condition
        allocated = False
        if victim.health_condition.lower() == 'critical':
            if camp.allocate_medical_kit():
                victim.receive_medical_kit()
                allocated = True
            else:
                flash('No medical kits available in camp', 'warning')
        # Only give food if not already received
        if not victim.food_received and camp.available_food_packets > 0:
            if camp.allocate_food():
                victim.receive_food()
                allocated = True
            else:
                flash('No food packets available in camp', 'warning')
        
        if allocated:
            db.session.commit()
            flash('Resources distributed', 'success')
        else:
            flash('Unable to allocate resources', 'warning')
        return redirect(url_for('resource.distribute_resources'))

    return render_template('distribute.html', camps=camps, victims=victims)

# TODO: Add endpoint for bulk distribution
