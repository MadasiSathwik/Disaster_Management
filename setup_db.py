from app import create_app
from extensions import db
from models import Camp, Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create admin if not exists
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin created (username: admin, password: admin123)')

    # Add sample camps in Telangana if they don't exist
    telangana_camps = [
        {'camp_id': 'CAMP_001', 'location': 'Hyderabad - HITEC City', 'max_capacity': 500, 'food': 1000, 'medical': 400, 'volunteers': 25},
        {'camp_id': 'CAMP_002', 'location': 'Secunderabad - Railway Station', 'max_capacity': 300, 'food': 600, 'medical': 250, 'volunteers': 15},
        {'camp_id': 'CAMP_003', 'location': 'Telangana Firhana - Medical Center', 'max_capacity': 400, 'food': 800, 'medical': 350, 'volunteers': 20},
        {'camp_id': 'CAMP_004', 'location': 'Warangal - District Hospital', 'max_capacity': 350, 'food': 700, 'medical': 300, 'volunteers': 18},
        {'camp_id': 'CAMP_005', 'location': 'Vijayawada - Collectorate', 'max_capacity': 450, 'food': 900, 'medical': 380, 'volunteers': 22},
        {'camp_id': 'CAMP_006', 'location': 'Karimnagar - Government Building', 'max_capacity': 280, 'food': 560, 'medical': 220, 'volunteers': 14},
        {'camp_id': 'CAMP_007', 'location': 'Khammam - Relief Center', 'max_capacity': 320, 'food': 640, 'medical': 270, 'volunteers': 16},
        {'camp_id': 'CAMP_008', 'location': 'Nizamabad - Community Hall', 'max_capacity': 290, 'food': 580, 'medical': 240, 'volunteers': 14},
    ]

    for camp_data in telangana_camps:
        if not Camp.query.filter_by(camp_id=camp_data['camp_id']).first():
            camp = Camp(
                camp_id=camp_data['camp_id'],
                location=camp_data['location'],
                max_capacity=camp_data['max_capacity'],
                current_occupancy=0,
                available_food_packets=camp_data['food'],
                available_medical_kits=camp_data['medical'],
                volunteers=camp_data['volunteers']
            )
            db.session.add(camp)
    
    db.session.commit()
    print('✓ Telangana camps initialized')
    print('\nDatabase setup complete! Ready to run the application.')
