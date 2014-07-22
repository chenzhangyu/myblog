import hashlib
import datetime
from blog import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import abort
from blog.db import db
from blog.db import User, Tags, Passages, pata, Comments, Talks


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['POST'])
def login(name=None):
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None:
        error = 'invalid username'
    else:
        if user.password == hashlib.md5(request.form['password']).hexdigest():
            session['username'] = request.form['username']
            session['userid'] = user.id
            session['eca6bf4563175e50b160924fd99d75fa'] = 'a8a297e50c6bfea50b15d440a30e5d9d'
            if user.root == '1':
                session['admin'] = True
                return redirect(url_for('manage'))
            else:
                return redirect(url_for('index'))
        else:
            error = 'invalid password'
    return render_template('test.html', error=error)


@app.route('/login/')
#@app.route('/login.html')
def show_login():
    return render_template('login.html')


@app.route('/logout/')
def logout():
    # resp = make_response(render_template('index.html'))
    # resp.set_cookie('username', '', expires=0)
    # return resp
    session.pop('username', None)
    session.pop('eca6bf4563175e50b160924fd99d75fa', None)
    session.pop('userid', None)
    if 'admin' in session:
        session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/register/')
def show_register():
    return render_template('register.html')


@app.route('/register/', methods=['POST'])
def register():
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None:
        if request.form['password'] == request.form['config']:
            if request.form['password'] == '':
                return render_template('test.html', error='password is None')
            else:
                user = User(username=request.form['username'],
                            password=hashlib.md5(request.form['password']).hexdigest(),
                            root='0')
                db.session.add(user)
                db.session.commit()
                return render_template('login.html', name=request.form['username'])
        else:
            return render_template('test.html', error='password is not the same')
    else:
        return render_template('test.html', error='invalid name!')


@app.route('/upload/')
def uploadpassage():
    # tags = db.session.query(Tags, Tags.id, Tags.tag)
    # i = 1
    # li = []
    # for tag in tags:
    #     a = list(tag)
    #     a.append(i)
    #     li.append(a)
    #     i += 1
    # page = make_response(render_template('upload.html',
    #                                      name=request.form['username'],
    #                                      taglist=li,
    #                                      sums=len(li)),
    #                                      uploadpassage=True)
    # #page.set_cookie('username', request.form['username'])
    # return page
    if 'admin' in session:
        tags = Tags.query.all()
        i = 1
        li = []
        for x in tags:
            a = x.id, x.tag, i
            a = list(a)
            li.append(a)
            print a
            i += 1
        print li
        sums = len(li)
        return render_template('/admin/upload.html', tags=li, sums=sums, uploadpassage=True)
    else:
        return redirect(url_for('show_login'))


@app.route('/upload/', methods=['POST'])
def upload():
    if 'admin' in session:
        if request.form['title'] == '' or request.form['content'] == '':
            return render_template('/admin/upload.html', error='something is missing!')
        else:
            # i = 0
            # li = []
            # while i < request.form['sum']:
            #     li.append(request.form[str(i)])
            # return render_template('test.html', tags=li, title=request.form['title'], content=request.form['content'])

            # if request.form.getlist('1') is None:
            #     res = 'tag1 is None'
            # else:
            #     res = request.form.getlist('1')[0]

            i = 0
            li = []
            while i < int(request.form['sum']):
                i += 1
                if request.form.getlist(str(i)):
                    res = request.form.getlist(str(i))
                    li.append(res)
                    # print i
                else:
                    # print 'no tag'
                    continue
            # if li:
            #     print li
            # else:
            #     print 'no li'
            passage = Passages(title=request.form['title'],
                               content=request.form['content'],
                               pubdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                               display=0)
            db.session.add(passage)
            db.session.commit()
            eng = db.get_engine(app=app)
            con = eng.connect()
            for n in li:
                res = pata.insert().values(passage_id=passage.id,
                                           tag_id=n[0])
                con.execute(res)
            con.close()
            return redirect(url_for('manage'))
    else:
        return redirect(url_for('show_login'))


@app.route('/update/<passageid>')
def updatepassage(passageid):
    if 'admin' in session:
        passage = Passages.query.get(passageid)
        taglist = Tags.query.all()
        li = []
        for tag in passage.pata:
            li.append(tag.id)
        i = 1
        t = []
        for x in taglist:
            x = x.id, x.tag, i
            x = list(x)
            i += 1
            t.append(x)
        for x in t:
            for n in li:
                flag = 0
                if n == x[0]:
                    flag = 1
                if flag:
                    x.append('checked')
                # print x
        print t
        # print 'passage is', passage
        return render_template('/admin/upload.html', passage=passage, tags=t, sums=len(t))
    else:
        return redirect(url_for('show_login'))


