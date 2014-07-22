from flask.ext.sqlalchemy import SQLAlchemy
from blog import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:chenzhangyu@localhost/myblog'
app.secret_key = '\xfb\xb6+~\x90P\x8d\xb5\x82N\x90\x8f\xdf\x8b\xc2\xf1\xc1\xa4e\xdd\x1f\xfa\x8a\xe0'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    root = db.Column(db.String(10))
    comment = db.relation('Comments', backref='comment', lazy='dynamic', passive_deletes=True)
    talk = db.relation('Talks', backref='talk', lazy='dynamic', passive_deletes=True)


pata = db.Table('pata',
                db.Column('passage_id', db.Integer, db.ForeignKey('passages.id', ondelete='CASCADE')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE')))


class Passages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    pubdate = db.Column(db.String(80))
    display = db.Column(db.Integer)
    pata = db.relationship('Tags', secondary=pata, backref=db.backref('tags', lazy='dynamic'), passive_deletes=True)
    comments = db.relation('Comments', backref='comments', lazy='dynamic', passive_deletes=True)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('passages.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    content = db.Column(db.String(500))
    pubdate = db.Column(db.String(30))
    display = db.Column(db.Integer)
    talks = db.relation('Talks', backref='talks', lazy='dynamic', passive_deletes=True)


class Talks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    originer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    content = db.Column(db.String(200))
    pubdate = db.Column(db.String(30))
    display = db.Column(db.Integer)