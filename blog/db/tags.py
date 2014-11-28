from ..app import db
from pas_tag import pas_tag

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)
    is_delete = db.Column(db.Boolean, default=False)
    tag_pas = db.relationship("Passages", 
            secondary=pas_tag, 
            backref=db.backref("tags", lazy="dynamic"), 
            passive_deletes=True)

    @classmethod
    def is_registered(cls, name):
        return True if cls.query.filter_by(tag=name).first() else False

    @classmethod
    def del_tag(cls, *tag_list):
        for tag in tag_list:
            assert cls.is_registered(tag), \
                    "attempt to delete a invalid tag :%r" % tag
            t = cls.query.filter_by(tag=tag).first()
            t.is_delete = True
            for p in t.passages:
                t.tag_pas.remove(p)

    @classmethod
    def update_tag(cls, origin, newTag):
        if cls.is_registered(newTag):
            return False
        t = cls.query.filter_by(tag=origin).first()
        t.tag = newTag
        return True

    @classmethod
    def get_all_tags(cls):
        """
        get info of all valid tags of db.Tags
        """
        result = []
        for tag in cls.query.all():
            if tag.is_delete == False:
                result.append({'tag': tag.tag, 'count': tag.passages.count()})
        return result


    @classmethod
    def reuse(cls, tag):
        t = cls.query.filter_by(tag=tag).first()
        assert t, "reuse a not exist tag:%r" % tag
        t.is_delete = False
