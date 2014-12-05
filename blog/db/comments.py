from . import db
import time

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)
    is_warning = db.Column(db.Integer, default=0)
    vote_ups = db.Column(db.Integer, default=0)
    pid = db.Column(db.Integer, 
            db.ForeignKey("passages.id"))
    uid = db.Column(db.Integer,
            db.ForeignKey('users.id'))
    talks = db.relationship('Talks', backref='comment', lazy='dynamic');

    def __init__(self, content, pid, uid):
        self.content = content
        self.pid = pid
        self.uid = uid
        self.pubdate = time.strftime('%Y-%m-%d %H:%M:%S')


    @classmethod
    def get_comment_by_id(cls, cid):
        return cls.query.get(cid)

    @classmethod
    def is_right(cls, cid, pid):
        """
        return True if there is a record of comment 
        corresponding to cid and pid
        """
        c = cls.get_comment_by_id(cid)
        if not c:
            return False
        else:
            return c.pid == pid
