# Main script to run the processing part of this project.

import os
import sys
import json

import filter
from sentiment import Sentiment
from omdb import Omdb
from merge import merge_gen


class bcolors:
    GREEN = '\033[92m'
    ENDC = '\033[0m'


def print_green(s):
    print(bcolors.GREEN + s + bcolors.ENDC)


raw_movie_dir = "Movies"
filtered_movie_dir = "FilteredMovies"
scored_movie_dir = "ScoredMovies"
results_dir = "Results"


class Main:
    """docstring for Main."""

    def __init__(self):
        # Create the necessary folders.
        for dirname in [filtered_movie_dir, scored_movie_dir, results_dir]:
            if not os.path.isdir(dirname):
                try:
                    os.mkdir(dirname)
                    print("Successfully created the directory {}".format(dirname))
                except OSError:
                    print("Creation of the directory {} failed".format(dirname))

    def process(self, media_list_file):
        # Filter the tweets.
        print_green("Filtering movies in {} to {}".format(
            raw_movie_dir, filtered_movie_dir))
        filter.filterAll(
            media_list_file, raw_movie_dir, filtered_movie_dir)
        # Run the sentiment analysis.
        print_green("Scoring movies in {} to {}".format(
            filtered_movie_dir, scored_movie_dir))
        Sentiment().run(filtered_movie_dir, scored_movie_dir)
        # Get the critic scores.
        Omdb().critic_scores(media_list_file)
        # Merge the critic scores and sentiment analysis scores into
        # the final data.json output file.
        merge_gen(
            'critic_scores.json', 'sentiment_scores.json', 'data.json')


if __name__ == '__main__':
    start = Main()
    if len(sys.argv) > 1:
        start.process(sys.argv[1])
    else:
        print('Usage: python2 main.py netflix-media.json')
