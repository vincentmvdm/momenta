from flask import Flask, render_template, request,redirect,jsonify
import os
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from flask.ext.heroku import Heroku
import json
import psycopg2
import datetime
import requests

app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
fp = os.path.join(SITE_ROOT, 'config.json')
app = Flask(__name__)
global token
token = None
global user
user = None
with open(fp) as cred:
    creds = json.load(cred)

app.config['GITHUB_CLIENT_ID'] = creds['id']
app.config['GITHUB_CLIENT_SECRET'] = creds['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/challenges'
#heroku = Heroku(app)
github = GitHub(app)
db = SQLAlchemy(app)
CORS(app)

class Challenge(db.Model):
    __tablename__ = "challenges"
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(80))
    user2 = db.Column(db.String(80))
    start = db.Column(db.DateTime)
    def __init__(self, u1, u2, start):
        self.user1 = u1
        self.user2 = u2
        self.start = start
    def __repr__(self):
        return '<(%r and %r) at %r>' % (self.user1, self.user2, self.start)
    def as_dict(self):
        return {'id': self.id, 'user1': self.user1, 'user2': self.user2, 'created_at': (datetime.datetime.now() - self.start).days}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return github.authorize()

@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    global token
    token = oauth_token
    global user
    user = github.get('user')['login']
    print(user)
    return redirect('/challenges')

@app.route('/profile')
def prof():
    if user is None:
        return redirect('/')
    else:
        data = github.get('user')
        return render_template('profile.html', data=data)

@app.route('/challenges')
def challenges():
    challenge_user = github.get('user/followers')
    print(challenge_user)
    jsondata = {'result': [u.as_dict() for u in Challenge.query.all()]}
    jsondata['followers'] = challenge_user
    return render_template('challenges.html', data=jsondata)

@app.route('/challenge/<cid>')
def challenge(cid):
    cha=Challenge.query.get(cid).as_dict()
    resp1 = requests.get(
        'https://shrouded-oasis-42259.herokuapp.com',
        params={'uname': cha['user1']}).json()['data']
    resp2 = requests.get(
        'https://shrouded-oasis-42259.herokuapp.com',
        params={'uname': cha['user2']}).json()['data']
    i1 = int(resp1)
    i2 = int(resp2)
    is_streak = 'yes' if i1 != 0 and i2 != 0 else 'no'
    cha['is_streak'] = is_streak
    return render_template('challenge.html', data=cha)

@app.route('/challenge_user')
def cha_usr():
    if 'user' in request.args:
        global user
        c = Challenge(request.args.get('user',''), user, datetime.datetime.now())
        db.session.add(c)
        db.session.commit()
    return jsonify({'status':200})

@github.access_token_getter
def token_getter():
    return token

if __name__ == "__main__":
    app.debug=True
    app.run()
