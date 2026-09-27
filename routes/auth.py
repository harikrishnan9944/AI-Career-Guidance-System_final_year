from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.profile import Profile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('career.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not name or not email or not password:
            flash('All required fields must be filled.', 'danger')
            return render_template('register.html', name=name, email=email)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', name=name, email=email)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html', name=name, email=email)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists.', 'danger')
            return render_template('register.html', name=name, email=email)

        # Create new user
        user = User(name=name, email=email, role='USER')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Create initial profile
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        # Auto login
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role
        flash('Registration successful! Welcome to CareerPath AI.', 'success')
        return redirect(url_for('profile.onboarding'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('user_role') == 'ADMIN':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('career.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html', email=email)

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email address or password.', 'danger')
            return render_template('login.html', email=email)

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role

        flash(f'Welcome back, {user.name}!', 'success')

        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        
        # If user profile is not completed, redirect to onboarding
        if user.profile and user.profile.profile_completion < 50:
            return redirect(url_for('profile.onboarding'))
            
        return redirect(url_for('career.dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
