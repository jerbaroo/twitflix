import json
import sys

import matplotlib.pyplot as plt
import numpy as np

# Load the data.
with open("data.json") as f:
    data = json.load(f)

mean_scores = []
std_devs = []
coefficients = []

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
    if metacritic != 0:
        num = float(metacritic.replace("/100", ""))
        text = "{:.1f}".format(num/10).replace(".0", "")
    elif imdb != 0:
        text = imdb.replace("/10", "").replace(".0", "")
    elif rottom != 0:
        num = float(rottom.replace("%", ""))
        text = "{:.1f}".format(num/10)
    else:
        text = 'NA'

    data[movie_name]['critic_score'] = text

    mean_twitter_score = np.mean(all_scores)
    standard_dev = np.std(all_scores)
    coefficient_of_variation = standard_dev / np.abs(mean_twitter_score)
    mean_scores.append(mean_twitter_score)
    std_devs.append(standard_dev)
    coefficients.append(coefficient_of_variation)
    #print("{:.4f} \t mean twitter score for {}".format(mean_twitter_score, movie_name))
    #print("{:.4f} \t standard deviation for {}".format(standard_dev, movie_name))
    #print("{:.4f} \t coefficient of variation for {}".format(coefficient_of_variation, movie_name))
    if coefficient_of_variation < 0.5:
        text = 'Very strong agreement'
    elif coefficient_of_variation < 1:
        text = 'Strong agreement'
    elif coefficient_of_variation < 5:
        text = 'General agreement'
    else:
        text = 'Mixed opinions'

    data[movie_name]['agreement'] = text

    # plt.hist(all_scores)
    # plt.show()

with open('new_data.json', 'w') as f:
    f.write(json.dumps(data, indent=2))

plt.hist(mean_scores)
plt.title('mean')
# plt.show()

plt.hist(std_devs)
plt.title('std-devs')
# plt.show()

plt.close()
plt.hist([x for x in coefficients if x < 15], bins=20)
plt.title('Variance of user opinion')
plt.xlabel('Variance')
plt.ylabel('Count of media with a variance range')
plt.show()

plt.close()
plt.hist([x for x in coefficients if x < 15], bins=20, cumulative=True)
plt.title('Cumulative variance of user opinion')
plt.xlabel('Variance')
plt.ylabel('Cumulative count of media with a variance range')
plt.show()
