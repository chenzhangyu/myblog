from . import db
from . import pas_tag

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50))
    is_delete = db.Column(db.Boolean, default=False)
    tag_pas = db.relationship("Passages", 
            secondary=pas_tag, 
            backref=db.backref("tags", lazy="dynamic"), 
            passive_deletes=True)

    @classmethod
    def get_avaliable_tag(cls, name):
        return cls.query.filter_by(tag=name, is_delete=False).first()

    @classmethod
    def is_avaliable(cls, name):
        """
        return True if 'name' is registered and is not deleted
        """
        return True if cls.query.filter_by(tag=name, is_delete=False).\
                first() else False

    @classmethod
    def is_registered(cls, name):
        """
        return True if 'name' is in table 'tags'
        """
        return True if cls.query.filter_by(tag=name).first() else False

    @classmethod
    def del_tag(cls, *tag_list):
        for tag in tag_list:
            assert cls.is_avaliable(tag), \
                    "attempt to delete a invalid tag :%r" % tag
            t = cls.get_avaliable_tag(tag)
            t.is_delete = True
            for p in t.passages:
                t.tag_pas.remove(p)

    @classmethod
    def update_tag(cls, origin, newTag):
        if cls.is_avaliable(newTag):
            return False
        else:
            cls.get_avaliable_tag(origin).tag = newTag
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
