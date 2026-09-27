from models.career import Career
from models.recommendation import Recommendation
from models.user import User
from models.profile import Profile, UserSkill, UserInterest, Skill, Interest
from models import db
from sqlalchemy import func

def get_career_categories():
    return [
        'Software',
        'Data',
        'AI & ML',
        'Cybersecurity',
        'Cloud & Infrastructure',
        'Networking',
        'Design & UI/UX',
        'Business & Strategy',
        'Finance & Analytics',
        'Digital Marketing',
        'Education & Research'
    ]

def get_admin_analytics_data():
    """
    Computes system statistics for the admin dashboard and analytics charts.
    """
    total_users = User.query.filter_by(role='USER').count()
    completed_profiles = Profile.query.filter(Profile.profile_completion >= 70).count()
    total_careers = Career.query.count()
    total_recommendations = Recommendation.query.count()

    # Most popular recommended career
    popular_rec = db.session.query(
        Career.name, func.count(Recommendation.id).label('rec_count')
    ).join(Recommendation, Recommendation.career_id == Career.id)\
     .group_by(Career.id)\
     .order_by(func.count(Recommendation.id).desc())\
     .first()

    most_popular_career = popular_rec[0] if popular_rec else "N/A"

    # Category distribution
    categories_query = db.session.query(
        Career.category, func.count(Career.id)
    ).group_by(Career.category).all()
    
    cat_labels = [c[0] for c in categories_query]
    cat_counts = [c[1] for c in categories_query]

    # Top recommended careers distribution (top 5)
    top_recs_query = db.session.query(
        Career.name, func.count(Recommendation.id)
    ).join(Recommendation, Recommendation.career_id == Career.id)\
     .group_by(Career.id)\
     .order_by(func.count(Recommendation.id).desc())\
     .limit(5).all()

    rec_labels = [r[0] for r in top_recs_query]
    rec_counts = [r[1] for r in top_recs_query]

    # User Interests distribution (top 6)
    interests_query = db.session.query(
        Interest.name, func.count(UserInterest.id)
    ).join(UserInterest, UserInterest.interest_id == Interest.id)\
     .group_by(Interest.id)\
     .order_by(func.count(UserInterest.id).desc())\
     .limit(6).all()

    interest_labels = [i[0] for i in interests_query]
    interest_counts = [i[1] for i in interests_query]

    # User Skills distribution (top 6)
    skills_query = db.session.query(
        Skill.name, func.count(UserSkill.id)
    ).join(UserSkill, UserSkill.skill_id == Skill.id)\
     .group_by(Skill.id)\
     .order_by(func.count(UserSkill.id).desc())\
     .limit(6).all()

    skill_labels = [s[0] for s in skills_query]
    skill_counts = [s[1] for s in skills_query]

    # Education Distribution
    edu_query = db.session.query(
        Profile.qualification, func.count(Profile.id)
    ).filter(Profile.qualification.isnot(None))\
     .group_by(Profile.qualification).all()

    edu_labels = [e[0] if e[0] else 'Unspecified' for e in edu_query]
    edu_counts = [e[1] for e in edu_query]

    return {
        'total_users': total_users,
        'completed_profiles': completed_profiles,
        'total_careers': total_careers,
        'total_recommendations': total_recommendations,
        'most_popular_career': most_popular_career,
        'categories_data': {'labels': cat_labels, 'counts': cat_counts},
        'top_recs_data': {'labels': rec_labels, 'counts': rec_counts},
        'interests_data': {'labels': interest_labels, 'counts': interest_counts},
        'skills_data': {'labels': skill_labels, 'counts': skill_counts},
        'edu_data': {'labels': edu_labels, 'counts': edu_counts}
    }
