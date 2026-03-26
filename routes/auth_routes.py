from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Admin
from extensions import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

# helper decorators

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def admin_required(f):
    def wrapper(*args, **kwargs):
        if session.get('is_admin') != True:
            flash('Admin access required', 'danger')
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password required', 'danger')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'warning')
            return redirect(url_for('auth.register'))
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = False
            flash('Logged in successfully', 'success')
            return redirect(url_for('report.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session.clear()
            session['user_id'] = admin.id
            session['username'] = admin.username
            session['is_admin'] = True
            flash('Admin logged in', 'success')
            return redirect(url_for('auth.admin_dashboard'))
        flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

@auth_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # placeholder page for admin
    return render_template('admin_dashboard.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))

# TODO: Add password reset, profile pages, more security
