from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes import admin_required
from models import db
from models.user import User
from models.profile import Profile
from models.career import Career, SavedCareer
from models.recommendation import Recommendation
from services.career_data import get_admin_analytics_data, get_career_categories

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = get_admin_analytics_data()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_careers = Career.query.order_by(Career.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_users=recent_users,
        recent_careers=recent_careers
    )


@admin_bp.route('/careers')
@admin_required
def careers():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    query = Career.query

    if search:
        query = query.filter(Career.name.ilike(f'%{search}%'))

    if category and category != 'All':
        query = query.filter(Career.category == category)

    careers_list = query.order_by(Career.id.desc()).all()
    categories = get_career_categories()

    return render_template(
        'admin/careers.html',
        careers=careers_list,
        categories=categories,
        search=search,
        selected_category=category
    )


@admin_bp.route('/careers/add', methods=['GET', 'POST'])
@admin_required
def add_career():
    categories = get_career_categories()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()

        # Comma-separated list inputs
        required_skills = [s.strip() for s in request.form.get('required_skills', '').split(',') if s.strip()]
        soft_skills = [s.strip() for s in request.form.get('soft_skills', '').split(',') if s.strip()]
        required_education = [s.strip() for s in request.form.get('required_education', '').split(',') if s.strip()]
        interests = [s.strip() for s in request.form.get('interests', '').split(',') if s.strip()]
        work_environment = [s.strip() for s in request.form.get('work_environment', '').split(',') if s.strip()]

        if not name or not category or not description:
            flash('Career Name, Category, and Description are required.', 'danger')
            return render_template('admin/career_form.html', categories=categories, career=None)

        existing = Career.query.filter_by(name=name).first()
        if existing:
            flash(f'A career named "{name}" already exists.', 'danger')
            return render_template('admin/career_form.html', categories=categories, career=None)

        # Build growth structure
        growth = [
            {"level": "Entry Level", "title": request.form.get('growth_entry', 'Junior Specialist')},
            {"level": "Mid Level", "title": request.form.get('growth_mid', 'Professional / Specialist')},
            {"level": "Senior Level", "title": request.form.get('growth_senior', 'Senior Specialist')},
            {"level": "Lead / Manager", "title": request.form.get('growth_lead', 'Team Lead / Manager')}
        ]

        # Build learning resources structure
        res_titles = request.form.getlist('resource_title')
        res_urls = request.form.getlist('resource_url')
        res_types = request.form.getlist('resource_type')

        learning_resources = []
        for t, u, tp in zip(res_titles, res_urls, res_types):
            if t.strip() and u.strip():
                learning_resources.append({'title': t.strip(), 'url': u.strip(), 'type': tp.strip() or 'Documentation'})

        career = Career(
            name=name,
            category=category,
            description=description,
            is_active=True
        )
        career.required_skills = required_skills
        career.soft_skills = soft_skills
        career.required_education = required_education
        career.interests = interests
        career.work_environment = work_environment
        career.career_growth = growth
        career.learning_resources = learning_resources

        db.session.add(career)
        db.session.commit()

        flash(f'Career "{career.name}" created successfully.', 'success')
        return redirect(url_for('admin.careers'))

    return render_template('admin/career_form.html', categories=categories, career=None)


@admin_bp.route('/careers/edit/<int:career_id>', methods=['GET', 'POST'])
@admin_required
def edit_career(career_id):
    career = Career.query.get_or_404(career_id)
    categories = get_career_categories()

    if request.method == 'POST':
        career.name = request.form.get('name', '').strip()
        career.category = request.form.get('category', '').strip()
        career.description = request.form.get('description', '').strip()

        career.required_skills = [s.strip() for s in request.form.get('required_skills', '').split(',') if s.strip()]
        career.soft_skills = [s.strip() for s in request.form.get('soft_skills', '').split(',') if s.strip()]
        career.required_education = [s.strip() for s in request.form.get('required_education', '').split(',') if s.strip()]
        career.interests = [s.strip() for s in request.form.get('interests', '').split(',') if s.strip()]
        career.work_environment = [s.strip() for s in request.form.get('work_environment', '').split(',') if s.strip()]

        growth = [
            {"level": "Entry Level", "title": request.form.get('growth_entry', 'Junior Specialist')},
            {"level": "Mid Level", "title": request.form.get('growth_mid', 'Professional / Specialist')},
            {"level": "Senior Level", "title": request.form.get('growth_senior', 'Senior Specialist')},
            {"level": "Lead / Manager", "title": request.form.get('growth_lead', 'Team Lead / Manager')}
        ]
        career.career_growth = growth

        res_titles = request.form.getlist('resource_title')
        res_urls = request.form.getlist('resource_url')
        res_types = request.form.getlist('resource_type')

        learning_resources = []
        for t, u, tp in zip(res_titles, res_urls, res_types):
            if t.strip() and u.strip():
                learning_resources.append({'title': t.strip(), 'url': u.strip(), 'type': tp.strip() or 'Documentation'})
        career.learning_resources = learning_resources

        db.session.commit()
        flash(f'Career "{career.name}" updated successfully.', 'success')
        return redirect(url_for('admin.careers'))

    return render_template('admin/career_form.html', categories=categories, career=career)


@admin_bp.route('/careers/toggle/<int:career_id>', methods=['POST'])
@admin_required
def toggle_career(career_id):
    career = Career.query.get_or_404(career_id)
    career.is_active = not career.is_active
    db.session.commit()
    status_str = 'activated' if career.is_active else 'deactivated'
    flash(f'Career "{career.name}" has been {status_str}.', 'info')
    return redirect(url_for('admin.careers'))


@admin_bp.route('/users')
@admin_required
def users():
    users_list = User.query.order_by(User.created_at.desc()).all()
    user_data = []

    for u in users_list:
        p_comp = u.profile.profile_completion if u.profile else 0
        saved_count = SavedCareer.query.filter_by(user_id=u.id).count()
        user_data.append({
            'user': u,
            'completion': p_comp,
            'saved_count': saved_count
        })

    return render_template('admin/users.html', user_data=user_data)


@admin_bp.route('/analytics')
@admin_required
def analytics():
    stats = get_admin_analytics_data()
    return render_template('admin/analytics.html', stats=stats)
