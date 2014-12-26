# -*-coding:utf-8-*-

from flask import Blueprint, render_template, redirect, request, url_for
from flask import session, abort, jsonify, flash
from itsdangerous import URLSafeSerializer, BadSignature
from datetime import timedelta
from ..db import db, Users, Details, Passages, Comments, Friends
from ..db import Tags, Talks, Votes, Reports
from ..db.pagination import Pagination
from ..weibo import get_client
from ..config import info as site_info
from ..mail import send_mail
import functools
import math
import time
import functools

def _get_referer():
    return session['Referer'] if 'Referer' in session else url_for('.index')

def _get_config():
    temp = {'title': site_info['site']['name'],
            'summary': site_info['site']['summary'],
            'kwywords': site_info['site']['keywords']}
    config_in_db = Details.get_info()
    for key in config_in_db:
        temp[key] = config_in_db[key]
    return {'info': temp,
            'friends':Friends.get_all_friends_exc_deleted()}

def _test_for_int(value):
    try:
        result = int(value)
        return False if result < 0 else True
    except ValueError:
        return False

def _config_for_reply():
    """
    check the post data about comment info
    return True if reliable
    """
    if 'cid' not in request.form or \
            not _test_for_int(request.form['cid']):
        return False
    return True

def _config_for_talk():
    """
    check the post data about talk info
    return True if reliable
    """
    if 'tid' not in request.form or \
            not _test_for_int(request.form['tid']):
        return False
    return True

def online_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if 'id' not in session:
            return redirect(url_for('index_module.index'))
        return func(*args, **kw)
    return wrapper

def get_serializer():
    return URLSafeSerializer(r'\xf72.3\xd9\xe6t\xf8\xd9\\\x90\xf1\x9di\x9e\x90\xb7\xe4"\x12Q\x9d\nB')

def get_activation_link(user):
    s = get_serializer()
    payload = s.dumps(user.id)
    return url_for('.activate', payload=payload, _external=True)

def send_reply_mail(user, url):
    assert user.is_activated
    sitename = site_info['site']['name']
    content = ('You have new messages in ' + sitename + ' \n'
               'For more details, click the following link\n\n' + url)
    send_mail(user.email, 'new messages in ' + sitename, content)
    return


index_module = Blueprint('index_module', __name__,
        template_folder='templates', static_folder='static')


@index_module.route('/')
@index_module.route('/index')
def index():
    if 'page' not in request.args or \
            not _test_for_int(request.args.get('page')):
        page = 0
    else:
        page = int(request.args.get('page'))
    ps = Passages.get_all_passages_for_index(offset=page*5)
    # when page not found
    if len(ps) == 0 and page != 0:
        abort(404)
    else:
        has_next = False if not page and not len(ps) or \
            Passages.is_end(ps[len(ps)-1].id) else True
        has_previous = True if page else False
    page_info = {'page': page,
                 'has_previous': has_previous, 
                 'has_next': has_next}
    return render_template('index/index.html', 
                           my_site_config=_get_config(), 
                           passages=ps,
                           page=page_info)


@index_module.route('/archive/', defaults={'page':1})
@index_module.route('/archive/<int:page>')
def archive(page):
    limit = 10
    ps = Passages.get_all_passages_for_list(limit=limit,
                                            offset=(page-1)*limit,
                                            kind='all')
    count = Passages.count_display()
    if not ps and page != 1:
        abort(404)
    pagination = Pagination(page, limit, count)
    return render_template('index/categories.html', 
                           my_site_config=_get_config(),
                           passages=ps,
                           pagination=pagination)


@index_module.route('/categories/<kind>/')
def categories(kind):
    if not Tags.is_avaliable(kind):
        abort(404)
    ps = Passages.get_all_passages_for_list(kind=kind)
    return render_template('index/categories.html', 
                           my_site_config=_get_config(),
                           passages=ps,
                           kind=kind)


@index_module.route('/passage')
def passage():
    if 'pid' not in request.args or \
            not _test_for_int(request.args.get('pid')):
        abort(404)

    p = Passages.get_passage_by_id(request.args.get('pid'))
    if not p or p.is_draft == True:
        abort(404)
    nav = {'prev': p.prev_item, 'next': p.next_item}
    return render_template('index/passage.html', 
                           my_site_config=_get_config(),
                           passage=p,
                           nav=nav)

@index_module.route('/about')
def about():
    return render_template('index/about.html',
                           my_site_config=_get_config())

@index_module.route('/comment', methods=['POST'])
@online_session
def comment():
    if 'pid' not in request.form or \
            'comment' not in request.form or \
            not request.form['comment'] or \
            not Passages.is_shown(request.form['pid']):
        abort(404)
    c = Comments(content=request.form['comment'],
                 pid=request.form['pid'],
                 uid=session['id'])
    db.session.add(c)
    db.session.commit()
    root = Users.query.get(1)
    if site_info['email']['engine'] == 'on' and root.is_activated:
        url = 'http://' + site_info['site']['url'] + url_for('.passage') + \
            '?pid=' + str(request.form['pid'])
        send_reply_mail(root, url)
    return jsonify(status=True)


@index_module.route('/reply', methods=['POST'])
@online_session
def reply():
    if 'content' not in request.form or \
            not request.form['content'] or \
            not _config_for_reply():
        return jsonify(status=False)
    c = Comments.get_comment_by_id(request.form['cid'])
    if not c:
        return jsonify(status=False)
    db.session.add(Talks(request.form['content'],
                         c.pid,
                         request.form['cid'],
                         session['id'],
                         c.uid))
    db.session.commit()
    if site_info['email']['engine'] == 'on' and c.user.is_activated:
        url = 'http://' + site_info['site']['url'] + url_for('.passage') + \
            '?pid=' + str(c.pid)
        send_reply_mail(c.user, url)
    return jsonify(status=True, refresh=True)


