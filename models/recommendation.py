from datetime import datetime
import json
from models import db

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False) # 0.0 - 100.0
    match_reasons_json = db.Column(db.Text, nullable=False, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def match_reasons(self):
        try:
            return json.loads(self.match_reasons_json) if self.match_reasons_json else []
        except Exception:
            return []

    @match_reasons.setter
    def match_reasons(self, val):
        self.match_reasons_json = json.dumps(val if isinstance(val, list) else [])

    @property
    def match_tier(self):
        score = self.match_score
        if score >= 90:
            return "Excellent Match"
        elif score >= 80:
            return "Strong Match"
        elif score >= 70:
            return "Good Match"
        elif score >= 50:
            return "Moderate Match"
        else:
            return "Low Match"

    @property
    def badge_class(self):
        tier = self.match_tier
        if tier == "Excellent Match":
            return "bg-success"
        elif tier == "Strong Match":
            return "bg-primary"
        elif tier == "Good Match":
            return "bg-info text-dark"
        elif tier == "Moderate Match":
            return "bg-warning text-dark"
        else:
            return "bg-secondary"
