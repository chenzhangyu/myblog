from . import db
import time

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer)
    is_talk = db.Column(db.Boolean)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(200))
    pubdate = db.Column(db.DateTime)

    def __init__(self, rid, uid, content, is_talk):
        self.rid = rid
        self.is_talk = is_talk
        self.uid = uid
        self.content = content
        self.pubdate = time.strftime('%Y-%m-%d %H:%M:%S')
