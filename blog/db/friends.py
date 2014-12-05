from . import db

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(40))
    is_delete = db.Column(db.Boolean, default=False)

    def __init__(self, link, description):
        self.link = link
        self.description = description

    @classmethod
    def is_registered_by_name(cls, friend):
        return True if cls.query.filter_by(description=friend,
                                           is_delete=False).first() else False

    @classmethod
    def is_registered_by_id(cls, fid):
        return True if cls.query.get(fid) else False

    @classmethod
    def get_all_friends_exc_deleted(cls):
        return cls.query.filter_by(is_delete=False).all()

    @classmethod
    def update_friend(cls, fid, friend, link):
        assert cls.is_registered_by_id(fid)
        f = cls.query.get(fid)
        f.description = friend
        f.link = link
        return

    @classmethod
    def del_friend(cls, fid):
        assert cls.is_registered_by_id(fid)
        f = cls.query.get(fid)
        f.is_delete = True
        return
