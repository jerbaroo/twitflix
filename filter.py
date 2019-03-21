from __future__ import division
import json
import sys

import numpy as np

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


def filterAll(media_list_file, in_movie_dir, out_movie_dir):
    """Filter all tweets in Movies folder, save to FilteredMovies."""
    with open(media_list_file) as f:
        names = json.load(f)

    count_tweets = []
    count_kept_tweets = []
    for name in names:
        with open("{}/{}.json".format(in_movie_dir, name)) as f:
            tweets = json.load(f)
            kept_tweets = [t for t in tweets.values() if keep(t)]
            print("total = {}\tkeep = {}\tName = {}".format(
                len(tweets), len(kept_tweets), name))
            count_tweets.append(len(tweets))
            count_kept_tweets.append(len(kept_tweets))
        with open("{}/{}.json".format(out_movie_dir, name), "w") as f:
            json.dump(kept_tweets, f)
    print("Mean tweets = {}".format(np.mean(count_tweets)))
    print("Mean kept tweets = {}".format(np.mean(count_kept_tweets)))
    print("Mean fraction kept tweets = {}".format(
        np.mean(count_kept_tweets) / np.mean(count_tweets)))


if __name__ == "__main__":
    in_file = "netflix-media.json"
    with open(in_file) as f:
        movies = json.load(f)
    filterAll("netflix-media.json", "Movies", "FilteredMovies")
    print("Amount of movies = {}".format(len(movies)))
