from flask import Blueprint, render_template, redirect, request, url_for
from flask import session, abort, jsonify
from ..app import db
from ..db.users import Users
from ..db.passages import Passages
from ..db.tags import Tags
from ..weibo import get_client
import functools, time


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
    tag_list = Tags.get_all_tags()
    return render_template('admin/tag_list.html', site=site, tags = tag_list)


@admin_module.route('/edit')
@admin_session
def edit():
    site = {'edit': 'active'}
    tagList = Tags.get_all_tags()
    if 'passage_id' not in request.args:
        return render_template('admin/edit.html', site=site, tags=tagList)


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
    p = Passages(
            title=request.form['title'],
            content=request.form['content'],
            description=request.form['description'],
            pubdate=time.strftime("%Y-%m-%d %H:%M:%S")
            )
    p.set_tags(request.form.getlist('tags'))
    db.session.add(p)
    db.session.commit()
    print request.form.getlist('tags')
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
    for item in request.json['tagList']:
        if Tags.is_registered(item):
            Tags.reuse(item)
        else:
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
    assert request.form['tag']
    Tags.del_tag(request.form['tag'])
    db.session.commit()
    return jsonify(status=True)

@admin_module.route('/update_tag', methods=['POST'])
@admin_session
def update_tag():
    assert request.form['origin']
    if Tags.update_tag(request.form['origin'], request.form['newTag']):
        db.session.commit()
        return jsonify(status=True)
    else:
        return jsonify(status=False)
