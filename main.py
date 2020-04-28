from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for, escape, send_from_directory, make_response

from flask_session import Session

import time

from userList import userList

app = Flask(__name__, static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


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
    return render_template('index.html', title='Main menu', msg=userinfo)


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
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', msg='Logged out.')


if __name__ == '__main__':
    app.secret_key = 'very hard to guess'
    app.run(host='127.0.0.1', debug=True)
