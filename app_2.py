from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use Sqlite3 as database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# Suppresses warnings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# db.init_app(app)


class Vo2max(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    modified = db.Column(db.Date, nullable=False, default=datetime.utcnow)
