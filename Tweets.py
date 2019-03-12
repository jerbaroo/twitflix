# Imports
import sys
import os
import datetime
import json

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
        pass

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
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(title).setMaxTweets(n)
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            self.SaveJSON(title, tweet)
            query = title + " #movierating"
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setMaxTweets(n)
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            self.SaveJSON(title+"#movierating", tweet)
            query = title + " #rating"
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setMaxTweets(n)
            tweet = got.manager.TweetManager.getTweets(tweetCriteria)
            self.SaveJSON(title+"#rating", tweet)
