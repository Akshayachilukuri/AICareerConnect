import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Application factory for Flask app initialization."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.ai import ai_bp
    from app.routes.voice import voice_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')

    # Ensure instance folder and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Create Database tables automatically within application context if not present
    with app.app_context():
        from app.models import user, chat, interview, resume
        db.create_all()

        # Automatic schema patch for existing databases missing bio/skills columns
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            if 'users' in inspector.get_table_names():
                cols = [c['name'] for c in inspector.get_columns('users')]
                if 'bio' not in cols:
                    db.session.execute(text("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT 'Passionate professional leveraging AI for career growth.'"))
                if 'skills' not in cols:
                    db.session.execute(text("ALTER TABLE users ADD COLUMN skills VARCHAR(255) DEFAULT 'Python, Flask, SQL, REST APIs, System Design'"))
                db.session.commit()
        except Exception as e:
            db.session.rollback()

    return app
