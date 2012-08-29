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
import feedparser
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
        feed = "http://www.reddit.com/r/" + config['subreddit'] + "/.rss"
        atomxml = feedparser.parse(feed)
        entries = atomxml['entries']

        output = 'DONE!\n==========\n\nTweets:\n'
        
        if len(entries) != 0:
            entries.reverse()
            for x in range(len(entries)):
                entry = entries[x]
                title = str(unicode(entry['title']).encode("utf-8"))
                link = str(unicode(entry['link']).encode("utf-8"))
                myid = str(unicode(entry['id']).encode("utf-8"))

                if "+" in config['subreddit']:
                    for i in config['subreddit'].split('+'):
                        if i in link:
                            newlink = link.replace("http://www.reddit.com/r/"+i+"/comments/","http://redd.it/")
                            newlink = re.sub("/[\w]{6,}/$","",newlink)
                            break
                        else:
                            continue
                else:
                    newlink = link.replace("http://www.reddit.com/r/"+config['subreddit']+"/comments/","http://redd.it/")
                    newlink = re.sub("/[\w]{6,}/$","",newlink)
                    
                status = " " + newlink

                try:
                    status = title[:(140 - len(status))] + status
                except:
                    status = repr(title[:(140 - len(status))]) + status

                query = TwitterDB.all()
                query.filter('reddit_id =', myid)
                res = query.fetch(1)

                if len(res) == 0:
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

