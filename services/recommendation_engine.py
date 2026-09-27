from models.career import Career
from models.recommendation import Recommendation
from models import db

def calculate_career_match(user, career):
    """
    Calculates transparent compatibility score between a user profile and a career.
    Weights:
    - Technical Skills: 30%
    - Education: 20%
    - Interests: 20%
    - Soft Skills: 10%
    - Work Environment: 10%
    - Personality & Career Goals: 10%
    """
    profile = user.profile
    reasons = []

    # 1. Technical Skills Match (Weight: 30)
    user_tech_skills = {
        s.skill.name.lower().strip() for s in user.skills if s.skill and s.skill.category == 'technical'
    }
    career_req_skills = [s.lower().strip() for s in career.required_skills]
    
    if career_req_skills:
        tech_matched = [s for s in career_req_skills if s in user_tech_skills]
        tech_ratio = len(tech_matched) / len(career_req_skills)
        tech_score = tech_ratio * 30.0
        if tech_matched:
            matched_display = ", ".join([s.title() for s in tech_matched[:4]])
            reasons.append(f"✓ Strong technical skill match ({len(tech_matched)}/{len(career_req_skills)}): {matched_display}")
    else:
        tech_score = 15.0 # baseline neutral score

    # 2. Education Match (Weight: 20)
    edu_score = 0.0
    user_field = (profile.field_of_study or "").lower().strip()
    user_degree = (profile.degree or "").lower().strip()
    user_qual = (profile.qualification or "").lower().strip()

    career_edus = [e.lower().strip() for e in career.required_education]
    edu_match_found = False

    for edu in career_edus:
        if (user_field and user_field in edu) or (user_degree and user_degree in edu) or (user_qual and user_qual in edu) or (edu in user_field) or (edu in user_degree):
            edu_match_found = True
            break

    if edu_match_found:
        edu_score = 20.0
        reasons.append(f"✓ Educational background ({profile.qualification or 'Degree'} in {profile.field_of_study or 'relevant field'}) matches requirements")
    elif user_qual or user_degree:
        edu_score = 10.0 # partial match for having higher education
        reasons.append(f"✓ Relevant academic foundation in {profile.field_of_study or 'related field'}")
    else:
        edu_score = 5.0

    # 3. Interests Match (Weight: 20)
    user_interests = {i.interest.name.lower().strip() for i in user.interests if i.interest}
    career_interests = [i.lower().strip() for i in career.interests]
    
    if career_interests:
        matched_interests = [i for i in career_interests if i in user_interests or any(ui in i for ui in user_interests)]
        interest_ratio = len(matched_interests) / len(career_interests) if len(career_interests) > 0 else 0
        interest_score = min(20.0, interest_ratio * 20.0 + (5.0 if matched_interests else 0.0))
        if matched_interests:
            reasons.append(f"✓ Aligns with your interests: {', '.join([i.title() for i in matched_interests[:3]])}")
    else:
        interest_score = 10.0

    # 4. Soft Skills Match (Weight: 10)
    user_soft_skills = {
        s.skill.name.lower().strip() for s in user.skills if s.skill and s.skill.category == 'soft'
    }
    career_soft_skills = [s.lower().strip() for s in career.soft_skills]

    if career_soft_skills:
        matched_soft = [s for s in career_soft_skills if s in user_soft_skills]
        soft_ratio = len(matched_soft) / len(career_soft_skills)
        soft_score = soft_ratio * 10.0
        if matched_soft:
            reasons.append(f"✓ Possesses key soft skills: {', '.join([s.title() for s in matched_soft[:3]])}")
    else:
        soft_score = 5.0

    # 5. Work Environment Match (Weight: 10)
    user_env = (profile.work_environment or "").lower().strip()
    career_envs = [env.lower().strip() for env in career.work_environment]

    if user_env and any(user_env in env or env in user_env for env in career_envs):
        env_score = 10.0
        reasons.append(f"✓ Preferred work environment ({profile.work_environment}) is available for this role")
    elif user_env:
        env_score = 5.0
    else:
        env_score = 5.0

    # 6. Personality & Goals Match (Weight: 10)
    personality = profile.get_personality()
    goal = (profile.career_goal or "").lower().strip()
    
    personality_score = 5.0
    if personality:
        # Evaluate technical problem solving preference vs career category
        if career.category.lower() in ['software', 'data', 'ai', 'cybersecurity', 'cloud', 'networking']:
            if personality.get('tech_solving') in ['Strongly Agree', 'Agree']:
                personality_score += 2.5
                reasons.append("✓ Work preference indicates strong affinity for technical problem solving")
        
        if personality.get('teamwork') in ['Strongly Agree', 'Agree']:
            personality_score += 2.5

    if goal:
        if 'salary' in goal or 'growth' in goal or 'leadership' in goal:
            personality_score = min(10.0, personality_score + 2.5)

    final_score = round(tech_score + edu_score + interest_score + soft_score + env_score + personality_score, 1)
    final_score = min(100.0, max(0.0, final_score))

    if not reasons:
        reasons.append("Found general baseline profile compatibility")

    return final_score, reasons


def generate_recommendations_for_user(user):
    """
    Generates and persists career recommendation scores for all active careers.
    """
    if not user or not user.profile:
        return []

    # Clear previous recommendations for clean update
    Recommendation.query.filter_by(user_id=user.id).delete()
    
    active_careers = Career.query.filter_by(is_active=True).all()
    recommendations = []

    for career in active_careers:
        score, reasons = calculate_career_match(user, career)
        rec = Recommendation(
            user_id=user.id,
            career_id=career.id,
            match_score=score,
            match_reasons=reasons
        )
        db.session.add(rec)
        recommendations.append(rec)

    db.session.commit()
    
    # Return sorted by match_score descending
    return Recommendation.query.filter_by(user_id=user.id).order_by(Recommendation.match_score.desc()).all()
