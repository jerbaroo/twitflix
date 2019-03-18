import json


def merge_gen(
        critic_scores_file, sentiment_scores_file, output_file):
    """Merge sentiment scores and critic scores."""
    data = {}

    with open(critic_scores_file) as f:
        c_list = json.load(f)
    with open(sentiment_scores_file) as f:
        s_list = json.load(f)

    for title in c_list:
        data[title] = {
            "genre": c_list[title]['genre'],
            "imdb": c_list[title]['imdb'],
            "rotten-tomatoes": c_list[title]['Rotten Tomatoes'],
            "metacritic": c_list[title]['Metacritic']
        }
        data[title]["scores"] = s_list[title + ".json"]

    with open(output_file, "w") as outfile:
        json.dump(data, outfile, indent=1)
