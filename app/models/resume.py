from datetime import datetime
from app import db

class ResumeAnalysis(db.Model):
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    target_job = db.Column(db.String(100), nullable=False)
    match_score = db.Column(db.Integer, default=0)  # 0 to 100
    skills_found = db.Column(db.Text, nullable=True)  # JSON or comma separated string
    missing_skills = db.Column(db.Text, nullable=True)
    feedback_summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'target_job': self.target_job,
            'match_score': self.match_score,
            'skills_found': self.skills_found.split(',') if self.skills_found else [],
            'missing_skills': self.missing_skills.split(',') if self.missing_skills else [],
            'feedback_summary': self.feedback_summary,
            'created_at': self.created_at.isoformat()
        }
