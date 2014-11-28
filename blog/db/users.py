from ..app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(30), unique=True)
    profile_img = db.Column(db.String(80))
    profile_url = db.Column(db.String(100), unique=True)
    is_root = db.Column(db.Boolean, default=False)
    comment = db.relationship('Comments', backref='user',
        lazy='dynamic', passive_deletes=True)
    talk = db.relationship('Talks', backref='user', lazy='dynamic')

    @classmethod
    def is_registered(cls, uid):
        return True if cls.query.filter_by(uid=uid).first() else False
