from flask import Flask, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from config import info

infoSql = info['SQL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        infoSql['type'] + '://' + infoSql['user'] + ':' + \
        infoSql['password'] + '@localhost/' + infoSql['database']

app.secret_key = info['site']['key']


from index import index_module
from admin import admin_module

@app.route('/')
def redirect_to_index():
    return redirect(url_for('index_module.index'), code=301)

app.register_blueprint(index_module, url_prefix='/blog')
app.register_blueprint(admin_module, url_prefix='/admin')
