from datetime import datetime
import json
from models import db

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    qualification = db.Column(db.String(100), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    field_of_study = db.Column(db.String(100), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    work_environment = db.Column(db.String(100), nullable=True) # Remote, Office, Hybrid, Startup, MNC, etc.
    career_goal = db.Column(db.String(100), nullable=True) # High salary, Stability, Leadership, etc.
    personality_scores = db.Column(db.Text, nullable=True, default='{}') # JSON string of personality survey answers
    profile_completion = db.Column(db.Integer, default=0) # Percentage 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_personality(self, scores_dict):
        self.personality_scores = json.dumps(scores_dict)

    def get_personality(self):
        try:
            return json.loads(self.personality_scores) if self.personality_scores else {}
        except Exception:
            return {}

    def calculate_completion(self):
        total_steps = 7
        completed = 0
        if self.qualification and self.degree and self.field_of_study:
            completed += 1
        
        # User skills
        if self.user.skills and len(self.user.skills) > 0:
            completed += 1
            
        # Soft skills
        soft_skills_count = sum(1 for s in self.user.skills if s.skill and s.skill.category == 'soft')
        if soft_skills_count > 0:
            completed += 1
            
        # User interests
        if self.user.interests and len(self.user.interests) > 0:
            completed += 1
            
        if self.work_environment:
            completed += 1
            
        if self.career_goal:
            completed += 1
            
        if self.personality_scores and len(self.get_personality()) > 0:
            completed += 1
            
        self.profile_completion = int((completed / total_steps) * 100)
        return self.profile_completion

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False, default='technical') # 'technical' or 'soft'

    def __repr__(self):
        return f'<Skill {self.name} ({self.category})>'

class UserSkill(db.Model):
    __tablename__ = 'user_skills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    proficiency = db.Column(db.String(20), default='Intermediate') # Beginner, Intermediate, Advanced

    skill = db.relationship('Skill')

class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Interest {self.name}>'

class UserInterest(db.Model):
    __tablename__ = 'user_interests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), nullable=False)

    interest = db.relationship('Interest')
