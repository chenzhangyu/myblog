from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

# if  __name__ == '__main':
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://root:chenzhangyu@localhost/test'
# else:
# from blog.config import info
# infoSql = info['SQL']
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#         infoSql['type'] + '://' + infoSql['user'] + ':' + \
#         infoSql['password'] + '@localhost/' + infoSql['database']

app.secret_key = r'\xf72.3\xd9\xe6t\xf8\xd9\\\x90\xf1\x9di\x9e\x90\xb7\xe4"\x12Q\x9d\nB'

db = SQLAlchemy(app)



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(30), unique=True)
    profile_img = db.Column(db.String(80))
    profile_url = db.Column(db.String(100), unique=True)
    is_root = db.Column(db.Boolean, default=False)
    comment = db.relationship('Comments', backref='user',
        lazy='dynamic', passive_deletes=True)
    talk = db.relationship('Talks', backref='user', lazy='dynamic')

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(30), unique=True)
#     password = db.Column(db.String(60))
#     is_root = db.Column(db.Boolean, default=False)
#     is_delete = db.Column(db.Boolean, default=False)
#     is_sina = db.Column(db.Boolean, default=False)
#     comment = db.relationship('Comments', backref='user',
#         lazy='dynamic', passive_deletes=True)
#     talk = db.relationship('Talks', backref='user', lazy='dynamic')
#     sina = db.relationship('Sina', backref='user', uselist=False)


# class Sina(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     uid = db.Column(db.String(30), unique=True)
#     username = db.Column(db.String(80))
#     profile_img = db.Column(db.String(80))
#     profile_url = db.Column(db.String(100), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    


pas_tag = db.Table('pas_tag',
        db.Column('pas_id', db.Integer, 
            db.ForeignKey('passages.id')),
        db.Column('tag_id', db.Integer,
            db.ForeignKey('tags.id'))
        )


class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    visits = db.Column(db.Integer)
    is_draft = db.Column(db.Boolean, default=False)
    pas_tag = db.relationship("Tags", 
            secondary=pas_tag, 
            backref=db.backref("passages", lazy="dynamic"), 
            passive_deletes=True)
    comments = db.relationship("Comments", backref="comments", 
            lazy="dynamic", passive_deletes=True)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)
    is_delete = db.Column(db.Boolean, default=False)


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


class Talks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)
    is_warning = db.Column(db.Integer, default=0)
    to_id = db.Column(db.Integer)
    vote_ups = db.Column(db.Integer, default=0)
    passage_id = db.Column(db.Integer, db.ForeignKey("passages.id"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments_id = db.Column(db.Integer, db.ForeignKey('comments.id'))


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_to = db.Column(db.Integer)
    is_talk = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print 'Congratulations! Databases reconstruction completes!'
