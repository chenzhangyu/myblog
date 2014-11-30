from . import db

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_to = db.Column(db.Integer)
    is_talk = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
