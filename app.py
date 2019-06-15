from requests_oauthlib import OAuth2Session
from flask_bootstrap import Bootstrap
from flask import Flask, request, redirect, session, url_for, json, render_template
from flask.json import jsonify
import os, sys, requests, string, random, datetime, operator
from  datetime import datetime
import pytz

app = Flask(__name__)

bootstrap = Bootstrap(app)

templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# This information is obtained upon registration of a new GitHub

# app.secret_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(24)])
app.secret_key = 'susper_secret_key'

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


def repositories():
    return [
        'https://api.github.com/repos/professorTalles/Hackaton2019',
        'https://api.github.com/repos/lucaspedronet/hackathon-catolica-integra',
        'https://api.github.com/repos/carlosccomp/hackaton2019',
        'https://api.github.com/repos/jpmoraes59/tonolucro-game',
        'https://api.github.com/repos/brunomoraisti/acadmy',
        'https://api.github.com/repos/alutsu/tonolucro',
        'https://api.github.com/repos/pedrohsantana1/HackathonUnicatolica2019',
        'https://api.github.com/repos/weltonjr/Hackaton-Catolica-2019',
        'https://api.github.com/repos/SkyList/api-hackathon-catolica',
        'https://api.github.com/repos/SkyList/gestor-hackathon-catolica',
        'https://api.github.com/repos/rfmeloneto/hackatom-2019',
        'https://api.github.com/repos/flamolino/ToNoGame-HackthonCatolica2019',
        'https://api.github.com/repos/GengisVhan/hackaton-catolica',
        'https://api.github.com/repos/Manjor/education',
        'https://api.github.com/repos/jhonathangimenes/catolica-hackathon',
        'https://api.github.com/repos/FernandorMurta/education',
        'https://api.github.com/repos/pgsilva1/app-hackathon-catolica',
        'https://api.github.com/repos/Nicollas1305/AppHackathon',
        'https://api.github.com/repos/adailsonaguiar/quiz',
        'https://api.github.com/repos/rcab/hackcatolica',
        'https://api.github.com/repos/vilmarferreira/hackathon_uniCatolica'
    ]


def getMessageRefeicao():
    h = datetime.now(pytz.timezone('america/araguaina')).hour
    h = h - 3
    print('time:')
    print(h)

    if h <= 8:
        return "café as 8h"

    elif h <= 11:
        return None
    elif h <= 13:
        return "lembre-se de comer algo"
    elif h <= 16:
        return "lanche as 16hrs"


def getCheckpointMessage():
    h = datetime.now(pytz.timezone('america/araguaina')).hour
    h = h - 3
    print(h)
    if h <= 10:
        return "checkpoint as 10hrs"
    elif h <= 15:
        return "checkpoint as 10hrs"
    elif h <= 17:
        return None
    elif h < 18:
        return "nos aproximando da reta final"
    elif h <= 19:
        return "reta final!!!!"


# projeto deletado
#


@app.route("/")
def demo():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    log('home:')
    log('state:')
    log(state)

    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('.acompanhamento'))


@app.route("/repos", methods=['GET'])
def repos():
    return jsonify(repositories())


@app.route("/acompanhamento", methods=["GET"])
def acompanhamento():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])

    repos = repositories()

    details_todos = []
    for r in repos:
        data = {**repo_last_event(r), **repo_details(r)}  # dict merge 3.5+
        details_todos.append(data)

        # details = sorted(data, key=itemgetter('total_seconds_ago'))

    details_todos.sort(key=operator.itemgetter('inativo', 'total_seconds_ago', 'name'))
    pages = os.listdir(templates_path)

    refeicao = getMessageRefeicao()
    checkpoint = getCheckpointMessage()

    motiva = ["não sofra sozinho", "se tiver duvida, chame um mentor", "alimente o readme.md",
              "tem energético no freezer", "coffe in, code out"]

    if refeicao:
        motiva.append(refeicao)
        motiva.append(refeicao)
    if checkpoint:
        motiva.append(motiva)
        motiva.append(motiva)

    return render_template('cards.html', data=details_todos, pages=pages, motiva=motiva)

    # return jsonify(details_todos)
    # return repo_details('https://api.github.com/repos/aricaldeira/PySPED')
    # return jsonify(github.get('https://api.github.com/user').json())


@app.route("/raw", methods=["GET"])
def raw():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])

    repos = repositories()

    details_todos = []
    for r in repos:
        data = {**repo_last_event(r), **repo_details(r)}  # dict merge 3.5+
        details_todos.append(data)

        # details = sorted(data, key=itemgetter('total_seconds_ago'))

    details_todos.sort(key=operator.itemgetter('inativo', 'total_seconds_ago', 'name'))
    return jsonify(details_todos)


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
    # log('repo_details')
    # log(repo)

    try:
        if len(r) > 0:
            return {
                'name': r['name'],
                'language': r['language'],
                'description': r['description'],
                'html_url': r['html_url'],
                'url': r['url']
            }
        return {
            'name': '',
            'language': '',
            'description': '',
            'html_url': repo,
            'url': repo
        }
    except:
        return {
            'name': 'erro',
            'language': '',
            'description': '',
            'html_url': repo,
            'url': repo
        }


