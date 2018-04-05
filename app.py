# -*- coding: utf-8 -*-

import os
import random
import sys
import json

import requests
from flask import Flask, request


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def repo():
    r = requests.get('https://api.github.com/repos/django/django')
    if (r.ok):
        repoItem = json.loads(r.text or r.content)
        return "Django repository created: " + repoItem['created_at']


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
