Yinzbot
==========

A google appengine-based twitter bot to post from a reddit feed.
~~See it in action [@YinzBot](http://twitter.com/YinzBot)~~

NOTICE:
---------
[@YinzBot](http://twitter.com/YinzBot) is no longer tweeting using this codebase, appengine appears to no longer be posting content as of 14 Sep 2016 and I have no idea if any of this code works anymore, this project is no longer maintained and yinzbot's twitter contents are posted by a currently non-public codebase. Sorry for any consternation this may cause.


Features
----------
1. Tweet reddit posts with a score of 5 or higher
1. add #hashtag of the subreddit post is in
1. Auto follow back
1. post #FF message, selected from followers who mention or RT the bot
1. find new friends via #FF's on your timeline

Setup
----------
Configuration is easy, in the source folder you will find config-sample.yaml that contains:

    consumer_key: ""
    consumer_secret: ""
    access_token: ""
    access_token_secret: ""
    user-agent: '@Yinzbot your friendly neighborhood reddit->twitter bot | maintained by /u/jkirchartz'
    subreddit: 'pittsburgh+penguins+buccos+steelers+pittsburghlocalmusic'
    username: 'yinzbot'

Note: Reddit prefers your username in the user-agent.

__To set it up:__

1. set up an [appengine](https://appengine.google.com/)
1. set up a [Twitter Account](https://twitter.com)
1. set up a [New Twitter App](https://dev.twitter.com/apps/new)
1. rename config-sample.yaml to config.yaml
1. Insert your consumer keys and access tokens for your twitter app
1. multiple subreddits can be combined with `+`
1. change username to your Account's name
1. change appname in app.yaml to the name of your app on appengine

Originally forked from [chrishan's twitter-bot-gae](https://github.com/chrishan/twitter-bot-gae/tree/0b6043e05d8069a0ed9b7b18e91341e90a041fd6)
