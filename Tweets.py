# Imports
import sys
import os
import datetime
import json
import twitter

# check for version of python
if sys.version_info[0] < 3:
    from GetOldTweets import got
else:
    from GetOldTweets import got3 as got


# converter to include datetime into json output file
def datetimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class Data:
    """docstring for data."""
    def __init__(self):
        if not os.path.isdir('Movies'):
            try:
                os.mkdir('Movies')
            except OSError:
                print("Creation of the directory Movies failed")
            else:
                print ("Successfully created the directory Movies")

    # function to save to json file
    def saveJSON(self, title, tweets):
        print(title)
        data = {}
        for tweet in tweets:
            # print(tweet.username)
            data[tweet.id] = {
                "Title": title,
                "Username": tweet.username,
                "Text": tweet.text,
                "Mentions": tweet.mentions,
                "Hashtags": tweet.hashtags,
                "Date": tweet.date,
                "Geo": tweet.geo
            }
        with open("Movies/%s.json" % title, "w") as outfile:
            json.dump(data, outfile, default=datetimeConverter, encoding="utf8")

    # Gather tweets about movies
    def gather(self, file, tweets):
        if not os.path.isdir('Movies'):
            try:
                os.mkdir('Movies')
            except OSError:
                print("Creation of the directory Movies failed")
            else:
                print ("Successfully created the directory Movies")

        n = int(tweets)
    # open netflix-media list
        with open(file) as f:
            movies = json.load(f)
    # iterate over the different titles and save output
        for title in movies:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(title).setMaxTweets(n).setUntil("2019-02-01")
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            self.saveJSON(title, tweet)
            # query = title + " #movierating"
            # tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setMaxTweets(n)
            # tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            # self.saveJSON(title+"#movierating", tweet)
            # query = title + " #rating"
            # tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setMaxTweets(n)
            # tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            # self.saveJSON(title+"#rating", tweet)

    def twitter(self, file, tweets):
        CONSUMER_KEY = 'qC3ZrVH8xRaXJlb7Rwjg1Xvpb'
        CONSUMER_SECRET = 'kR2Q7CdQkPMSBPucJecHfa2cNQIQZgOypSydhsplF44aGR0X2C'
        OAUTH_TOKEN = '85152226-6jv1nfU8tRoqaIjEiEVSAlwlgloA2E7qNyRbTX15v'
        OAUTH_TOKEN_SECRET = '0JYy1gELC7eNuRfWNUqDz8zZXQlqSQvAktnkuC17nl7Nh'
        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        twitter_api = twitter.Twitter(auth=auth)

        with open(file) as f:
            movies = json.load(f)
        count = int(tweets)

        for title in movies:
            search_results = twitter_api.search.tweets(q=title, count=count)
            statuses = search_results['statuses']
            data = {}
            for status in statuses:
                status_id = status['id']
                status_user = status['user']
                status_text = status['text']
                status_lang = status['lang']
                status_date = status['created_at']
                status_hashtags = status['entities']
                status_geo = status['geo']
                status_place = status['place']

                data[status_id] = {
                    "Title": title,
                    "User": status_user,
                    "Text": status_text,
                    "Lang": status_lang,
                    "Date": status_date,
                    "Hashtags": status_hashtags,
                    "Geo": status_geo,
                    "Place": status_place
                }
            with open('Movies/%s.json' % title, "w") as outfile:
                json.dump(data, outfile, indent=1, encoding='utf8')
