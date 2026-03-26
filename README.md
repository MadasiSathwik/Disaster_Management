# SMART DISASTER RELIEF RESOURCE MANAGEMENT SYSTEM

This is a full-stack Flask application for managing camps, victims, and resource distribution during disasters. The system includes user and administrator authentication, analytics reporting, and a Bootstrap/Chart.js frontend.

## Features
- Camp & victim management
- Resource distribution with prioritization logic
- User registration/login and separate admin portal
- Analytics dashboard with Chart.js
- Report generation saved to `reports/analytics.txt`
- Modular architecture with Blueprints
- PostgreSQL (Neon) via SQLAlchemy
- TODOs for enhancements: auth, REST API, Docker, tests, etc.

## Setup Instructions

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**:
   - Create a Neon PostgreSQL database and user.
   - Set `DATABASE_URL` in `.env` (sample provided).
   - Example: `postgresql://user:pass@host:5432/dbname`

4. **Initialize database**:
   ```bash
   python -c "from app import create_app; app=create_app(); from extensions import db; db.init_app(app); with app.app_context(): db.create_all()"
   ```
   or simply run `python app.py` once to auto-create tables.

5. **Create an admin user** (only one needed, keep credentials secret):
   ```bash
   python - <<'PY'
from app import create_app
from extensions import db
from models import Admin
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    if not Admin.query.filter_by(username='admin').first():
        a = Admin(username='admin', password=generate_password_hash('yourpassword'))
        db.session.add(a)
        db.session.commit()
        print('Admin created')
    else:
        print('Admin already exists')
PY
   ```

6. **Run application**:
   ```bash
   flask run
   # or
   python app.py
   ```

7. **Deployment with Gunicorn**:
   ```bash
   gunicorn app:create_app
   ```
   Set `DATABASE_URL` and `SECRET_KEY` in your hosting environment (Render, Heroku, etc.).

## Admin & User Portals
- **User**: `/login`, `/register` to manage victims/resource actions.
- **Admin**: `/admin/login` and `/admin/dashboard` (link appears after login).

## Notes
- Only the admin credentials are known to the administrator; no public signup.
- All actions require login (protected by `login_required`).
- Future enhancements are marked with TODO comments in code.

---
Happy coding! 🚀