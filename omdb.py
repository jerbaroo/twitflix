# Script to get the critic scores via omdb

import requests
import json
import os


class Omdb(object):
    """docstring for Omdb."""
    def __init__(self):
        if not os.path.isdir('Results'):
            try:
                os.mkdir('Results')
            except OSError:
                print('Creation of the directory Results failed')
            else:
                print('Successfully created the directory Results')
        self.response = 0
        self.imdb = {}
        self.rotten_tomatoes = {}
        self.metacritic = {}
        self.missing = 0
        self.genre = 0

    def critic_scores(self, file):
        key = '289bb0f9'
        url = 'http://www.omdbapi.com/?apikey=289bb0f9&t='
        with open(file) as f:
            movies = json.load(f)
        result = {}

        for title in movies:
            data = {}
            result[title] = {
                "genre": "",
                "imdb": 0,
                "Rotten Tomatoes": 0,
                "Metacritic": 0
            }
            url = 'http://www.omdbapi.com/?apikey=289bb0f9&t='
            url = url+title
            response = requests.post(url)
            response = response.json()
            self.response = response
            try:
                genre = response['Genre']
                data['genre'] = genre
                result[title]['genre'] = genre
            except KeyError:
                self.genre += 1

            try:
                ratings = response['Ratings']
                for platform in ratings:
                    if platform['Source'] == 'Internet Movie Database':
                        self.imdb[title] = platform['Value']
                        data['imdb'] = platform['Value']
                        result[title]['imdb'] = platform['Value']
                    elif platform['Source'] == 'Rotten Tomatoes':
                        self.rotten_tomatoes[title] = platform['Value']
                        data['Rotten Tomatoes'] = platform['Value']
                        result[title]['Rotten Tomatoes'] = platform['Value']
                    elif platform['Source'] == 'Metacritic':
                        self.metacritic[title] = platform['Value']
                        data['Metacritic'] = platform['Value']
                        result[title]['Metacritic'] = platform['Value']

                # with open('Results/%s.json' % title, "w") as outfile:
                #     json.dump(data, outfile, indent=1)
            except KeyError:
                print(title)
                self.missing += 1

        with open('Results/results.json', "w") as target:
            json.dump(result, target, indent=1)
