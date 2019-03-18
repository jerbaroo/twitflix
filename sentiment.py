# coding: utf-8
import json
import langid
import os
import re
import time
import sys

import numpy as np
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment(object):
    """Docstring for Sentiment."""

    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def clean_text(self, input_text):
        """Return the input text but cleaned of unecessary data."""
        text = re.sub(
            r'http[s]?://(?:[ ]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            '', input_text)
        text2 = re.sub('@ *([_]|[a-zA-Z]|[0-9])+', '', text)
        text3 = re.sub('#', '', text2)
        # text3 = re.sub('#([_]|[a-zA-Z]|[0-9])+','',text2)
        text4 = re.sub(r'\( +\)', '', text3)
        text5 = re.sub('pic.twitter.com/([a-zA-Z]|[0-9])+', '', text4)
        text6 = re.sub(r'\' \'', '', text5)
        text6 = re.sub('…', '', text6)
        text7 = re.sub('[ ][ ]+', ' ', text6)
        return text7

    def add_sentiment_scores(self, tweet):
        language = langid.classify(tweet['Text'])
        if 'scores' not in tweet:
            tweet['scores'] = dict()
        if language[0] == 'en':
            ss = self.sid.polarity_scores(tweet['Text'])
            for k in sorted(ss):
                tweet['scores'][k] = ss[k]

    def run(self, in_movie_dir, out_movie_dir):
        # For each movie in the input folder.
        movie_list = os.listdir(in_movie_dir)
        output = {}  # Build up our resulting data.
        for i in range(len(movie_list)):
            print("Calculating sentiment of {}".format(
                movie_list[i][:-5]))
            path = os.path.join(in_movie_dir, movie_list[i])
            name = os.path.basename(path)
            # Clean the tweets for each movie and add sentiment scores.
            with open('{}/{}'.format(in_movie_dir, name)) as f:
                tweets = json.load(f)
                output[name] = {
                    'scores': [],
                    'mean_scores': {},
                    'failed': 0
                }
                for tweet in tweets:
                    tweet['Text'] = self.clean_text(tweet['Text'])
                    self.add_sentiment_scores(tweet)
                    # Only add tweet scores if scores were calculated.
                    if len(tweet['scores'].keys()) > 0:
                        output[name]['scores'].append(
                            [tweet['scores'], tweet['Date']])
                    else:
                        output[name]['failed'] += 1
        # Output a file mapping movies to sentiments.
        for name in output:
            for score_type in ['pos', 'neu', 'neg', 'compound']:
                all_of_type = [
                    x[0][score_type]
                    for x in output[name]['scores']
                    if score_type in x[0]
                ]
                output[name]['mean_scores'][score_type] = np.mean(
                    all_of_type)
        with open('sentiment_scores.json', 'w') as f:
            json.dump(output, f, indent=2)
