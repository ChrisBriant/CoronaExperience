from flask import render_template, flash, redirect, url_for, request, jsonify
from wtforms.validators import ValidationError
from coronaexperience import app
from coronaexperience.forms import TweetsUntilForm
import datetime, json, re, secrets, requests
import tweepy, os
from tweepy import OAuthHandler
import pandas as pd

access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
#api = tweepy.API(auth)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/<string:tweet_id>", methods=['GET', 'POST'])
def home(tweet_id=None):
    form = TweetsUntilForm()
    tweets = []

    try:
        if form.validate_on_submit():
            until = form.dateuntil.data
            tweetsuntil = until.strftime("%Y-%m-%d")
        else:
            now = datetime.datetime.now()
            tweetsuntil = now.strftime("%Y-%m-%d")

        if tweet_id:
            tweepycursor = tweepy.Cursor(api.search,q="#medicalfreedom",count=450,since="2020-02-10",until=tweetsuntil,max_id=tweet_id).items(10)
        else:
            tweepycursor = tweepy.Cursor(api.search,q="#medicalfreedom",count=450,since="2020-02-10",until=tweetsuntil).items(10)
        for tweet in tweepycursor:
            try:
                tweetdict = dict()
                tweetdict["id"] = tweet.id
                tweetdict["created_at"] = tweet.created_at
                tweetdict["text"] = tweet.text
                tweetdict["screen_name"] = tweet.user._json['screen_name']
                tweetdict["name"] = tweet.user._json['name']
                tweetdict["account_creation_data"] =  tweet.user._json['created_at']
                tweetdict["urls"] = tweet.entities['urls']
                print(tweetdict["created_at"])
                #data = [tweet.created_at, tweet.id, tweet.text, tweet.user._json['screen_name'], tweet.user._json['name'], tweet.user._json['created_at'], tweet.entities['urls']]
                #data = tuple(data)
                tweets.append(tweetdict)
            except tweepy.TweepError as e:
                print(e.reason)
                continue
    except Exception as e:
        print(e)
    return render_template("home.html", tweets=tweets, form=form)
