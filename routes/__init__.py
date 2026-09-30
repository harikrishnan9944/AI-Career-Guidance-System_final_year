from functools import wraps
from flask import session, redirect, url_for, flash, g
from models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('Session expired or user not found. Please log in again.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('Session expired or user not found. Please log in again.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'ADMIN':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('career.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
