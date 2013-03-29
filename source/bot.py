#!/usr/bin/env python

# --------- Imports --------
import webapp2,cgi,urllib
from google.appengine.api import xmpp,urlfetch
from google.appengine.ext import db
from md5 import md5
import simplejson as json
import tweepy
import re
import logging
import time
import yaml
import os.path
import urllib2


# ------- Database Handling -----
class TwitterDB(db.Model):
    reddit_id = db.StringProperty()

# ---- The Job Handler --------
class TwitterBot(webapp2.RequestHandler):
    def get(self):
        config = yaml.load(open(os.path.dirname(__file__) + '/config.yaml', 'r'));
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])
        bot = tweepy.API(auth)
        url = "http://www.reddit.com/r/" + config['subreddit'] + "/.json"
        headers = {'User-Agent':config['user-agent']}
        result = urlfetch.fetch(url=url,headers=headers,deadline=30)
        if result.status_code != 200:
            output = "reddit feed status = " + str(result.status_code)
            logging.info(output)
            self.response.out.write(output)
            return

        feeddata = json.loads(result.content)

        output = '<pre>DONE!\n==========\n\nTweets:\n'

        if 'data' in feeddata and 'children' in feeddata['data']:
            for entry in feeddata['data']['children']:
                title = str(unicode(entry['data']['title']).encode("utf-8"))
                subreddit = str(unicode(entry['data']['subreddit']).encode("utf-8"))
                myid = str(unicode(entry['data']['id']).encode("utf-8"))
                link = 'http://redd.it/' + myid
                status = " " + link

                try:
                    status = title[:(120 - len(status))] + status
                except:
                    status = repr(title[:(120 - len(status))]) + status
                    output += "\n<<<<< repr >>>>>\n"

                query = TwitterDB.all()
                query.filter('reddit_id =', myid)
                res = query.fetch(1)

                if len(res) == 0 and entry['data']['score'] > 5:

                    if (len(status) + len(subreddit) + 2) < 140:
                        status += " #" + subreddit

                    output +=  status + '\n'

                    try:
                        bot.update_status(status,headers=headers)
                    except (DeadlineExceededError, tweepy.TweepError) as e:
                        logging.warning(e)
                        continue

                    item = TwitterDB()
                    item.reddit_id = myid
                    item.put()
                else:
                    continue
                time.sleep(15) # wait a minute before trying to post again



        if time.strftime('%a') == 'Fri':
            output += '\n\nFind new #FF friends:\n----------\n'
            try:
                for status in bot.home_timeline(headers=headers):
                    tweet = repr(status.text)

                    if '#FF' in tweet or '#FollowFriday' in tweet:
                        tweeps = set(who.strip('@') for who in tweet.split() if who.startswith("@"))
                        for tweep in tweeps:
                            for result in  bot.search_users(q=tweep,headers=headers):
                                if result.screen_name == tweep:
                                    try:
                                        result.follow()
                                    except (DeadlineExceededError, tweepy.TweepError) as e:
                                        logging.warning(e)

                                    output += tweep + '\n'
                                    time.sleep(15) # wait a minute before adding a new friend.
            except (DeadlineExceededError, tweepy.TweepError) as e:
                logging.warning(e)

        output += '</pre>'
        logging.info(output)
        self.response.out.write(output)


app = webapp2.WSGIApplication([('/twitterbot/bot',TwitterBot)], debug=True)
