import sys, os
import json
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main(argv):
# import the tweet file
    if len(argv) == 0:
        print('input the file for sentiment analysis')
        return

    with open(argv[0]) as f:
        data = json.load(f)

# run vader over the tweet text and return scores
    text = []
    sentences = []
    for entry in data:
        text.append(data[entry]['Text'])
    for paragraph in text:
        lines_list = tokenize.sent_tokenize(paragraph)
        sentences.extend(lines_list)
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]))
        print()


if __name__ == '__main__':
    main(sys.argv[1:])
