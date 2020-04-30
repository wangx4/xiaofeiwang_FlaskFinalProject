from flask import Flask
from flask import render_template
from flask import request, flash, session, redirect, url_for, escape, send_from_directory, make_response

from flask_session import Session
from werkzeug.utils import secure_filename

import time, os

from user import userList
import config




app = Flask(__name__, static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

UPLOAD_FOLDER = config.UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False


@app.route('/')
@app.route('/main')
def index():
    if checkSession() == False:
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('main.html', title='Main menu', msg=userinfo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    -check login
    -set session
    -redirect to menu
    -check session on login pages
    '''
    print('-------------------------')
    if request.form.get('email') is not None and request.form.get(
            'password') is not None:
        c = userList()
        if c.tryLogin(request.form.get('email'), request.form.get('password')):
            print('login ok')
            session['user'] = c.data[0]
            session['active'] = time.time()

            return redirect('main')
        else:
            print('login failed')
            return render_template('login.html',
                                   title='Login',
                                   msg='Incorrect login.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if checkSession() == False:
        return redirect('login')
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', msg='Logged out.')

@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if checkSession() == False:
        return redirect('login')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            #return redirect(request.url)
            return render_template('uploadfile.html',title='upload file', msg='please select a file')
        #if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload_success.html', title='upload success',msg=filename+' upload success')
    return render_template('uploadfile.html',title='upload file')


@app.route('/upload_success')
def upload_success():
    if checkSession() == False:
        return redirect('login')
    return render_template('upload_success.html',title='upload success')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',msg = request.path + " not found"), 404

if __name__ == '__main__':
    app.secret_key = 'very hard to guess'
    app.run(host='127.0.0.1', debug=True)
