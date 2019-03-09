# Imports
import sys, os, datetime, json

# check for version of python
if sys.version_info[0] < 3:
    from GetOldTweets import got
else:
    from GetOldTweets import got3 as got

# converter to include datetime into json output file
def datetimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# function to save to json file
def saveJSON(title, tweets):
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
        json.dump(data, outfile, default=datetimeConverter)


def main(argv):
    if not os.path.isdir('Movies'):
        try:
            os.mkdir('Movies')
        except OSError:
            print("Creation of the directory Movies failed")
        else:
            print ("Successfully created the directory Movies")

    if len(argv) == 0:
        print("enter the number of tweets per title")
        return

    n = int(argv[0])
    print(n)
# open netflix-media list
    with open('netflix-media.json') as f:
        movies = json.load(f)
# iterate over the different titles and save output
    for title in movies:
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(title).setMaxTweets(n)
        tweet = got.manager.TweetManager.getTweets(tweetCriteria)
        saveJSON(title, tweet)

if __name__ == '__main__':
    main(sys.argv[1:])
