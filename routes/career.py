from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes import login_required
from models import db
from models.user import User
from models.profile import Profile
from models.career import Career, SavedCareer
from models.recommendation import Recommendation
from services.recommendation_engine import generate_recommendations_for_user
from services.skill_analysis import analyze_skill_gap
from services.career_data import get_career_categories

career_bp = Blueprint('career', __name__)

@career_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    profile = user.profile or Profile(user_id=user.id)
    completion = profile.calculate_completion()

    # Recommendations
    recommendations = Recommendation.query.filter_by(user_id=user.id).order_by(Recommendation.match_score.desc()).all()
    
    # If no recommendations yet and profile has data, generate them
    if not recommendations and completion > 30:
        recommendations = generate_recommendations_for_user(user)

    top_match = recommendations[0] if recommendations else None
    top_matches = recommendations[:3]

    # Saved careers
    saved_careers = SavedCareer.query.filter_by(user_id=user.id).all()

    return render_template(
        'dashboard.html',
        user=user,
        profile=profile,
        completion=completion,
        top_match=top_match,
        top_matches=top_matches,
        saved_careers=saved_careers,
        total_recommendations=len(recommendations)
    )


@career_bp.route('/recommendations')
@login_required
def recommendations():
    user = User.query.get(session['user_id'])
    
    # Refresh or generate recommendations
    recommendations_list = Recommendation.query.filter_by(user_id=user.id).order_by(Recommendation.match_score.desc()).all()
    
    if not recommendations_list:
        recommendations_list = generate_recommendations_for_user(user)

    saved_career_ids = {sc.career_id for sc in SavedCareer.query.filter_by(user_id=user.id).all()}

    return render_template(
        'recommendations.html',
        user=user,
        recommendations=recommendations_list,
        saved_career_ids=saved_career_ids
    )


@career_bp.route('/career/<int:career_id>')
@login_required
def career_details(career_id):
    career = Career.query.get_or_404(career_id)
    user = User.query.get(session['user_id'])
    
    rec = Recommendation.query.filter_by(user_id=user.id, career_id=career.id).first()
    match_score = rec.match_score if rec else None
    
    skill_gap = analyze_skill_gap(user, career)
    is_saved = SavedCareer.query.filter_by(user_id=user.id, career_id=career.id).first() is not None

    # Find related roles in the same category
    related_roles = Career.query.filter(
        Career.category == career.category,
        Career.id != career.id,
        Career.is_active == True
    ).limit(3).all()

    return render_template(
        'career_details.html',
        career=career,
        match_score=match_score,
        rec=rec,
        skill_gap=skill_gap,
        is_saved=is_saved,
        related_roles=related_roles
    )


@career_bp.route('/career/<int:career_id>/skill-gap')
@login_required
def skill_gap(career_id):
    career = Career.query.get_or_404(career_id)
    user = User.query.get(session['user_id'])
    skill_gap_data = analyze_skill_gap(user, career)

    return render_template(
        'skill_gap.html',
        career=career,
        skill_gap=skill_gap_data
    )


@career_bp.route('/career/<int:career_id>/roadmap')
@login_required
def learning_path(career_id):
    career = Career.query.get_or_404(career_id)
    user = User.query.get(session['user_id'])
    skill_gap_data = analyze_skill_gap(user, career)

    # Build roadmap steps based on required skills & skill gap
    user_skills_lower = {s.skill.name.lower().strip() for s in user.skills if s.skill}
    
    roadmap_steps = []
    step_num = 1
    for skill in career.required_skills:
        is_completed = skill.lower().strip() in user_skills_lower
        roadmap_steps.append({
            'step': step_num,
            'title': skill,
            'status': 'Completed' if is_completed else ('Start Learning' if step_num == len(skill_gap_data['acquired_tech']) + 1 else 'Upcoming'),
            'badge_class': 'success' if is_completed else ('primary' if step_num == len(skill_gap_data['acquired_tech']) + 1 else 'secondary'),
            'is_completed': is_completed
        })
        step_num += 1

    return render_template(
        'learning_path.html',
        career=career,
        roadmap_steps=roadmap_steps,
        skill_gap=skill_gap_data,
        resources=career.learning_resources
    )


@career_bp.route('/explore')
def explore():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    query = Career.query.filter_by(is_active=True)

    if search_query:
        query = query.filter(Career.name.ilike(f'%{search_query}%') | Career.description.ilike(f'%{search_query}%'))

    if category_filter and category_filter != 'All':
        query = query.filter(Career.category == category_filter)

    careers = query.all()
    categories = get_career_categories()

    user_saved_ids = set()
    if 'user_id' in session:
        user_saved_ids = {sc.career_id for sc in SavedCareer.query.filter_by(user_id=session['user_id']).all()}

    return render_template(
        'explore.html',
        careers=careers,
        categories=categories,
        search_query=search_query,
        selected_category=category_filter,
        user_saved_ids=user_saved_ids
    )


@career_bp.route('/save-career/<int:career_id>', methods=['POST'])
@login_required
def save_career(career_id):
    career = Career.query.get_or_404(career_id)
    user_id = session['user_id']

    existing = SavedCareer.query.filter_by(user_id=user_id, career_id=career.id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f'Removed "{career.name}" from your saved careers.', 'info')
    else:
        new_save = SavedCareer(user_id=user_id, career_id=career.id)
        db.session.add(new_save)
        db.session.commit()
        flash(f'Saved "{career.name}" to your profile bookmarks!', 'success')

    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('career.saved_careers'))


@career_bp.route('/saved-careers')
@login_required
def saved_careers():
    user = User.query.get(session['user_id'])
    saved_items = SavedCareer.query.filter_by(user_id=user.id).order_by(SavedCareer.created_at.desc()).all()

    # Recommendations for match scores
    recs_map = {r.career_id: r.match_score for r in Recommendation.query.filter_by(user_id=user.id).all()}

    return render_template(
        'saved_careers.html',
        saved_items=saved_items,
        recs_map=recs_map
    )


@career_bp.route('/compare')
@login_required
def compare():
    c1_id = request.args.get('c1', type=int)
    c2_id = request.args.get('c2', type=int)
    c3_id = request.args.get('c3', type=int)

    selected_ids = [cid for cid in [c1_id, c2_id, c3_id] if cid]

    careers_to_compare = []
    comparison_data = []

    user = User.query.get(session['user_id'])

    all_careers = Career.query.filter_by(is_active=True).order_by(Career.name).all()

    for cid in selected_ids:
        career = Career.query.get(cid)
        if career:
            careers_to_compare.append(career)
            rec = Recommendation.query.filter_by(user_id=user.id, career_id=career.id).first()
            gap = analyze_skill_gap(user, career)
            comparison_data.append({
                'career': career,
                'match_score': rec.match_score if rec else 'N/A',
                'skill_match_pct': gap['skill_match_pct'],
                'acquired_count': len(gap['acquired_tech']),
                'missing_count': len(gap['missing_tech']),
                'growth': career.career_growth
            })

    return render_template(
        'compare.html',
        all_careers=all_careers,
        selected_ids=selected_ids,
        comparison_data=comparison_data
    )
