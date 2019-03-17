# Main script to run the processing part of this project.

import os
import sys
import json

import filter
from sentiment import Sentiment
from omdb import Omdb
from merge import Output

class Main:
    """docstring for Main."""

    def __init__(self):
        # Create the necessary folders.
        if not os.path.isdir('FilteredMovies'):
            try:
                os.mkdir('FilteredMovies')
            except OSError:
                print('Creation of the directory FilteredMovies failed')
            else:
                print('Successfully created the directory FilteredMovies')
        if not os.path.isdir('ScoredMovies'):
            try:
                os.mkdir('ScoredMovies')
            except OSError:
                print('Creation of the directory ScoredMovies failed')
            else:
                print('Successfully created the directory ScoredMovies')
        if not os.path.isdir('Results'):
            try:
                os.mkdir('Results')
            except OSError:
                print('Creation of the directory Results failed')
            else:
                print('Successfully created the directory Results')

    def process(self, file):
        # Filter the tweets.
        filter.filterAll(file)
        # Run the sentiment analysis.
        s = Sentiment()
        s.run()
        # Get the critic scores.
        o = Omdb()
        critic = o.critic_scores(file)
        # Merge the critic scores and sentiment analysis scores into the final data.json output file
        m = Output()
        m.generate('critic_scores.json')

if __name__ == '__main__':
    start = Main()
    if len(sys.argv) > 1:
        start.process(sys.argv[1])
    else:
        print('Usage: python2 main.py netflix-media.json')
