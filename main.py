from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 

from flask_session import Session 

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
   app.secret_key = 'very hard to guess'
   app.run(host='127.0.0.1',debug=True)  