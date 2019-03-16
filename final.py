# coding: utf-8
import os, json, re, langid, time
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def clean(input):
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

def clean_language(input):
    global com
    if input != "" and input != " " and input != "@":
        language = langid.classify(input)
        if language[0] == 'en':
            print input
            tweets["text"] = input
            tweets["data"] = kv[1]['Date']
            ss = sid.polarity_scores(input)
            for k in sorted(ss):
                tweets[k] = ss[k]
            com += ss["compound"]
            data.append(tweets)
        

rootdir = './Movies'
list = os.listdir(rootdir)
sid = SentimentIntensityAnalyzer()
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    if os.path.isfile(path):
        name = os.path.basename(path)
        with open('./Movies/{0}'.format(name)) as f:
            with open('./finalMovies/{0}'.format(name),'w') as f2:
                texts = convert(json.load(f))
                data = []
                movie = {}
                print name
                print ("\n"*5)
                time.sleep(5)
                com = 0
                for kv in texts.items():
                    tweets = {}
                    cleaned_data = clean(kv[1]['Text'])
                    clean_language(cleaned_data)
                movie['number'] = len(data)
                movie['texts'] = data
                movie['compound_ave'] = com/len(data)
                json.dump(movie,f2)


