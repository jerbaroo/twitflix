import sys
import os
import json
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment:
    """docstring for sentiment."""

    def __init__(self):
        pass

    # Sentiment analysis of tweets
    def analysis(self, file):
        # Import the tweet file
        with open(file) as f:
            data = json.load(f)

        # Run vader over the tweet text and return scores
        text = []
        sentences = []
        for entry in data:
            text.append(data[entry]['Text'])
        for paragraph in text:
            lines_list = tokenize.sent_tokenize(paragraph)
            sentences.extend(lines_list)
        sid = SentimentIntensityAnalyzer()
        for sentence in sentences:
            print(sentence)
            ss = sid.polarity_scores(sentence)
            for k in sorted(ss):
                print('{0}: {1}, '.format(k, ss[k]))
            print()
