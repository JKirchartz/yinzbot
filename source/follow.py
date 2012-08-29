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

        status = '#FF '
        tweeps = []
        output = '\n\n#FollowFriday:\n----------\n'
        for mention in bot.mentions(include_rts=True):
            tweeps.append(mention.user.screen_name)

        for tweep in list(set(tweeps)):
            if tweep != config['username']:
                status += '@'+tweep+' '
                if len(status) >= 100:
                    break
                    
        try: 
            output += status                
            bot.update_status(status)
        except tweepy.TweepError, e:
            logging.warning(e)
        
        
        try:
            output += '\n\nFollowBack:\n----------\n\n'

            friends = []
        
            for friend in bot.friends():
                friends.append(friend.screen_name)
        
            followers = []
        
            for follower in bot.followers():
                followers.append(friend.screen_name)

            to_follow = [x for x in followers if x not in friends]
            for user in to_follow:
                output += repr(user.screen_name) + '\n'
                user.follow()
        except tweepy.TweepError, e:
            logging.warning(e)

        logging.info(output)    
        self.response.out.write(output)


application = webapp.WSGIApplication([('/twitterbot/follow', TwitterBot)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

