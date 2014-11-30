from . import db

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)
    is_warning = db.Column(db.Integer, default=0)
    vote_ups = db.Column(db.Integer, default=0)
    passage_id = db.Column(db.Integer, 
            db.ForeignKey("passages.id"))
    user_id = db.Column(db.Integer,
            db.ForeignKey('users.id'))
    talks = db.relationship('Talks', backref='talks', lazy='dynamic');
