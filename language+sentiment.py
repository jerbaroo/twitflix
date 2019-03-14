import langid, json, re
from langdetect import detect
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import sys
reload(sys)
sys.setdefaultencoding('gb18030') 

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, type(list)):
        return [convert(element) for element in input] 
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

all_data = {}
'''
rootdir = './newMovies'
list = os.listdir(rootdir)
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    data = []
    if os.path.isfile(path):
        name = os.path.basename(path)
'''

with open('./newMovies/Sex Education.json') as f:
    texts = json.load(f)
    new_texts = []
    sid = SentimentIntensityAnalyzer()
    for t in texts["texts"]:
        language = detect(t)
        if language == 'en':
            new_texts.append(convert(t))
    for t in new_texts:
        print t
        ss = sid.polarity_scores(t)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]))
