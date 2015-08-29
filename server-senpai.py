#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, json, render_template, url_for, redirect
import os, datetime

app = Flask(__name__)
app.config["DEBUG"] = True

def user_cache():
    cache = {"USLACKBOT": {"id": "USLACKBOT","name": "slackbot","deleted": False,"status": None,"color": "2b6836","real_name": "Bot of Slack","tz": None,"tz_label": "Pacific Daylight Time","tz_offset": -25200,"profile": {"first_name": "Bot","last_name": "of Slack","image_24": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_24.png","image_32": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_32.png","image_48": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_48.png","image_72": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_72.png","image_192": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_192.png","image_original": "https://slack-assets2.s3-us-west-2.amazonaws.com/10068/img/slackbot_192.png","real_name": "Bot of Slack","real_name_normalized": "Bot of Slack","email": "bot@slack.com"},"is_admin": False,"is_owner": False,"is_primary_owner": False,"is_restricted": False,"is_ultra_restricted": False,"is_bot": True}}
    with open(os.path.join("database","users.json")) as f:
        for user in json.load(f):
            cache[user["id"]] = user
    return cache

@app.route("/")
def channels():
    with open(os.path.join("database","channels.json")) as f:
        c = json.load(f)
        return render_template("channels.html", channels=c)

@app.route("/channel/<name>")
def channel(name):
    if not os.path.isdir(os.path.join("database",name)):
        return redirect(url_for("channels"))
    return redirect(url_for("channel_log", name=name, stamp=sorted(os.listdir(os.path.join("database",name)))[-1].rpartition(".json")[0]))

@app.route("/channel/<name>/log/<stamp>")
def channel_log(name, stamp):
    if not os.path.isdir(os.path.join("database",name)):
        return redirect(url_for("channels"))
    if not os.path.isfile(os.path.join("database",name,stamp+".json")):
        return redirect(url_for("channel", name=name))
    with open(os.path.join("database","channels.json")) as f, open(os.path.join("database",name,stamp+".json")) as g:
        return render_template("log.html", user=user_cache(), datetime=datetime, int=int, float=float, stamp=stamp, channel=list(filter((lambda x: x["name"] == name), json.load(f)))[0], log = json.load(g))

if __name__ == '__main__':
    app.run()
