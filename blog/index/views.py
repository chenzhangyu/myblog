from flask import Blueprint, render_template, redirect, request, url_for
from flask import session
from datetime import timedelta
from ..app import db
from ..db.users import Users
from ..weibo import get_client
import functools


def _get_referer():
    return session['Referer'] if 'Referer' in session else url_for('.index')


index_module = Blueprint('index_module', __name__,
        template_folder='templates', static_folder='static')


@index_module.route('/')
@index_module.route('/index/')
def index():
    return render_template('index/index.html')

@index_module.route('/categories/')
def categories():
    return render_template('index/categories.html')


@index_module.route('/passage/')
def passage():
    return render_template('index/passage.html')


@index_module.route('/login/')
def login():
    session['Referer'] = request.headers.get('Referer')
    # client = _construct_client()
    client = get_client()
    url = client.get_authorize_url()
    return redirect(url)


@index_module.route('/logout/')
def logout():
    if not 'uid' in session:
        return redirect(url_for('.index'))
    else:
        session.clear()
        return redirect(request.headers.get('Referer'))


@index_module.route('/response/login')
def test_for_login():
    if request.args.get('error') == 'access_denied':
        redirect_uri = _get_referer()
        session.pop('Referer')
        return redirect(redirect_uri)
    code = request.args.get('code')
    print code
    # client = _construct_client()
    client = get_client()
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client.set_access_token(access_token, expires_in)
    print 'uid is', r.uid
    session.permanent = True
    index_module.permanent_session_lifetime = timedelta(seconds=r.expires_in)
    session['access_token'] = client.access_token
    session['uid'] = r.uid
    result = client.users.show.get(uid=r.uid)
    session['profile_url'] = result.profile_url
    session['username'] = result.screen_name
    if Users.is_registered(r.uid) == False:
        u_add = Users(uid=r.uid, username=result.screen_name,
                profile_img=result.profile_image_url,
                profile_url=result.profile_url)
        db.session.add(u_add)
        db.session.commit()
        session['id'] = u_add.id
    else:
        u_update = Users.query.filter_by(uid=r.uid).first()
        u_update.username = result.screen_name
        u_update.profile_img = result.profile_image_url
        u_update.profile_url = result.profile_url
        db.session.commit()
        if u_update.is_root:
            session['root'] = True
        session['id'] = u_update.id
    redirect_uri = _get_referer()
    session.pop('Referer')
    return redirect(redirect_uri)
