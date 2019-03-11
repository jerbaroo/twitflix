import os, json, re
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def clean(input):
    text = re.sub(r'http[s]?://(?:[ ]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',input)
    text2 = re.sub('@([ ]|[_]|[a-zA-Z]|[0-9])+','',text)
    text3 = re.sub('#([_]|[a-zA-Z]|[0-9])+','',text2)
    text4 = re.sub(r'\( +\)','',text3)
    text5 = re.sub('pic.twitter.com/([a-zA-Z]|[0-9])+','',text4)
    text5 = re.sub('[ ][ ]+','',text5)
    return text5

rootdir = './Movies'
list = os.listdir(rootdir)
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    if os.path.isfile(path):
        name = os.path.basename(path)
        with open('./Movies/{0}'.format(name)) as f:
            with open('./newMovies/{0}'.format(name),'w') as f2:
                texts = convert(json.load(f))
                data = []
                print name
                num = 0
                for kv in texts.items():
                    data.append(clean(kv[1]['Text']))
                json.dump(data,f2)


