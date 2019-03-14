# Script to get the critic scores via omdb

import requests
import json

class Omdb(object):
    """docstring for Omdb."""
    def __init__(self):
        self.response = 0
        self.imdb = {}
        self.rotten_tomatoes = {}
        self.metacritic = {}
        self.missing = 0

    def critic_scores(self, file):
        key = '289bb0f9'
        url = 'http://www.omdbapi.com/?apikey=289bb0f9&t='
        with open(file) as f:
            movies = json.load(f)

        for title in movies:
            url = 'http://www.omdbapi.com/?apikey=289bb0f9&t='
            url = url+title
            print(url)
            response = requests.post(url)
            response = response.json()
            print(response)
            self.response = response
            try:
                ratings = response['Ratings']
                data = {}
                for platform in ratings:
                    if platform['Source'] == 'Internet Movie Database':
                        self.imdb[title] = platform['Value']
                        data['imdb'] = platform['Value']
                    elif platform['Source'] == 'Rotten Tomatoes':
                        self.rotten_tomatoes[title] = platform['Value']
                        data['Rotten Tomatoes'] = platform['Value']
                    elif platform['Source'] == 'Metacritic':
                        self.metacritic[title] = platform['Value']
                        data['Metacritic'] = platform['Value']

                with open('Results/%s.json' % title, "w") as outfile:
                    json.dump(data, outfile, indent=1)
            except KeyError:
                self.missing += 1
