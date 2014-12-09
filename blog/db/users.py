from . import db
import time

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sina_uid = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(30), unique=True)
    profile_img = db.Column(db.String(80))
    profile_url = db.Column(db.String(100), unique=True)
    registered_time = db.Column(db.DateTime)
    is_root = db.Column(db.Boolean, default=False)
    is_activated = db.Column(db.Boolean, default=False)
    comment = db.relationship('Comments', backref='user',
        lazy='dynamic', passive_deletes=True)
    f_talk = db.relationship('Talks', foreign_keys='Talks.f_uid', 
                             backref='f_user', lazy='dynamic')
    t_talk = db.relationship('Talks', foreign_keys='Talks.t_uid', 
                             backref='t_user', lazy='dynamic')

    def __init__(self, sina_uid, username, img, url):
        self.sina_uid = sina_uid
        self.username = username
        self.profile_img = img
        self.profile_url = url
        self.registered_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def activate(self):
        self.is_activated = True

    @classmethod
    def is_registered(cls, sina_uid):
        return True if cls.query.filter_by(sina_uid=sina_uid).first() \
        else False