@app.route('/update/', methods=['POST'])
def update():
    if 'admin' in session:
        if request.form['title'] == '' or request.form['content'] == '':
            return render_template('/admin/upload.html', error='something is missing!')
        else:
            i = 0
            li = []
            while i < int(request.form['sum']):
                i += 1
                if request.form.getlist(str(i)):
                    res = request.form.getlist(str(i))
                    li.append(res)
                else:
                    continue
            passage = Passages.query.get(request.form['id'])
            passage.title = request.form['title']
            passage.content = request.form['content']
            passage.pubdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            eng = db.get_engine(app=app)
            con = eng.connect()
            con.execute(pata.delete().where(pata.c.passage_id == request.form['id']))

            # passage = Passages(title=request.form['title'],
            #                    content=request.form['content'],
            #                    pubdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # db.session.add(passage)
            db.session.commit()
            # eng = db.get_engine(app=app)
            # con = eng.connect()
            for n in li:
                res = pata.insert().values(passage_id=request.form['id'],
                                           tag_id=n[0])
                con.execute(res)
            con.close()
            # return render_template('test.html',
            #                        tags=li,
            #                        title=request.form['title'],
            #                        content=request.form['content'])
            return redirect(url_for('manage'))
    else:
        return redirect(url_for('show_login'))


@app.route('/display/<passageid>/<flag>')
def display(passageid, flag):
    if 'admin' in session:
        passage = Passages.query.get(passageid)
        passage.display = int(flag)
        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('show_login'))


@app.route('/deletepassage/<int:passageid>')
def deletepassage(passageid):
    if 'admin' in session:
        passage = Passages.query.get(passageid)
        db.session.delete(passage)
        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('show_login'))


@app.route('/manage/')
def manage():
    if 'admin' in session:
        passages = Passages.query.all()
        tags = Tags.query.all()
        passageslist = []
        for passage in passages:
            a = passage.id, passage.title, passage.pubdate, passage.display
            a = list(a)
            tagslist = []
            for tag in passage.pata:
                tagslist.append(tag.tag)
            a.append(tagslist)
            passageslist.append(a)
        print passageslist
        return render_template('/admin/manage.html',
                               passages=passageslist,
                               tags=tags)
    else:
        return redirect(url_for('show_login'))

# @app.route('/blog/')
# def blogindex():
#     if len(Passages.query.all)


@app.route('/blog/')
@app.route('/blog/<passageid>')
def blog(passageid=None):
    flag = 0
    passagelist = Passages.query.filter_by(display=1).order_by(Passages.id).all()
    passagelist.reverse()
    if passagelist:
        limitpassage = 20
        if len(passagelist) > limitpassage:
            passagelist = passagelist[:limitpassage]
        if passageid:
            passage = Passages.query.get(int(passageid))
            if passage.display == 0:
                abort(404)
        else:
            try:
                passage = passagelist[0]
            except IndexError:
                flag = 1
        tags = passage.pata
    else:
        flag = 2
    if flag:
        return render_template('/blog/blog.html', error='nothing')
    # passage = Passages.query.get(passageid)
    li = []
    li.append(passage.id)
    comments = []
    for x in passage.comments:
        comment = []
        comment.append(x.id)
        comment.append(x.user_id)
        usernameofcomment = User.query.get(x.user_id).username
        comment.append(usernameofcomment)
        comment.append(x.content)
        comment.append(x.pubdate)
        comment.append(x.display)
        talks = []
        for n in x.talks:
            talk = []
            talk.append(n.user_id)
            talk.append(User.query.get(n.user_id).username)
            if n.originer_id:
                username = User.query.get(n.originer_id).username
            else:
                username = usernameofcomment
            talk.append(username)
            talk.append(n.content)
            talk.append(n.pubdate)
            talk.append(n.display)
            talks.append(talk)
        comment.append(talks)
        comments.append(comment)
    li.append(comments)
    # print li
    # print len(li[1])
    if len(li[1]):
        pass
    else:
        li.pop()
    print li
    return render_template('/blog/blog.html', passagelist=passagelist, passage=passage, tags=tags, comments=li)


@app.route('/list/')
def passagelist():
    passages = Passages.query.filter_by(display=1).order_by(Passages.id).all()
    tags = Tags.query.all()
    passages.reverse()
    return render_template('/blog/list.html', passages=passages, tags=tags)


@app.route('/list/<tagid>')
def listbytag(tagid=1):
    eng = db.get_engine(app=app)
    con = eng.connect()
    a = pata.select(pata.c.passage_id).where(pata.c.tag_id == tagid)
    res = con.execute(a).fetchall()
    li = []
    for x in res:
        li.append(x[0])
    li.sort()
    passagelist = []
    for n in li:
        passage = Passages.query.get(n)
        if passage.display:
            passagelist.append(passage)
    passagelist.reverse()
    tags = Tags.query.all()
    con.close()
    return render_template('/blog/list.html', passages=passagelist, tags=tags)


