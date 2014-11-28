from ..app import db

pas_tag = db.Table('pas_tag',
        db.Column('pas_id', db.Integer, 
            db.ForeignKey('passages.id')),
        db.Column('tag_id', db.Integer,
            db.ForeignKey('tags.id'))
        )
