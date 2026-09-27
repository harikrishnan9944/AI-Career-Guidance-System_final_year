from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes import login_required
from models import db
from models.user import User
from models.profile import Profile, Skill, UserSkill, Interest, UserInterest
from services.recommendation_engine import generate_recommendations_for_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    user = User.query.get(session['user_id'])
    profile = user.profile or Profile(user_id=user.id)

    # Fetch available preset skills & interests for multi-step checkboxes
    all_tech_skills = Skill.query.filter_by(category='technical').all()
    all_soft_skills = Skill.query.filter_by(category='soft').all()
    all_interests = Interest.query.all()

    if request.method == 'POST':
        # Step 1: Education
        profile.qualification = request.form.get('qualification')
        profile.degree = request.form.get('degree')
        profile.field_of_study = request.form.get('field_of_study')
        try:
            profile.graduation_year = int(request.form.get('graduation_year', 0)) if request.form.get('graduation_year') else None
        except ValueError:
            profile.graduation_year = None

        # Step 2: Technical Skills
        selected_tech_skill_ids = request.form.getlist('tech_skills')
        custom_tech_skills = request.form.get('custom_tech_skills', '').split(',')

        # Step 3: Soft Skills
        selected_soft_skill_ids = request.form.getlist('soft_skills')

        # Clear existing user skills
        UserSkill.query.filter_by(user_id=user.id).delete()

        # Add tech skills
        for s_id in selected_tech_skill_ids:
            if s_id.isdigit():
                db.session.add(UserSkill(user_id=user.id, skill_id=int(s_id), proficiency='Intermediate'))

        # Process custom tech skills
        for custom_s in custom_tech_skills:
            c_name = custom_s.strip()
            if c_name:
                existing_s = Skill.query.filter_by(name=c_name).first()
                if not existing_s:
                    existing_s = Skill(name=c_name, category='technical')
                    db.session.add(existing_s)
                    db.session.flush()
                db.session.add(UserSkill(user_id=user.id, skill_id=existing_s.id, proficiency='Intermediate'))

        # Add soft skills
        for s_id in selected_soft_skill_ids:
            if s_id.isdigit():
                db.session.add(UserSkill(user_id=user.id, skill_id=int(s_id), proficiency='Intermediate'))

        # Step 4: Interests
        selected_interest_ids = request.form.getlist('interests')
        UserInterest.query.filter_by(user_id=user.id).delete()
        for i_id in selected_interest_ids:
            if i_id.isdigit():
                db.session.add(UserInterest(user_id=user.id, interest_id=int(i_id)))

        # Step 5: Work Environment
        profile.work_environment = request.form.get('work_environment')

        # Step 6: Career Goal
        profile.career_goal = request.form.get('career_goal')

        # Step 7: Personality / Work Preference Assessment
        personality_dict = {
            'tech_solving': request.form.get('p_tech_solving', 'Neutral'),
            'teamwork': request.form.get('p_teamwork', 'Neutral'),
            'learning': request.form.get('p_learning', 'Neutral'),
            'data_analysis': request.form.get('p_data_analysis', 'Neutral'),
            'creativity': request.form.get('p_creativity', 'Neutral')
        }
        profile.set_personality(personality_dict)

        # Save profile changes
        db.session.add(profile)
        db.session.commit()

        # Recalculate completion percentage
        profile.calculate_completion()
        db.session.commit()

        # Generate recommendations immediately
        generate_recommendations_for_user(user)

        flash('Your career profile has been saved successfully! Check out your recommendations.', 'success')
        return redirect(url_for('career.recommendations'))

    # Get user's current selected skill & interest IDs for pre-checking
    user_skill_ids = [us.skill_id for us in user.skills]
    user_interest_ids = [ui.interest_id for ui in user.interests]
    personality = profile.get_personality()

    return render_template(
        'onboarding.html',
        profile=profile,
        all_tech_skills=all_tech_skills,
        all_soft_skills=all_soft_skills,
        all_interests=all_interests,
        user_skill_ids=user_skill_ids,
        user_interest_ids=user_interest_ids,
        personality=personality
    )
