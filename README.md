Yinzbot
==========

A twitter bot to post from a reddit feed.


Configuration
----------
Configuration is easy, in the source folder you will find config-sample.yaml that contains:

{% highlight yaml %}
    consumer_key: ""
    consumer_secret: ""
    access_token: ""
    access_token_secret: ""
    subreddit: 'pittsburgh+penguins+buccos+steelers+pittsburghlocalmusic'
    username: 'yinzbot'
{% endhighlight %}


1. rename config-sample.yaml to config.yaml
2. Insert you consumer keys and access tokens for your twitter app
3. multiple subreddits can be combined with `+`
