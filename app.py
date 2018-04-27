from requests_oauthlib import OAuth2Session 
from flask import Flask, request, redirect, session, url_for, json, render_template
from flask.json import jsonify
import os, sys, requests, string, random, datetime

app = Flask(__name__)


templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# This information is obtained upon registration of a new GitHub

# app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(24)])
app.secret_key = 'susper_secret_key'

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.route("/")
def demo():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])

    repos = [
        'https://api.github.com/repos/aricaldeira/PySPED',
        'https://api.github.com/repos/guilhermebferreira/horta-urbana',
        'https://api.github.com/repos/guilhermebferreira/python-github-api'
    ]

    details = []
    details_todos = []
    for r in repos:
        data = {**repo_last_event(r), **repo_details(r)}  # dict merge 3.5+
        details_todos.append(data)

    return jsonify(details_todos)
    # return repo_details('https://api.github.com/repos/aricaldeira/PySPED')
    # return jsonify(github.get('https://api.github.com/user').json())


@app.route('/repo')
def repo():
    r = requests.get('https://api.github.com/repos/django/django')
    if (r.ok):
        repoItem = json.loads(r.text or r.content)
        return "Django repository created: " + repoItem['created_at']


@app.route('/lang')
def language():
    return repo_languages('https://api.github.com/repos/guilhermebferreira/horta-urbana')


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


def repo_details(repo):
    github = OAuth2Session(client_id, token=session['oauth_token'])
    r = github.get(repo).json()

    if len(r) > 0:
        return {
            'name': r['name'],
            'language': r['language'],
            'description': r['description'],
            'url': r['url']
        }
    else:
        return {
            'name': '',
            'language': '',
            'description': '',
            'url': ''
        }


def repo_last_event(repo):
    github = OAuth2Session(client_id, token=session['oauth_token'])
    url = ''.join([repo, '/events'])
    r = github.get(url).json()

    log('repo_last_event:')
    log(url)
    log('size:')
    log(len(r))

    if len(r) > 0:
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        d1 = datetime.datetime.strptime(r[0]['created_at'], fmt)
        d2 = datetime.datetime.now()

        daysDiff, secondsDiff = (d2 - d1).days, (d2 - d1).seconds
        minutesDiff = (secondsDiff % 3600) // 60
        hoursDiff = daysDiff * 24 + secondsDiff // 3600

        return {
            'user_avatar': r[0]['actor']['avatar_url'],
            'user_login': r[0]['actor']['login'],
            'user_url': r[0]['actor']['url'],
            'created_at': r[0]['created_at'],
            'days_ago': daysDiff,
            'hours_ago': hoursDiff,
            'minutes_ago': minutesDiff,
            'type': r[0]['type']

        }

    return {
        'user_avatar': '',
        'user_login': '',
        'user_url': '',
        'created_at': '',

        'hours_ago': 0,
        'minutes_ago': 0,
        'type': ''

    }


def log(msg):  # print on heroku log
    print(msg)
    sys.stdout.flush()


def repo_languages(repo):
    github = OAuth2Session(client_id, token=session['oauth_token'])

    r = github.get(repo).json()
    l = github.get(r['languages_url']).json()

    return jsonify(l)




if __name__ == "__main__":
    # This allows us to use a plain HTTP callback

    os.environ['DEBUG'] = "1"

    app.run(debug=True)
