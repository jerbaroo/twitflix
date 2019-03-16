# Main script to run the processing part of this project.

import os
import json

from omdb import Omdb

class Main:
    """docstring for Main."""

    def __init__(self):
        # Create the necessary folders.
        if not os.path.isdir('Movies'):
            try:
                os.mkdir('Movies')
            except OSError:
                print('Creation of the directory Movies failed')
            else:
                print('Successfully created the directory Movies')
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
        # Load the movie list
        with open(file) as f:
            movie_list = json.load(f)

        # Import the tweets related to the movies in movie list.

        # Filter the tweets.

        # Run the sentiment analysis.

        # Get the critic scores.
        critic = critic_scores(movie_list)
        # Merge the critic scores and sentiment analysis scores into the final data.json output file