@index_module.route('/talk', methods=['POST'])
@online_session
def talk():
    if 'content' not in request.form or \
            not request.form['content'] or \
            not _config_for_talk():
        return jsonify(status=False)
    t = Talks.get_talk_by_id(request.form['tid'])
    if not t:
        return jsonify(status=False)
    db.session.add(Talks(request.form['content'],
                         t.pid,
                         t.cid,
                         session['id'],
                         t.f_uid))
    db.session.commit()
    if site_info['email']['engine'] == 'on' and t.f_user.is_activated:
        url = 'http://' + site_info['site']['url'] + url_for('.passage') + \
            '?pid=' + str(t.pid)
        send_reply_mail(t.f_user, url)
    return jsonify(status=True, refresh=True)


@index_module.route('/vote', methods=['POST'])
@online_session
def vote():
    if 'mode' not in request.form:
        abort(404)
    if request.form['mode'] == 'reply':
        if not _config_for_reply():
            return jsonify(status=False)
        c = Comments.get_comment_by_id(request.form['cid'])
        if not c or c.is_delete:
            return jsonify(status=False)
        v = Votes.get_vote(c.id, session['id'], False)
        if v is not None:
            db.session.delete(v)
            c.vote_ups -= 1
            result = False
        else:
            db.session.add(Votes(c.id, session['id'], False))
            c.vote_ups += 1
            result = True
        db.session.commit()
        return jsonify(status=True, result=result)
    elif request.form['mode'] == 'talk':
        if not _config_for_talk():
            return jsonify(status=False)
        t = Talks.get_talk_by_id(request.form['tid'])
        if not t or t.is_delete:
            return jsonify(status=False)
        v = Votes.get_vote(t.id, session['id'], True)
        if v is not None:
            db.session.delete(v)
            t.vote_ups -= 1
            result = False
        else:
            db.session.add(Votes(t.id, session['id'], True))
            t.vote_ups += 1
            result = True
        db.session.commit()
        return jsonify(status=True, result=result)
    else:
        return jsonify(status=False)


@index_module.route('/report_reply', methods=['POST'])
@index_module.route('/report_talk', methods=['POST'])
@online_session
def report():
    if 'mode' not in request.form or \
            'content' not in request.form or \
            not request.form['content']:
        abort(404)
    if request.form['mode'] == 'report_reply':
        if not _config_for_reply():
            return jsonify(status=False)
        c = Comments.get_comment_by_id(request.form['cid'])
        if not c or c.is_delete:
            return jsonify(status=False)
        db.session.add(Reports(c.id, 
                               session['id'],
                               request.form['content'],
                               False))
        db.session.commit()
    elif request.form['mode'] == 'report_talk':
        if not _config_for_talk():
            return jsonify(status=False)
        t = Talks.get_talk_by_id(request.form['tid'])
        if not t or t.is_delete:
            return jsonify(status=False)
        db.session.add(Reports(t.id,
                               session['id'],
                               request.form['content'],
                               False))
        db.session.commit()
    return jsonify(status=True, refresh=False)


@index_module.route('/get_content', methods=['POST'])
def get_content():
    if 'pid' not in request.form or not _test_for_int(request.form['pid']):
        abort(404)
    p = Passages.get_passage_by_id(request.form['pid'])
    if not p or p.is_draft == True:
        return jsonify(status=False)
    return jsonify(status=True, result=p.content)


@index_module.route('/login/')
def login():
    session['Referer'] = request.headers.get('Referer')
    client = get_client()
    url = client.get_authorize_url()
    return redirect(url)


@index_module.route('/logout/')
def logout():
    if not 'sina_uid' in session:
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
    client = get_client()
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client.set_access_token(access_token, expires_in)
    session.permanent = True
    index_module.permanent_session_lifetime = timedelta(seconds=r.expires_in)
    session['access_token'] = client.access_token
    session['sina_uid'] = r.uid
    result = client.users.show.get(uid=r.uid)
    session['profile_url'] = result.profile_url
    session['username'] = result.screen_name
    if Users.is_registered(r.uid) == False:
        session['input_email'] = True
        u_add = Users(sina_uid=r.uid, 
                      username=result.screen_name,
                      img=result.profile_image_url,
                      url=result.profile_url)
        db.session.add(u_add)
        db.session.commit()
        session['id'] = u_add.id
        return redirect(url_for('.email_input'))
    else:
        u_update = Users.query.filter_by(sina_uid=r.uid).first()
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

@index_module.route('/email')
def email_input():
    if 'input_email' not in session:
        abort(404)
    return render_template('index/email.html')


@index_module.route('/activate/<payload>')
def activate(payload):
    s = get_serializer()
    try:
        uid = s.loads(payload)
    except BadSignature:
        abort(404)
    u = Users.query.get_or_404(uid)
    u.activate()
    db.session.commit()
    flash(u'成功激活邮箱', 'bg-success')
    return redirect(url_for('.index'))


@index_module.route('/add_email', methods=['POST'])
def add_email():
    if 'input_email' not in session:
        abort(404)
    session.pop('input_email')
    if 'address' in request.form and request.form['address']:
        u = Users.query.get_or_404(session['id'])
        u.email = request.form['address']
        db.session.commit()
        sitename = site_info['site']['name']
        url = get_activation_link(u)
        content = ('Please activate your account in ' + sitename + ' by click'
               'the following link.\n'
               'Ignore this email if you are not aware of it\n\n' + url)
        send_mail(request.form['address'], 'activate your account', content)
    redirect_uri = _get_referer()
    if 'Referer' in session:
        session.pop('Referer')
    return redirect(redirect_uri)
