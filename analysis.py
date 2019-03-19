import json
import sys

import matplotlib.pyplot as plt
import numpy as np

# Print function that will pretty print JSON.
jprint = lambda j: print(json.dumps(j, indent=2))

# Load the data.
with open("data.json") as f:
    data = json.load(f)

for movie_name, movie_data in data.items():
    # movie_data["scores"] has three keys, "mean_scores", "failed", and "scores".
    #
    # "mean_scores" has an average for each of "pos", "neu", "neg", and
    # "compound".
    #
    # "failed" show the amount of tweets we couldn't get a sentiment for.
    #
    # "scores" is a list like [(sentiment, date), (sentiment, date), ...]
    # with sentiment data and a date for each tweet. We put that into the
    # following variable movie_sentiments_and_dates.
    movie_sentiments_and_dates = movie_data["scores"]["scores"]

    # If we want a list of just compound sentiment like [0.7, 0.5, ...] we
    # can take the compound value from each sentiment with a list comprehension.
    # The [0] takes the sentiment mentioned above, and then we get the compound
    # specific value.
    all_scores = [x[0]["compound"] for x in movie_sentiments_and_dates]

    # The :.4f means show four decimal places.
    print("{:.4f} \t variance for {}".format(np.var(all_scores), movie_name))

    plt.hist(all_scores)
    plt.show()
