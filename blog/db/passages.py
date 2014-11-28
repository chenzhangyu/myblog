from ..app import db
from pas_tag import pas_tag

class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    visits = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_draft = db.Column(db.Boolean, default=True)
    pas_tag = db.relationship("Tags", 
            secondary=pas_tag, 
            backref=db.backref("passages", lazy="dynamic"), 
            passive_deletes=True)
    comments = db.relationship("Comments", backref="comments", 
            lazy="dynamic", passive_deletes=True)
