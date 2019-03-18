# twitflix
Twitter opinions on Netflix.

# Usage
To run the full script first run `pip install -r requirements.txt` to install
the required packages. Furthermore for the sentiment analysis part some nltk
packages might need to be downloaded if not already installed. Not that the
resulting files from running the scripts are already available, so the first
script to download all tweets can be skipped.

To pull in the tweets needed you can use the tweets.py script. Usage example:
`python netflix-media.json 10` to download 10 tweets for each media in the file
`netflix-media.json`. Run tweets.py with python2 as there is some error when
using python3 with GetOldTweets.

Then to get cleaned and processed data from the tweets you can run `python2
main.py netflix-media.json`. The main.py script will created the needed
directories for the project, it will then filter irrelevant tweets, determine
sentiment of the remaining tweets, determine critic score, and finally merge the
sentiment and critic information into a single file `data.json`.

# Options
If some of the intermediate results are already on your system, you could skip
these stages. for example, the critic_scores.json file contains the critic
scores for the netflix-media.json titles and thus to reduce api calls you could
comment out get critic scores part of the main.py script.
