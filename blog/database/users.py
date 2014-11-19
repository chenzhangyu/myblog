from .. import db

_user = db.Users()

class Users(db.Users):
    """A wrapper class for query data from table users"""

    @staticmethod
    def is_registered(uid):
        return True if _user.query.filter_by(uid=uid).first() else False
