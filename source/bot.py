#!/usr/bin/env python

# --------- Imports --------
import cgi,urllib
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
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
class TwitterBot(webapp.RequestHandler):
    def get(self):
        config = yaml.load(open(os.path.dirname(__file__) + '/config.yaml', 'r'));
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])
        bot = tweepy.API(auth)
        feed = "http://www.reddit.com/r/" + config['subreddit'] + "/.json"
        feeddata = json.loads(urllib2.urlopen(feed).read())

        output = 'DONE!\n==========\n\nTweets:\n'
        
        if 'data' in feeddata and 'children' in feeddata['data']:
            for entry in feeddata['data']['children']:
                title = str(unicode(entry['data']['title']).encode("utf-8"))
                myid = str(unicode(entry['data']['id']).encode("utf-8"))
                link = 'http://redd.it/' + myid 

                status = " " + link

                try:
                    status = title[:(140 - len(status))] + status
                except:
                    status = repr(title[:(140 - len(status))]) + status

                query = TwitterDB.all()
                query.filter('reddit_id =', myid)
                res = query.fetch(1)

                if len(res) == 0 and entry['data']['score'] > 5:
                    output +=  status + '\n'
                    
                    try:
                        bot.update_status(status)
                    except tweepy.TweepError, e:
                        logging.warning(e)
                    
                    item = TwitterDB()
                    item.reddit_id = myid
                    item.put()
                else:
                    continue

        if time.strftime('%a') == 'Fri':
            output += '\n\nFind new #FF friends:\n----------\n'
            try:
                for status in bot.friends_timeline():
                    tweet = repr(status.text)

                    if '#FF' in tweet or '#FollowFriday' in tweet:
                        tweeps = set(who.strip('@') for who in tweet.split() if who.startswith("@"))
                        for tweep in tweeps:
                            for result in  bot.search_users(q=tweep):
                                if result.screen_name == tweep:
                                    try:
                                        result.follow()
                                        output += tweep + '\n'
                                    except tweepy.TweepError, e:
                                        logging.warning(e)
            except tweepy.TweepError, e:
                logging.warning(e)

        logging.info(output)    
        self.response.out.write(output)


application = webapp.WSGIApplication([('/twitterbot/bot', TwitterBot)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

