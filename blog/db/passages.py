from . import db
from . import Tags
from . import pas_tag

class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    visits = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_delete = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=True)
    pas_tag = db.relationship("Tags", 
            secondary=pas_tag, 
            backref=db.backref("passages", lazy="dynamic"), 
            passive_deletes=True)
    comments = db.relationship("Comments", backref="comments", 
            lazy="dynamic", passive_deletes=True)

    def set_tags(self, tag_list):
        for t in self.tags:
            self.tags.remove(t)
        for t in tag_list:
            self.tags.append(Tags.get_avaliable_tag(t))
        return

    def _set_status_deleted(self, status):
        self.is_delete = status
        return

    def update_tags(self, tag_list):
        return self.set_tags(tag_list)

    def del_passage(self):
        self._set_status_deleted(status=True)
        return 

    def recycle_passage(self):
        self._set_status_deleted(status=False)
        return

    def update_passage(self, title, content, description):
        self.title = title
        self.content = content
        self.description = description
        return


    @classmethod
    def _is_avaliable(cls, id):
        return True if cls.query.get(id) else False

    @classmethod
    def _set_status(cls, id, status):
        if not cls._is_avaliable(id):
            return False
        cls.query.get(id).is_draft = status
        return True

    @classmethod
    def get_passage_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all_passages_exc_deleted(cls):
        return cls.query.filter_by(is_delete=False).order_by(cls.pubdate).all()

    @classmethod
    def get_all_passages_deleted(cls):
        return cls.query.filter_by(is_delete=True).order_by(cls.pubdate).all()

    @classmethod
    def display(cls, id):
        return cls._set_status(id=id, status=False)

    @classmethod
    def rollback(cls, id):
        return cls._set_status(id=id, status=True)