@app.route('/managetag/')
@app.route('/managetag/<error>')
def managetag(error=None):
    if 'admin' in session:
        tags = Tags.query.all()
        return render_template('/admin/managetag.html', tags=tags, error=error)
    else:
        return redirect(url_for('show_login'))


@app.route('/deletetag/<int:tagid>')
def deletetag(tagid):
    if 'admin' in session:
        tag = Tags.query.get(tagid)
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('managetag'))
    else:
        return redirect(url_for('show_login'))


@app.route('/addtag/', methods=['POST'])
def addtag():
    if 'admin' in session:
        if request.form['tag']:
            tag = Tags(tag=request.form['tag'])
            db.session.add(tag)
            db.session.commit()
            return redirect(url_for('managetag'))
        else:
            print 'no tag'
            return redirect(url_for('managetag', error="tag can't be null"))
    else:
        return redirect(url_for('show_login'))


@app.route('/test/')
def justtest():
    return render_template('test.html', test=0)


@app.route('/test/<int:passageid>')
def getcomments(passageid):
    passage = Passages.query.get(passageid)
    li = []
    li.append(passage.id)
    comments = []
    for x in passage.comments:
        comment = []
        comment.append(x.user_id)
        usernameofcomment = User.query.get(x.user_id).username
        comment.append(usernameofcomment)
        comment.append(x.content)
        comment.append(x.pubdate)
        talks = []
        for n in x.talks:
            talk = []
            talk.append(n.user_id)
            talk.append(User.query.get(n.user_id).username)
            if n.id:
                username = User.query.get(n.originer_id).username
            else:
                username = usernameofcomment
            talk.append(username)
            talk.append(n.content)
            talk.append(n.pubdate)
            talks.append(talk)
        comment.append(talks)
        comments.append(comment)
    li.append(comments)
    print li
    return render_template('test.html', comments=li)


@app.route('/comment/<int:passageid>', methods=['POST'])
def comment(passageid):
    # print session['userid']
    print request.form['comment_content']
    a = Comments(passage_id=passageid,
                 user_id=session['userid'],
                 content=request.form['comment_content'],
                 pubdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 display=1)
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('blog', passageid=passageid))


@app.route('/reply/<comment_id>/<originer_id>', methods=['POST'])
def reply(comment_id, originer_id):

    # print 'comment_id', comment_id
    # print 'originer_id', originer_id
    a = Talks(comment_id=int(comment_id),
              originer_id=int(originer_id),
              user_id=session['userid'],
              content=request.form['reply_content'],
              pubdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              display=1)
    db.session.add(a)
    db.session.commit()
    if 'return' in request.form:
        return redirect(url_for('checkreply', passageid=request.form['passageid']))
    if 'passageid' in request.form:
        return redirect(url_for('blog', passageid=request.form['passageid']))
    return redirect(url_for('blog'))


@app.route('/checkreply/<int:passageid>')
# @app.route('/checkreply/', methods=['POST'])
def checkreply(passageid):
    if 'admin' in session:
        li = []
        li.append(passageid)
        passage = Passages.query.get(passageid)
        comments = []
        for x in passage.comments:
            comment = []
            comment.append(x.id)
            comment.append(x.user_id)
            usernameofcomment = User.query.get(x.user_id).username
            comment.append(usernameofcomment)
            comment.append(x.content)
            comment.append(x.pubdate)
            comment.append(x.display)
            talks = []
            for n in x.talks:
                talk = []
                talk.append(n.id)
                talk.append(n.user_id)
                talk.append(User.query.get(n.user_id).username)
                if n.originer_id:
                    username = User.query.get(n.originer_id).username
                else:
                    username = usernameofcomment
                talk.append(username)
                talk.append(n.content)
                talk.append(n.pubdate)
                talk.append(n.display)
                talks.append(talk)
            comment.append(talks)
            comments.append(comment)
        li.append(comments)
        # print li
        # print len(li[1])
        if len(li[1]):
            pass
        else:
            li.pop()
        print li
        return render_template('/admin/checkreply.html', passage=passage, comments=li)
    else:
        return redirect(url_for('show_login'))


@app.route('/deletereply/<id>/<flag>/<passageid>')
def deletereply(id, flag, passageid):
    if 'admin' in session:
        if flag == 'comment':
            a = Comments.query.get(int(id))
        else:
            a = Talks.query.get(int(id))
        a.display = 0
        db.session.commit()
        return redirect(url_for('checkreply', passageid=passageid))
    else:
        return redirect(url_for('show_login'))
# data structure of checkreply
#[passageid, [[comment1-id, comment1-user_id, comment1-username, comment1-content, comment1-pubdate,
# [reply-id, reply1-user_id, reply1-username, reply1-originer-username, reply1-content, reply1-content]...]
# ...]...]
