from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, session
from models import Camp, Victim
from extensions import db
from utils.analytics import compute_analytics, save_analytics_to_file
from routes.auth_routes import login_required

report_bp = Blueprint('report', __name__, template_folder='../templates')

@report_bp.route('/dashboard')
@login_required
def dashboard():
    data = compute_analytics()
    return render_template('dashboard.html', analytics=data)

@report_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_victim():
    victim = None
    camp = None
    if request.method == 'POST':
        vid = request.form.get('victim_id')
        victim = Victim.query.filter_by(victim_id=vid).first()
        if victim:
            camp = victim.camp
        else:
            flash('Victim not found', 'warning')
    return render_template('search.html', victim=victim, camp=camp)

@report_bp.route('/generate', methods=['GET'])
@login_required
def generate_report():
    data = compute_analytics()
    save_analytics_to_file(data, 'reports/analytics.txt')
    flash('Report generated at reports/analytics.txt', 'success')
    return redirect(url_for('report.dashboard'))

# static route to download report file
@report_bp.route('/reports/<path:filename>')
def download_report(filename):
    return send_from_directory('reports', filename)

# TODO: Add PDF export
