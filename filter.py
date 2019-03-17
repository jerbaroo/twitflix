import json

keep_words = ["Movie", "Film", "netflix", "tv", "series", "watch"]
keep_words = [word.lower() for word in keep_words]


def keep(tweet):
    """Keep a word if it contains a keep word."""
    text = tweet["Text"].lower()
    hashtags = " ".join(tweet["Hashtags"]).lower()
    for word in keep_words:
        if word in text:
            # print("{} in text {}".format(word, text))
            return True
        if word in hashtags:
            # print("{} in hashtags {}".format(word, hastags))
            return True
    return False


def filterAll(file):
    """Filter all tweets in Movies folder, save to FilteredMovies."""
    with open(file) as f:
        names = json.load(f)

    for name in names:
        with open("Movies/{}.json".format(name)) as f:
            tweets = json.load(f)
            kept_tweets = [t for t in tweets.values() if keep(t)]
            print("total = {}\tkeep = {}\tName = {}".format(
                len(tweets), len(kept_tweets), name))
        with open("FilteredMovies/{}.json".format(name), "w") as f:
            json.dump(kept_tweets, f)


if __name__ == "__main__":
    filterAll()
