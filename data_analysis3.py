import json
import sys

import matplotlib.pyplot as plt
import numpy as np

# Load the data.
with open("json_data") as f:
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

    # Critic scores
    imdb = movie_data['imdb']
    metacritic = movie_data['metacritic']
    rottom = movie_data['rotten-tomatoes']
    if imdb != 0:
        text = ('Critic score: {}'.format(imdb))
    elif metacritic != 0:
        text = ('Critic score: {}'.format(metacritic))
    elif rottom != 0:
        text = ('Critic score: {}'.format(rottom))
    else:
        text = 'Unknown'

    data[movie_name]['critic_score'] = text

    # Coefficient of variation (The :.4f means show four decimal places)
    mean_twitter_score = np.mean(all_scores)
    standard_dev = np.std(all_scores)
    coefficient_of_variation = (standard_dev)/(mean_twitter_score)
    #print("{:.4f} \t mean twitter score for {}".format(mean_twitter_score, movie_name))
    #print("{:.4f} \t standard deviation for {}".format(standard_dev, movie_name))
    #print("{:.4f} \t coefficient of variation for {}".format(coefficient_of_variation, movie_name))
    if coefficient_of_variation < 0.5:
        text = 'Very strong inter-rater agreement'
    elif coefficient_of_variation < 1:
        text = 'Strong inter-rater agreement'
    elif coefficient_of_variation < 10:
        text = 'Weak inter-rater agreement'
    else:
        text = 'Very weak inter-rater agreement'

    data[movie_name]['agreement']=text

with open('new_data.json', 'w') as f:
    f.write(json.dumps(data, indent=2))


    #plt.hist(all_scores)
    #plt.show()