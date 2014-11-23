from .. import db

_tag = db.Tags()

class Tags(db.Tags):
    """A wrapper class for oprations on table tags"""

    @staticmethod
    def is_registered(name):
        return True if _tag.query.filter_by(tag=name).first() else False

    @staticmethod
    def del_tag(tag_list):
        for tag in tag_list:
            t = _tag.query.filter_by(tag=tag).first()
            t.is_delete = True
        return
