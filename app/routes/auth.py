from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        target_role = request.form.get('target_role', 'Software Engineer').strip()
        career_level = request.form.get('career_level', 'Mid Level').strip()

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'warning')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return render_template('auth/register.html')

        user = User(
            username=username,
            email=email,
            target_role=target_role,
            career_level=career_level
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Log user in immediately upon registration
        login_user(user, remember=True)
        flash(f'Account created successfully! Welcome to AI Career Connect, {user.username}.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('auth/register.html')

@auth_bp.route('/demo')
def demo_login():
    """Provides a 1-click instant demo login for testing."""
    demo_user = User.query.filter_by(username='demo_user').first()
    if not demo_user:
        demo_user = User(
            username='demo_user',
            email='demo@aicareerconnect.com',
            target_role='Senior Software Engineer',
            career_level='Mid-Senior Level'
        )
        demo_user.set_password('demo1234')
        db.session.add(demo_user)
        db.session.commit()

    login_user(demo_user, remember=True)
    flash('Logged in as Demo User!', 'info')
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
