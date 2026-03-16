from extensions import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import models
import secrets
from datetime import datetime, timedelta
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    session_token = db.Column(db.String(128), unique=True, nullable=True)
    session_expiration = db.Column(db.DateTime, nullable=True)

    def generate_session_token(self, duration_days=30):
        self.session_token = secrets.token_urlsafe(32)
        self.session_expiration = datetime.utcnow() + timedelta(days=duration_days)
        db.session.commit()
        return self.session_token

    def clear_session_token(self):
        self.session_token = None
        self.session_expiration = None
        db.session.commit()

def create_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        hashed_password = generate_password_hash("admin", method="pbkdf2:sha256")
        new_admin = User(username="admin", password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created.")

