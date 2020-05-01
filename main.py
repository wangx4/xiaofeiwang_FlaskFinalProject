from flask import Flask
from flask import render_template
from flask import request, flash, send_file, session, redirect, url_for, escape, send_from_directory, make_response

from flask_session import Session
from werkzeug.utils import secure_filename

import time, os
from functools import wraps

from user import userList
from file import fileList
from user_file import userFileList
from shared_file import sharedFileList

import config
import util

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
        if timeSinceAct > 600:  # if a user has no action more than 10 minutes, the session is expired
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if checkSession() == False:
            return redirect('login')
        return fn(*args, **kwargs)

    return wrapper


@app.route('/')
@app.route('/main')
@login_required
def main():
    status_msg = request.args.get('status_msg')
    user_id = session['user']['id']
    user_files = userFileList()
    this_user_files = user_files.getByField('user_id', user_id)
    this_user_files = [
        this_file for this_file in this_user_files
        if this_file['is_deleted'] == 0
    ]
    for file in this_user_files:
        if file['is_shared'] == 0:
            file['is_shared'] = "No"
        else:
            file['is_shared'] = "Yes"

    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('main.html',
                           title='Main menu',
                           msg=userinfo,
                           files=this_user_files,
                           status_msg=status_msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    -check login
    -set session
    -redirect to menu
    -check session on login pages
    '''
    print('-------------------------')
    email = request.form.get('email')
    password = request.form.get('password')
    if email != None and password != None:
        users = userList()
        is_ok, user_data = users.tryLogin(email, password)
        if is_ok:
            print('login ok')
            session['user'] = user_data
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
@login_required
def logout():
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', msg='Logged out.')


@app.route('/uploadfile', methods=['GET', 'POST'])
@login_required
def upload_file():
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
            return render_template('uploadfile.html',
                                   title='upload file',
                                   status_msg='Please select a file !')

        filename = secure_filename(file.filename)
        user_id = session['user']['id']
        files = fileList()
        user_files = userFileList()
        _, ext = util.split_filename(filename)
        file_storage_name = util.gen_uuid_str() + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_storage_name))

        file_data = {"storage_name": file_storage_name}
        file_id = files.insert(file_data)

        user_file_data = {
            'user_id': user_id,
            "file_id": file_id,
            "filename": filename
        }
        user_files.insert(user_file_data)
        return render_template('uploadfile.html',
                               title='upload success',
                               status_msg=filename + ' upload success !')
    return render_template('uploadfile.html', title='upload file')


"""
@app.route('/upload_success')
@login_required
def upload_success():
    return render_template('upload_success.html',title='upload success')
"""


@app.route('/downloadfile')
@login_required
def download_file():
    user_file_id = request.args.get('id')
    temp = user_file_id
    try:
        user_file_id = int(user_file_id)
    except:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    user_files = userFileList()
    query_data = {
        'user_id': int(session['user']['id']),
        'file_id': int(user_file_id)
    }
    this_user_file = user_files.getByFields(query_data)
    print(this_user_file)
    if len(this_user_file) == 0:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    filename = this_user_file[0]['filename']
    file_id = this_user_file[0]['file_id']
    files = fileList()
    this_file = files.getById(file_id)
    file_storage_name = this_file[0]['storage_name']
    file_abs_path = os.path.join(config.UPLOAD_FOLDER, file_storage_name)
    return send_file(file_abs_path,
                     as_attachment=True,
                     attachment_filename=filename)


@app.route('/deletefile')
@login_required
def delete_file():
    user_file_id = request.args.get('id')
    temp = user_file_id
    try:
        user_file_id = int(user_file_id)
    except:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    user_files = userFileList()
    query_data = {
        'user_id': int(session['user']['id']),
        'file_id': int(user_file_id)
    }
    this_user_file = user_files.getByFields(query_data)
    print(this_user_file)
    if len(this_user_file) == 0:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))
    data = {'is_deleted': 1, 'id': user_file_id}
    user_files.update(data)

    return redirect(
        url_for('main',
                status_msg=f"delete file with id = `{user_file_id}` succeed"))


@app.route('/recycle_bin')
@login_required
def recycle_bin():
    status_msg = request.args.get('status_msg')
    user_id = session['user']['id']
    user_files = userFileList()
    this_user_files = user_files.getByField('user_id', user_id)
    this_user_files = [
        this_file for this_file in this_user_files
        if this_file['is_deleted'] == 1
    ]
    for file in this_user_files:
        if file['is_shared'] == 0:
            file['is_shared'] = "No"
        else:
            file['is_shared'] = "Yes"

    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('recycle_bin.html',
                           title='Main menu',
                           msg=userinfo,
                           files=this_user_files,
                           status_msg=status_msg)


@app.route('/recoverfile')
@login_required
def recoverfile():
    user_file_id = request.args.get('id')
    temp = user_file_id
    try:
        user_file_id = int(user_file_id)
    except:
        return redirect(
            url_for('recycle_bin',
                    status_msg=f"file with id = `{temp}` did not found"))

    user_files = userFileList()
    query_data = {
        'user_id': int(session['user']['id']),
        'file_id': int(user_file_id)
    }
    this_user_file = user_files.getByFields(query_data)
    print(this_user_file)
    if len(this_user_file) == 0:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    if this_user_file[0]['is_deleted'] == 0:
        return redirect(
            url_for(
                'recycle_bin',
                status_msg=f"recycle bin file with {user_file_id} did not found"
            ))
    data = {'is_deleted': 0, 'id': user_file_id}
    user_files.update(data)

    return redirect(
        url_for('recycle_bin',
                status_msg=f"recover file with id = `{user_file_id}` succeed"))


@app.route('/reallydeletefile')
@login_required
def reallydeletefile():
    user_file_id = request.args.get('id')
    temp = user_file_id
    try:
        user_file_id = int(user_file_id)
    except:
        return redirect(
            url_for('recycle_bin',
                    status_msg=f"file with id = `{temp}` did not found"))

    user_files = userFileList()
    query_data = {
        'user_id': int(session['user']['id']),
        'file_id': int(user_file_id)
    }
    this_user_file = user_files.getByFields(query_data)
    print(this_user_file)
    if len(this_user_file) == 0:
        return redirect(
            url_for('recycle_bin',
                    status_msg=f"file with id = `{temp}` did not found"))

    if this_user_file[0]['is_deleted'] == 0:
        return redirect(
            url_for(
                'recycle_bin',
                status_msg=f"recycle bin file with {user_file_id} did not found"
            ))

    user_files.deleteById(user_file_id)

    return redirect(
        url_for('recycle_bin',
                status_msg=f"delete file with id = `{user_file_id}` succeed"))


@app.route('/sharefile')
@login_required
def sharefile():
    user_file_id = request.args.get('id')
    temp = user_file_id
    try:
        user_file_id = int(user_file_id)
    except:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    user_files = userFileList()
    query_data = {
        'user_id': int(session['user']['id']),
        'file_id': int(user_file_id)
    }
    this_user_file = user_files.getByFields(query_data)
    print(this_user_file)
    if len(this_user_file) == 0:
        return redirect(
            url_for('main',
                    status_msg=f"file with id = `{temp}` did not found"))

    if this_user_file[0]['is_deleted'] == 1:
        return redirect(
            url_for('main',
                    status_msg=f"file with {user_file_id} did not found"))

    shared_files = sharedFileList()
    share_id = util.gen_share_id()
    access_token = util.gen_access_token()

    data = {
        'id': share_id,
        'access_token': access_token,
        'user_id': query_data['user_id'],
        'user_file_id': user_file_id,
        'filename': this_user_file[0]['filename']
    }
    shared_files.insert(data)

    data = {'is_shared': 1, 'id': user_file_id}
    user_files.update(data)
    return redirect(
        url_for(
            'main',
            status_msg=
            f"share file with id = `{user_file_id}` succeed, the share link is {config.share_link_prefix+share_id} the access token is {access_token}"
        ))


@app.route('/myshares')
@login_required
def myshares():
    status_msg = request.args.get('status_msg')
    user_id = session['user']['id']
    shared_files = sharedFileList()
    this_user_shared_files = shared_files.getByField('user_id', user_id)
    print(this_user_shared_files)

    userinfo = 'Hello, ' + session['user']['fname']
    return render_template('myshares.html',
                           title='My shares',
                           msg=userinfo,
                           files=this_user_shared_files,
                           status_msg=status_msg)


"""
    if checkSession() == False:
        return redirect('login')
"""


@app.route('/s/<share_id>')
def handle_share(share_id):
    shared_files = sharedFileList()
    if request.method == 'POST':
        token = request.form.get('token')
        this_shared_file = shared_files.getById(share_id)
        if len(this_shared_file) == 0:
            return render_template(
                'share.html',
                status_msg=f"share with share_id = `{share_id}` does not exist"
            )

        if this_shared_file[0]['access_token'] != token:
            return render_template('share.html', status_msg=f"token incorrect")

        user_files = userFileList()
        this_user_file = user_files.getById(
            this_shared_file[0]['user_file_id'])
        if len(this_user_file) == 0 or this_user_file[0][
                'is_deleted'] == 1 or this_user_file[0]['is_shared'] == 0:
            return render_template(
                'share.html',
                status_msg=f"share with share_id = `{share_id}` does not exist"
            )

        filename = this_shared_file[0]['filename']
        file_id = this_user_file[0]['file_id']
        files = fileList()
        this_file = files.getById(file_id)
        file_storage_name = this_file[0]['storage_name']
        file_abs_path = os.path.join(config.UPLOAD_FOLDER, file_storage_name)
        return send_file(file_abs_path,
                         as_attachment=True,
                         attachment_filename=filename)

    this_shared_file = shared_files.getById(share_id)
    if len(this_shared_file) == 0:
        return render_template(
            'share.html',
            status_msg=f"share with share_id = `{share_id}` does not exist")
    user_files = userFileList()
    this_user_file = user_files.getById(this_shared_file[0]['user_file_id'])
    if len(this_user_file) == 0 or this_user_file[0][
            'is_deleted'] == 1 or this_user_file[0]['is_shared'] == 0:
        return render_template(
            'share.html',
            status_msg=f"share with share_id = `{share_id}` does not exist")

    return render_template(
        'share.html', share_exist=True,
        filename='youknow')  #filename=this_shared_file[0]['filename']


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=request.path + " not found"), 404


if __name__ == '__main__':
    app.secret_key = 'very hard to guess'
    app.run(host='127.0.0.1', debug=True)
