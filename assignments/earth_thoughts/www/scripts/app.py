from flask import Flask, url_for
from flask import request
from flask_cors import CORS
import json
from flask import jsonify
import random
import praw
import os
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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
    return jsonify({"success":True,"url":imageList[random.randint(0,len(imageList)-1)]})


@app.route('/get_text')
def get_text():
    return jsonify({"success":True,"text":textList[random.randint(0,len(textList)-1)]})

def update_posts():
    print('updating posts...')
    reddit = praw.Reddit(client_id=os.environ['client_id'],
			client_secret=os.environ['client_secret'],
			user_agent='earth thoughts by /u/csos95')
    for submission in reddit.subreddit('Showerthoughts').hot(limit=100):
        textList.append(submission.title)
    for submission in reddit.subreddit('EarthPorn').hot(limit=100):
        if submission.url.endswith('.jpg') or submission.url.endswith('.png'):
            imageList.append(submission.url)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=update_posts,
    trigger=IntervalTrigger(hours=1),
    id='update_posts_job',
    name='updating Showerthoughs and EarthPorn posts every hour',
                            replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

update_posts()
