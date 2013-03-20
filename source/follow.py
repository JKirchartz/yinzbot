#!/usr/bin/env python

# --------- Imports --------
import webapp2,cgi,urllib
from google.appengine.api import xmpp
from google.appengine.ext import db
from md5 import md5
import simplejson as json
import tweepy
import re
import logging
import time
import yaml
import os.path


# ---- The Job Handler --------
class TwitterBot(webapp.RequestHandler):
    def get(self):
        config = yaml.load(open(os.path.dirname(__file__) + '/config.yaml', 'r'));
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token'], config['access_token_secret'])
        bot = tweepy.API(auth)

        try:

            friends = []

            for friend in bot.friends():
                friends.append(friend.screen_name)

            followers = []

            for follower in bot.followers():
                followers.append(follower.screen_name)

            ff_tweeps = []

            status = '#FF '
            output = '\n\n#FollowFriday:\n----------\n'
            for mention in bot.mentions(include_rts=True):
                ff_tweeps.append(mention.user.screen_name)

            to_ff = [x for x in followers if x not in ff_tweeps]
            for tweep in list(set(to_ff)):
                if tweep != config['username']:
                    status += '@'+tweep+' '
                    if len(status) >= 120:
                        break

            output += status
            bot.update_status(status)
            output += '\n\nFollowBack:\n----------\n\n'
            to_follow = [x for x in followers if x not in friends]
            for user in to_follow:
                output += repr(user) + '\n'
                bot.create_friendship(user)
                time.sleep(10) # wait 10 seconds before adding another friend


        except tweepy.TweepError, e:
            logging.warning(e)

        logging.info(output)
        self.response.out.write(output)


app = webapp2.WSGIApplication([('/twitterbot/follow',TwitterBot)], debug=True)
