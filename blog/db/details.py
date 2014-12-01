from . import db

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    keywords = db.Column(db.String(80))
    summary = db.Column(db.String(50))
    description = db.Column(db.Text)

    @classmethod
    def is_default(cls):
        """
        return True if info is not set in databases
        """
        return False if cls.query.get(1) else True

    @classmethod
    def get_info(cls):
        """
        return info of site if exists else return default info
        """
        info = cls.query.get(1)
        if info is None:
            info = {'title': 'title',
                    'keywords': 'keywords',
                    'summary': 'summary',
                    'description': 'description'}
        return info

    @classmethod
    def update_info(cls, title='title', keywords='keywords', summary='summary',
                    description='description'):
        assert not cls.is_default()
        d = cls.query.get(1)
        d.title = title
        d.keywords = keywords
        d.summary = summary
        d.description = description
        return
