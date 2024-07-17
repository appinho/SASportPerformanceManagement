# Define database models using SQLAlchemy

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sport(db.Model):
    __tablename__ = 'sports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Sport {self.name}>'

class VO2Max(db.Model):
    __tablename__ = 'vo2max'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    sport = db.relationship('Sport', backref=db.backref('vo2max_entries', lazy=True))
    
    def __repr__(self):
        return f'<VO2Max {self.date} - {self.value}>'
