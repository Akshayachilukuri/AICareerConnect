from datetime import datetime
from app import db

class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_title = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)  # 0 to 100
    status = db.Column(db.String(20), default='in_progress')  # 'in_progress', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    qa_pairs = db.relationship('InterviewQA', backref='session', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'role_title': self.role_title,
            'score': self.score,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'qa_count': self.qa_pairs.count()
        }

class InterviewQA(db.Model):
    __tablename__ = 'interview_qa'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, default=0)  # 1 to 10
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'question': self.question,
            'answer': self.answer,
            'feedback': self.feedback,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }
