from datetime import datetime
from sqlalchemy.orm import relationship
from extensions import db

class Camp(db.Model):
    __tablename__ = 'camps'

    id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False, default=0)
    current_occupancy = db.Column(db.Integer, nullable=False, default=0)
    available_food_packets = db.Column(db.Integer, nullable=False, default=0)
    available_medical_kits = db.Column(db.Integer, nullable=False, default=0)
    volunteers = db.Column(db.Integer, nullable=False, default=0)

    victims = relationship('Victim', backref='camp', lazy=True)

    def __repr__(self):
        return f"<Camp {self.camp_id} at {self.location}>"

    @property
    def occupancy_percentage(self):
        if self.max_capacity:
            return round((self.current_occupancy / self.max_capacity) * 100, 2)
        return 0

    def has_space(self):
        return self.current_occupancy < self.max_capacity

    def allocate_food(self, quantity=1):
        if self.available_food_packets >= quantity:
            self.available_food_packets -= quantity
            return True
        return False

    def allocate_medical_kit(self, quantity=1):
        if self.available_medical_kits >= quantity:
            self.available_medical_kits -= quantity
            return True
        return False

    # TODO: Add methods to increment volunteers, restock resources, etc.

class Victim(db.Model):
    __tablename__ = 'victims'

    id = db.Column(db.Integer, primary_key=True)
    victim_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_condition = db.Column(db.String(20), nullable=False, default='Normal')
    assigned_camp_id = db.Column(db.Integer, db.ForeignKey('camps.id'), nullable=True)
    food_received = db.Column(db.Boolean, default=False)
    medical_kit_received = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Victim {self.victim_id} - {self.name}>"

    def assign_to_camp(self, camp: Camp):
        """Try assigning victim to given camp if space available."""
        if camp and camp.has_space():
            self.assigned_camp_id = camp.id
            camp.current_occupancy += 1
            return True
        return False

    def receive_food(self):
        self.food_received = True

    def receive_medical_kit(self):
        self.medical_kit_received = True

    # TODO: Add more validation (age limits, unique id checks, etc.)

# Authentication models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admin {self.username}>"

    # TODO: Add role/permission fields if multi-admin needed
