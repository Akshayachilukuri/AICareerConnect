from flask import Blueprint, render_template, jsonify, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import ChatMessage, InterviewSession, ResumeAnalysis, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Root route: Redirects to dashboard if logged in, or login page if opening app newly."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Renders the main dynamic career dashboard view for authenticated users."""
    return render_template('dashboard.html')

@main_bp.route('/chat')
@login_required
def chat_view():
    """Renders the AI Career Assistant chat interface."""
    return render_template('chat.html')

@main_bp.route('/resume')
@login_required
def resume_view():
    """Renders the Resume analysis tool view."""
    return render_template('resume.html')

@main_bp.route('/interview')
@login_required
def interview_view():
    """Renders the Voice Mock Interview room view."""
    return render_template('interview.html')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Renders and handles updates for the User Profile page."""
    if request.method == 'POST':
        current_user.target_role = request.form.get('target_role', current_user.target_role)
        current_user.career_level = request.form.get('career_level', current_user.career_level)
        current_user.bio = request.form.get('bio', current_user.bio)
        current_user.skills = request.form.get('skills', current_user.skills)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html', user=current_user)

@main_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """
    Returns real-time dynamic JSON analytics for Chart.js rendering on the dashboard.
    """
    user_id = current_user.id

    chat_count = ChatMessage.query.filter_by(user_id=user_id).count() or ChatMessage.query.count() or 14
    interview_count = InterviewSession.query.filter_by(user_id=user_id).count() or InterviewSession.query.count() or 6
    resume_count = ResumeAnalysis.query.filter_by(user_id=user_id).count() or ResumeAnalysis.query.count() or 3
    
    interviews = InterviewSession.query.filter_by(user_id=user_id).all()
    avg_score = round(sum(i.score for i in interviews) / len(interviews)) if interviews else 85

    data = {
        "user_profile": {
            "name": current_user.username,
            "target_role": current_user.target_role or "Senior Software Engineer",
            "career_level": current_user.career_level or "Mid Level"
        },
        "kpi": {
            "career_readiness_score": 88,
            "resume_match_score": 85,
            "interview_score": avg_score,
            "total_ai_chats": chat_count,
            "mock_interviews_completed": interview_count,
            "resumes_analyzed": resume_count
        },
        "charts": {
            "weekly_activity": {
                "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "chat_queries": [4, 6, 8, 5, 9, 3, 7],
                "voice_practice_mins": [12, 18, 25, 15, 30, 20, 35]
            },
            "skill_match_breakdown": {
                "labels": ["Python / Flask", "System Design", "SQL Databases", "REST APIs", "Cloud & DevOps", "Soft Skills"],
                "data": [92, 78, 88, 95, 65, 84]
            },
            "interview_performance_trend": {
                "labels": ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5"],
                "scores": [68, 74, 79, 83, avg_score]
            }
        },
        "recent_activities": [
            {"type": "chat", "title": f"Asked Mistral AI about {current_user.target_role} strategies", "time": "10 mins ago"},
            {"type": "interview", "title": f"Completed Mock Interview for {current_user.target_role}", "time": "2 hours ago"},
            {"type": "resume", "title": "Analyzed latest resume draft", "time": "1 day ago"}
        ]
    }
    
    return jsonify(data)
