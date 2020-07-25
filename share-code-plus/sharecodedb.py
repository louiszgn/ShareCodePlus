#!/usr/bin/env python3

from flask import Flask, request, render_template, \
                  redirect

from model_sqlite import save_code, \
                  read_code, \
                  get_last_entries_from_db, \
                  get_users_from_db

from languages import langs

app = Flask(__name__)

@app.route('/')
def index():
    d = { 'last_added':get_last_entries_from_db() }
    return render_template('index.html',**d)

@app.route('/admin/')
def admin():
    d = { 'users':get_users_from_db() }
    return render_template('admin.html',**d)

@app.route('/create')
def create():
    uid = save_code()
    return redirect("{}edit/{}".format(request.host_url,uid))
    
@app.route('/edit/<string:uid>/')
def edit(uid):
    infos = read_code(uid)
    if infos[0][0] is None:
        return render_template('error.html',uid=uid)
    d = dict( uid=uid, code=infos[0][0], langs=langs, lang=infos[0][1],
              url="{}view/{}".format(request.host_url,uid))
    return render_template('edit.html', **d) 

@app.route('/publish',methods=['POST'])
def publish():
    code = request.form['code']
    uid  = request.form['uid']
    lang  = request.form['language']
    save_code(uid,code,lang)
    return redirect("{}{}/{}".format(request.host_url,
                                     request.form['submit'],
                                     uid))

@app.route('/view/<string:uid>/')
def view(uid):
    infos = read_code(uid)
    if infos[0][0] is None:
        return render_template('error.html',uid=uid)
    d = dict( uid=uid, code=infos[0][0], lang=infos[0][1],
              url="{}view/{}".format(request.host_url,uid))
    return render_template('view.html', **d)

if __name__ == '__main__':
    app.run()

