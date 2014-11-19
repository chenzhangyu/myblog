from flask import Blueprint, render_template, redirect, request, url_for
from flask import session
from ..database import Users
from ..db import db
from ..weibo import APIClient
import functools


_APP_KEY = '2858452607'
_APP_SECRET = '307003f29a4ed1d6656ed81c01f2db9d'
_CALLBACK_URL = 'http://127.0.0.1:5000/blog/response/login'

admin_module = Blueprint('admin_module', __name__,
        template_folder='templates', static_folder='static')


@admin_module.route('/')
@admin_module.route('/index')
def index():
    return render_template('admin/index.html')
