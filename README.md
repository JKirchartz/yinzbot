Yinzbot
==========

An appengine twitter bot to post from a reddit feed.


Configuration
----------
Configuration is easy, in the source folder you will find config-sample.yaml that contains:

    consumer_key: ""
    consumer_secret: ""
    access_token: ""
    access_token_secret: ""
    subreddit: 'pittsburgh+penguins+buccos+steelers+pittsburghlocalmusic'
    username: 'yinzbot'


__To set it up:__
1. set up an [appengine](https://appengine.google.com/)
1. set up a [Twitter Account](https://twitter.com)
1. set up a [New Twitter App](https://dev.twitter.com/apps/new)
2. rename config-sample.yaml to config.yaml
3. Insert you consumer keys and access tokens for your twitter app
4. multiple subreddits can be combined with `+`
5. change username to your Account's name
6. change appname in app.yaml to the name of your app on appengine

Originally forked from [chrishan's twitter-bot-gae](https://github.com/chrishan/twitter-bot-gae/tree/0b6043e05d8069a0ed9b7b18e91341e90a041fd6)
