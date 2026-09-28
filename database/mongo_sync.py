import os
import logging
from sqlalchemy import event
from database.mongo_client import get_mongo_db

logger = logging.getLogger('mongo_sync')

def model_to_mongo_dict(obj):
    """Convert a SQLAlchemy model instance into a clean dictionary for MongoDB."""
    model_name = obj.__class__.__name__
    
    if model_name == 'User':
        return {
            "_id": obj.id,
            "id": obj.id,
            "name": obj.name,
            "email": obj.email,
            "password_hash": obj.password_hash,
            "role": obj.role,
            "created_at": obj.created_at
        }
    elif model_name == 'Profile':
        return {
            "_id": obj.id,
            "id": obj.id,
            "user_id": obj.user_id,
            "qualification": obj.qualification,
            "degree": obj.degree,
            "field_of_study": obj.field_of_study,
            "graduation_year": obj.graduation_year,
            "work_environment": obj.work_environment,
            "career_goal": obj.career_goal,
            "personality_scores": obj.get_personality() if hasattr(obj, 'get_personality') else {},
            "profile_completion": obj.profile_completion,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }
    elif model_name == 'Career':
        return {
            "_id": obj.id,
            "id": obj.id,
            "name": obj.name,
            "category": obj.category,
            "description": obj.description,
            "required_education": obj.required_education if hasattr(obj, 'required_education') else [],
            "required_skills": obj.required_skills if hasattr(obj, 'required_skills') else [],
            "soft_skills": obj.soft_skills if hasattr(obj, 'soft_skills') else [],
            "interests": obj.interests if hasattr(obj, 'interests') else [],
            "work_environment": obj.work_environment if hasattr(obj, 'work_environment') else [],
            "career_growth": obj.career_growth if hasattr(obj, 'career_growth') else [],
            "learning_resources": obj.learning_resources if hasattr(obj, 'learning_resources') else [],
            "is_active": obj.is_active,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }
    elif model_name == 'Skill':
        return {
            "_id": obj.id,
            "id": obj.id,
            "name": obj.name,
            "category": obj.category
        }
    elif model_name == 'Interest':
        return {
            "_id": obj.id,
            "id": obj.id,
            "name": obj.name
        }
    elif model_name == 'UserSkill':
        return {
            "_id": obj.id,
            "id": obj.id,
            "user_id": obj.user_id,
            "skill_id": obj.skill_id,
            "proficiency": obj.proficiency
        }
    elif model_name == 'UserInterest':
        return {
            "_id": obj.id,
            "id": obj.id,
            "user_id": obj.user_id,
            "interest_id": obj.interest_id
        }
    elif model_name == 'SavedCareer':
        return {
            "_id": obj.id,
            "id": obj.id,
            "user_id": obj.user_id,
            "career_id": obj.career_id,
            "created_at": obj.created_at
        }
    elif model_name == 'Recommendation':
        return {
            "_id": obj.id,
            "id": obj.id,
            "user_id": obj.user_id,
            "career_id": obj.career_id,
            "match_score": obj.match_score,
            "match_reasons": obj.match_reasons if hasattr(obj, 'match_reasons') else [],
            "created_at": obj.created_at
        }
    return None

def get_collection_name(model_name):
    mapping = {
        'User': 'users',
        'Profile': 'profiles',
        'Career': 'careers',
        'Skill': 'skills',
        'Interest': 'interests',
        'UserSkill': 'user_skills',
        'UserInterest': 'user_interests',
        'SavedCareer': 'saved_careers',
        'Recommendation': 'recommendations'
    }
    return mapping.get(model_name)

def init_mongo_sync(db_sqlalchemy):
    """Register SQLAlchemy session event listeners to automatically sync all DB writes to MongoDB."""
    
    @event.listens_for(db_sqlalchemy.session, 'before_commit')
    def before_commit(session):
        mongo_db = get_mongo_db()
        if mongo_db is None:
            return

        try:
            # Flush changes to assign auto-increment IDs for new objects before serializing
            session.flush()
        except Exception as e:
            logger.warning(f"Error during session.flush in before_commit: {e}")
            return

        to_sync = []
        for obj in list(session.new) + list(session.dirty):
            coll_name = get_collection_name(obj.__class__.__name__)
            if coll_name:
                try:
                    doc = model_to_mongo_dict(obj)
                    if doc and doc.get("_id"):
                        to_sync.append((coll_name, doc["_id"], doc))
                except Exception as e:
                    logger.warning(f"Error converting {obj.__class__.__name__} for Mongo sync: {e}")

        to_delete = []
        for obj in session.deleted:
            coll_name = get_collection_name(obj.__class__.__name__)
            if coll_name and hasattr(obj, 'id') and obj.id:
                to_delete.append((coll_name, obj.id))

        session.info['mongo_sync_pending'] = (to_sync, to_delete)

    @event.listens_for(db_sqlalchemy.session, 'after_commit')
    def after_commit(session):
        mongo_db = get_mongo_db()
        if mongo_db is None:
            return

        pending = session.info.pop('mongo_sync_pending', None)
        if not pending:
            return

        to_sync, to_delete = pending

        for coll_name, doc_id, doc in to_sync:
            try:
                mongo_db[coll_name].replace_one({"_id": doc_id}, doc, upsert=True)
            except Exception as e:
                logger.warning(f"Error syncing {coll_name} to MongoDB: {e}")

        for coll_name, doc_id in to_delete:
            try:
                mongo_db[coll_name].delete_one({"_id": doc_id})
            except Exception as e:
                logger.warning(f"Error deleting {coll_name} from MongoDB: {e}")

def sync_all_existing_data(app, db_sqlalchemy):
    """Sync all existing SQL database data into MongoDB Atlas on startup."""
    with app.app_context():
        mongo_db = get_mongo_db()
        if mongo_db is None:
            return

        from models.user import User
        from models.profile import Profile, Skill, Interest, UserSkill, UserInterest
        from models.career import Career, SavedCareer
        from models.recommendation import Recommendation

        models_list = [
            (User, 'users'),
            (Profile, 'profiles'),
            (Career, 'careers'),
            (Skill, 'skills'),
            (Interest, 'interests'),
            (UserSkill, 'user_skills'),
            (UserInterest, 'user_interests'),
            (SavedCareer, 'saved_careers'),
            (Recommendation, 'recommendations')
        ]

        for model_cls, coll_name in models_list:
            try:
                records = model_cls.query.all()
                for rec in records:
                    doc = model_to_mongo_dict(rec)
                    if doc and rec.id:
                        mongo_db[coll_name].replace_one({"_id": rec.id}, doc, upsert=True)
            except Exception as e:
                logger.warning(f"Failed to initial sync {coll_name} to MongoDB: {e}")
