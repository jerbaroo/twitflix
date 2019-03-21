import json
import numpy as np
import matplotlib.pyplot as plt

# Scale an input number from one range to another range.
def scale(num, in_min, in_max, out_min, out_max):
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

with open("new_data.json") as f:
  data = json.load(f)

# For each movie name:
# - "mean_twitter": mean twitter score
# - "mean_critic": mean critic score
movie_scores = {}

# For each genre:
# - "mean_twitter": mean twitter score
# - "mean_critic": mean critic score
# - "all_twitter": all mean movie twitter scores
# - "all_critic": all mean critic scores
genre_scores = {}

##### Setup the data ##########################################################

for movie_name, movie_data in data.items():

  movie_scores[movie_name] = {
    "mean_twitter": scale(
      movie_data["scores"]["mean_scores"]["compound"],
      -1, 1,
      0, 10
    ),
    "mean_critic": movie_data["critic_score"]
  }
  try:
    movie_scores[movie_name]["mean_critic"] = float(
      movie_scores[movie_name]["mean_critic"])
  except ValueError:
    del movie_scores[movie_name]

  # Only for movies we have data.
  if movie_name in movie_scores:
    genres = movie_data["genre"].split(", ")
    # For all genres of this film.
    for genre in genres:
      if genre not in genre_scores:
        genre_scores[genre] = {
          "all_twitter": [],
          "all_critic": []
        }
      genre_scores[genre]["all_twitter"].append(
        movie_scores[movie_name]["mean_twitter"])
      genre_scores[genre]["all_critic"].append(
        movie_scores[movie_name]["mean_critic"])

# Calculate mean genre scores from list of data.
for genre_name, genre_data in genre_scores.items():
  genre_data["mean_twitter"] = np.mean(genre_data["all_twitter"])
  genre_data["mean_critic"] = np.mean(genre_data["all_critic"])

# Delete N/A genre and War (poor twitter data).
for genre_to_del in ["N/A", "War"]:
  print("Del {} mean twitter {} mean critic {}".format(
    genre_to_del,
    genre_scores[genre_to_del]["mean_twitter"],
    genre_scores[genre_to_del]["mean_critic"]
  ))
  del genre_scores[genre_to_del]

##### End setup the data ######################################################

for genre_name, genre_data in genre_scores.items():
  print("Genre {}\ttwitter {}\tcritic {}".format(
    genre_name, genre_data["mean_twitter"], genre_data["mean_critic"]))

sorted_genres = sorted(
  [genre_name for genre_name in genre_scores.keys()],
  key=(lambda genre_name: genre_scores[genre_name]["mean_critic"])
)

print("Genres, lowest critic first:\n\t{}".format(json.dumps(sorted_genres)))

plt.plot(
  [genre_scores[genre_name]["mean_critic"]
   for genre_name in sorted_genres],
  label="Critic"
)
plt.plot(
  [genre_scores[genre_name]["mean_twitter"]
   for genre_name in sorted_genres],
  label="Twitter"
)
plt.xticks(np.arange(len(sorted_genres)), [x[:5] for x in sorted_genres])
for tick in plt.gca().xaxis.get_major_ticks()[1::2]:
    tick.set_pad(15)
plt.legend()
plt.show()