def repo_last_event(repo):
    github = OAuth2Session(client_id, token=session['oauth_token'])
    url = ''.join([repo, '/events'])
    r = github.get(url).json()

    # log('repo_last_event:')
    # log(url)
    # log('size:')
    # log(len(r))

    try:

        if len(r) > 0:
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            d1 = datetime.datetime.strptime(r[0]['created_at'], fmt)
            d2 = datetime.datetime.now()

            daysDiff, total_seconds = (d2 - d1).days, (d2 - d1).total_seconds()

            hoursDiff = int(total_seconds / 3600)
            minutesDiff = int(total_seconds / 60) % 60

            return {
                'user_avatar': r[0]['actor']['avatar_url'],
                'user_login': r[0]['actor']['login'],
                'user_url': r[0]['actor']['url'],
                'created_at': r[0]['created_at'],
                'days_ago': daysDiff,
                'hours_ago': hoursDiff,
                'minutes_ago': minutesDiff,
                'total_seconds_ago': total_seconds,
                'inativo': 0,
                'type': r[0]['type']

            }

        return {
            'user_avatar': '',
            'user_login': '',
            'user_url': '',
            'created_at': '',

            'days_ago': 0,
            'hours_ago': 0,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            'inativo': 9,
            'type': ''

        }
    except:
        return {
            'user_avatar': '',
            'user_login': '',
            'user_url': '',
            'created_at': '',

            'days_ago': 0,
            'hours_ago': 0,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            'inativo': 9,
            'type': 'erro'

        }


def repo_last_event_all(repo):
    github = OAuth2Session(client_id, token=session['oauth_token'])
    url = ''.join([repo, '/events'])
    r = github.get(url).json()

    # log('repo_last_event:')
    # log(url)
    # log('size:')
    # log(len(r))

    if len(r) > 0:
        return jsonify(r[0])

    return {
        'user_avatar': '',
        'user_login': '',
        'user_url': '',
        'created_at': '',
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


@app.route('/template')
def template_test():
    # method to test template locally

    h = datetime.now(pytz.timezone('america/araguaina')).hour

    print(h)
    data_test = [
        {
            "created_at": "2018-04-26T19:16:33Z",
            "description": "Sistema P\u00fablico de Escritura\u00e7\u00e3o Digital em Python",
            "language": "Python",
            "name": "PySPED",
            "type": "PushEvent",
            "url": "https://api.github.com/repos/aricaldeira/PySPED",
            "user_avatar": "https://avatars.githubusercontent.com/u/185558?",
            "user_login": "aricaldeira",
            'days_ago': 0,
            'hours_ago': 0,
            'minutes_ago': 20,
            'total_seconds_ago': 0,
            "user_url": "https://api.github.com/users/aricaldeira"
        },
        {
            "created_at": "",
            "description": 'null',
            "language": "Python",
            "name": "horta-urbana",
            "type": "",
            "url": "https://api.github.com/repos/guilhermebferreira/horta-urbana",
            "user_avatar": "",
            "user_login": "",
            'days_ago': 0,
            'hours_ago': 20,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": ""
        },
        {
            "created_at": "2018-04-23T01:43:49Z",
            "description": 'null',
            "language": "Python",
            "name": "python-github-api",
            "type": "PushEvent",
            "url": "https://api.github.com/repos/guilhermebferreira/python-github-api",
            "user_avatar": "https://avatars.githubusercontent.com/u/5393392?",
            "user_login": "guilhermebferreira",
            'days_ago': 3,
            'hours_ago': 12,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": "https://api.github.com/users/guilhermebferreira"
        },
        {
            "created_at": "",
            "description": 'null',
            "language": "Python",
            "name": "horta-urbana",
            "type": "",
            "url": "https://api.github.com/repos/guilhermebferreira/horta-urbana",
            "user_avatar": "",
            "user_login": "",
            'days_ago': 0,
            'hours_ago': 20,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": ""
        },
        {
            "created_at": "2018-04-23T01:43:49Z",
            "description": 'null',
            "language": "Python",
            "name": "python-github-api",
            "type": "PushEvent",
            "url": "https://api.github.com/repos/guilhermebferreira/python-github-api",
            "user_avatar": "https://avatars.githubusercontent.com/u/5393392?",
            "user_login": "guilhermebferreira",
            'days_ago': 3,
            'hours_ago': 12,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": "https://api.github.com/users/guilhermebferreira"
        },
        {
            "created_at": "",
            "description": 'null',
            "language": "Python",
            "name": "horta-urbana",
            "type": "",
            "url": "https://api.github.com/repos/guilhermebferreira/horta-urbana",
            "user_avatar": "",
            "user_login": "",
            'days_ago': 0,
            'hours_ago': 20,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": ""
        },
        {
            "created_at": "2018-04-23T01:43:49Z",
            "description": 'null',
            "language": "Python",
            "name": "python-github-api",
            "type": "PushEvent",
            "url": "https://api.github.com/repos/guilhermebferreira/python-github-api",
            "user_avatar": "https://avatars.githubusercontent.com/u/5393392?",
            "user_login": "guilhermebferreira",
            'days_ago': 3,
            'hours_ago': 12,
            'minutes_ago': 0,
            'total_seconds_ago': 0,
            "user_url": "https://api.github.com/users/guilhermebferreira"
        }
    ]

    motiva = ["não sofra sozinho", "se tiver duvida, chame um mentor", "alimente o readme.md",
              "tem energético no freezer", "coffe in, code out"]
    refeicao = getMessageRefeicao()
    checkpoint = getCheckpointMessage()
    if refeicao:
        motiva.append(refeicao)
    if checkpoint:
        motiva.append(motiva)

    pages = os.listdir(templates_path)
    return render_template('cards.html', data=data_test, pages=pages, motiva=motiva)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback

    os.environ['DEBUG'] = "1"

    app.run(debug=True)
