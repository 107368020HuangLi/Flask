from app import db, login
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    Up = db.relationship('Up', backref=db.backref('who', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

class Up(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Down = db.relationship('Down', backref=db.backref('who_time', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.timestamp

class Down(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    downtime = db.Column(db.DateTime, default=datetime.utcnow)
    up_id = db.Column(db.Integer, db.ForeignKey('up.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.downtime