from .. import db

_tag = db.Tags()

class Tags(db.Tags):
    """A wrapper class for oprations on table tags"""

    @staticmethod
    def is_registered(name):
        return True if _tag.query.filter_by(tag=name).first() else False
