from . import db
from . import Tags
from . import pas_tag
from datetime import datetime

class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime, default=datetime.now)
    last_modified = db.Column(db.DateTime, 
                              default=datetime.now,
                              onupdate=datetime.now)
    visits = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_delete = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=True)
    pas_tag = db.relationship("Tags", 
            secondary=pas_tag, 
            backref=db.backref("passages", lazy="dynamic"), 
            passive_deletes=True)
    # pas_tag = db.relationship('Tags',
    #                           secondary=pas_tag,
    #                           backref='passages',
    #                           lazy='dynamic')
    comments = db.relationship("Comments", backref="passage", 
            lazy="dynamic", passive_deletes=True)

    def __init__(self, title, content, description, init_time=None):
        self.title = title
        self.content = content
        self.description = description
        self.pubdate = init_time


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
        self.is_draft=True
        for t in self.tags:
            self.tags.remove(t)
        return 

    def recycle_passage(self):
        self._set_status_deleted(status=False)
        return

    def update_passage(self, title, content, description):
        self.title = title
        self.content = content
        self.description = description
        return

    @property
    def prev_item(self):
        """
        return previous passage on show
        """
        return self.query.filter(Passages.id > self.id,
                                 Passages.is_draft ==False).first()

    @property
    def next_item(self):
        """
        return next passage on show
        """
        return self.query.filter(Passages.id < self.id,
                                 Passages.is_draft ==False)\
            .order_by(Passages.id.desc()).first()


    @classmethod
    def _is_avaliable(cls, pid):
        return True if cls.query.get(pid) else False

    @classmethod
    def _set_status(cls, id, status):
        if not cls._is_avaliable(id):
            return False
        cls.query.get(id).is_draft = status
        return True

    @classmethod
    def _get_limit_passages(cls, limit=0, offset=0):
        return cls.query.filter_by(is_draft=False)\
            .order_by(cls.pubdate.desc()).offset(offset).limit(limit).all()

    @classmethod
    def is_shown(cls, pid):
        p = cls.get_passage_by_id(pid)
        if p is None or p.is_draft == True:
            return False
        else:
            return True

    @classmethod
    def is_end(cls, pid):
        """
        check if the passage is the oldest passage
        """
        last_passage = cls.query.filter_by(is_draft=False)\
            .order_by(cls.pubdate).first()
        return pid == last_passage.id or last_passage is None

    @classmethod
    def count_display(cls):
        """
        return the sum of passages on show
        """
        return cls.query.filter_by(is_draft=False).count()

    @classmethod
    def count_admin(cls):
        """
        return the sum fo passages for administrator view
        """
        return cls.query.filter_by(is_delete=False).count()

    @classmethod
    def get_passage_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all_passages_for_index(cls, limit=5, offset=0):
        """
        get passages which are not draft for the homepage
        """
        return cls._get_limit_passages(limit=limit, offset=offset)


    @classmethod
    def get_all_passages_for_list(cls, limit=10, offset=0, kind='all'):
        """
        get passages which are not draft for list
        """
        if kind == 'all':
            return cls._get_limit_passages(limit=limit, offset=offset)
        else:
            return Tags.get_passages_for_list(tag=kind)

    @classmethod
    def get_all_passages_exc_deleted(cls, limit=20, offset=0):
        return cls.query.filter_by(is_delete=False)\
            .order_by(cls.last_modified.desc()).offset(offset)\
            .limit(limit).all()

    @classmethod
    def get_all_passages_deleted(cls):
        return cls.query.filter_by(is_delete=True).order_by(cls.pubdate).all()

    @classmethod
    def display(cls, id):
        return cls._set_status(id=id, status=False)

    @classmethod
    def rollback(cls, id):
        return cls._set_status(id=id, status=True)
