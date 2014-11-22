from flask import Blueprint, render_template, redirect, request, url_for
from flask import session, abort, jsonify
from ..database import Users, Passages, Tags
from ..db import db
from ..weibo import get_client
import functools


admin_module = Blueprint('admin_module', __name__,
        template_folder='templates', static_folder='static')


def admin_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if 'root' not in session:
            return redirect(url_for('index_module.index'))
        return func(*args, **kw)
    return wrapper


@admin_module.route('/')
@admin_module.route('/index/')
@admin_module.route('/home/')
@admin_session
def index():
    site = {'index': 'active'}
    site['home'] = 'class=active'
    return render_template('admin/index.html', site=site)


@admin_module.route('/dust')
@admin_session
def index_dust():
    site = {'index': 'active'}
    site['dust'] = 'class=active'
    return render_template('admin/dust_passage.html', site=site)
   

@admin_module.route('/tags')
@admin_session
def index_tags():
    site = {'index': 'active'}
    site['tags'] = 'class=active'
    return render_template('admin/tag_list.html', site=site)


@admin_module.route('/edit')
@admin_session
def edit():
    site = {'edit': 'active'}
    if 'passage_id' not in request.args:
        return render_template('admin/edit.html', site=site)


@admin_module.route('/config/')
@admin_session
def config():
    site = {'config': 'active'}
    return render_template('admin/config.html', site=site)


@admin_module.route('/friend/')
@admin_session
def friend():
    site = {'friend': 'active'}
    return render_template('admin/friend.html', site=site)


@admin_module.route('/upload_passage', methods=['POST'])
@admin_session
def upload_passage():
    _infoForPassage = ['title', 'content', 'description']
    assert request.method == 'POST'
    assert request.path == '/admin/upload_passage'
    for need in _infoForPassage:
        print need
        if need not in request.form or not request.form[need]:
            print 'illegal'
            abort(400)
    p = Passages()
    return redirect(url_for('.index'))


@admin_module.route('/add_tag', methods=['POST'])
@admin_session
def add_tag():
    print request.json
    print request.json['tagList']
    if not 'tagList' in request.json or not request.json['tagList']:
        print '>>>self stop'
        abort(400)
    t_list = []
    for item in [x for x in request.json['tagList'] \
            if not Tags.is_registered(x)]:
        print 'item ', item
        t = Tags(tag=item)
        db.session.add(t)
        t_list.append(t)
    db.session.commit()
    result = [{'tid': x.id, 'tag': x.tag} for x in t_list]
    print result
    if t_list:
        return jsonify(status=True, result=result)
    else:
        return jsonify(status=False)


@admin_module.route('/del_tag', methods=['POST'])
@admin_session
def del_tag():
    print request.form['tag']
    return jsonify(status=True)
