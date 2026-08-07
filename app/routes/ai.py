from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from app import db
from app.models.chat import ChatMessage
from app.models.resume import ResumeAnalysis
from app.models.interview import InterviewSession, InterviewQA
from app.services.mistral_service import MistralService

ai_bp = Blueprint('ai', __name__)

def get_mistral_service():
    api_key = current_app.config.get('MISTRAL_API_KEY')
    model = current_app.config.get('MISTRAL_MODEL')
    return MistralService(api_key=api_key, model=model)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """Handles text or voice transcribed messages and queries Mistral AI."""
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    msg_type = data.get('message_type', 'text')

    if not user_message:
        return jsonify({"error": "Message content cannot be empty"}), 400

    user_id = current_user.id if hasattr(current_user, 'id') and current_user.is_authenticated else 1
    target_role = getattr(current_user, 'target_role', 'Software Engineer') if hasattr(current_user, 'target_role') else 'Software Engineer'

    # Save user message to SQLite DB
    user_chat = ChatMessage(user_id=user_id, role='user', content=user_message, message_type=msg_type)
    db.session.add(user_chat)

    # Get recent conversation context
    history = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.desc()).limit(6).all()
    history.reverse()

    # Query Mistral AI Service
    mistral = get_mistral_service()
    ai_reply = mistral.generate_chat_response(user_message, conversation_history=history, target_role=target_role)

    # Save AI response to SQLite DB
    ai_chat = ChatMessage(user_id=user_id, role='assistant', content=ai_reply, message_type='text')
    db.session.add(ai_chat)
    db.session.commit()

    return jsonify({
        "success": True,
        "user_message": user_message,
        "reply": ai_reply,
        "timestamp": ai_chat.timestamp.isoformat()
    })

@ai_bp.route('/resume/analyze', methods=['POST'])
def analyze_resume():
    """Analyzes uploaded/pasted resume text against a target job role."""
    data = request.get_json() or {}
    resume_text = data.get('resume_text', '').strip()
    target_job = data.get('target_job', 'Software Engineer').strip()

    if not resume_text:
        return jsonify({"error": "Resume content is required"}), 400

    user_id = current_user.id if hasattr(current_user, 'id') and current_user.is_authenticated else 1

    mistral = get_mistral_service()
    analysis_text = mistral.analyze_resume(resume_text, target_job)

    # Store analysis result in SQLite database
    analysis_record = ResumeAnalysis(
        user_id=user_id,
        filename=data.get('filename', 'Text Upload'),
        target_job=target_job,
        match_score=85,
        skills_found="Python, Flask, SQL, REST APIs",
        missing_skills="Docker, CI/CD, Kubernetes",
        feedback_summary=analysis_text
    )
    db.session.add(analysis_record)
    db.session.commit()

    return jsonify({
        "success": True,
        "analysis": analysis_text,
        "record_id": analysis_record.id
    })

@ai_bp.route('/interview/generate', methods=['POST'])
def generate_interview():
    """Generates mock interview questions for a role."""
    data = request.get_json() or {}
    role_title = data.get('role_title', 'Software Engineer').strip()

    user_id = current_user.id if hasattr(current_user, 'id') and current_user.is_authenticated else 1

    mistral = get_mistral_service()
    questions = mistral.generate_interview_questions(role_title, count=3)

    # Create new session in SQLite
    session = InterviewSession(user_id=user_id, role_title=role_title, score=80, status='in_progress')
    db.session.add(session)
    db.session.flush()

    qa_list = []
    for q_text in questions:
        qa = InterviewQA(session_id=session.id, question=q_text)
        db.session.add(qa)
        qa_list.append({"question": q_text})

    db.session.commit()

    return jsonify({
        "success": True,
        "session_id": session.id,
        "role_title": role_title,
        "questions": qa_list
    })
