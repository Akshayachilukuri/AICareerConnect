from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    target_role = db.Column(db.String(100), default='Software Engineer')
    career_level = db.Column(db.String(50), default='Mid Level')
    bio = db.Column(db.Text, default='Passionate professional leveraging AI for career growth.')
    skills = db.Column(db.String(255), default='Python, Flask, SQL, REST APIs, System Design')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    chats = db.relationship('ChatMessage', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    interviews = db.relationship('InterviewSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    resumes = db.relationship('ResumeAnalysis', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'target_role': self.target_role,
            'career_level': self.career_level,
            'created_at': self.created_at.isoformat()
        }

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
