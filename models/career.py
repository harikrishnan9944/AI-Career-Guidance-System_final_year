from datetime import datetime
import json
from models import db

class Career(db.Model):
    __tablename__ = 'careers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False) # Software, Data, AI, Cybersecurity, etc.
    description = db.Column(db.Text, nullable=False)
    
    # Store lists as JSON text
    required_education_json = db.Column(db.Text, nullable=False, default='[]')
    required_skills_json = db.Column(db.Text, nullable=False, default='[]')
    soft_skills_json = db.Column(db.Text, nullable=False, default='[]')
    interests_json = db.Column(db.Text, nullable=False, default='[]')
    work_environment_json = db.Column(db.Text, nullable=False, default='[]')
    career_growth_json = db.Column(db.Text, nullable=False, default='[]') # e.g. [{"level": "Entry", "title": "..."}, ...]
    learning_resources_json = db.Column(db.Text, nullable=False, default='[]') # e.g. [{"title": "MDN JS", "url": "...", "type": "Docs"}, ...]

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recommendations = db.relationship('Recommendation', backref='career', cascade='all, delete-orphan')
    saved_by_users = db.relationship('SavedCareer', backref='career', cascade='all, delete-orphan')

    # Helper getters & setters for JSON fields
    def get_list_property(self, field_name):
        raw = getattr(self, field_name, '[]')
        try:
            return json.loads(raw) if raw else []
        except Exception:
            return []

    def set_list_property(self, field_name, val):
        setattr(self, field_name, json.dumps(val if isinstance(val, list) else []))

    @property
    def required_education(self):
        return self.get_list_property('required_education_json')

    @required_education.setter
    def required_education(self, val):
        self.set_list_property('required_education_json', val)

    @property
    def required_skills(self):
        return self.get_list_property('required_skills_json')

    @required_skills.setter
    def required_skills(self, val):
        self.set_list_property('required_skills_json', val)

    @property
    def soft_skills(self):
        return self.get_list_property('soft_skills_json')

    @soft_skills.setter
    def soft_skills(self, val):
        self.set_list_property('soft_skills_json', val)

    @property
    def interests(self):
        return self.get_list_property('interests_json')

    @interests.setter
    def interests(self, val):
        self.set_list_property('interests_json', val)

    @property
    def work_environment(self):
        return self.get_list_property('work_environment_json')

    @work_environment.setter
    def work_environment(self, val):
        self.set_list_property('work_environment_json', val)

    @property
    def career_growth(self):
        return self.get_list_property('career_growth_json')

    @career_growth.setter
    def career_growth(self, val):
        self.set_list_property('career_growth_json', val)

    @property
    def learning_resources(self):
        return self.get_list_property('learning_resources_json')

    @learning_resources.setter
    def learning_resources(self, val):
        self.set_list_property('learning_resources_json', val)


class SavedCareer(db.Model):
    __tablename__ = 'saved_careers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'career_id', name='_user_career_uc'),)
