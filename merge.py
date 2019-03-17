import json


class Output(object):
    """docstring for Output."""
    def __init__(self):
        self.data = {}

    def generate(self, file):
        data = {}
        with open(file) as f:
            c_list = json.load(f)

        for title in c_list:
            print(title)
            data[title] = {
                "genre": c_list[title]['genre'],
                "imdb": c_list[title]['imdb'],
                "Rotten Tomatoes": c_list[title]['Rotten Tomatoes'],
                "Metacritic": c_list[title]['Metacritic'],
                "Sentiment score": 0
            }
            try:
                with open('scoredMovies/%s.json' % title) as m:
                    s_list = json.load(m)
                print(s_list['compound_ave'])
                data[title]['Sentiment score'] = s_list['compound_ave']
            except IOError:
                print("0")

            self.data[title] = data[title]
        with open('data.json', "w") as outfile:
            json.dump(data, outfile, indent=1)
