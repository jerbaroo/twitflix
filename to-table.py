import json


# Scale an input number from one range to another range.
def scale(num, in_min=-1, in_max=1, out_min=0, out_max=10):
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


with open("new_data.json") as f:
    data = json.load(f)

movie_names = []
movie_genres = []
twitter_scores = []
critic_scores = []

for movie_name, movie_data in data.items():
    movie_names.append(movie_name)
    movie_genres.append(movie_data["genre"])
    critic_scores.append(movie_data["critic_score"])
    twitter_scores.append(scale(movie_data["scores"]["mean_scores"]["compound"]))
    print("name = {} genres = {} twitter = {} critic = {}".format(
        movie_names[-1], movie_genres[-1], twitter_scores[-1], critic_scores[-1]))
