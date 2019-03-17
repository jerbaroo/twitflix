# coding: utf-8
import os, json, re, langid, time
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment(object):
    """docstring for Sentiment."""

    def __init__(self):
        self.data = []
        self.tweets = {}
        self.sid = SentimentIntensityAnalyzer()
        self.com = 0

    def convert(self, input):
        if isinstance(input, dict):
            return {self.convert(key): self.convert(value) for key, value in input.iteritems()}
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def clean(self, input):
        text = re.sub(r'http[s]?://(?:[ ]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',input)
        text2 = re.sub('@ *([_]|[a-zA-Z]|[0-9])+','',text)
        text3 = re.sub('#','',text2)
    #    text3 = re.sub('#([_]|[a-zA-Z]|[0-9])+','',text2)
        text4 = re.sub(r'\( +\)','',text3)
        text5 = re.sub('pic.twitter.com/([a-zA-Z]|[0-9])+','',text4)
        text6 = re.sub(r'\' \'','',text5)
        text6 = re.sub('…','',text6)
        text7 = re.sub('[ ][ ]+',' ',text6)
        return text7

    def clean_language(self, input):
        if input != "" and input != " " and input != "@":
            language = langid.classify(input[1]['Text'])
            if language[0] == 'en':
                print input
                self.tweets["text"] = input[1]['Text']
                self.tweets["data"] = input[1]['Date']
                ss = self.sid.polarity_scores(input[1]['Text'])
                for k in sorted(ss):
                    self.tweets[k] = ss[k]
                self.com += ss["compound"]
                self.data.append(self.tweets)

    def run(self):
        rootdir = './Movies'
        list = os.listdir(rootdir)
        for i in range(0,len(list)):
            path = os.path.join(rootdir,list[i])
            if os.path.isfile(path):
                name = os.path.basename(path)
                with open('./Movies/{0}'.format(name)) as f:
                    with open('./ScoredMovies/{0}'.format(name),'w') as f2:
                        texts = self.convert(json.load(f))
                        movie = {}
                        print name
                        print ("\n"*5)
                        time.sleep(5)
                        for kv in texts.items():
                            tweets = {}
                            kv[1]['Text'] = self.clean(kv[1]['Text'])
                            self.clean_language(kv)
                        movie['number'] = len(self.data)
                        movie['texts'] = self.data
                        movie['compound_ave'] = self.com/len(self.data)
                        json.dump(movie,f2)
