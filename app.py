from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, json
from flask.json import jsonify
import os, sys, requests

app = Flask(__name__)

app.secret_key = "super secret key"

# This information is obtained upon registration of a new GitHub

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
    return repo_details('https://api.github.com/repos/guilhermebferreira/horta-urbana')
    #return jsonify(github.get('https://api.github.com/user').json())



@app.route('/repo')
def repo():
    r = requests.get('https://api.github.com/repos/django/django')
    if (r.ok):
        repoItem = json.loads(r.text or r.content)
        return "Django repository created: " + repoItem['created_at']

@app.route('/lang')
def language():
    return repo_languages('https://api.github.com/repos/guilhermebferreira/horta-urbana')

@app.route('/collaborators')
def collaborators():
    return repo_collaborators('https://api.github.com/repos/guilhermebferreira/horta-urbana')

@app.route('/commits')
def commits():
    return repo_commits('https://api.github.com/repos/guilhermebferreira/horta-urbana')


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()

def repo_details(repo):

    github = OAuth2Session(client_id, token=session['oauth_token'])
    r = github.get(repo).json()

    return jsonify(r)

def repo_languages(repo):

    github = OAuth2Session(client_id, token=session['oauth_token'])
    r = github.get(repo).json()
    l = github.get(r['languages_url']).json()

    return jsonify(l)

def repo_collaborators(repo):

    github = OAuth2Session(client_id, token=session['oauth_token'])
    r = github.get(repo).json()
    c = github.get(r['collaborators_url']).json()

    return jsonify(c)

def repo_commits(repo):

    github = OAuth2Session(client_id, token=session['oauth_token'])
    r = github.get(repo).json()
    c = github.get(r['commits_url']).json()

    return jsonify(c)

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback

    os.environ['DEBUG'] = "1"

    app.run(debug=True)
