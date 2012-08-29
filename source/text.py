import yaml, os.path

config = yaml.load(open('config.yaml', 'r'));
link = "http://test.com/r/pittsburgh+pittsburghlocalmusic+steelers+buccos+penguins"

if "+" in config['subreddit']:
    for i in config['subreddit'].split('+'):
        #newlink = link.replace("http://www.reddit.com/r/"+i+"/comments/","http://redd.it/")
        print i
else:
    print "+ not found"
