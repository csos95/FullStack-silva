from flask import Flask, url_for
from flask import request
from flask_cors import CORS
import json
from flask import jsonify
import random
import praw
import os

app = Flask(__name__)
CORS(app)

textList = []
imageList = []

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/', methods=['GET'])
def index():
    return site_map()


@app.route('/site-map', methods=['GET'])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if not url == '/site-map':
                links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    if len(links) > 0:
        return jsonify({"success": True,"routes":links})
    else:
        return jsonify({"success": False,"routes":links})


@app.route('/get_image')
def get_image():
    random.shuffle(imageList)
    return jsonify({"success":True,"url":imageList[0]})


@app.route('/get_text')
def get_text():
    random.shuffle(textList)
    return jsonify({"success":True,"text":textList[0]})

def update_posts():
    reddit = praw.Reddit(client_id=os.environ['client_id'],
			client_secret=os.environ['client_secret'],
			user_agent='earth thoughts by /u/csos95')
    for submission in reddit.subreddit('Showerthoughts').hot(limit=100):
        textList.append(submission.title)
    for submission in reddit.subreddit('EarthPorn').hot(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            imageList.append(submission.url)
    print(imageList)

update_posts()
