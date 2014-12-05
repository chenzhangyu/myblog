from . import db
import time

class Talks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)
    is_warning = db.Column(db.Integer, default=0)
    vote_ups = db.Column(db.Integer, default=0)
    pid = db.Column(db.Integer, db.ForeignKey("passages.id"))
    cid = db.Column(db.Integer, db.ForeignKey('comments.id'))
    f_uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    t_uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, pid, cid, f_uid, t_uid):
        self.content = content
        self.pid = pid
        self.cid = cid
        self.f_uid = f_uid
        self.t_uid = t_uid
        self.pubdate = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_talk_by_id(cls, tid):
        return cls.query.get(tid)

    @classmethod
    def is_right(cls, tid, cid, pid):
        t = cls.get_talk_by_id(tid)
        if not t:
            return False
        return t.pid == pid and t.cid == cid
