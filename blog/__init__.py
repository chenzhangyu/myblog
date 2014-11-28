# from flask import Flask
# from blog.config import info
# from blog.index import index_module
# from blog.admin import admin_module
# # from blog.db import app

# # infoSql = info['SQL']
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#         infoSql['type'] + '://' + infoSql['user'] + ':' + \
#         infoSql['password'] + '@localhost/' + infoSql['database']


# app.register_blueprint(index_module, url_prefix='/blog')
# app.register_blueprint(admin_module, url_prefix='/admin')

# #import blog.db
# from app import app
