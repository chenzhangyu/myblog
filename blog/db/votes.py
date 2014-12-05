from . import db

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_to = db.Column(db.Integer)
    is_talk = db.Column(db.Boolean, default=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, vote_to, uid, is_talk=True):
        self.vote_to = vote_to
        self.is_talk = is_talk
        self.uid = uid

    @classmethod
    def get_vote(cls, to, uid, is_talk):
        return cls.query.filter_by(vote_to=to, uid=uid, is_talk=is_talk)\
            .first()
