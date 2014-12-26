from . import db
from datetime import datetime

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    pubdate = db.Column(db.DateTime, 
                        default=datetime.now, 
                        onupdate=datetime.now)

    def __init__(self, description):
        self.description = description

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
            config = {'description': 'description',
                      'pubdate': datetime.now()}
        else:
            config = {'description': info.description,
                      'pubdate': info.pubdate}
        return config

    @classmethod
    def update_info(cls, description='description'):
        assert not cls.is_default()
        d = cls.query.get(1)
        d.description = description
        return
