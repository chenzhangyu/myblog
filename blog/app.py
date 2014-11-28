from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import info

infoSql = info['SQL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        infoSql['type'] + '://' + infoSql['user'] + ':' + \
        infoSql['password'] + '@localhost/' + infoSql['database']

app.secret_key = r'\xf72.3\xd9\xe6t\xf8\xd9\\\x90\xf1\x9di\x9e\x90\xb7\xe4"\x12Q\x9d\nB'

db = SQLAlchemy(app)

from index import index_module
from admin import admin_module

app.register_blueprint(index_module, url_prefix='/blog')
app.register_blueprint(admin_module, url_prefix='/admin')
